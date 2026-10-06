"""Lay a silk painting onto the poster paper as if painted on it.

The painting's own silk tone is normalised to white, then the result is
multiplied onto the canvas through a soft mask, so the background melts
into the poster paper and only the brushwork remains.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def load(name, crop=None):
    im = Image.open(ASSETS / name).convert("RGB")
    return im.crop(crop) if crop else im


def silk_tone(im, box):
    """Median colour of a patch of bare silk inside the painting."""
    a = np.asarray(im.crop(box), np.float32).reshape(-1, 3)
    return np.median(a, axis=0)


def lay(canvas, painting, x, y, mask, bg, strength=1.0):
    """Multiply `painting` (already sized in canvas px) onto canvas at (x, y).

    mask: L image same size as painting (255 = full paint)."""
    w, h = painting.size
    region = np.asarray(canvas.crop((x, y, x + w, y + h)), np.float32)
    f = np.clip(np.asarray(painting, np.float32) / np.asarray(bg, np.float32)[None, None, :], 0, 1)
    m = (np.asarray(mask, np.float32) / 255.0 * strength)[..., None]
    out = region * (1 - m + m * f)
    canvas.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), (x, y))


def soft_mask(size, inset=0.05, blur=0.07, roughness=0.5, fade_top=0.0, fade_bottom=0.0, fade_x=0.0, seed=7):
    """Frameless mask: a blurred rounded shape whose edge bleeds unevenly like
    watercolour on silk. fade_top / fade_bottom: extra vertical fade as a
    fraction of the height; fade_x: the same for both sides, as a fraction of the width."""
    from PIL import ImageDraw, ImageFilter
    w, h = size
    s = min(w, h)
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([int(s * inset), int(s * inset), int(w - s * inset), int(h - s * inset)],
                                        radius=int(s * 0.32), fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(s * blur)), np.float32) / 255
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (12, 9)).astype(np.float32)
    n = np.asarray(Image.fromarray(n).resize((w, h), Image.BICUBIC), np.float32)
    m = np.clip(m + roughness * n * m * (1 - m) * 4, 0, 1)      # only the edge band wobbles
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    if fade_top:
        m *= np.clip(y / fade_top, 0, 1) ** 1.5
    if fade_bottom:
        m *= np.clip((1 - y) / fade_bottom, 0, 1) ** 1.5
    if fade_x:
        x = np.linspace(0, 1, w, dtype=np.float32)[None, :]
        m *= (np.clip(x / fade_x, 0, 1) * np.clip((1 - x) / fade_x, 0, 1)) ** 1.2
    return Image.fromarray((m * 255).astype(np.uint8))
