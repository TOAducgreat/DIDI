"""Bản C — Phố cổ: thiếu nữ áo dài bên xe hoa, không khung, nền ngà → hồng sen. Chữ trên, tranh dưới."""
from PIL import Image, ImageDraw

from brush import wash
from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W, OUT_DIR,
                    Typesetter, font, p, paper, save, seal, seed)
from paint import lay, load, silk_tone, soft_mask

seed(1749)
IVORY, LOTUS_BG = (244, 238, 228), (241, 222, 218)
INK = (32, 30, 30)
INK2 = (104, 96, 90)
INK3 = (164, 152, 144)
SON = (160, 56, 42)

img = paper(LOTUS_BG, top=IVORY, grain=3.0, vignette=14, fibres=700, fibre_col=(214, 202, 190))
cx = W / 2

# warm breath of light where the painting sits
wash(img, [], (250, 244, 234), alpha=0.7, blur=90, ellipses=[(cx - 820, 1150, cx + 820, 2950)])

# ---------- header ----------
T = Typesetter(img)
d = ImageDraw.Draw(img)
small = font("BeVietnamPro-Light.ttf", 24)
T.put("PHỐ CỔ  ·  HÀ NỘI", small, M, 250, INK2, track=8)
T.put("THĂNG LONG  —  NGHÌN NĂM VĂN HIẾN", small, W - M, 250, INK2, track=8, anchor="r")
d.line([(p(M), p(286)), (p(W - M), p(286))], fill=INK3, width=2)

# ---------- title (top) ----------
T.put(TITLE, font("PlayfairDisplay[wght].ttf", 200, 400), cx, 560, INK, track=1, anchor="c")
sw = T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 150, 400), cx, 745, SON, anchor="c")
seal(img, cx + sw / 2 + 88, 700, 104, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 26, 500))
d = ImageDraw.Draw(img)
oy = 830
d.line([(p(cx - 200), p(oy)), (p(cx - 24), p(oy))], fill=INK3, width=2)
d.line([(p(cx + 24), p(oy)), (p(cx + 200), p(oy))], fill=INK3, width=2)
d.ellipse([p(cx - 6), p(oy - 6), p(cx + 6), p(oy + 6)], fill=SON)
cf = font("PlayfairDisplay-Italic[wght].ttf", 40, 400)
T.put(CA_DAO[0], cf, cx, oy + 86, INK2, anchor="c")
T.put(CA_DAO[1], cf, cx, oy + 142, INK2, anchor="c")

# ---------- the painting, frameless (bottom) ----------
src = load("xe-hoa.png")
bg = silk_tone(src, (200, 100, 900, 500))
crop = src.crop((84, 702, 1034, 1948))
aw = 1480
ah = int(crop.height * aw / crop.width)
art = crop.resize((p(aw), p(ah)), Image.LANCZOS)
ay = 1050
mask = soft_mask(art.size, inset=0.04, blur=0.09, roughness=0.7, fade_top=0.18, fade_bottom=0.12, fade_x=0.12, seed=11)
lay(img, art, int(p(cx - aw / 2)), int(p(ay)), mask, bg)
d = ImageDraw.Draw(img)

# ---------- credits ----------
by = 3150
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK3, width=2)
nf = font("BeVietnamPro-Medium.ttf", 38)
lf = font("BeVietnamPro-Light.ttf", 30)
T.put(NAMES[0], nf, M, by + 100, INK)
T.put(NAMES[1], nf, M, by + 160, INK)
T.put(CLASS, lf, W - M, by + 100, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 160, INK, anchor="r")
d.line([(p(cx), p(by + 60)), (p(cx), p(by + 170))], fill=INK3, width=2)

save(img, "C-cua-o", OUT_DIR.parent / "final")
