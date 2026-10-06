"""Phương án A — Đêm Hồ Gươm: trăng rằm, Tháp Rùa, mặt hồ, nền mực chàm."""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, H, M, W, CW, CH,
                    Typesetter, font, p, paper, save, seal, seed)

seed(1010)
NIGHT_TOP, NIGHT = (22, 29, 42), (15, 19, 28)
CREAM = (236, 226, 204)
CREAM2 = (176, 168, 150)
GOLD = (198, 166, 112)
SON = (170, 52, 38)

img = paper(NIGHT, grain=2.2, vignette=10, top=NIGHT_TOP, fibres=0)
cx = W / 2
MOON_Y, MOON_R = 1080, 400
WATER = 1560

# ---- moon glow + disc ----
glow = Image.new("L", (CW, CH), 0)
ImageDraw.Draw(glow).ellipse([p(cx - MOON_R - 60), p(MOON_Y - MOON_R - 60),
                              p(cx + MOON_R + 60), p(MOON_Y + MOON_R + 60)], fill=60)
glow = glow.filter(ImageFilter.GaussianBlur(p(120)))
img = Image.composite(Image.new("RGB", (CW, CH), (90, 92, 96)), img, glow)

moon = Image.new("L", (CW, CH), 0)
ImageDraw.Draw(moon).ellipse([p(cx - MOON_R), p(MOON_Y - MOON_R), p(cx + MOON_R), p(MOON_Y + MOON_R)], fill=255)
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
# quiet surface: soft shading + mottled grain
r = np.sqrt((xx - p(cx - 90)) ** 2 + (yy - p(MOON_Y - 110)) ** 2) / p(MOON_R * 1.6)
shade = np.clip(1 - r * 0.22, 0, 1)
mott = np.clip(np.random.normal(128, 40, (CH // 24, CW // 24)), 0, 255).astype(np.uint8)
mott = Image.fromarray(mott).filter(ImageFilter.GaussianBlur(1.6)).resize((CW, CH), Image.BICUBIC)
mott = (np.asarray(mott, np.float32) - 128) / 10
mc = (np.array(CREAM, np.float32) * shade[..., None]) - (mott[..., None] * 4)
moon_rgb = Image.fromarray(np.clip(mc, 0, 255).astype(np.uint8))
img = Image.composite(moon_rgb, img, moon.filter(ImageFilter.GaussianBlur(1.5)))
del yy, xx, r, shade, mott, mc
d = ImageDraw.Draw(img)

# ---- Tháp Rùa (front silhouette) ----
SIL = (13, 16, 23)
tx, ty, u = cx, WATER - 34, 0.86


def R(x0, y0, x1, y1):
    d.rectangle([p(tx + x0 * u), p(ty - y1 * u), p(tx + x1 * u), p(ty - y0 * u)], fill=SIL)


def arch(xc, y0, w, h, col):
    """Arched opening; y0 = sill height."""
    x0, x1 = tx + (xc - w / 2) * u, tx + (xc + w / 2) * u
    top = ty - (y0 + h) * u
    rr = w / 2 * u
    d.rectangle([p(x0), p(top + rr), p(x1), p(ty - y0 * u)], fill=col)
    d.ellipse([p(x0), p(top), p(x1), p(top + 2 * rr)], fill=col)


def roundwin(xc, yc, rr, col):
    d.ellipse([p(tx + (xc - rr) * u), p(ty - (yc + rr) * u), p(tx + (xc + rr) * u), p(ty - (yc - rr) * u)], fill=col)


LIT = (92, 84, 70)
R(-150, 0, 150, 168)
R(-166, 168, 166, 182)
R(-112, 182, 112, 300)
R(-124, 300, 124, 312)
R(-74, 312, 74, 398)
R(-86, 398, 86, 410)
R(-46, 410, 46, 462)
# curved roof of the crowning pavilion
roof = []
for i in range(41):
    t = i / 40
    x = -78 + 156 * t
    y = 462 + 48 * (1 - abs(2 * t - 1)) ** 0.7 + (10 if t in (0, 1) else 0)
    roof.append((p(tx + x * u), p(ty - y * u)))
roof += [(p(tx + 60 * u), p(ty - 462 * u)), (p(tx - 60 * u), p(ty - 462 * u))]
d.polygon(roof, fill=SIL)
for sx in (-1, 1):  # upturned eaves
    d.line([(p(tx + sx * 66 * u), p(ty - 466 * u)), (p(tx + sx * 84 * u), p(ty - 478 * u))], fill=SIL, width=p(6))
d.line([(p(tx), p(ty - 505 * u)), (p(tx), p(ty - 552 * u))], fill=SIL, width=p(5))
d.ellipse([p(tx - 8 * u), p(ty - 560 * u), p(tx + 8 * u), p(ty - 544 * u)], fill=SIL)
# openings, faintly lit
arch(0, 22, 62, 110, LIT)
arch(-92, 30, 38, 82, LIT)
arch(92, 30, 38, 82, LIT)
arch(0, 202, 46, 74, LIT)
roundwin(-70, 240, 14, LIT)
roundwin(70, 240, 14, LIT)
roundwin(0, 356, 22, LIT)
arch(0, 420, 24, 32, LIT)

# islet with trees
d.ellipse([p(cx - 330), p(WATER - 40), p(cx + 330), p(WATER + 16)], fill=SIL)
random.seed(7)
for side in (-1, 1):
    for k in range(26):
        off = random.uniform(150, 320)
        bx = cx + side * off
        by = WATER - 26 - random.uniform(0, 1) * (90 - off * 0.22)
        rr = random.uniform(14, 30)
        d.ellipse([p(bx - rr), p(by - rr), p(bx + rr), p(by + rr)], fill=SIL)

# ---- water: moon reflection broken into ripples ----
water_top = WATER + 18
random.seed(11)
for k in range(120):
    y = water_top + k * 7.2
    if y > 2240:
        break
    depth = (y - water_top) / (2240 - water_top)
    half = MOON_R * (0.95 - depth * 0.55) * random.uniform(0.75, 1.05)
    alpha = 0.95 - depth * 0.9
    col = tuple(int(NIGHT[i] + (CREAM[i] - NIGHT[i]) * alpha) for i in range(3))
    # tower reflection gap
    gap = (64 if depth < 0.16 else 0) * random.uniform(0.85, 1.1)
    x = cx - half
    while x < cx + half:
        seg = random.uniform(18, 120)
        x1 = min(x + seg, cx + half)
        a0, a1 = x, x1
        if gap and a1 > cx - gap and a0 < cx + gap:
            if a0 < cx - gap:
                d.line([(p(a0), p(y)), (p(cx - gap), p(y))], fill=col, width=p(2))
            if a1 > cx + gap:
                d.line([(p(cx + gap), p(y)), (p(a1), p(y))], fill=col, width=p(2))
        else:
            d.line([(p(a0), p(y)), (p(a1), p(y))], fill=col, width=p(2))
        x = x1 + random.uniform(6, 40)
# far ripples across the whole lake
for k in range(60):
    y = water_top + 10 + k * 12
    if y > 2250:
        break
    for _ in range(3):
        L = random.uniform(30, 160)
        xs = random.uniform(M, W - M - L)
        d.line([(p(xs), p(y)), (p(xs + L), p(y))], fill=(40, 46, 58), width=3)

# horizon line
d.line([(p(M), p(WATER + 4)), (p(cx - 360), p(WATER + 4))], fill=(58, 62, 72), width=p(1))
d.line([(p(cx + 360), p(WATER + 4)), (p(W - M), p(WATER + 4))], fill=(58, 62, 72), width=p(1))

# ---- typography ----
T = Typesetter(img)
small = font("BeVietnamPro-Light.ttf", 24)
T.put("HỒ HOÀN KIẾM", small, M, 250, CREAM2, track=8)
T.put("ĐÊM RẰM  ·  THÁNG TÁM", small, W - M, 250, CREAM2, track=8, anchor="r")
T.vertical("THĂNG LONG  ·  ĐÔNG ĐÔ  ·  HÀ NỘI", small, M + 4, 1100, CREAM2, track=10)
T.vertical("NGHÌN NĂM VĂN HIẾN", small, W - M - 4, 1100, CREAM2, track=10)

ty0 = 2540
T.put(TITLE, font("PlayfairDisplay[wght].ttf", 228, 400), cx, ty0, CREAM, track=1, anchor="c")
T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 160, 400), cx, ty0 + 200, GOLD, anchor="c")
oy = ty0 + 300
d = ImageDraw.Draw(img)
d.line([(p(cx - 220), p(oy)), (p(cx - 24), p(oy))], fill=(90, 90, 92), width=p(1))
d.line([(p(cx + 24), p(oy)), (p(cx + 220), p(oy))], fill=(90, 90, 92), width=p(1))
d.ellipse([p(cx - 6), p(oy - 6), p(cx + 6), p(oy + 6)], fill=SON)
cf = font("PlayfairDisplay-Italic[wght].ttf", 44, 400)
T.put(CA_DAO[0], cf, cx, oy + 100, CREAM2, anchor="c")
T.put(CA_DAO[1], cf, cx, oy + 168, CREAM2, anchor="c")

by = 3240
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=(70, 72, 80), width=p(1))
nf = font("BeVietnamPro-Regular.ttf", 34)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(f"{NAMES[0]}   ·   {NAMES[1]}", nf, M, by + 80, CREAM, track=1)
T.put(CLASS, lf, M, by + 132, CREAM2, track=1)
T.put(SCHOOL, lf, W - M, by + 132, CREAM2, track=1, anchor="r")
T.put("2026", lf, W - M, by + 80, CREAM2, track=4, anchor="r")

seal(img, cx + 650, ty0 + 128, 108, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 28, 500))
save(img, "A-dem-ho-guom")
