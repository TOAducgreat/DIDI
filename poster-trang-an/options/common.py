"""Shared canvas, paper and typography helpers for the poster options."""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"
OUT_DIR = Path(__file__).resolve().parent

S = 2
W, H = 2480, 3508
CW, CH = W * S, H * S
M = 170

TITLE = "Nét thanh lịch"
SUB = "người Tràng An"
CA_DAO = ("Chẳng thơm cũng thể hoa nhài,", "dẫu không thanh lịch cũng người Tràng An.")
NAMES = ("Đặng Vũ Hà Châu", "Nguyễn Thụy Anh")
CLASS = "Lớp 10 Chuyên Sử 1"
SCHOOL = "Trường THPT chuyên Hà Nội – Amsterdam"


def p(v):
    return v * S


def font(name, size, wght=None):
    f = ImageFont.truetype(str(FONT_DIR / name), int(size * S))
    if wght is not None:
        f.set_variation_by_axes([wght])
    return f


def seed(n):
    random.seed(n)
    np.random.seed(n)


def paper(color, grain=3.0, vignette=24, fibres=700, fibre_col=None, top=None):
    """Textured paper; optional vertical gradient from `top` to `color`."""
    if top is None:
        base = np.zeros((CH, CW, 3), np.float32) + np.array(color, np.float32)
    else:
        t = np.linspace(0, 1, CH, dtype=np.float32)[:, None, None]
        base = np.array(top, np.float32) * (1 - t) + np.array(color, np.float32) * t
        base = np.broadcast_to(base, (CH, CW, 3)).copy()
    g = np.random.normal(0, grain, (CH // 4, CW // 4)).astype(np.float32)
    g = np.array(Image.fromarray(g).resize((CW, CH), Image.BICUBIC))
    base += g[..., None]
    yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
    d = np.sqrt(((xx - CW / 2) / (CW / 2)) ** 2 + ((yy - CH / 2) / (CH / 2)) ** 2)
    base -= (np.clip(d - 0.55, 0, None) ** 2 * vignette)[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    if fibres and fibre_col:
        fib = Image.new("L", (CW, CH), 0)
        fd = ImageDraw.Draw(fib)
        for _ in range(fibres):
            x, y = random.uniform(0, CW), random.uniform(0, CH)
            a = random.uniform(0, math.pi)
            L = random.uniform(p(20), p(90))
            pts = [(x + math.cos(a) * L * i / 7 + math.sin(i) * p(3),
                    y + math.sin(a) * L * i / 7 + math.cos(i) * p(3)) for i in range(8)]
            fd.line(pts, fill=random.randint(10, 26), width=1)
        fib = fib.filter(ImageFilter.GaussianBlur(1.2))
        img = Image.composite(Image.new("RGB", (CW, CH), fibre_col), img, fib)
    return img


class Typesetter:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def width(self, t, f, track=0):
        if not track:
            return self.d.textlength(t, font=f)
        return sum(self.d.textlength(c, font=f) for c in t) + p(track) * (len(t) - 1)

    def put(self, t, f, x, y, fill, track=0, anchor="l"):
        """x, y in final px; y is the baseline."""
        x, y = p(x), p(y)
        w = self.width(t, f, track)
        if anchor == "c":
            x -= w / 2
        elif anchor == "r":
            x -= w
        if not track:
            self.d.text((x, y), t, font=f, fill=fill, anchor="ls")
            return w / S
        for c in t:
            self.d.text((x, y), c, font=f, fill=fill, anchor="ls")
            x += self.d.textlength(c, font=f) + p(track)
        return w / S

    def vertical(self, t, f, x, y_center, fill, track=0):
        w = int(self.width(t, f, track)) + p(20)
        h = int(f.size * 1.6)
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        xx = p(10)
        for c in t:
            ld.text((xx, h * 0.72), c, font=f, fill=tuple(fill) + (255,), anchor="ls")
            xx += ld.textlength(c, font=f) + p(track)
        layer = layer.rotate(90, expand=True, resample=Image.BICUBIC)
        self.img.paste(layer, (int(p(x) - layer.width / 2), int(p(y_center) - layer.height / 2)), layer)


def seal(img, cx, cy, size, color, lines, fnt, rot=-3):
    """Vermilion seal with paper-coloured characters (cut out)."""
    sz = p(size)
    m = Image.new("L", (sz, sz), 0)
    sd = ImageDraw.Draw(m)
    sd.rounded_rectangle([0, 0, sz - 1, sz - 1], radius=p(7), fill=255)
    n = len(lines)
    for i, t in enumerate(lines):
        sd.text((sz / 2, sz * (0.5 + (i - (n - 1) / 2) * 0.36)), t, font=fnt, fill=0, anchor="mm")
    inner = p(8)
    sd.rounded_rectangle([inner, inner, sz - inner, sz - inner], radius=p(4), outline=0, width=p(2))
    noise = (np.random.rand(sz, sz) > 0.07).astype(np.float32)
    m = Image.fromarray((np.array(m) * noise).astype(np.uint8))
    m = m.filter(ImageFilter.GaussianBlur(1.1)).rotate(rot, resample=Image.BICUBIC, expand=True)
    m = m.point(lambda v: int(v * 0.92))
    img.paste(Image.new("RGB", m.size, color), (int(p(cx) - m.width / 2), int(p(cy) - m.height / 2)), m)


def save(img, name):
    out = img.resize((W, H), Image.LANCZOS)
    path = OUT_DIR / f"{name}.png"
    out.save(path, dpi=(300, 300))
    out.save(path.with_suffix(".pdf"), resolution=300)
    print("saved", path)
    return out
