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
def _ogive(x0, x1, yb, ys, yt):
    """Pointed (Gothic) arch opening: sides up to ys, two curves meeting at yt."""
    xm = (x0 + x1) / 2
    k = (ys - yt) * 0.55
    return (f"M{f(x0)},{f(yb)} L{f(x0)},{f(ys)} C{f(x0)},{f(ys - k)} {f(xm - (x1 - x0) * 0.18)},{f(yt + 4)} {f(xm)},{f(yt)} "
            f"C{f(xm + (x1 - x0) * 0.18)},{f(yt + 4)} {f(x1)},{f(ys - k)} {f(x1)},{f(ys)} L{f(x1)},{f(yb)} Z")


def thap_rua(doc, cx, base, s, rnd_seed=4):
    """Turtle Tower seen at 3/4: lit front face, shaded side face, Gothic arches, balustrades,
    round window on the third tier and a small pavilion with a double curved roof on top."""
    rnd = random.Random(rnd_seed)
    front = doc.lin([(0, "#ece4d2"), (0.6, "#e2d8c3"), (1, "#cfc3aa")])
    side = doc.lin([(0, "#bdb19a"), (1, "#a59882")])
    dark = doc.lin([(0, "#3f4644"), (1, "#262c2b")])
    trim, trim_s = "#f3ecdc", "#cfc4ac"
    moss = "#7f9468"
    out = []
    SK = 0.28                                    # side face width ratio (perspective)
    LIFT = 0.0                                  # side face recedes upward

    def X(u):
        return cx + u * s

    def Y(v):
        return base - v * s

    def block(w, y0, y1, arches=(), side_arches=0, round_win=False):
        hw = w / 2
        sw = w * SK
        # front face
        out.append(rect(X(-hw), Y(y1), w * s, (y1 - y0) * s, front))
        # side face (parallelogram)
        out.append(P(poly([(X(hw), Y(y0)), (X(hw + sw), Y(y0) - sw * LIFT * s), (X(hw + sw), Y(y1) - sw * LIFT * s), (X(hw), Y(y1))]), side))
        # weathering streaks under the cornice
        for _ in range(int(w / 26)):
            xs = rnd.uniform(-hw + 6, hw - 6)
            out.append(rect(X(xs), Y(y1), rnd.uniform(3, 9) * s, rnd.uniform(0.2, 0.6) * (y1 - y0) * s, "#8f8572", rnd.uniform(0.08, 0.18)))
        h = y1 - y0
        for xc, aw, ah in arches:
            out.append(P(_ogive(X(xc - aw / 2 - 5), X(xc + aw / 2 + 5), Y(y0 + 6), Y(y0 + ah * 0.62), Y(y0 + ah + 8)), trim_s))
            out.append(P(_ogive(X(xc - aw / 2), X(xc + aw / 2), Y(y0 + 6), Y(y0 + ah * 0.62), Y(y0 + ah)), dark))
        for k in range(side_arches):                         # narrow arches on the receding face
            t = (k + 0.5) / side_arches
            xa = hw + sw * t
            lift = sw * t * LIFT
            aw = w * SK / side_arches * 0.45
            out.append(P(_ogive(X(xa - aw / 2), X(xa + aw / 2), Y(y0 + 6) - lift * s, Y(y0 + h * 0.5) - lift * s, Y(y0 + h * 0.78) - lift * s), "#2b3130", 0.85))
        if round_win:
            out.append(f'<circle cx="{f(X(0))}" cy="{f(Y(y0 + h * 0.55))}" r="{f(h * 0.3 * s)}" fill="{trim_s}"/>')
            out.append(f'<circle cx="{f(X(0))}" cy="{f(Y(y0 + h * 0.55))}" r="{f(h * 0.24 * s)}" fill="{dark}"/>')
        # pilasters at the corners
        for u in (-hw, hw - 8):
            out.append(rect(X(u), Y(y1), 8 * s, h * s, trim, 0.7))

    def cornice(w, y, rail=True):
        hw = w / 2 + 10
        sw = (w + 20) * SK
        out.append(rect(X(-hw), Y(y + 12), (2 * hw) * s, 12 * s, trim))
        out.append(P(poly([(X(hw), Y(y)), (X(hw + sw), Y(y) - sw * LIFT * s), (X(hw + sw), Y(y + 12) - sw * LIFT * s), (X(hw), Y(y + 12))]), trim_s))
        out.append(rect(X(-hw), Y(y + 1), (2 * hw) * s, 3 * s, "#9c917c", 0.7))
        out.append(rect(X(-hw + 4), Y(y + 15), (2 * hw - 8) * s, 3 * s, moss, 0.75))
        if rail:                                                # little balustrade
            out.append(rect(X(-hw + 6), Y(y + 30), (2 * hw - 12) * s, 3 * s, trim))
            for k in range(int((2 * hw - 12) / 14) + 1):
                out.append(rect(X(-hw + 6 + k * 14), Y(y + 30), 3 * s, 16 * s, trim, 0.9))

    block(300, 0, 150, arches=((-96, 46, 104), (0, 60, 122), (96, 46, 104)), side_arches=2)
    cornice(300, 150)
    block(220, 180, 280, arches=((-64, 34, 70), (0, 40, 78), (64, 34, 70)), side_arches=2)
    cornice(220, 280)
    block(150, 310, 390, arches=((-50, 22, 46), (50, 22, 46)), side_arches=1, round_win=True)
    cornice(150, 390)
    block(78, 420, 466, arches=((0, 26, 38),), side_arches=1)
    # double curved roof of the crowning pavilion, upturned eaves
    roof_d = doc.lin([(0, "#6f6a5f"), (1, "#4d4941")])
    for y, w, h in ((466, 132, 34), (500, 96, 46)):
        hw = w / 2
        e = w * SK * 0.5
        pts = [(X(-hw - 10), Y(y)), (X(-hw - 30), Y(y + 22)), (X(-hw - 4), Y(y + 14)), (X(-hw * 0.4), Y(y + h * 0.75)),
               (X(e * 0.3), Y(y + h)), (X(hw * 0.4 + e), Y(y + h * 0.75)), (X(hw + 4 + e), Y(y + 14)), (X(hw + 30 + e), Y(y + 22)),
               (X(hw + 10 + e), Y(y))]
        out.append(P(smooth(pts, tension=0.6), roof_d))
        out.append(L(smooth([(X(-hw - 12), Y(y + 6)), (X(0), Y(y + h * 0.45)), (X(hw + 12 + w * SK * 0.4), Y(y + 6) - 5 * s)], closed=False),
                     "#8d877a", 2.5 * s, 0.8))
    out.append(rect(X(e * 0.3 - 2.5), Y(586), 5 * s, 44 * s, "#4d4941"))
    out.append(f'<circle cx="{f(X(e * 0.3))}" cy="{f(Y(588))}" r="{f(7 * s)}" fill="#4d4941"/>')
    # moss and small plants on the ledges
    for y, w in ((150, 300), (280, 220), (390, 150)):
        for _ in range(4):
            u = rnd.uniform(-w / 2, w / 2)
            out.append(P(smooth(ellipse_pts(X(u), Y(y + 18), rnd.uniform(6, 14) * s, rnd.uniform(4, 8) * s, n=10, wob=0.2, seed=rnd.random())), moss, 0.85))
    # islet: grassy mound, shrubs and a few trees around the base
    isl = doc.lin([(0, "#a7b986"), (1, "#6f8a5d")])
    out.insert(0, P(smooth(ellipse_pts(X(40), Y(-6), 330 * s, 40 * s, n=22, wob=0.05, seed=2)), isl))
    shrub_pal = ("#b7cc8f", "#86a96a", "#5a8452")
    for u, w, h in ((-250, 120, 120), (-190, 90, 80), (300, 130, 150), (240, 90, 90)):
        out.insert(1, tree_cluster(doc, X(u), Y(-4), w * s, h * s, shrub_pal, rnd, n=7))
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
