"""Render replacement text as RGBA patches in reference-frame coordinates."""
import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
SS = 4  # supersampling


def _font(cap_px, path=FONT):
    f = ImageFont.truetype(path, 100)
    b = f.getbbox('H')
    cap100 = b[3] - b[1]
    return ImageFont.truetype(path, max(4, int(round(cap_px * SS * 100 / cap100))))


def _strip(text, font, hscale=1.0, track=0.0):
    """Render text white-on-transparent; return alpha (float 0..1) and baseline y,
    plus cap-top y in strip coords."""
    asc, desc = font.getmetrics()
    pad = int(font.size * 0.6)
    w = int(font.getlength(text) + pad * 2 + abs(track) * len(text) * SS)
    h = asc + desc + pad * 2
    im = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(im)
    x = pad
    for ch in text:
        d.text((x, pad), ch, font=font, fill=255)
        x += font.getlength(ch) + track * SS
    a = np.asarray(im).astype(np.float32) / 255
    base = pad + asc
    capt = base - (font.getbbox('H')[3] - font.getbbox('H')[1])
    if hscale != 1.0:
        a = cv2.resize(a, (max(1, int(a.shape[1] * hscale)), a.shape[0]), interpolation=cv2.INTER_AREA)
    # crop horizontally to ink
    cols = np.where(a.max(0) > 0.01)[0]
    a = a[:, cols[0]:cols[-1] + 1] if len(cols) else a
    return a, base, capt


def _colorize(a, base, capt, color, grad):
    """a: alpha strip. returns float BGRA strip. grad: (top_mult, bottom_mult)."""
    h, w = a.shape
    y = np.arange(h, dtype=np.float32)[:, None]
    t = np.clip((y - capt) / max(1, base - capt), 0, 1)
    m = grad[0] + (grad[1] - grad[0]) * t
    rgb = np.clip(np.array(color, np.float32)[None, None, :] * m[..., None], 0, 255)
    rgb = np.broadcast_to(rgb, (h, w, 3))
    return np.dstack([rgb, a])


def _place(canvas, strip, anchor, angle_deg, pos):
    """Rotate strip about anchor (x,y in strip coords) by angle (deg, clockwise on
    screen) and alpha-composite onto canvas so anchor lands on pos (canvas coords)."""
    h, w = strip.shape[:2]
    anchor = (float(anchor[0]), float(anchor[1]))
    M = cv2.getRotationMatrix2D(anchor, -angle_deg, 1.0)
    M[:, 2] += np.array(pos) - np.array(anchor)
    H, W = canvas.shape[:2]
    rgb = cv2.warpAffine(strip[..., :3] * strip[..., 3:], M, (W, H), flags=cv2.INTER_LINEAR)
    al = cv2.warpAffine(strip[..., 3], M, (W, H), flags=cv2.INTER_LINEAR)
    canvas[..., :3] = rgb + canvas[..., :3] * (1 - al[..., None])
    canvas[..., 3] = al + canvas[..., 3] * (1 - al)


