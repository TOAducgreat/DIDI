"""Silk-painting helpers: smooth splines, soft washes, lotus flowers and leaves."""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from common import CH, CW, p


def spline(pts, closed=True, n=24):
    """Catmull-Rom through pts (final-px coords) -> dense list (final-px)."""
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    if not closed:
        out.append(P[-2])
    return out


def S(pts):
    return [(p(x), p(y)) for x, y in pts]


def silk(color, weave=(0, 0, 0), strength=5):
    """Silk ground: soft tone variation + fine warp/weft threads."""
    base = np.zeros((CH, CW, 3), np.float32) + np.array(color, np.float32)
    blot = np.clip(np.random.normal(128, 40, (CH // 60, CW // 60)), 0, 255).astype(np.uint8)
    blot = Image.fromarray(blot).filter(ImageFilter.GaussianBlur(2)).resize((CW, CH), Image.BICUBIC)
    base += ((np.asarray(blot, np.float32) - 128) / 128 * 6)[..., None]
    g = np.random.normal(0, 2.2, (CH // 2, CW // 2)).astype(np.float32)
    g = np.array(Image.fromarray(g).resize((CW, CH), Image.BILINEAR))
    base += g[..., None]
    ys = (np.sin(np.arange(CH, dtype=np.float32) * 2 * math.pi / 7) * 0.5 + 0.5)[:, None]
    xs = (np.sin(np.arange(CW, dtype=np.float32) * 2 * math.pi / 7) * 0.5 + 0.5)[None, :]
    base -= ((ys * 0.5 + xs * 0.5) * strength)[..., None]
    yy, xx = np.mgrid[0:CH:1, 0:CW:1].astype(np.float32)
    d = np.sqrt(((xx - CW / 2) / (CW / 2)) ** 2 + ((yy - CH / 2) / (CH / 2)) ** 2)
    base -= (np.clip(d - 0.5, 0, None) ** 2 * 30)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")


def wash(img, polys, color, alpha=0.5, blur=6, ellipses=()):
    """Soft colour wash through polygon/ellipse mask (final-px coords)."""
    m = Image.new("L", (CW, CH), 0)
    md = ImageDraw.Draw(m)
    for poly in polys:
        md.polygon(S(poly), fill=int(255 * alpha))
    for (x0, y0, x1, y1) in ellipses:
        md.ellipse([p(x0), p(y0), p(x1), p(y1)], fill=int(255 * alpha))
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(p(blur)))
    img.paste(Image.new("RGB", (CW, CH), color), (0, 0), m)


def gradient_fill(img, poly, c_top, c_bot, y_top, y_bot, alpha=1.0, blur=1.2):
    m = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(m).polygon(S(poly), fill=int(255 * alpha))
    if blur:
        m = m.filter(ImageFilter.GaussianBlur(blur))
    bbox = m.getbbox()
    if not bbox:
        return
    x0, y0, x1, y1 = bbox
    h = y1 - y0
    t = np.clip((np.arange(y0, y1, dtype=np.float32) - p(y_top)) / max(1, p(y_bot) - p(y_top)), 0, 1)[:, None, None]
    col = np.array(c_top, np.float32) * (1 - t) + np.array(c_bot, np.float32) * t
    col = np.broadcast_to(col, (h, x1 - x0, 3)).astype(np.uint8)
    img.paste(Image.fromarray(col.copy()), (x0, y0), m.crop(bbox))


def ink(d, pts, col, w=1.6, closed=False):
    pts = list(pts)
    if closed:
        pts = pts + [pts[0]]
    d.line(S(pts), fill=col, width=max(1, int(round(w * 2))), joint="curve")


def stroke(d, pts, col, w0=1.0, w1=4.0, closed=False):
    """Brush stroke that swells in the middle: draw as tapered polygon."""
    pts = list(pts)
    n = len(pts)
    left, right = [], []
    for i in range(n):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        t = i / (n - 1)
        w = w0 + (w1 - w0) * math.sin(math.pi * t)
        left.append((pts[i][0] + nx * w / 2, pts[i][1] + ny * w / 2))
        right.append((pts[i][0] - nx * w / 2, pts[i][1] - ny * w / 2))
    d.polygon(S(left + right[::-1]), fill=col)


def petal(base, length, width, angle, cup=0.0):
    """Lotus petal outline (pointed tip); angle in radians, 0 = pointing right."""
    bx, by = base
    ca, sa = math.cos(angle), math.sin(angle)
    left, right = [], []
    N = 28
    for j in range(N + 1):
        t = j / N
        half = width * (math.sin(math.pi * min(1, t * 1.05)) ** 0.9) * (1 - 0.55 * t ** 2.2)
        along = length * t
        bend = cup * math.sin(math.pi * t) * width * 0.3
        for side, arr in ((1, left), (-1, right)):
            lx, ly = along, side * half + bend
            arr.append((bx + lx * ca - ly * sa, by + lx * sa + ly * ca))
    return left + right[::-1]


def lotus(img, d, cx, cy, size, ink_col, pink_light, pink_deep, open_=1.0, tilt=0.0):
    """Side-view lotus bloom centred on its base (cx, cy). Back petals first."""
    spec = [  # (angle from vertical deg, length, width, layer)
        (-62, 0.82, 0.30, 0), (62, 0.82, 0.30, 0), (-34, 0.98, 0.32, 0), (34, 0.98, 0.32, 0),
        (-12, 1.02, 0.30, 0), (12, 1.02, 0.30, 0),
        (-48, 0.80, 0.30, 1), (48, 0.80, 0.30, 1), (-22, 0.92, 0.32, 1), (22, 0.92, 0.32, 1),
        (0, 0.96, 0.34, 2), (-70, 0.62, 0.26, 2), (70, 0.62, 0.26, 2),
    ]
    for ang, L, Wd, layer in spec:
        a = math.radians(-90 + ang * open_ + tilt)
        poly = petal((cx, cy), size * L, size * Wd, a, cup=0.4)
        ys = [q[1] for q in poly]
        top_y, bot_y = min(ys), max(ys)
        # light base -> pink tip (tip is the far end of the petal)
        gradient_fill(img, poly, pink_deep, pink_light, top_y, top_y + (bot_y - top_y) * 0.75)
        ink(d, poly, ink_col, w=1.1, closed=True)
        # petal veins
        ca, sa = math.cos(a), math.sin(a)
        for v in (-0.3, 0, 0.3):
            pts = []
            for j in range(10):
                t = 0.12 + 0.7 * j / 9
                lx, ly = size * L * t, size * Wd * v * math.sin(math.pi * (t + 0.05))
                pts.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
            ink(d, pts, pink_deep, w=0.7)
    # seed pod glimpse
    d.ellipse([p(cx - size * 0.12), p(cy - size * 0.2), p(cx + size * 0.12), p(cy - size * 0.08)],
              fill=(214, 196, 120), outline=ink_col, width=2)


def bud(img, d, cx, cy, size, ink_col, pink_light, pink_deep, tilt=0.0):
    for ang, Wd in ((-14, 0.36), (14, 0.36), (0, 0.42)):
        a = math.radians(-90 + ang + tilt)
        poly = petal((cx, cy), size, size * Wd, a, cup=0.2)
        ys = [q[1] for q in poly]
        gradient_fill(img, poly, pink_deep, pink_light, min(ys), max(ys))
        ink(d, poly, ink_col, w=1.1, closed=True)


def leaf(img, d, cx, cy, rx, ry, ink_col, green, green_deep, rot=0.0, curl=0.0):
    """Lotus leaf seen in perspective: wavy ellipse with radial veins."""
    pts = []
    N = 90
    random.seed(int(cx * 7 + cy))
    for k in range(N):
        a = 2 * math.pi * k / N
        wob = 1 + 0.035 * math.sin(a * 9 + cx) + 0.02 * math.sin(a * 17)
        x, y = math.cos(a) * rx * wob, math.sin(a) * ry * wob
        if curl and math.sin(a) < 0:
            y *= 1 + curl * (-math.sin(a))
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    gradient_fill(img, pts, green, green_deep, cy - ry, cy + ry)
    ink(d, pts, ink_col, w=1.2, closed=True)
    for k in range(18):
        a = 2 * math.pi * k / 18
        x, y = math.cos(a) * rx * 0.92, math.sin(a) * ry * 0.92
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        ink(d, [(cx, cy), (cx + xr * 0.5 + yr * 0.04, cy + yr * 0.5), (cx + xr, cy + yr)], green_deep, w=0.8)
    d.ellipse([p(cx - 5), p(cy - 3), p(cx + 5), p(cy + 3)], fill=green_deep)
