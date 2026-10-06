"""Phương án C — Cửa Ô & mái ngói: khối son trầm phủ hoa văn ngói vảy cá, cổng vòm mở ra trang giấy."""
import math

from PIL import Image, ImageDraw

from common import (CA_DAO, CLASS, NAMES, SCHOOL, CH, CW, H, M, W, OUT_DIR,
                    Typesetter, font, p, paper, save, seal, seed)

seed(1749)
PAPER = (241, 236, 225)
BRICK = (128, 52, 40)
BRICK_L = (150, 72, 58)
CREAM = (238, 226, 205)
INK = (32, 30, 30)
INK2 = (108, 100, 92)
GOLD = (196, 158, 98)

img = paper(PAPER, grain=3.0, vignette=16, fibres=700, fibre_col=(214, 204, 186))
cx = W / 2
BLOCK = 2480
AW, A_TOP = 560, 560       # half-width of the arch, top of its curve

# ---- brick block with fish-scale tiles (ngói vảy cá) ----
blk = paper(BRICK, grain=4.0, vignette=0, fibres=0)
bd = ImageDraw.Draw(blk)
R = 46
row = 0
y = -R
while y < BLOCK + R:
    off = R if row % 2 else 0
    x = -2 * R + off
    while x < W + 2 * R:
        bd.arc([p(x - R), p(y - R), p(x + R), p(y + R)], 0, 180, fill=BRICK_L, width=3)
        bd.arc([p(x - R + 12), p(y - R + 12), p(x + R - 12), p(y + R - 12)], 20, 160, fill=(140, 62, 50), width=2)
        x += 2 * R
    y += R * 0.9
    row += 1

mask = Image.new("L", (CW, CH), 0)
md = ImageDraw.Draw(mask)
md.rectangle([0, 0, CW, p(BLOCK)], fill=255)
# the gateway: rectangle + semicircle cut out of the block
md.rectangle([p(cx - AW), p(A_TOP + AW), p(cx + AW), p(BLOCK)], fill=0)
md.ellipse([p(cx - AW), p(A_TOP), p(cx + AW), p(A_TOP + 2 * AW)], fill=0)
img.paste(blk, (0, 0), mask)
d = ImageDraw.Draw(img)

# voussoir ring around the arch (cream hairlines + brick joints)
for rr, w in ((AW + 26, 3), (AW + 70, 2)):
    d.arc([p(cx - rr), p(A_TOP + AW - rr), p(cx + rr), p(A_TOP + AW + rr)], 180, 360, fill=CREAM, width=w)
    d.line([(p(cx - rr), p(A_TOP + AW)), (p(cx - rr), p(BLOCK))], fill=CREAM, width=w)
    d.line([(p(cx + rr), p(A_TOP + AW)), (p(cx + rr), p(BLOCK))], fill=CREAM, width=w)
for k in range(25):
    a = math.pi + math.pi * k / 24
    r0, r1 = AW + 26, AW + 70
    d.line([(p(cx + math.cos(a) * r0), p(A_TOP + AW + math.sin(a) * r0)),
            (p(cx + math.cos(a) * r1), p(A_TOP + AW + math.sin(a) * r1))], fill=CREAM, width=2)
# gate-tower (vọng lâu) crowning the gate, in cream hairlines
tb = A_TOP - 160                       # base line of the tower = top of the plaque
d.line([(p(cx - 330), p(tb)), (p(cx + 330), p(tb))], fill=CREAM, width=3)
d.rectangle([p(cx - 200), p(tb - 74), p(cx + 200), p(tb)], outline=CREAM, width=3)
for k in range(-2, 3):                 # small arched openings
    x = cx + k * 76
    d.rectangle([p(x - 16), p(tb - 44), p(x + 16), p(tb - 12)], outline=CREAM, width=2)
    d.arc([p(x - 16), p(tb - 60), p(x + 16), p(tb - 28)], 180, 360, fill=CREAM, width=2)
# tiled roof: straight slopes, ridge, upturned eave tips (đầu đao)
ey, ry = tb - 80, tb - 128           # eave line, ridge line
roof = [(cx - 286, ey), (cx - 196, ry), (cx + 196, ry), (cx + 286, ey)]
d.polygon([(p(x), p(y)) for x, y in roof], fill=(140, 62, 50), outline=CREAM, width=3)
for k in range(1, 30):               # tile ribs
    t = k / 30
    d.line([(p(cx - 286 + 572 * t), p(ey - 2)), (p(cx - 196 + 392 * t), p(ry + 2))], fill=BRICK_L, width=2)
for sx in (-1, 1):
    tip = [(cx + sx * 286, ey), (cx + sx * 312, ey - 6), (cx + sx * 330, ey - 26), (cx + sx * 324, ey - 34)]
    d.line([(p(x), p(y)) for x, y in tip], fill=CREAM, width=3, joint="curve")
    d.line([(p(cx + sx * 196), p(ry)), (p(cx + sx * 214), p(ry - 18))], fill=CREAM, width=3)
