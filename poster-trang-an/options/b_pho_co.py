"""Phương án B — Phố cổ: dãy nhà ống tường vàng, xe đạp chở hoa cúc họa mi."""
import math
import random

from PIL import ImageDraw

from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W,
                    Typesetter, font, p, paper, save, seal, seed)

seed(1976)
PAPER = (241, 235, 222)
NAVY = (34, 45, 66)
NAVY2 = (98, 108, 124)
YELLOW = (232, 205, 146)     # vàng tường Hà Nội
YELLOW2 = (219, 186, 122)
SON = (164, 62, 46)
WHITE = (250, 247, 240)

img = paper(PAPER, grain=3.0, vignette=18, fibres=700, fibre_col=(214, 204, 184))
d = ImageDraw.Draw(img)
T = Typesetter(img)
LW = 3  # base stroke (supersampled px)


def L(pts, col=NAVY, w=LW):
    d.line([(p(x), p(y)) for x, y in pts], fill=col, width=w, joint="curve")


def rect(x0, y0, x1, y1, col=NAVY, w=LW, fill=None):
    d.rectangle([p(x0), p(y0), p(x1), p(y1)], outline=col, width=w, fill=fill)


# ---------- header + title ----------
small = font("BeVietnamPro-Light.ttf", 24)
T.put("PHỐ CỔ HÀ NỘI", small, M, 250, NAVY2, track=8)
T.put("36 PHỐ PHƯỜNG", small, W - M, 250, NAVY2, track=8, anchor="r")
d.line([(p(M), p(286)), (p(W - M), p(286))], fill=NAVY2, width=2)

T.put(TITLE, font("PlayfairDisplay[wght].ttf", 250, 500), M - 10, 600, NAVY)
T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 180, 400), M + 360, 820, SON)
cf = font("PlayfairDisplay-Italic[wght].ttf", 40, 400)
T.put(CA_DAO[0], cf, M, 990, NAVY2)
T.put(CA_DAO[1], cf, M, 1050, NAVY2)

# ---------- street of tube houses ----------
GROUND = 2790
houses = [  # x0, width, floors, roof style
    (M + 20, 360, 3, "tile"),
    (M + 380, 300, 2, "tile"),
    (M + 680, 420, 4, "flat"),
    (M + 1100, 330, 3, "tile"),
    (M + 1430, 290, 2, "tile"),
    (M + 1720, 400, 3, "flat"),
]
FLOOR = 330


def louvres(x0, y0, x1, y1, step=16):
    rect(x0, y0, x1, y1)
    xm = (x0 + x1) / 2
    L([(xm, y0), (xm, y1)], w=2)
    y = y0 + step
    while y < y1 - 4:
        L([(x0 + 6, y), (xm - 6, y)], col=NAVY2, w=2)
        L([(xm + 6, y), (x1 - 6, y)], col=NAVY2, w=2)
        y += step


def balcony(x0, x1, y):
    L([(x0 - 14, y), (x1 + 14, y)], w=LW + 1)
    L([(x0 - 14, y - 70), (x1 + 14, y - 70)], w=2)
    x = x0 - 14
    while x <= x1 + 14:
        L([(x, y - 70), (x, y)], col=NAVY2, w=2)
        x += 18


for i, (x0, wd, fl, roof) in enumerate(houses):
    x1 = x0 + wd
    top = GROUND - fl * FLOOR
    tint = YELLOW if i % 2 == 0 else YELLOW2
    if i == 3:
        tint = (228, 214, 190)
    d.rectangle([p(x0), p(top), p(x1), p(GROUND)], fill=tint)
    rect(x0, top, x1, GROUND)
    # cornice per floor
    for f in range(1, fl):
        y = GROUND - f * FLOOR
        L([(x0 - 8, y), (x1 + 8, y)], w=LW + 1)
    # roof
    if roof == "tile":
        rh = 120
        poly = [(x0 - 22, top), (x0 + 28, top - rh), (x1 - 28, top - rh), (x1 + 22, top)]
        d.polygon([(p(a), p(b)) for a, b in poly], fill=(176, 104, 80), outline=NAVY, width=LW)
        # tile rows
        for k in range(1, 7):
            yy = top - rh * k / 7
            off = 50 * k / 7
            L([(x0 - 22 + off * 1.0, yy), (x1 + 22 - off, yy)], col=(120, 70, 58), w=2)
        n = int(wd / 22)
        for k in range(n + 1):
            t = k / n
            L([(x0 - 22 + (wd + 44) * t, top), (x0 + 28 + (wd - 56) * t, top - rh)], col=(140, 82, 66), w=1)
        L([(x0 + 20, top - rh - 6), (x1 - 20, top - rh - 6)], w=LW + 1)
    else:
        # parapet with a little pediment
        L([(x0 - 14, top), (x1 + 14, top)], w=LW + 2)
        rect(x0 + 10, top - 50, x1 - 10, top)
        cxh = (x0 + x1) / 2
        L([(cxh - 80, top - 50), (cxh, top - 110), (cxh + 80, top - 50)], w=LW)
        d.ellipse([p(cxh - 14), p(top - 88), p(cxh + 14), p(top - 60)], outline=NAVY, width=2)
    # upper floors: shuttered windows + balconies
    for f in range(1, fl):
        yb = GROUND - f * FLOOR
        nwin = 2 if wd > 320 else 1
        ww = 92 if nwin == 2 else 110
        gap = (wd - nwin * ww) / (nwin + 1)
        for k in range(nwin):
            wx = x0 + gap * (k + 1) + ww * k
            # arched head
            d.arc([p(wx), p(yb - 250), p(wx + ww), p(yb - 250 + ww)], 180, 360, fill=NAVY, width=LW)
            louvres(wx, yb - 250 + ww / 2, wx + ww, yb - 30)
            # open shutters on some windows
            if (i + f + k) % 3 == 0:
                d.rectangle([p(wx + 8), p(yb - 250 + ww / 2 + 8), p(wx + ww - 8), p(yb - 38)], fill=(60, 66, 80))
        if (i + f) % 2 == 0:
            balcony(x0 + 24, x1 - 24, yb - 6)
            # potted plants on balcony
            for k in range(3):
                px = x0 + 50 + k * (wd - 100) / 2
                d.ellipse([p(px - 20), p(yb - 112), p(px + 20), p(yb - 72)], fill=(96, 120, 92))
    # ground floor: folding wooden doors
    gy = GROUND - FLOOR + 40
    rect(x0 + 24, gy, x1 - 24, GROUND)
    nd = int((wd - 48) / 40)
    for k in range(1, nd):
        xx = x0 + 24 + (wd - 48) * k / nd
        L([(xx, gy), (xx, GROUND)], col=NAVY2, w=2)
    # shop sign
    rect(x0 + 40, gy - 34, x1 - 40, gy - 6, w=2, fill=WHITE)

