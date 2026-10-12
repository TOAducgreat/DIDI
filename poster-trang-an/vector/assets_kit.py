"""Load third-party CC0 vector elements (already sanitised, see assets/NGUON.md),
recolour them to the poster palette and place them as <symbol>/<use>."""
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

# Khuê Văn Các (openclipart #288742): stone pillars → warm ivory stone, lacquer → poster vermilion
KVC_COLORS = {
    "#675e59": "#5b544b",   # roof ridge ornaments, dark
    "#978e89": "#b3a68f",   # pillar shade
    "#afa7a4": "#cfc4ae",   # pillar
    "#b4ada7": "#d6ccb7",
    "#bcb4ad": "#ddd3bf",
    "#c3bbb8": "#e6ddca",   # pillar light
    "#90532a": "#7c3a26",   # timber
    "#a62031": "#9c2e22",   # lacquered red
    "#7f0917": "#6f1f17",   # red shade
    "#c14630": "#b5553c",   # platform / tiles
}
KVC_DROP = ("rect8134",)                                   # flat blue backdrop in the source file
KVC_FILL = {"path270063": "#b5553c", "path270067": "#a84a34"}  # roofs (tile pattern removed when sanitising)


def khue_van_cac(doc):
    return symbol(doc, "khue-van-cac.svg", colors=KVC_COLORS, drop_ids=KVC_DROP, fill_ids=KVC_FILL)


def _body(name):
    s = (ASSETS / name).read_text(encoding="utf-8")
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r"^.*?<svg[^>]*>", "", s, count=1, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
    return vb, inner


def symbol(doc, name, colors=None, fill=None, prefix=None, drop_ids=(), fill_ids=None):
    """Register an asset as <symbol>; returns (symbol id, viewBox tuple).
    drop_ids: elements to remove (e.g. the artist's background); fill_ids: {id: fill} for unfilled shapes."""
    vb, inner = _body(name)
    for i in drop_ids:
        inner = re.sub(rf'<(\w+)[^>]*\bid="{re.escape(i)}"[^>]*/>', "", inner)
    for i, col in (fill_ids or {}).items():
        inner = re.sub(rf'(<\w+)([^>]*\bid="{re.escape(i)}")', rf'\1 fill="{col}"\2', inner)
    if colors:
        for a, b in colors.items():
            inner = re.sub(re.escape(a), b, inner, flags=re.I)
    if fill:                                   # monochrome assets: force one colour
        inner = re.sub(r'fill:#[0-9a-fA-F]{3,6}', f"fill:{fill}", inner)
        inner = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="{fill}"', inner)
        inner = f'<g fill="{fill}">{inner}</g>'
    pid = prefix or doc.uid("as")
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{pid}-{m.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f"url(#{pid}-{m.group(1)})", inner)
    sid = doc.uid("sym")
    doc.defs.append(f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>')
    return sid, tuple(float(v) for v in vb.split())


def use(sid, vb, cx, cy, width, op=1.0, flip=False, extra=""):
    """Place a symbol centred at (cx, cy) with the given width (height keeps aspect)."""
    w = width
    h = width * vb[3] / vb[2]
    t = f' transform="translate({2 * cx},0) scale(-1,1)"' if flip else ""
    return (f'<g{t} opacity="{op}" {extra}><use href="#{sid}" x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" '
            f'width="{w:.1f}" height="{h:.1f}"/></g>')
