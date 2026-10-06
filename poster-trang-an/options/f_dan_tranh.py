"""Phương án F — Tiếng đàn bên sen: thiếu nữ áo dài gảy đàn tranh, đầm sen, nền lụa."""
import math

from PIL import Image, ImageDraw

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

base = silk(SILK)
img = Image.new("RGBA", base.size, SILK + (0,))   # scene layer, scaled into place later
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
d.rectangle([p(470), p(GROUND), p(2060), p(GROUND + 44)], fill=WOOD)
d.rectangle([p(470), p(GROUND + 44), p(2060), p(GROUND + 110)], fill=WOOD_D)
for k in range(8):
    x = 505 + k * 194
    d.rounded_rectangle([p(x), p(GROUND + 56), p(x + 150), p(GROUND + 98)], radius=p(10), outline=(140, 96, 64), width=2)
d.line(S([(470, GROUND), (2060, GROUND)]), fill=INK, width=3)
d.line(S([(470, GROUND + 44), (2060, GROUND + 44)]), fill=INK, width=2)
for x in (510, 2020):
    d.rectangle([p(x - 22), p(GROUND + 110), p(x + 22), p(GROUND + 170)], fill=WOOD_D)

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
face = spline([(880, 1846), (920, 1836), (942, 1852), (950, 1874), (952, 1890), (963, 1906), (952, 1912),
               (955, 1921), (949, 1926), (952, 1933), (944, 1948), (924, 1962), (898, 1960), (874, 1934), (862, 1890)], n=12)
d.polygon(S(face), fill=SKIN)
ink(d, face[24:132], INK, w=1.0)
wash(img, [], (232, 180, 168), alpha=0.35, blur=6, ellipses=[(906, 1910, 936, 1930)])
# hair: smooth crown swept back into a low bun (búi tóc)
hair = spline([(856, 1930), (846, 1880), (856, 1842), (886, 1820), (922, 1818), (946, 1834), (950, 1852),
               (930, 1850), (904, 1852), (884, 1870), (876, 1904), (874, 1936)], n=14)
d.polygon(S(hair), fill=(30, 28, 30))
d.ellipse(S([(808, 1876), (868, 1932)]), fill=(30, 28, 30))
ink(d, [(812, 1900), (864, 1906)], (70, 66, 66), w=1.0)
d.line(S([(806, 1886), (832, 1870)]), fill=(196, 160, 90), width=4)   # hairpin
# lowered eyelid + brow
ink(d, spline([(922, 1886), (930, 1890), (938, 1888)], closed=False, n=6), INK, w=1.1)
ink(d, [(916, 1874), (938, 1870)], INK, w=0.8)
d.ellipse(S([(948, 1922), (952, 1925)]), fill=(186, 96, 90))

# ---------------- đàn tranh ----------------
top = [(960, 2306), (1930, 2388), (1960, 2416), (980, 2352)]
side = [(980, 2352), (1960, 2416), (1960, 2442), (984, 2380)]
gradient_fill(img, top, (186, 134, 92), (140, 94, 60), 2290, 2410)
d.polygon(S(side), fill=WOOD_D)
ink(d, top + [top[0]], INK, w=1.2)
ink(d, [side[2], side[3], side[0]], INK, w=1.2)
# strings + bridges (nhạn đàn) in a diagonal
for k in range(16):
    t = (k + 0.5) / 16
    a = (960 + 20 * t, 2306 + 46 * t)
    b = (1930 + 30 * t, 2388 + 28 * t)
    d.line(S([a, b]), fill=(236, 226, 206), width=1)
    bt = 0.38 + 0.36 * t
    bx, by = a[0] + (b[0] - a[0]) * bt, a[1] + (b[1] - a[1]) * bt
    d.polygon(S([(bx - 7, by + 3), (bx + 7, by + 3), (bx, by - 9)]), fill=(232, 222, 200), outline=INK, width=1)
for x in (1300, 1880):  # small feet
    d.rectangle([p(x - 12), p(2374 + (x - 980) * 0.065), p(x + 12), p(GROUND)], fill=WOOD_D)

# ---------------- arms (over the instrument) ----------------
arm2 = spline([(940, 2236), (1010, 2290), (1096, 2318), (1100, 2336), (1060, 2334), (990, 2306), (930, 2262)], n=12)
gradient_fill(img, arm2, AO_SH, (190, 192, 188), 2230, 2340)
ink(d, arm2, INK, w=1.0, closed=True)
d.polygon(S(spline([(1096, 2318), (1130, 2326), (1146, 2340), (1110, 2340)], n=8)), fill=SKIN)
arm = spline([(860, 2010), (888, 2008), (904, 2080), (914, 2160), (940, 2214), (1000, 2262), (1040, 2290),
              (1030, 2306), (982, 2286), (912, 2236), (878, 2176), (862, 2090)], n=14)
gradient_fill(img, arm, AO, AO_SH, 2000, 2310)
ink(d, arm, INK, w=1.2, closed=True)
hand = spline([(1036, 2288), (1066, 2296), (1088, 2310), (1076, 2318), (1040, 2312)], n=10)
d.polygon(S(hand), fill=SKIN)
ink(d, hand, INK, w=0.9, closed=True)

# ---------------- place the scene: scale up, anchor the platform low ----------------
K, AX, AY, BX, BY = 1.3, 1265, 2510, 1240, 2800
img = img.resize((int(img.width * K), int(img.height * K)), Image.LANCZOS)
ox, oy = int(p(BX) - p(AX) * K), int(p(BY) - p(AY) * K)
base.paste(img, (ox, oy), img)
img = base
d = ImageDraw.Draw(img)

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
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=(196, 186, 170), width=2)
nf = font("BeVietnamPro-Medium.ttf", 36)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(NAMES[0], nf, M, by + 100, INK)
T.put(NAMES[1], nf, M, by + 156, INK)
T.put(CLASS, lf, W - M, by + 100, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 156, INK, anchor="r")
seal(img, M + 1180, 760, 110, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 28, 500))
save(img, "F-dan-tranh-ben-sen")