# street
L([(M - 40, GROUND), (W - M + 40, GROUND)], w=LW + 2)
for k in range(5):
    y = GROUND + 30 + k * 26
    L([(M + 40 * k, y), (W - M - 40 * k, y)], col=(200, 190, 170), w=2)

# ---------- bicycle with daisies ----------
K = 1.2
WR = 150 * K
bx0, by0 = 1120, GROUND + 76 - WR   # rear hub
fx0 = bx0 + 470 * K
d.rectangle([p(bx0 - WR - 30), p(GROUND + 64), p(fx0 + WR + 30), p(GROUND + 78)], fill=(222, 212, 192))


def wheel(cx, cy):
    for rr, w in ((WR, LW + 3), (WR - 10, 2)):
        d.ellipse([p(cx - rr), p(cy - rr), p(cx + rr), p(cy + rr)], outline=NAVY, width=w)
    for k in range(28):
        a = 2 * math.pi * k / 28
        L([(cx, cy), (cx + math.cos(a) * (WR - 10), cy + math.sin(a) * (WR - 10))], col=NAVY2, w=1)
    d.ellipse([p(cx - 9), p(cy - 9), p(cx + 9), p(cy + 9)], fill=NAVY)


wheel(bx0, by0)
wheel(fx0, by0)
BB = (bx0 + 200 * K, by0 + 6)
seat_top = (bx0 + 150 * K, by0 - 230 * K)
head_top = (fx0 - 60 * K, by0 - 250 * K)
head_bot = (fx0 - 48 * K, by0 - 190 * K)
FR = (SON, LW + 5)
L([BB, (bx0, by0)], *FR)
L([seat_top, (bx0, by0)], *FR)
L([BB, seat_top], *FR)
# step-through curved down tube
curve = []
for k in range(21):
    t = k / 20
    x = (1 - t) ** 2 * BB[0] + 2 * (1 - t) * t * (BB[0] + 120) + t * t * head_bot[0]
    y = (1 - t) ** 2 * BB[1] + 2 * (1 - t) * t * (BB[1] - 40) + t * t * head_bot[1]
    curve.append((x, y))
L(curve, *FR)
L([head_top, head_bot], col=SON, w=LW + 7)
L([head_bot, (fx0, by0)], *FR)  # fork
# handlebar
L([head_top, (head_top[0] - 6, head_top[1] - 40), (head_top[0] - 70, head_top[1] - 56), (head_top[0] - 110, head_top[1] - 46)], w=LW + 3)
# saddle
d.ellipse([p(seat_top[0] - 54), p(seat_top[1] - 22), p(seat_top[0] + 40), p(seat_top[1] + 4)], fill=NAVY)
L([(seat_top[0], seat_top[1]), (seat_top[0] + 2, seat_top[1] - 8)], w=LW)
# chainring + mudguards
d.ellipse([p(BB[0] - 34), p(BB[1] - 34), p(BB[0] + 34), p(BB[1] + 34)], outline=NAVY, width=LW)
L([BB, (BB[0] + 30, BB[1] + 60)], w=LW + 1)
L([(BB[0] + 14, BB[1] + 60), (BB[0] + 50, BB[1] + 60)], w=LW + 4)
for cx in (bx0, fx0):
    d.arc([p(cx - WR - 16), p(by0 - WR - 16), p(cx + WR + 16), p(by0 + WR + 16)], 200, 340, fill=SON, width=LW + 1)
