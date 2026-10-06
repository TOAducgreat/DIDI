"""Phương án C — Cửa Ô & mái ngói: khối son trầm phủ hoa văn ngói vảy cá, cổng vòm mở ra trang giấy."""
import math

from PIL import Image, ImageDraw

from common import (CA_DAO, CLASS, NAMES, SCHOOL, CH, CW, H, M, W,
                    Typesetter, font, p, paper, save, seed)

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

# ---- below the block ----
cf = font("PlayfairDisplay-Italic[wght].ttf", 46, 400)
T.put(CA_DAO[0], cf, cx, BLOCK + 190, INK2, anchor="c")
T.put(CA_DAO[1], cf, cx, BLOCK + 256, INK2, anchor="c")
T.put("— CA DAO —", font("BeVietnamPro-Light.ttf", 20), cx, BLOCK + 320, INK2, track=8, anchor="c")

by = 3150
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK2, width=2)
nf = font("BeVietnamPro-Medium.ttf", 38)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(NAMES[0], nf, M, by + 100, INK)
T.put(NAMES[1], nf, M, by + 160, INK)
T.put(CLASS, lf, W - M, by + 100, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 160, INK, anchor="r")
d.line([(p(cx), p(by + 60)), (p(cx), p(by + 170))], fill=INK2, width=2)

save(img, "C-cua-o")
