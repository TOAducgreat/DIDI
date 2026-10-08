"""Hero scene pieces: sky, far city, trees, Tháp Rùa, lake, old-quarter corner, embankment."""
import math
import random

from svg_kit import ellipse_pts, f, poly, smooth


def P(d, fill, op=1, extra=""):
    return f'<path d="{d}" fill="{fill}" opacity="{op}" {extra}/>'


def L(d, stroke, sw=2, op=1, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round" opacity="{op}" {extra}/>')


def rect(x, y, w, h, fill, op=1, rx=0, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" opacity="{op}" {extra}/>'


# ---------------------------------------------------------------- sky
def sky(doc, x0, y0, x1, y1, horizon, sun):
    g = doc.lin([(0, "#f3ead6"), (0.62, "#f4e3bd"), (1, "#eed9a8")])
    out = [rect(x0, y0, x1 - x0, horizon - y0 + 40, g)]
    glow = doc.rad([(0, "#fff4d6", 0.95), (0.35, "#fbe5b0", 0.55), (1, "#f6dca0", 0)])
    sx, sy, sr = sun
    out.append(f'<circle cx="{sx}" cy="{sy}" r="{sr * 4.2}" fill="{glow}"/>')
    out.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#fbf0d4" opacity="0.95"/>')
    return "".join(out)


def cloud_swirl(x, y, s, col="#a9c9bb", op=0.55, flip=False):
    """Tường vân: a long ribbon of cloud ending in a curl."""
    k = -1 if flip else 1
    pts = [(x, y), (x + k * 120 * s, y - 18 * s), (x + k * 260 * s, y - 6 * s), (x + k * 360 * s, y - 34 * s),
           (x + k * 420 * s, y - 70 * s), (x + k * 392 * s, y - 104 * s), (x + k * 350 * s, y - 92 * s),
           (x + k * 356 * s, y - 64 * s)]
    return (L(smooth(pts, closed=False), col, 10 * s, op) +
            L(smooth([(p[0], p[1] + 16 * s) for p in pts[:4]], closed=False), col, 5 * s, op * 0.7))


# ---------------------------------------------------------------- far city & trees
def far_city(doc, x0, x1, base, rnd):
    out = []
    g = doc.lin([(0, "#ddd6c6"), (1, "#e6dfcf")])
    x = x0
    while x < x1:
        w = rnd.uniform(70, 160)
        h = rnd.uniform(90, 260)
        out.append(rect(x, base - h, w, h, g, 0.75))
        for wy in range(int(base - h + 18), int(base - 20), 26):
            for wx in range(int(x + 12), int(x + w - 14), 22):
                out.append(rect(wx, wy, 9, 12, "#cfc6b4", 0.6))
        x += w + rnd.uniform(-10, 30)
    return "".join(out)


def tree_cluster(doc, cx, base, w, h, palette, rnd, n=14, op=1.0):
    """Flat-vector tree: trunk, then the same blobs in dark → mid → light, each pass nudged up-left."""
    light, mid, dark = palette
    out = []
    for k in range(rnd.randint(1, 2)):
        tx = cx + rnd.uniform(-w * 0.15, w * 0.15)
        out.append(L(f"M{f(tx)},{f(base)} Q{f(tx + rnd.uniform(-20, 20))},{f(base - h * 0.4)} {f(tx + rnd.uniform(-30, 30))},{f(base - h * 0.62)}",
                     "#6a5a48", max(4, w * 0.05), op))
    blobs = []
    for _ in range(n):
        bx = cx + rnd.gauss(0, w * 0.22)
        by = base - h * rnd.uniform(0.45, 0.95)
        r = rnd.uniform(0.16, 0.26) * w
        blobs.append((bx, by, r, rnd.random() * 9))
    for col, dx, dy, sc in ((dark, 0, 0, 1.0), (mid, -0.1, -0.16, 0.82), (light, -0.22, -0.34, 0.45)):
        for bx, by, r, sd in blobs:
            out.append(P(smooth(ellipse_pts(bx + dx * r, by + dy * r, r * sc, r * sc * 0.86, n=14, wob=0.07, seed=sd)), col, op))
    return "".join(out)


def tree_band(doc, x0, x1, base, rnd, palettes, height, op=1.0, step=170):
    out = []
    x = x0
    while x < x1:
        pal = rnd.choice(palettes)
        out.append(tree_cluster(doc, x, base, rnd.uniform(160, 260), height * rnd.uniform(0.7, 1.1), pal, rnd, n=9, op=op))
        x += step * rnd.uniform(0.7, 1.2)
    return "".join(out)


# ---------------------------------------------------------------- Tháp Rùa
def thap_rua(doc, cx, base, s):
    """Turtle Tower, front view with a lit front face and shaded right side (3D-ish)."""
    wall_l = doc.lin([(0, "#efe6d4"), (1, "#d8cdb6")], x1=0, y1=0, x2=1, y2=1)
    wall_s = "#b9ad97"
    arch = doc.lin([(0, "#4d5552"), (1, "#2f3634")])
    trim = "#f4ecdc"
    moss = "#8fa076"
    out = []

    def tier(x0, x1, y0, y1, side=14):
        X0, X1 = cx + x0 * s, cx + x1 * s
        Y0, Y1 = base - y1 * s, base - y0 * s
        out.append(rect(X0, Y0, X1 - X0, Y1 - Y0, wall_l))
        out.append(rect(X1 - side * s, Y0, side * s, Y1 - Y0, wall_s, 0.75))

    def cornice(x0, x1, y, h=12):
        X0, X1 = cx + x0 * s, cx + x1 * s
        out.append(rect(X0, base - (y + h) * s, X1 - X0, h * s, trim))
        out.append(rect(X0, base - y * s - 3 * s, X1 - X0, 3 * s, "#a99c86", 0.8))
        out.append(rect(X0 + 6 * s, base - (y + h) * s - 4 * s, X1 - X0 - 12 * s, 4 * s, moss, 0.7))

    def arch_open(xc, y0, w, h):
        x0 = cx + (xc - w / 2) * s
        x1 = cx + (xc + w / 2) * s
        yb = base - y0 * s
        yt = base - (y0 + h) * s
        r = w / 2 * s
        d = f"M{f(x0)},{f(yb)} L{f(x0)},{f(yt + r)} A{f(r)},{f(r)} 0 0 1 {f(x1)},{f(yt + r)} L{f(x1)},{f(yb)} Z"
        out.append(P(d, arch))
        out.append(L(f"M{f(x0 - 4 * s)},{f(yb)} L{f(x0 - 4 * s)},{f(yt + r)} A{f(r + 4 * s)},{f(r + 4 * s)} 0 0 1 {f(x1 + 4 * s)},{f(yt + r)} L{f(x1 + 4 * s)},{f(yb)}",
                     trim, 3 * s))

    tier(-160, 160, 0, 170, 22)
    for xc, w in ((-104, 44), (-34, 50), (34, 50), (104, 44)):
        arch_open(xc, 18, w, 108 if abs(xc) < 60 else 96)
    cornice(-176, 176, 170)
    tier(-116, 116, 182, 300, 18)
    for xc in (-58, 0, 58):
        arch_open(xc, 200, 34, 74)
    cornice(-130, 130, 300)
    tier(-78, 78, 312, 400, 14)
    out.append(f'<circle cx="{f(cx)}" cy="{f(base - 356 * s)}" r="{f(22 * s)}" fill="{arch}"/>')
    out.append(f'<circle cx="{f(cx)}" cy="{f(base - 356 * s)}" r="{f(26 * s)}" fill="none" stroke="{trim}" stroke-width="{f(3 * s)}"/>')
    for xc in (-48, 48):
        arch_open(xc, 330, 20, 46)
    cornice(-92, 92, 400)
    tier(-48, 48, 412, 462, 10)
    arch_open(0, 420, 22, 34)
    # crowning roof with upturned eaves
    roof = [(cx - 82 * s, base - 462 * s), (cx - 96 * s, base - 476 * s), (cx - 50 * s, base - 490 * s),
            (cx, base - 516 * s), (cx + 50 * s, base - 490 * s), (cx + 96 * s, base - 476 * s), (cx + 82 * s, base - 462 * s)]
    out.append(P(smooth(roof), doc.lin([(0, "#7c7468"), (1, "#5b544b")])))
    out.append(rect(cx - 3 * s, base - 556 * s, 6 * s, 42 * s, "#5b544b"))
    out.append(f'<circle cx="{f(cx)}" cy="{f(base - 560 * s)}" r="{f(8 * s)}" fill="#5b544b"/>')
    # moss/grass islet
    isl = doc.lin([(0, "#9fb27f"), (1, "#6f8a5d")])
    out.append(P(smooth(ellipse_pts(cx, base + 6 * s, 300 * s, 34 * s, n=20, wob=0.05, seed=2)), isl))
    return "".join(out)


# ---------------------------------------------------------------- lake
def lake(doc, x0, x1, top, bottom, rnd):
    g = doc.lin([(0, "#cfdcd0"), (0.35, "#a9c3b9"), (1, "#6f978e")])
    out = [rect(x0, top, x1 - x0, bottom - top, g)]
    out.append(rect(x0, top, x1 - x0, 6, "#f3ead2", 0.8))
    for k in range(70):
        y = top + 20 + (k / 70) ** 1.4 * (bottom - top - 30)
        xs = rnd.uniform(x0, x1 - 200)
        ln = rnd.uniform(60, 260) * (0.6 + (y - top) / (bottom - top))
        out.append(L(f"M{f(xs)},{f(y)} L{f(xs + ln)},{f(y)}", "#eef3ea", rnd.uniform(2, 4), rnd.uniform(0.25, 0.6)))
    return "".join(out)


def reflection(inner, axis_y, op=0.32):
    return f'<g transform="translate(0,{f(2 * axis_y)}) scale(1,-1)" opacity="{op}">{inner}</g>'


# ---------------------------------------------------------------- old-quarter corner
def old_house(doc, x0, x1, top, ground, rnd):
    out = []
    wall = doc.lin([(0, "#efd394"), (0.6, "#e3be70"), (1, "#d3a95c")], x1=0, y1=0, x2=1, y2=1)
    out.append(rect(x0, top, x1 - x0, ground - top, wall))
    # weathering stains
    for _ in range(9):
        cx, cy = rnd.uniform(x0, x1), rnd.uniform(top, ground)
        out.append(P(smooth(ellipse_pts(cx, cy, rnd.uniform(40, 120), rnd.uniform(30, 90), n=14, wob=0.15, seed=rnd.random() * 5)),
                     "#b98d47", rnd.uniform(0.06, 0.14)))
    # roof eave with tiles
    roof = doc.lin([(0, "#c4573c"), (1, "#9c3f2c")])
    out.append(P(poly([(x0 - 40, top + 10), (x1 + 50, top - 40), (x1 + 70, top + 30), (x0 - 40, top + 60)]), roof))
    for k in range(18):
        t = k / 17
        xa, ya = x0 - 40 + t * (x1 + 90 - x0), top + 10 - t * 50
        out.append(L(f"M{f(xa)},{f(ya)} L{f(xa + 16)},{f(ya + 52)}", "#e07f5f", 3, 0.6))
    out.append(L(f"M{f(x0 - 40)},{f(top + 60)} L{f(x1 + 70)},{f(top + 30)}", "#7c2e20", 6))
    # shuttered windows, two floors
    sh = doc.lin([(0, "#3f8670"), (1, "#2a5f50")])
    for fy, fh in ((top + 140, 300), (top + 520, 330)):
        for wx in (x0 + 80, x0 + 330):
            ww = 200
            out.append(rect(wx - 14, fy - 14, ww + 28, fh + 28, "#c99f58", 0.6))
            out.append(rect(wx, fy, ww / 2 - 4, fh, sh))
            out.append(rect(wx + ww / 2 + 4, fy, ww / 2 - 4, fh, sh))
            for ly in range(int(fy + 16), int(fy + fh - 10), 16):
                out.append(L(f"M{f(wx + 10)},{f(ly)} L{f(wx + ww / 2 - 14)},{f(ly)}", "#5ea58c", 2.5, 0.8))
                out.append(L(f"M{f(wx + ww / 2 + 14)},{f(ly)} L{f(wx + ww - 10)},{f(ly)}", "#5ea58c", 2.5, 0.8))
            out.append(rect(wx + ww / 2 - 4, fy, 8, fh, "#1e463b", 0.6))
    # balcony rail on first floor
    by = top + 470
    out.append(rect(x0 + 40, by, x1 - x0 - 60, 10, "#3b3a36"))
    for k in range(int((x1 - x0 - 60) / 26)):
        bx = x0 + 52 + k * 26
        out.append(L(f"M{f(bx)},{f(by + 10)} L{f(bx)},{f(by + 90)}", "#3b3a36", 4))
        out.append(f'<circle cx="{f(bx + 13)}" cy="{f(by + 50)}" r="9" fill="none" stroke="#3b3a36" stroke-width="3"/>')
    out.append(rect(x0 + 40, by + 90, x1 - x0 - 60, 8, "#3b3a36"))
    # shadow on right edge
    out.append(rect(x1 - 30, top, 30, ground - top, "#8d6a33", 0.25))
    return "".join(out)


def bicycle(doc, x, y, s, flowers):
    """Old black bicycle with a basket of flowers on the rear rack. (x, y) = rear hub."""
    out = []
    R = 92 * s
    fx = x + 300 * s
    for cx in (x, fx):
        out.append(f'<circle cx="{f(cx)}" cy="{f(y)}" r="{f(R)}" fill="none" stroke="#2a2a28" stroke-width="{f(9 * s)}"/>')
        out.append(f'<circle cx="{f(cx)}" cy="{f(y)}" r="{f(R - 8 * s)}" fill="none" stroke="#6b6a63" stroke-width="{f(2 * s)}"/>')
        for k in range(18):
            a = math.pi * 2 * k / 18
            out.append(L(f"M{f(cx)},{f(y)} L{f(cx + math.cos(a) * (R - 8 * s))},{f(y + math.sin(a) * (R - 8 * s))}", "#8a887e", 1.4 * s))
    bb = (x + 130 * s, y + 4 * s)
    st = (x + 100 * s, y - 150 * s)
    ht = (fx - 30 * s, y - 165 * s)
    fr = "#24302b"
    for a, b in ((bb, (x, y)), (st, (x, y)), (bb, st), (bb, (fx - 22 * s, y - 120 * s)), (ht, (fx, y)), (st, ht)):
        out.append(L(f"M{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])}", fr, 8 * s))
    out.append(L(f"M{f(ht[0])},{f(ht[1])} L{f(ht[0] - 10 * s)},{f(ht[1] - 30 * s)} L{f(ht[0] - 60 * s)},{f(ht[1] - 40 * s)}", fr, 7 * s))
    out.append(P(smooth(ellipse_pts(st[0] - 6 * s, st[1] - 10 * s, 34 * s, 10 * s, n=12)), "#3b2c22"))
    # rear basket of flowers
    bk = doc.lin([(0, "#d9b06c"), (1, "#a9783d")])
    bx0, bx1, byt, byb = x - 100 * s, x + 90 * s, y - 210 * s, y - 110 * s
    out.append(P(poly([(bx0, byt), (bx1, byt), (bx1 - 12 * s, byb), (bx0 + 12 * s, byb)]), bk))
    for k in range(1, 5):
        yy = byt + (byb - byt) * k / 5
        out.append(L(f"M{f(bx0 + 3 * k * s)},{f(yy)} L{f(bx1 - 3 * k * s)},{f(yy)}", "#8a5f2e", 2 * s, 0.7))
    out.append(flowers(doc, (bx0 + bx1) / 2, byt + 6 * s, 105 * s, 70 * s))
    return "".join(out)


def embankment(doc, x0, x1, y, depth):
    """Stone lake edge and the pavement in front of it."""
    edge = doc.lin([(0, "#d9d1bf"), (1, "#b8ae98")])
    pave = doc.lin([(0, "#e7e0cf"), (1, "#d8cfba")])
    out = [rect(x0, y, x1 - x0, 26, edge), rect(x0, y + 26, x1 - x0, depth, pave)]
    for k in range(int((x1 - x0) / 120)):
        xx = x0 + k * 120
        out.append(L(f"M{f(xx)},{f(y)} L{f(xx)},{f(y + 26)}", "#a69c87", 2, 0.6))
    for k in range(5):
        yy = y + 26 + depth * (k + 1) / 6
        out.append(L(f"M{f(x0)},{f(yy)} L{f(x1)},{f(yy)}", "#cfc5ae", 2, 0.35))
    return "".join(out)
