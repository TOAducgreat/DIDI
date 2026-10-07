"""Bộ poster thông tin "Nét thanh lịch người Tràng An": ảnh chính + 4 mục ảnh/chữ, nền ngà lụa.

    python3 info_poster.py          # dựng cả 5 bản
    python3 info_poster.py 0 A      # chỉ dựng bản 0 và A
Nội dung từng bản nằm ở noi_dung.py.
"""
import sys

from PIL import Image, ImageDraw

from brush import leaf, lotus, wash
from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W, OUT_DIR,
                    Typesetter, font, p, paper, save, seal, seed)
from noi_dung import SPECS
from paint import lay, load, silk_tone, soft_mask

FINAL = OUT_DIR.parent / "final"
IVORY = (244, 238, 228)
INK, INK2, INK3 = (30, 28, 26), (92, 84, 78), (168, 156, 148)
SON = (166, 50, 38)
PINK_L, PINK_D = (246, 228, 224), (214, 152, 150)
GREEN, GREEN_D = (190, 200, 172), (122, 140, 110)


def wrap(T, text, f, maxw):
    """Greedy word wrap; maxw in final px."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if T.width(trial, f) <= p(maxw) or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lay_art(img, name, frac, x, y, w, h=None, mask=None):
    """Crop a painting by fractions, scale to width w (and height h if given), lay it frameless."""
    src = load(name)
    box = tuple(int(v * s) for v, s in zip(frac, (src.width, src.height, src.width, src.height)))
    crop = src.crop(box)
    if h is None:
        h = crop.height * w / crop.width
    else:                                            # cover the w×h cell, centred
        r = max(w / crop.width, h / crop.height)
        cw, ch = w / r, h / r
        cx0 = (crop.width - cw) / 2
        cy0 = (crop.height - ch) / 2
        crop = crop.crop((int(cx0), int(cy0), int(cx0 + cw), int(cy0 + ch)))
    art = crop.resize((p(int(w)), p(int(h))), Image.LANCZOS)
    bg = silk_tone(src, (int(src.width * 0.1), int(src.height * 0.03), int(src.width * 0.9), int(src.height * 0.18)))
    m = soft_mask(art.size, **(mask or {}))
    lay(img, art, int(p(x)), int(p(y)), m, bg)
    return h


def tower_outline(d, cx, base, s, col):
    """Tháp Rùa in hairline ink, front view; base = ground line y, s = scale."""
    def R(x0, y0, x1, y1):
        d.rectangle([p(cx + x0 * s), p(base - y1 * s), p(cx + x1 * s), p(base - y0 * s)], outline=col, width=2)
    R(-150, 0, 150, 168); R(-166, 168, 166, 182)
    R(-112, 182, 112, 300); R(-124, 300, 124, 312)
    R(-74, 312, 74, 398); R(-86, 398, 86, 410); R(-46, 410, 46, 462)
    d.line([(p(cx - 78 * s), p(base - 462 * s)), (p(cx), p(base - 510 * s)), (p(cx + 78 * s), p(base - 462 * s))], fill=col, width=2)
    d.line([(p(cx), p(base - 510 * s)), (p(cx), p(base - 548 * s))], fill=col, width=2)
    for xc, y0, w, h in ((0, 22, 62, 110), (-92, 30, 38, 82), (92, 30, 38, 82), (0, 202, 46, 74)):
        x0, x1 = cx + (xc - w / 2) * s, cx + (xc + w / 2) * s
        top = base - (y0 + h) * s
        d.line([(p(x0), p(base - y0 * s)), (p(x0), p(top + w / 2 * s))], fill=col, width=2)
        d.line([(p(x1), p(base - y0 * s)), (p(x1), p(top + w / 2 * s))], fill=col, width=2)
        d.arc([p(x0), p(top), p(x1), p(top + w * s)], 180, 360, fill=col, width=2)
    d.ellipse([p(cx - 22 * s), p(base - 378 * s), p(cx + 22 * s), p(base - 334 * s)], outline=col, width=2)


def ho_guom_band(img, y):
    """Faint ink drawing of Hồ Gươm across the foot of the page: Thê Húc bridge, Tháp Rùa, willows."""
    d = ImageDraw.Draw(img)
    col = (178, 168, 160)
    horizon = y + 110
    d.line([(p(M), p(horizon)), (p(W - M), p(horizon))], fill=col, width=2)
    for k in range(4):                                # water
        yy = horizon + 14 + k * 12
        for x0 in range(M + 60 + k * 40, W - M - 200, 260):
            d.line([(p(x0), p(yy)), (p(x0 + 120 - k * 18), p(yy))], fill=(206, 198, 190), width=2)
    # Thê Húc bridge: a long low arch of red-painted beams (drawn in ink)
    bx0, bx1 = M + 80, M + 700
    pts = [(bx0 + (bx1 - bx0) * t / 40, horizon - 70 * (1 - (2 * t / 40 - 1) ** 2)) for t in range(41)]
    d.line([(p(x), p(yy)) for x, yy in pts], fill=col, width=3, joint="curve")
    d.line([(p(x), p(yy - 22)) for x, yy in pts], fill=col, width=2, joint="curve")
    for i in range(0, 41, 3):
        x, yy = pts[i]
        d.line([(p(x), p(yy - 22)), (p(x), p(yy))], fill=col, width=2)
    d.rectangle([p(bx1 - 10), p(horizon - 70), p(bx1 + 60), p(horizon)], outline=col, width=2)   # Đắc Nguyệt lầu gate
    d.line([(p(bx1 - 20), p(horizon - 70)), (p(bx1 + 25), p(horizon - 96)), (p(bx1 + 70), p(horizon - 70))], fill=col, width=2)
    # Tháp Rùa on its islet
    tower_outline(d, W / 2 + 120, horizon - 4, 0.27, col)
    d.arc([p(W / 2 - 20), p(horizon - 16), p(W / 2 + 260), p(horizon + 12)], 180, 360, fill=col, width=2)
    # willows on the right bank
    for k, x in enumerate((W - M - 420, W - M - 260, W - M - 120)):
        top = horizon - 120 + k * 12
        d.line([(p(x), p(horizon)), (p(x - 10), p(top))], fill=col, width=3)
        for j in range(9):
            sx = x - 70 + j * 17
            d.arc([p(sx - 30), p(top - 6), p(sx + 30), p(top + 70 + (j % 3) * 14)], 270, 360, fill=col, width=2)


def item(img, T, x, y, w, h, heading, art, body, image_left):
    iw = 420
    tx = x + iw + 44 if image_left else x
    ix = x if image_left else x + w - iw
    lay_art(img, art[0], art[1], ix, y + 10, iw, iw,
            mask=dict(inset=0.03, blur=0.07, roughness=0.6, fade_top=0.06, fade_bottom=0.08, fade_x=0.06, seed=len(heading)))
    T = Typesetter(img)
    d = ImageDraw.Draw(img)
    tw = w - iw - 44
    d.polygon([(p(tx + 10), p(y + 34)), (p(tx + 20), p(y + 44)), (p(tx + 10), p(y + 54)), (p(tx), p(y + 44))], fill=SON)
    hf = font("PlayfairDisplay-Italic[wght].ttf", 46, 500)
    hy = y + 62
    for line in wrap(T, heading, hf, tw - 34):
        T.put(line, hf, tx + 34, hy, SON)
        hy += 58
    d.line([(p(tx), p(hy - 20)), (p(tx + 90), p(hy - 20))], fill=INK3, width=2)
    bf = font("BeVietnamPro-Light.ttf", 31)
    by = hy + 34
    for line in wrap(T, body, bf, tw):
        T.put(line, bf, tx, by, INK2)
        by += 49
    assert by - 49 < y + h + 10, f"text overflows cell: {heading}"
    return T


def render(spec):
    seed(sum(map(ord, spec["name"])))
    img = paper(spec["bottom"], top=IVORY, grain=3.0, vignette=14, fibres=700, fibre_col=(212, 202, 190))
    cx = W / 2

    # corner lotus, ink & wash
    d = ImageDraw.Draw(img)
    leaf(img, d, M + 170, 640, 150, 40, (120, 112, 104), GREEN, GREEN_D, rot=-0.1, curl=0.5)
    lotus(img, d, M + 150, 600, 170, (110, 100, 96), PINK_L, PINK_D, open_=0.95)
    T = Typesetter(img)
    d = ImageDraw.Draw(img)

    # header label with rules
    lf = font("BeVietnamPro-Light.ttf", 26)
    label = "HÀ NỘI XƯA  ·  THĂNG LONG"
    lw = T.width(label, lf, 10) / 2
    T.put(label, lf, cx, 214, INK2, track=10, anchor="c")
    d.line([(p(cx - lw / 2 - 260), p(205)), (p(cx - lw / 2 - 40), p(205))], fill=INK3, width=2)
    d.line([(p(cx + lw / 2 + 40), p(205)), (p(cx + lw / 2 + 260), p(205))], fill=INK3, width=2)
    T.put(spec["no"], font("BeVietnamPro-Light.ttf", 24), W - M, 214, INK3, track=6, anchor="r")

    # title
    T.put(TITLE, font("PlayfairDisplay[wght].ttf", 200, 400), cx, 450, INK, track=1, anchor="c")
    sw = T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 136, 400), cx, 620, SON, anchor="c")
    seal(img, cx + sw / 2 + 86, 578, 100, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 25, 500))
    T = Typesetter(img)
    T.put(spec["theme"].upper(), font("BeVietnamPro-Medium.ttf", 30), cx, 730, SON, track=12, anchor="c")
    lead_f = font("PlayfairDisplay-Italic[wght].ttf", 38, 400)
    ly = 800
    for line in wrap(T, spec["lead"], lead_f, 1500):
        T.put(line, lead_f, cx, ly, INK2, anchor="c")
        ly += 54

    # hero painting
    wash(img, [], (250, 246, 240), alpha=0.7, blur=80, ellipses=[(cx - 1000, ly, cx + 1000, 1780)])
    hw = spec["hero_w"]
    gy = 1820
    hero_top = ly + 10
    lay_art(img, spec["hero"][0], spec["hero"][1], cx - hw / 2, hero_top, hw, gy - 60 - hero_top,
            mask=dict(inset=0.03, blur=0.08, roughness=0.7, fade_top=0.16, fade_bottom=0.16, fade_x=0.1, seed=2))

    # 2×2 grid of items
    T = Typesetter(img)
    d = ImageDraw.Draw(img)
    gx0, gx1 = M, W - M
    cw, chh, gap = (gx1 - gx0 - 80) / 2, 450, 60
    d.line([(p(cx), p(gy + 20)), (p(cx), p(gy + 2 * chh + gap - 20))], fill=INK3, width=2)
    d.line([(p(gx0 + 40), p(gy + chh + gap / 2)), (p(gx1 - 40), p(gy + chh + gap / 2))], fill=INK3, width=2)
    for i, (heading, art, body) in enumerate(spec["items"]):
        r, c = divmod(i, 2)
        x = gx0 + c * (cw + 80)
        y = gy + r * (chh + gap)
        T = item(img, T, x, y, cw, chh, heading, art, body, image_left=(r == 0))

    # closing ca dao + Hồ Gươm band
    d = ImageDraw.Draw(img)
    cy0 = gy + 2 * chh + gap + 90
    cf = font("PlayfairDisplay-Italic[wght].ttf", 42, 400)
    T.put(CA_DAO[0], cf, cx, cy0, INK, anchor="c")
    T.put(CA_DAO[1], cf, cx, cy0 + 58, INK, anchor="c")
    ho_guom_band(img, cy0 + 130)
    d = ImageDraw.Draw(img)

    # credits
    T = Typesetter(img)
    by = 3260
    d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK3, width=2)
    nf = font("BeVietnamPro-Medium.ttf", 34)
    sf = font("BeVietnamPro-Light.ttf", 29)
    T.put(f"{NAMES[0]}  ·  {NAMES[1]}", nf, M, by + 80, INK)
    T.put("THỰC HIỆN", font("BeVietnamPro-Light.ttf", 20), M, by + 132, INK2, track=7)
    T.put(f"{CLASS}  ·  {SCHOOL}", sf, W - M, by + 80, INK, anchor="r")
    T.put("ĐƠN VỊ", font("BeVietnamPro-Light.ttf", 20), W - M, by + 132, INK2, track=7, anchor="r")

    return save(img, spec["name"], FINAL)


def contact_sheet():
    names = [s["name"] for s in SPECS.values() if (FINAL / f"{s['name']}.png").exists()]
    thumbs = [Image.open(FINAL / f"{n}.png").resize((620, 877), Image.LANCZOS) for n in names]
    sheet = Image.new("RGB", (40 + 660 * len(thumbs), 957), (228, 224, 218))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (40 + 660 * i, 40))
    sheet.save(FINAL / "tong-hop.png")
    print("saved", FINAL / "tong-hop.png")


if __name__ == "__main__":
    for k in sys.argv[1:] or list(SPECS):
        render(SPECS[k])
    contact_sheet()
