"""Phương án F — Tiếng đàn bên sen: thiếu nữ áo dài gảy đàn tranh, đầm sen, nền lụa."""
import math

from PIL import ImageDraw

from brush import S, bud, gradient_fill, ink, leaf, lotus, silk, spline, stroke, wash
from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W,
                    Typesetter, font, p, save, seal, seed)

seed(1802)
SILK = (240, 233, 217)
INK = (40, 36, 34)
INK2 = (110, 102, 94)
PINK_L, PINK_D = (246, 226, 222), (214, 150, 150)
GREEN, GREEN_D = (178, 190, 160), (110, 128, 100)
SKIN = (240, 216, 196)
AO = (238, 236, 228)        # áo dài lụa trắng ngà
AO_SH = (208, 210, 206)
WOOD, WOOD_D = (150, 100, 66), (98, 62, 40)
SON = (164, 58, 44)

img = silk(SILK)
d = ImageDraw.Draw(img)

# halo — a pale full moon behind the player
wash(img, [], (232, 216, 206), alpha=0.55, blur=40, ellipses=[(380, 1340, 1500, 2460)])
wash(img, [], (246, 238, 226), alpha=0.6, blur=10, ellipses=[(470, 1430, 1410, 2370)])
d = ImageDraw.Draw(img)

# ---------------- lotus pond (behind) ----------------
stems = [((1870, 2520), (1880, 1520), 0.9), ((2150, 2520), (2160, 1280), 0.7), ((1700, 2520), (1690, 1190), 0.6),
         ((2290, 2520), (2270, 1760), 0.6), ((2000, 2520), (1990, 1900), 0.7)]
for (x0, y0), (x1, y1), w in stems:
    pts = spline([(x0, y0), (x0 + (x1 - x0) * 0.3 + 18, y0 + (y1 - y0) * 0.35), (x0 + (x1 - x0) * 0.7 - 14, y0 + (y1 - y0) * 0.7), (x1, y1)], closed=False, n=16)
    stroke(d, pts, GREEN_D, w0=5, w1=8)
leaf(img, d, 2280, 1520, 190, 52, INK, GREEN, GREEN_D, rot=-0.08, curl=0.6)
leaf(img, d, 2000, 1900, 230, 62, INK, GREEN, GREEN_D, rot=0.05, curl=0.4)
leaf(img, d, 1700, 2080, 280, 74, INK, GREEN, GREEN_D, rot=-0.04, curl=0.3)
leaf(img, d, 2210, 2230, 260, 70, INK, GREEN, GREEN_D, rot=0.03, curl=0.3)
lotus(img, d, 1880, 1520, 250, INK, PINK_L, PINK_D, open_=1.0)
lotus(img, d, 2270, 1760, 170, INK, PINK_L, PINK_D, open_=0.9, tilt=6)
bud(img, d, 2160, 1280, 190, INK, PINK_L, PINK_D, tilt=4)
bud(img, d, 1690, 1190, 150, INK, PINK_L, PINK_D, tilt=-6)
lotus(img, d, 1990, 1900, 150, INK, PINK_L, PINK_D, open_=0.8, tilt=-4)

# ---------------- low wooden platform (sập) ----------------
GROUND = 2510
d.rectangle([p(400), p(GROUND), p(2120), p(GROUND + 44)], fill=WOOD)
d.rectangle([p(400), p(GROUND + 44), p(2120), p(GROUND + 120)], fill=WOOD_D)
for k in range(9):
    x = 470 + k * 200
    d.rounded_rectangle([p(x), p(GROUND + 58), p(x + 140), p(GROUND + 106)], radius=p(10), outline=(140, 96, 64), width=2)
d.line(S([(400, GROUND), (2120, GROUND)]), fill=INK, width=3)
d.line(S([(400, GROUND + 44), (2120, GROUND + 44)]), fill=INK, width=2)
for x in (440, 2080):
    d.rectangle([p(x - 22), p(GROUND + 120), p(x + 22), p(GROUND + 200)], fill=WOOD_D)

# ---------------- the player ----------------
# back flap of the áo dài spreading on the platform
ta_sau = spline([(842, 2250), (806, 2380), (720, 2460), (600, 2496), (520, 2508), (700, 2510), (820, 2500), (860, 2420)], n=16)
gradient_fill(img, ta_sau, AO, AO_SH, 2250, 2510)
ink(d, ta_sau, INK, w=1.2, closed=True)
# folded legs / white trousers
legs = spline([(818, 2360), (900, 2338), (1010, 2370), (1086, 2410), (1094, 2474), (1050, 2506), (900, 2508), (790, 2500), (780, 2440)], n=16)
gradient_fill(img, legs, (250, 249, 245), (222, 222, 218), 2340, 2510)
ink(d, legs, INK, w=1.2, closed=True)
# bodice
body = spline([(866, 1972), (900, 1980), (930, 2050), (926, 2120), (904, 2190), (900, 2260), (918, 2330),
               (870, 2372), (818, 2368), (826, 2280), (838, 2170), (836, 2070), (846, 2000)], n=16)
gradient_fill(img, body, AO, AO_SH, 1970, 2380)
ink(d, body, INK, w=1.3, closed=True)
# front flap draping over the lap onto the platform
ta_truoc = spline([(900, 2250), (980, 2310), (1080, 2380), (1140, 2450), (1164, 2508), (1080, 2510), (1040, 2440), (960, 2370), (902, 2320)], n=16)
gradient_fill(img, ta_truoc, AO, AO_SH, 2250, 2510)
ink(d, ta_truoc, INK, w=1.2, closed=True)
for k in range(3):  # silk folds
    ink(d, spline([(930 + k * 40, 2320 + k * 18), (1010 + k * 34, 2390 + k * 14), (1060 + k * 30, 2490)], closed=False, n=10), AO_SH, w=1.0)