# rear rack + basket
rack_y = by0 - WR - 24
L([(bx0 - 110, rack_y), (bx0 + 130, rack_y)], w=LW + 2)
L([(bx0 - 90, rack_y), (bx0, by0)], w=2)
L([(bx0 + 110, rack_y), (bx0, by0)], w=2)
kx0, kx1, ky0 = bx0 - 130, bx0 + 150, rack_y - 150
d.polygon([(p(kx0), p(ky0)), (p(kx1), p(ky0)), (p(kx1 - 18), p(rack_y)), (p(kx0 + 18), p(rack_y))],
          fill=(206, 170, 112), outline=NAVY, width=LW)
for k in range(1, 6):
    y = ky0 + 150 * k / 6
    L([(kx0 + 3 * k, y), (kx1 - 3 * k, y)], col=(140, 104, 62), w=2)
for k in range(1, 12):
    t = k / 12
    L([(kx0 + (kx1 - kx0) * t, ky0), (kx0 + 18 + (kx1 - kx0 - 36) * t, rack_y)], col=(160, 122, 76), w=1)

# daisies (cúc họa mi) heaped above the basket
random.seed(5)
centers = []
for _ in range(80):
    a = random.uniform(math.pi * 1.04, math.pi * 1.96)
    rr = random.uniform(0, 1) ** 0.6
    x = (kx0 + kx1) / 2 + math.cos(a) * 190 * rr
    y = ky0 + 10 + math.sin(a) * 170 * rr
    centers.append((x, y, random.uniform(14, 24)))
centers.sort(key=lambda c: c[1])
for x, y, r in centers:
    L([(x, y), (x + random.uniform(-20, 20), ky0 + 20)], col=(110, 130, 96), w=2)
for x, y, r in centers:
    for k in range(12):
        a = 2 * math.pi * k / 12 + random.uniform(-0.1, 0.1)
        ex, ey = x + math.cos(a) * r * 0.62, y + math.sin(a) * r * 0.62
        d.ellipse([p(ex - r * 0.42), p(ey - r * 0.42), p(ex + r * 0.42), p(ey + r * 0.42)], fill=WHITE, outline=(170, 168, 160), width=1)
    d.ellipse([p(x - r * 0.3), p(y - r * 0.3), p(x + r * 0.3), p(y + r * 0.3)], fill=(214, 168, 64))

# a few daisies also in the front basket
fb0, fb1, fy0, fy1 = head_top[0] + 14, head_top[0] + 130, head_top[1] + 4, head_top[1] + 96
random.seed(9)
front = [(fb0 + 14 + 22 * k + random.uniform(-4, 4), fy0 - 6 - 26 * math.sin(math.pi * k / 4) - random.uniform(0, 6), 15) for k in range(5)] + \
        [(fb0 + 26 + 22 * k, fy0 - 34 - 18 * math.sin(math.pi * k / 3), 14) for k in range(4)]
for x, y, r in front:
    L([(x, y), (x, fy0 + 10)], col=(110, 130, 96), w=2)
d.polygon([(p(fb0), p(fy0)), (p(fb1), p(fy0)), (p(fb1 - 10), p(fy1)), (p(fb0 + 10), p(fy1))], fill=(206, 170, 112), outline=NAVY, width=LW)
for k in range(1, 4):
    L([(fb0 + 3 * k, fy0 + 23 * k), (fb1 - 3 * k, fy0 + 23 * k)], col=(140, 104, 62), w=2)
L([(fb0, fy0 + 10), head_top], w=LW)
for x, y, r in front:
    for j in range(10):
        a = 2 * math.pi * j / 10
        ex, ey = x + math.cos(a) * r * 0.6, y + math.sin(a) * r * 0.6
        d.ellipse([p(ex - r * 0.4), p(ey - r * 0.4), p(ex + r * 0.4), p(ey + r * 0.4)], fill=WHITE, outline=(170, 168, 160), width=1)
    d.ellipse([p(x - 4), p(y - 4), p(x + 4), p(y + 4)], fill=(214, 168, 64))

# ---------- credits ----------
by = 3150
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=NAVY2, width=2)
nf = font("BeVietnamPro-Medium.ttf", 36)
lf = font("BeVietnamPro-Light.ttf", 30)
lab = font("BeVietnamPro-Light.ttf", 20)
T.put("THỰC HIỆN", lab, M, by + 64, NAVY2, track=7)
T.put(NAMES[0], nf, M, by + 124, NAVY)
T.put(NAMES[1], nf, M, by + 180, NAVY)
T.put("ĐƠN VỊ", lab, W - M, by + 64, NAVY2, track=7, anchor="r")
T.put(CLASS, lf, W - M, by + 124, NAVY, anchor="r")
T.put(SCHOOL, lf, W - M, by + 180, NAVY, anchor="r")

seal(img, W - M - 70, 760, 120, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 28, 500))
save(img, "B-pho-co")