d.line([(p(cx - 196), p(ry)), (p(cx + 196), p(ry))], fill=CREAM, width=4)
d.ellipse([p(cx - 9), p(ry - 22), p(cx + 9), p(ry - 4)], outline=CREAM, width=2)

# keystone plaque
pw, ph, py = 300, 74, A_TOP - 150
d.rectangle([p(cx - pw / 2), p(py), p(cx + pw / 2), p(py + ph)], fill=CREAM)
d.rectangle([p(cx - pw / 2 + 8), p(py + 8), p(cx + pw / 2 - 8), p(py + ph - 8)], outline=BRICK, width=2)
T = Typesetter(img)
T.put("TRÀNG AN", font("ArsenalSC-Regular.ttf", 38), cx, py + 50, BRICK, track=10, anchor="c")

small = font("BeVietnamPro-Light.ttf", 24)
T.put("CỬA Ô  ·  QUAN CHƯỞNG", small, M, 250, CREAM, track=8)
T.put("THĂNG LONG  —  HÀ NỘI", small, W - M, 250, CREAM, track=8, anchor="r")

# ---- inside the gate ----
gy = A_TOP + AW + 230
T.put("NÉT THANH LỊCH", font("BeVietnamPro-Light.ttf", 44), cx, gy + 10, INK2, track=22, anchor="c")
d.line([(p(cx - 60), p(gy + 60)), (p(cx + 60), p(gy + 60))], fill=GOLD, width=3)
big = font("PlayfairDisplay-Italic[wght].ttf", 210, 400)
T.put("người", big, cx, gy + 290, INK, anchor="c")
T.put("Tràng An", big, cx, gy + 520, BRICK, anchor="c")

# ---- through the gate: the old quarter's rooftops, faint ink ----
SKY = (122, 112, 104)
x = cx - AW
random_w = [150, 120, 170, 110, 160, 130, 140, 140]
random_h = [210, 300, 170, 260, 230, 190, 280, 200]
k = 0
while x < cx + AW - 4:
    w = min(random_w[k % 8], cx + AW - x)
    h = random_h[k % 8]
    top = BLOCK - h
    d.rectangle([p(x), p(top), p(x + w), p(BLOCK)], fill=(236, 228, 212), outline=SKY, width=2)
    if k % 3 != 1:                      # pitched tile roof
        d.polygon([(p(x - 6), p(top)), (p(x + 14), p(top - 46)), (p(x + w - 14), p(top - 46)), (p(x + w + 6), p(top))],
                  fill=(226, 206, 190), outline=SKY)
        for j in range(1, 4):
            yy = top - 46 * j / 4
            d.line([(p(x - 6 + 20 * j / 4), p(yy)), (p(x + w + 6 - 20 * j / 4), p(yy))], fill=SKY, width=1)
    else:                               # flat parapet with a small pediment
        d.line([(p(x - 6), p(top)), (p(x + w + 6), p(top))], fill=SKY, width=3)
        d.line([(p(x + w / 2 - 30), p(top)), (p(x + w / 2), p(top - 26)), (p(x + w / 2 + 30), p(top))], fill=SKY, width=2)
    # shuttered windows
    for fy in range(top + 34, BLOCK - 130, 86):
        for wx in (x + w * 0.28, x + w * 0.72):
            d.rectangle([p(wx - 13), p(fy), p(wx + 13), p(fy + 44)], outline=SKY, width=2)
            d.line([(p(wx), p(fy)), (p(wx), p(fy + 44))], fill=SKY, width=1)
    d.line([(p(x + 12), p(BLOCK - 62)), (p(x + w - 12), p(BLOCK - 62))], fill=SKY, width=2)
    x += w
    k += 1
d.line([(p(cx - AW), p(BLOCK - 1)), (p(cx + AW), p(BLOCK - 1))], fill=INK2, width=3)

# ---- below the block ----
cf = font("PlayfairDisplay-Italic[wght].ttf", 46, 400)
T.put(CA_DAO[0], cf, cx, BLOCK + 250, INK2, anchor="c")
T.put(CA_DAO[1], cf, cx, BLOCK + 318, INK2, anchor="c")
T.put("— CA DAO —", font("BeVietnamPro-Light.ttf", 20), cx, BLOCK + 388, INK2, track=8, anchor="c")

by = 3150
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK2, width=2)
nf = font("BeVietnamPro-Medium.ttf", 38)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(NAMES[0], nf, M, by + 100, INK)
T.put(NAMES[1], nf, M, by + 160, INK)
T.put(CLASS, lf, W - M, by + 100, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 160, INK, anchor="r")
d.line([(p(cx), p(by + 60)), (p(cx), p(by + 170))], fill=INK2, width=2)
seal(img, cx + 600, BLOCK + 282, 100, (164, 58, 44), ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 23, 500))

save(img, "C-cua-o", OUT_DIR.parent / "final")