def render(spec, bbox):
    """spec: dict with keys type(line|arc|glyphpart), text, cap, color, ...
    bbox: (x0,y0,x1,y1) ref coords of the patch. Returns premultiplied BGRA float
    image at 1x in bbox space."""
    x0, y0, x1, y1 = bbox
    W, H = (x1 - x0) * SS, (y1 - y0) * SS
    canvas = np.zeros((H, W, 4), np.float32)
    font = _font(spec['cap'], spec.get('font', FONT))
    color = spec['color']; grad = spec.get('grad', (1.0, 1.0))
    hs = spec.get('hscale', 1.0); trk = spec.get('spacing', 0.0)
    P = lambda p: ((p[0] - x0) * SS, (p[1] - y0) * SS)
    t = spec['type']
    if t == 'line':
        a, base, capt = _strip(spec['text'], font, hs, trk)
        if spec.get('italic'):
            k = math.tan(math.radians(spec['italic']))
            pad = int(abs(k) * a.shape[0]) + 2
            M = np.float32([[1, -k, k * base + pad], [0, 1, 0]])
            a = cv2.warpAffine(a, M, (a.shape[1] + 2 * pad, a.shape[0]))
        s = _colorize(a, base, capt, color, grad)
        if spec.get('width'):
            cols = np.where(a.max(0) > 0.05)[0]
            print('text ink width px:', (cols[-1] - cols[0]) / SS)
        _place(canvas, s, (a.shape[1] / 2, base), spec.get('angle', 0), P(spec['pos']))
    elif t == 'arc':
        # text centred on angle `mid` (deg, 0=up, clockwise positive) of circle
        cx, cy = spec['center']; R = spec['radius'] * SS
        chars = spec['text']
        widths = [font.getlength(c) * hs + trk * SS for c in chars]
        total = sum(widths)
        ang = math.radians(spec.get('mid', 0)) - (total / R) / 2
        yscale = spec.get('yscale', 1.0)  # ellipse squash for perspective
        for c, wdt in zip(chars, widths):
            a_c = ang + (wdt / 2) / R
            ang += wdt / R
            if c == ' ':
                continue
            a, base, capt = _strip(c, font, hs, 0)
            s = _colorize(a, base, capt, color, grad)
            px = cx * SS + R * math.sin(a_c)
            py = cy * SS - R * math.cos(a_c) * yscale
            # tangent angle of ellipse at a_c
            tang = math.degrees(math.atan2(R * math.sin(a_c) * yscale, R * math.cos(a_c)))
            _place(canvas, s, (a.shape[1] / 2, base), tang,
                   ((px - x0 * SS), (py - y0 * SS)))
    elif t == 'arc3':
        # circle through baseline points L, M, R; text centred at M, fitted to span L..R
        L, Mp, Rp = [np.array(v, float) for v in spec['pts']]
        ax, ay = L; bx, by = Mp; cx_, cy_ = Rp
        d = 2 * (ax * (by - cy_) + bx * (cy_ - ay) + cx_ * (ay - by))
        ux = ((ax**2 + ay**2) * (by - cy_) + (bx**2 + by**2) * (cy_ - ay) + (cx_**2 + cy_**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx_ - bx) + (bx**2 + by**2) * (ax - cx_) + (cx_**2 + cy_**2) * (bx - ax)) / d
        R1 = math.hypot(ax - ux, ay - uy)
        angf = lambda p: math.atan2(p[0] - ux, -(p[1] - uy))
        aL, aM, aR = angf(L), angf(Mp), angf(Rp)
        R = R1 * SS
        chars = spec['text']
        nat = sum(font.getlength(c) for c in chars)
        span = (aR - aL) * R
        hs = spec.get('hscale') or min(1.0, span / nat)
        widths = [font.getlength(c) * hs for c in chars]
        total = sum(widths)
        ang = (aL + aR) / 2 + math.radians(spec.get('shift_deg', 0)) - (total / R) / 2
        print('arc3: radius %.1f span %.1f natural %.1f hscale %.3f' % (R1, span / SS, nat / SS, hs))
        for c, wdt in zip(chars, widths):
            a_c = ang + (wdt / 2) / R
            ang += wdt / R
            if c == ' ':
                continue
            a, base, capt = _strip(c, font, hs, 0)
            st = _colorize(a, base, capt, color, grad)
            px = ux * SS + R * math.sin(a_c)
            py = uy * SS - R * math.cos(a_c)
            _place(canvas, st, (a.shape[1] / 2, base), math.degrees(a_c), (px - x0 * SS, py - y0 * SS))
    elif t == 'glyphpart':
        # draw only the part of `text` glyph that is not in `minus` glyph (e.g. hook of Ả)
        a1, b1, c1 = _strip(spec['text'], font, hs)
        a2, b2, c2 = _strip(spec['minus'], font, hs)
        w = min(a1.shape[1], a2.shape[1])
        a = np.clip(a1[:, :w] - cv2.dilate(a2[:, :w], np.ones((3, 3))), 0, 1)
        a[int(c1) - 2:, :] = 0  # keep only above cap height
        ys, xs = np.where(a > 0.05)
        anchor = (xs.mean(), ys.max())  # bottom centre of mark
        s = _colorize(a, b1, ys.min(), color, grad)
        _place(canvas, s, anchor, spec.get('angle', 0), P(spec['pos']))
    out = canvas
    al = canvas[..., 3]
    if spec.get('bold'):
        # thicken strokes by r px (1x units)
        r = max(1, int(round(spec['bold'] * SS)))
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        a2 = cv2.dilate(al, k)
        rgb = canvas[..., :3] / np.maximum(al[..., None], 1e-4)
        rgb = cv2.dilate(rgb, k)
        out = np.dstack([rgb * a2[..., None], a2]); al = a2
    under = np.zeros_like(out)
    if spec.get('outline'):
        r, col = spec['outline']  # radius px, BGR
        r = max(1, int(round(r * SS)))
        oa = cv2.dilate(al, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
        oa = cv2.GaussianBlur(oa, (0, 0), SS * 0.5)
        under = np.dstack([np.array(col, np.float32) * oa[..., None], oa])
    if spec.get('shadow'):
        sh = spec['shadow']  # (dx, dy, blur, opacity[, BGR])
        M = np.float32([[1, 0, sh[0] * SS], [0, 1, sh[1] * SS]])
        sa = cv2.warpAffine(al, M, (W, H))
        if sh[2] > 0:
            sa = cv2.GaussianBlur(sa, (0, 0), sh[2] * SS)
        sa *= sh[3]
        col = np.array(sh[4] if len(sh) > 4 else (0, 0, 0), np.float32)
        sl = np.dstack([col * sa[..., None], sa])
        under = under + sl * (1 - under[..., 3:4])
    out = out + under * (1 - out[..., 3:4])
    out = cv2.resize(out, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
    return out
