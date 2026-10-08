"""Small SVG toolkit: smooth paths, gradients, paper texture, Chromium rendering."""
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "final"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 2480, 3508


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def smooth(pts, closed=True, tension=1.0):
    """Catmull-Rom through points -> cubic Bézier path data."""
    n = len(pts)
    if n < 2:
        return ""
    d = [f"M{f(pts[0][0])},{f(pts[0][1])}"]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d.append(f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}")
    if closed:
        d.append("Z")
    return " ".join(d)


def poly(pts, closed=True):
    s = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    return s + (" Z" if closed else "")


class Doc:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.defs, self.body = [], []
        self._id = 0

    def uid(self, p="g"):
        self._id += 1
        return f"{p}{self._id}"

    def add(self, s):
        self.body.append(s)

    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, units="objectBoundingBox"):
        i = self.uid("lg")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="{units}">{st}</linearGradient>')
        return f"url(#{i})"

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, units="objectBoundingBox"):
        i = self.uid("rg")
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        fxy = f' fx="{fx}" fy="{fy}"' if fx is not None else ""
        self.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{fxy} gradientUnits="{units}">{st}</radialGradient>')
        return f"url(#{i})"

    def blur(self, sd):
        i = self.uid("bl")
        self.defs.append(f'<filter id="{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
        return f"url(#{i})"

    def clip(self, d):
        i = self.uid("cp")
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return f"url(#{i})"

    def mask(self, inner):
        i = self.uid("mk")
        self.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.w}" height="{self.h}">{inner}</mask>')
        return f"url(#{i})"

    def path(self, d, fill="none", stroke=None, sw=1, op=1, extra=""):
        s = f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
        self.add(f'<path d="{d}" fill="{fill}"{s} opacity="{op}" {extra}/>')

    def group(self, inner, transform="", extra=""):
        self.add(f'<g transform="{transform}" {extra}>{"".join(inner) if isinstance(inner, list) else inner}</g>')

    def text(self, x, y, s, size, family, fill, anchor="middle", weight=400, style="normal", ls=0, op=1, extra=""):
        s = s.replace("&", "&amp;")
        self.add(f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                 f'font-style="{style}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}" {extra}>{s}</text>')

    def svg(self, fonts_css=""):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                f'<style>{fonts_css}</style><defs>{"".join(self.defs)}</defs>{"".join(self.body)}</svg>')


def _stops(stops):
    out = []
    for s in stops:
        o, c = s[0], s[1]
        a = s[2] if len(s) > 2 else 1
        out.append((o, c, a))
    return out


def font_css(rel="../fonts/"):
    faces = [
        ("Playfair", "PlayfairDisplay[wght].ttf", "100 900", "normal"),
        ("Playfair", "PlayfairDisplay-Italic[wght].ttf", "100 900", "italic"),
        ("PlayfairSC", "PlayfairDisplaySC-Black.ttf", "900", "normal"),
        ("PlayfairSC", "PlayfairDisplaySC-Bold.ttf", "700", "normal"),
        ("BeVN", "BeVietnamPro-Light.ttf", "300", "normal"),
        ("BeVN", "BeVietnamPro-Regular.ttf", "400", "normal"),
        ("BeVN", "BeVietnamPro-Medium.ttf", "500", "normal"),
        ("Hand", "DancingScript[wght].ttf", "400 700", "normal"),
    ]
    return "".join(f"@font-face{{font-family:'{n}';src:url('{rel}{fn}');font-weight:{w};font-style:{st};}}"
                   for n, fn, w, st in faces)


def paper_texture(doc, base="#efe6d2"):
    """Cream paper: base fill, large mottling, fine fibres (multiply)."""
    mot = doc.uid("pf")
    fib = doc.uid("pf")
    doc.defs.append(
        f'<filter id="{mot}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.0022" numOctaves="3" seed="7"/>'
        f'<feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.45  0 0 0 0 0.30  0 0 0 0.16 0"/></filter>'
        f'<filter id="{fib}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.9 0.35" numOctaves="2" seed="3"/>'
        f'<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.10 0"/></filter>')
    doc.add(f'<rect width="{doc.w}" height="{doc.h}" fill="{base}"/>')
    doc.add(f'<rect width="{doc.w}" height="{doc.h}" filter="url(#{mot})"/>')
    doc.add(f'<rect width="{doc.w}" height="{doc.h}" filter="url(#{fib})"/>')


def paper_grain_overlay(doc):
    """Very light grain over everything so vector fills sit in the paper."""
    g = doc.uid("pf")
    doc.defs.append(
        f'<filter id="{g}" x="0" y="0" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="11"/>'
        f'<feColorMatrix values="0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0 0.2  0 0 0 0.07 0"/></filter>')
    doc.add(f'<rect width="{doc.w}" height="{doc.h}" filter="url(#{g})" style="mix-blend-mode:multiply"/>')


def render(svg_text, name, pdf=True):
    FINAL.mkdir(exist_ok=True)
    svg_path = FINAL / f"{name}.svg"
    svg_path.write_text(svg_text, encoding="utf-8")
    png = FINAL / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--disable-gpu",
                    f"--window-size={W},{H + 400}", "--force-device-scale-factor=1",
                    "--virtual-time-budget=8000", f"--screenshot={png}", svg_path.as_uri()],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open(png).convert("RGB").crop((0, 0, W, H))
    im.save(png, dpi=(300, 300))
    if pdf:
        im.save(png.with_suffix(".pdf"), resolution=300)
    print("saved", png)
    return png


def ellipse_pts(cx, cy, rx, ry, n=24, wob=0.0, seed=0, rot=0.0):
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        r = 1 + wob * math.sin(a * 5 + seed) + wob * 0.5 * math.sin(a * 9 + seed * 2)
        x, y = math.cos(a) * rx * r, math.sin(a) * ry * r
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
    return pts
