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