# neck + collar
neck = [(872, 1930), (896, 1932), (900, 1982), (868, 1980)]
d.polygon(S(neck), fill=SKIN)
d.polygon(S([(864, 1964), (902, 1966), (906, 1994), (862, 1992)]), fill=AO, outline=INK, width=2)
# head (profile, gently bowed, facing right)
face = spline([(864, 1856), (904, 1838), (930, 1852), (944, 1882), (958, 1906), (948, 1914), (950, 1928),
               (944, 1940), (940, 1956), (918, 1966), (894, 1958), (870, 1932), (856, 1896)], n=14)
d.polygon(S(face), fill=SKIN)
ink(d, face[len(face) // 6: len(face) * 3 // 4], INK, w=1.1)
# hair: smooth cap + low bun + a long lock down the back
hair = spline([(850, 1900), (848, 1856), (874, 1828), (912, 1822), (942, 1840), (938, 1858), (910, 1852), (884, 1866), (872, 1900), (868, 1934)], n=14)
d.polygon(S(hair), fill=(30, 28, 30))
d.ellipse(S([(800, 1864), (862, 1922)]), fill=(30, 28, 30))
stroke(d, spline([(840, 1910), (826, 1990), (824, 2080), (832, 2150)], closed=False, n=12), (30, 28, 30), w0=12, w1=20)
d.ellipse(S([(926, 1884), (934, 1888)]), fill=INK)     # closed eye
ink(d, [(914, 1878), (934, 1876)], INK, w=0.9)        # brow

# ---------------- đàn tranh ----------------
top = [(1010, 2296), (1980, 2382), (2010, 2410), (1030, 2342)]
side = [(1030, 2342), (2010, 2410), (2010, 2436), (1034, 2370)]
gradient_fill(img, top, (186, 134, 92), (140, 94, 60), 2290, 2410)
d.polygon(S(side), fill=WOOD_D)
ink(d, top + [top[0]], INK, w=1.2)
ink(d, [side[2], side[3], side[0]], INK, w=1.2)
# strings + bridges (nhạn đàn) in a diagonal
for k in range(16):
    t = (k + 0.5) / 16
    a = (1010 + 20 * t, 2296 + 46 * t)
    b = (1980 + 30 * t, 2382 + 28 * t)
    d.line(S([a, b]), fill=(236, 226, 206), width=1)
    bt = 0.38 + 0.36 * t
    bx, by = a[0] + (b[0] - a[0]) * bt, a[1] + (b[1] - a[1]) * bt
    d.polygon(S([(bx - 7, by + 3), (bx + 7, by + 3), (bx, by - 9)]), fill=(232, 222, 200), outline=INK, width=1)
for x in (1100, 1900):  # small feet
    d.rectangle([p(x - 12), p(2370 + (x - 1030) * 0.07), p(x + 12), p(GROUND)], fill=WOOD_D)

# ---------------- arms (over the instrument) ----------------
arm = spline([(880, 2000), (902, 2080), (930, 2170), (1010, 2246), (1090, 2290), (1102, 2312), (1080, 2316),
              (996, 2280), (906, 2200), (868, 2100), (858, 2020)], n=14)
gradient_fill(img, arm, AO, AO_SH, 2000, 2320)
ink(d, arm, INK, w=1.2, closed=True)
hand = spline([(1090, 2288), (1124, 2296), (1146, 2310), (1134, 2318), (1104, 2316)], n=10)
d.polygon(S(hand), fill=SKIN)
ink(d, hand, INK, w=0.9, closed=True)
arm2 = spline([(1000, 2262), (1080, 2300), (1180, 2318), (1210, 2330), (1186, 2338), (1074, 2318), (996, 2284)], n=12)
gradient_fill(img, arm2, AO, AO_SH, 2260, 2340)
ink(d, arm2, INK, w=1.0, closed=True)
d.polygon(S(spline([(1200, 2324), (1238, 2330), (1252, 2342), (1220, 2344)], n=8)), fill=SKIN)

# ---------------- typography ----------------
T = Typesetter(img)
small = font("BeVietnamPro-Light.ttf", 24)
T.put("TIẾNG ĐÀN BÊN SEN", small, M, 250, INK2, track=8)
T.put("THĂNG LONG  ·  HÀ NỘI", small, W - M, 250, INK2, track=8, anchor="r")
d.line([(p(M), p(286)), (p(W - M), p(286))], fill=(196, 186, 170), width=2)
T.put(TITLE, font("PlayfairDisplay[wght].ttf", 210, 400), M - 6, 600, INK)
T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 150, 400), M + 4, 790, SON)
cf = font("PlayfairDisplay-Italic[wght].ttf", 40, 400)
T.put(CA_DAO[0], cf, M, 940, INK2)
T.put(CA_DAO[1], cf, M, 998, INK2)

by = 3170
d = ImageDraw.Draw(img)
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=(196, 186, 170), width=2)
nf = font("BeVietnamPro-Medium.ttf", 36)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(NAMES[0], nf, M, by + 100, INK)
T.put(NAMES[1], nf, M, by + 156, INK)
T.put(CLASS, lf, W - M, by + 100, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 156, INK, anchor="r")
seal(img, M + 1180, 760, 110, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 28, 500))
save(img, "F-dan-tranh-ben-sen")
