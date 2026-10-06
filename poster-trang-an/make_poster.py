"""Bản 0 — Mặc Nguyệt: tranh lụa đàn tranh bên sen, không khung, nền ngà → hồng sen."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent / "options"))
from brush import wash  # noqa: E402
from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W, OUT_DIR,  # noqa: E402
                    Typesetter, font, p, paper, save, seal, seed)
from paint import lay, load, silk_tone, soft_mask  # noqa: E402

seed(1010)
IVORY, LOTUS_BG = (244, 238, 228), (241, 222, 218)
INK = (28, 26, 24)
INK2 = (96, 88, 82)
INK3 = (160, 148, 140)
SON = (168, 46, 34)

img = paper(LOTUS_BG, top=IVORY, grain=3.0, vignette=14, fibres=700, fibre_col=(214, 202, 190))
cx = W / 2

# a full moon with no outline — only a lighter breath of silk behind the player
wash(img, [], (250, 245, 238), alpha=0.85, blur=70, ellipses=[(cx - 660, 560, cx + 660, 1880)])

# ---------- the painting, frameless ----------
src = load("dan-tranh.png")
bg = silk_tone(src, (100, 100, 600, 500))
crop = src.crop((0, 560, 1116, 2000))
aw = 1640
ah = int(crop.height * aw / crop.width)
art = crop.resize((p(aw), p(ah)), Image.LANCZOS)
ax, ay = cx - aw / 2, 250
mask = soft_mask(art.size, inset=0.05, blur=0.09, roughness=0.7, fade_top=0.12, fade_bottom=0.2, fade_x=0.1, seed=3)
lay(img, art, int(p(ax)), int(p(ay)), mask, bg)

# ---------- header + margins ----------
T = Typesetter(img)
d = ImageDraw.Draw(img)
hf = font("Jura-Light.ttf", 30)
T.put("Nº 01", hf, M, 240, INK2, track=6)
T.put("TRÀNG AN  ·  1010", hf, cx, 240, INK2, track=6, anchor="c")
T.put("21°01'N  105°51'E", hf, W - M, 240, INK2, track=4, anchor="r")
d.line([(p(M), p(282)), (p(W - M), p(282))], fill=INK3, width=2)
vf = font("Jura-Light.ttf", 26)
T.vertical("THĂNG LONG  ·  ĐÔNG ĐÔ  ·  HÀ NỘI", vf, M + 6, 1300, INK2, track=9)
T.vertical("TIẾNG ĐÀN  ·  HOA SEN  ·  VẦNG NGUYỆT", vf, W - M - 6, 1300, INK2, track=9)
d = ImageDraw.Draw(img)

# ---------- title ----------
ty = 2500
T.put(TITLE, font("PlayfairDisplay[wght].ttf", 214, 400), cx, ty, INK, track=1, anchor="c")
sw = T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 150, 400), cx, ty + 196, SON, anchor="c")
seal(img, cx + sw / 2 + 90, ty + 150, 108, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 27, 500))
d = ImageDraw.Draw(img)

oy = ty + 290
d.line([(p(cx - 230), p(oy)), (p(cx - 26), p(oy))], fill=INK3, width=2)
d.line([(p(cx + 26), p(oy)), (p(cx + 230), p(oy))], fill=INK3, width=2)
d.ellipse([p(cx - 7), p(oy - 7), p(cx + 7), p(oy + 7)], fill=SON)
cf = font("PlayfairDisplay-Italic[wght].ttf", 42, 400)
T.put(CA_DAO[0], cf, cx, oy + 96, INK2, anchor="c")
T.put(CA_DAO[1], cf, cx, oy + 154, INK2, anchor="c")
T.put("— CA DAO —", font("Jura-Light.ttf", 22), cx, oy + 212, INK3, track=8, anchor="c")

# ---------- credits ----------
by = 3200
d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK3, width=2)
lab = font("Jura-Light.ttf", 20)
T.put("THỰC HIỆN", lab, M, by + 70, INK2, track=7)
T.put("ĐƠN VỊ", lab, W - M, by + 70, INK2, track=7, anchor="r")
nf = font("BeVietnamPro-Medium.ttf", 36)
lf = font("BeVietnamPro-Light.ttf", 31)
T.put(NAMES[0], nf, M, by + 132, INK)
T.put(NAMES[1], nf, M, by + 188, INK)
T.put(CLASS, lf, W - M, by + 132, INK, anchor="r")
T.put(SCHOOL, lf, W - M, by + 188, INK, anchor="r")

save(img, "0-mac-nguyet", OUT_DIR.parent / "final")
