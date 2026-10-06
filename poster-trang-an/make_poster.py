"""Poster: Nét thanh lịch người Tràng An — phong cách "Mặc Nguyệt"."""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = Path(sys.argv[1])
OUT = Path(__file__).with_name("poster-net-thanh-lich-trang-an.png")

S = 2                      # supersampling
W, H = 2480, 3508          # A-series ratio, final pixels
CW, CH = W * S, H * S
random.seed(1010)
np.random.seed(1010)

PAPER = (238, 232, 218)
INK = (28, 26, 24)
INK2 = (88, 84, 78)
INK3 = (150, 144, 134)
MIST = (196, 189, 175)
SON = (168, 46, 34)        # lacquer vermilion


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), int(size * S))


def p(v):
    return v * S


# ---------- paper ----------
base = np.zeros((CH, CW, 3), np.float32) + np.array(PAPER, np.float32)
grain = np.random.normal(0, 3.2, (CH // 4, CW // 4)).astype(np.float32)
grain = np.array(Image.fromarray(grain).resize((CW, CH), Image.BICUBIC))
base += grain[..., None]
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
d = np.sqrt(((xx - CW / 2) / (CW / 2)) ** 2 + ((yy - CH / 2) / (CH / 2)) ** 2)
base -= (np.clip(d - 0.55, 0, None) ** 2 * 26)[..., None]
img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")

# fibres of giấy dó
fib = Image.new("L", (CW, CH), 0)
fd = ImageDraw.Draw(fib)
for _ in range(900):
    x, y = random.uniform(0, CW), random.uniform(0, CH)
    a = random.uniform(0, math.pi)
    L = random.uniform(p(20), p(90))
    pts = []
    for i in range(8):
        t = i / 7
        pts.append((x + math.cos(a) * L * t + math.sin(t * 5) * p(3),
                    y + math.sin(a) * L * t + math.cos(t * 4) * p(3)))
    fd.line(pts, fill=random.randint(10, 26), width=1)
fib = fib.filter(ImageFilter.GaussianBlur(1.2))
img = Image.composite(Image.new("RGB", (CW, CH), (205, 196, 178)), img, fib)

draw = ImageDraw.Draw(img)


def text_w(t, f, track=0):
    if not track:
        return draw.textlength(t, font=f)
    return sum(draw.textlength(c, font=f) for c in t) + track * S * (len(t) - 1)


def put(t, f, x, y, fill, track=0, anchor="l"):
    w = text_w(t, f, track)
    if anchor == "c":
        x -= w / 2
    elif anchor == "r":
        x -= w
    if not track:
        draw.text((x, y), t, font=f, fill=fill, anchor="ls")
        return
    for c in t:
        draw.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += draw.textlength(c, font=f) + track * S


M = 170                                   # margin
F_SANS = "Jura-Light.ttf"
F_SC = "ArsenalSC-Regular.ttf"
F_SERIF = "CrimsonPro-Regular.ttf"
F_ITAL = "CrimsonPro-Italic.ttf"

# ---------- header ----------
put("Nº 01", font(F_SANS, 30), p(M), p(240), INK2, track=6)
put("TRÀNG AN  ·  1010", font(F_SANS, 30), p(W / 2), p(240), INK2, track=6, anchor="c")
put("21°01'N  105°51'E", font(F_SANS, 30), p(W - M), p(240), INK2, track=4, anchor="r")
draw.line([(p(M), p(282)), (p(W - M), p(282))], fill=INK3, width=p(1))

# ---------- the window / moon ----------
cx, cy = W / 2, 1330
R_OUT, R_IN = 740, 372

# faint moon wash behind
wash = Image.new("L", (CW, CH), 0)
ImageDraw.Draw(wash).ellipse([p(cx - R_IN + 6), p(cy - R_IN + 6),
                              p(cx + R_IN - 6), p(cy + R_IN - 6)], fill=70)
wash = wash.filter(ImageFilter.GaussianBlur(p(26)))
img = Image.composite(Image.new("RGB", (CW, CH), (224, 216, 199)), img, wash)
draw = ImageDraw.Draw(img)

# radiating hairlines — the Khuê Văn Các sun window
N = 360
for i in range(N):
    a = 2 * math.pi * i / N - math.pi / 2
    if i % 30 == 0:
        r0, r1, col, w = R_IN - 14, R_OUT + 34, INK, 2
    elif i % 10 == 0:
        r0, r1, col, w = R_IN, R_OUT + 14, INK, 2
    elif i % 5 == 0:
        r0, r1, col, w = R_IN + 22, R_OUT, INK2, 1
    else:
        r0, r1, col, w = R_IN + 48, R_OUT - 26, INK3, 1
    ca, sa = math.cos(a), math.sin(a)
    draw.line([(p(cx + ca * r0), p(cy + sa * r0)),
               (p(cx + ca * r1), p(cy + sa * r1))], fill=col, width=w * S // 1)


def ring(r, col, w=1):
    draw.ellipse([p(cx - r), p(cy - r), p(cx + r), p(cy + r)], outline=col, width=w * S)


ring(R_OUT + 62, INK3)
ring(R_OUT + 74, MIST)
ring(R_IN - 30, INK2)
ring(R_IN - 40, MIST)

# dotted inner ring
for i in range(144):
    a = 2 * math.pi * i / 144
    r = R_IN - 64
    x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
    draw.ellipse([p(x - 2.2), p(y - 2.2), p(x + 2.2), p(y + 2.2)], fill=INK2)

# hour-like numerals around the outer ring (thin, archival)
numf = font(F_SANS, 20)
for k in range(12):
    a = 2 * math.pi * k / 12 - math.pi / 2
    r = R_OUT + 112
    label = f"{k * 30:03d}"
    x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
    draw.text((p(x), p(y)), label, font=numf, fill=INK3, anchor="mm")


# ---------- lotus (sen Hồ Tây), hairline ----------
def lens(base_xy, length, width, angle, col, w=1, steps=60):
    bx, by = base_xy
    ca, sa = math.cos(angle), math.sin(angle)
    left, right = [], []
    for j in range(steps + 1):
        t = j / steps
        along = length * t
        half = width * math.sin(math.pi * t) ** 0.85 * (1 - 0.25 * t)
        for side, arr in ((1, left), (-1, right)):
            lx, ly = along, side * half
            arr.append((p(bx + lx * ca - ly * sa), p(by + lx * sa + ly * ca)))
    draw.line(left + right[::-1], fill=col, width=w * S, joint="curve")


lb = (cx, cy + 172)
petals = [(-90, 300, 64), (-64, 262, 58), (-116, 262, 58),
          (-40, 210, 52), (-140, 210, 52), (-18, 150, 42), (-162, 150, 42)]
for deg, L, Wd in petals:
    for k, (sc, col) in enumerate(((1.0, INK), (0.82, INK2), (0.64, INK3))):
        lens(lb, L * sc, Wd * sc, math.radians(deg), col)

# a single seed-line beneath — water
for k in range(5):
    y = cy + 196 + k * 13
    half = 200 - k * 36
    col = (INK2, INK3, INK3, MIST, MIST)[k]
    draw.line([(p(cx - half), p(y)), (p(cx + half), p(y))], fill=col, width=S)

# ---------- vertical marginal text ----------
def vertical(t, f, x, y_center, fill, track):
    w = int(text_w(t, f, track)) + p(20)
    h = p(60)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    xx = p(10)
    for c in t:
        ld.text((xx, h * 0.72), c, font=f, fill=fill + (255,), anchor="ls")
        xx += ld.textlength(c, font=f) + track * S
    layer = layer.rotate(90, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(p(x) - layer.width / 2), int(p(y_center) - layer.height / 2)), layer)


vertical("THĂNG LONG  ·  ĐÔNG ĐÔ  ·  HÀ NỘI", font(F_SANS, 26), M + 6, cy, INK2, 9)
vertical("HÌNH THỨC  —  KHUÊ VĂN  ·  SEN  ·  NGUYỆT", font(F_SANS, 26), W - M - 6, cy, INK2, 9)
draw = ImageDraw.Draw(img)

# ---------- seal (dấu son) ----------
sx, sy, ss = cx + 700, cy + 730, 124
seal = Image.new("L", (p(ss), p(ss)), 0)
sd = ImageDraw.Draw(seal)
sd.rounded_rectangle([0, 0, p(ss) - 1, p(ss) - 1], radius=p(8), fill=255)
sf = font(F_SERIF, 44)
sd.text((p(ss / 2), p(ss * 0.43)), "Tràng", font=sf, fill=0, anchor="ms")
sd.text((p(ss / 2), p(ss * 0.80)), "An", font=sf, fill=0, anchor="ms")
inner = p(9)
sd.rounded_rectangle([inner, inner, p(ss) - inner, p(ss) - inner], radius=p(5), outline=0, width=p(2))
# worn ink texture
noise = (np.random.rand(p(ss), p(ss)) > 0.06).astype(np.uint8) * 255
seal = Image.fromarray((np.array(seal) * (noise / 255)).astype(np.uint8))
seal = seal.filter(ImageFilter.GaussianBlur(1.1)).rotate(-3, resample=Image.BICUBIC, expand=True)
seal = seal.point(lambda v: int(v * 0.92))
img.paste(Image.new("RGB", seal.size, SON), (int(p(sx - ss / 2)), int(p(sy - ss / 2))), seal)
draw = ImageDraw.Draw(img)

# ---------- title ----------
ty = 2470
put("Nét thanh lịch", font(F_SERIF, 238), p(cx), p(ty), INK, track=2, anchor="c")
put("người Tràng An", font(F_ITAL, 158), p(cx), p(ty + 200), INK, track=1, anchor="c")

# small ornament: rule — dot — rule
oy = ty + 300
draw.line([(p(cx - 230), p(oy)), (p(cx - 26), p(oy))], fill=INK3, width=S)
draw.line([(p(cx + 26), p(oy)), (p(cx + 230), p(oy))], fill=INK3, width=S)
draw.ellipse([p(cx - 7), p(oy - 7), p(cx + 7), p(oy + 7)], fill=SON)

cf = font(F_ITAL, 46)
put("Chẳng thơm cũng thể hoa nhài,", cf, p(cx), p(oy + 100), INK2, anchor="c")
put("dẫu không thanh lịch cũng người Tràng An.", cf, p(cx), p(oy + 162), INK2, anchor="c")
put("— CA DAO —", font(F_SANS, 22), p(cx), p(oy + 224), INK3, track=8, anchor="c")

# ---------- credits ----------
by = 3200
draw.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK3, width=S)
draw.line([(p(M), p(by + 8)), (p(W - M), p(by + 8))], fill=MIST, width=S)

lab = font(F_SANS, 20)
put("THỰC HIỆN", lab, p(M), p(by + 70), INK2, track=7)
put("ĐƠN VỊ", lab, p(W - M), p(by + 70), INK2, track=7, anchor="r")

nf = font(F_SC, 40)
put("Đặng Vũ Hà Châu", nf, p(M), p(by + 132), INK, track=3)
put("Nguyễn Thụy Anh", nf, p(M), p(by + 188), INK, track=3)

sf2 = font(F_SC, 34)
put("Lớp 10 Chuyên Sử 1", sf2, p(W - M), p(by + 132), INK, track=3, anchor="r")
put("Trường THPT chuyên Hà Nội – Amsterdam", sf2, p(W - M), p(by + 188), INK, track=2, anchor="r")

# ---------- finish ----------
out = img.resize((W, H), Image.LANCZOS)
out.save(OUT, dpi=(300, 300))
out.convert("RGB").save(OUT.with_suffix(".pdf"), resolution=300)
print("saved", OUT)
