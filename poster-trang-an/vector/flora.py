"""Flowers and leaves: cúc họa mi, hoa sữa branches, lotus flowers and leaves."""
import math
import random

from scene import L, P
from svg_kit import ellipse_pts, f, smooth


def daisy(cx, cy, r, rot=0.0, tilt=1.0):
    """Cúc họa mi: white petals around a golden heart; tilt < 1 squashes it into perspective."""
    out = []
    n = 14
    for k in range(n):
        a = rot + 2 * math.pi * k / n
        px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55 * tilt
        pts = ellipse_pts(px, py, r * 0.5, r * 0.16, n=10, rot=math.atan2(math.sin(a) * tilt, math.cos(a)))
        out.append(P(smooth(pts), "#fbf8f0"))
        out.append(P(smooth(pts), "none", extra='stroke="#d8d2c2" stroke-width="1.2"'))
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.26)}" fill="#e7b43a"/>')
    out.append(f'<circle cx="{f(cx - r * 0.06)}" cy="{f(cy - r * 0.06)}" r="{f(r * 0.12)}" fill="#f6d36c"/>')
    return "".join(out)


def daisy_heap(doc, cx, top, w, h, seed=1, size=1.0):
    """A dome of daisies (for baskets)."""
    rnd = random.Random(seed)
    out = []
    pts = []
    for _ in range(int(60 * size)):
        a = rnd.uniform(math.pi, 2 * math.pi)
        rr = rnd.uniform(0, 1) ** 0.6
        pts.append((cx + math.cos(a) * w * rr, top + math.sin(a) * h * rr + 6, rnd.uniform(12, 20) * size))
    pts.sort(key=lambda q: q[1])
    for x, y, r in pts:
        out.append(L(f"M{f(x)},{f(y)} L{f(x + rnd.uniform(-8, 8))},{f(top + 10)}", "#7f9a62", 2))
        out.append(P(smooth(ellipse_pts(x + r, y + r * 0.6, r * 0.7, r * 0.25, n=8, rot=0.6)), "#86a466", 0.9))
    for x, y, r in pts:
        out.append(daisy(x, y, r, rot=rnd.random(), tilt=rnd.uniform(0.75, 1.0)))
    return "".join(out)


def leaf(doc, x, y, length, width, angle, c_light="#9fbf7f", c_dark="#4f7a46", vein=True):
    """Single pointed leaf with a two-tone fill split along the midrib."""
    ca, sa = math.cos(angle), math.sin(angle)

    def T(u, v):
        return (x + u * ca - v * sa, y + u * sa + v * ca)
    left = [T(length * t, width * math.sin(math.pi * t) ** 0.9) for t in [i / 8 for i in range(9)]]
    right = [T(length * t, -width * math.sin(math.pi * t) ** 0.9) for t in [i / 8 for i in range(9)]]
    out = [P(smooth(left + right[::-1][1:-1]), c_dark),
           P(smooth(left + [T(length * t, 0) for t in [i / 8 for i in range(8, -1, -1)]][1:-1]), c_light)]
    if vein:
        out.append(L(f"M{f(T(0, 0)[0])},{f(T(0, 0)[1])} L{f(T(length * 0.92, 0)[0])},{f(T(length * 0.92, 0)[1])}", "#e7efd8", 1.6, 0.7))
    return "".join(out)


def hoa_sua_branch(doc, x, y, length, angle, seed=3, scale=1.0, droop=0.35):
    """Branch of hoa sữa (Alstonia): glossy whorls of leaves and creamy flower clusters."""
    rnd = random.Random(seed)
    out = []
    pts = []
    for i in range(9):
        t = i / 8
        a = angle + droop * t * t
        pts.append((x + math.cos(a) * length * t, y + math.sin(a) * length * t + 30 * math.sin(t * 3)))
    out.append(L(smooth(pts, closed=False), "#5b4632", 12 * scale))
    out.append(L(smooth(pts, closed=False), "#7d6448", 4 * scale, 0.7))
    for i in range(2, 9):
        bx, by = pts[i]
        for k in range(5):                                  # leaf whorl
            a = rnd.uniform(0, 2 * math.pi)
            out.append(leaf(doc, bx, by, rnd.uniform(90, 150) * scale, rnd.uniform(18, 26) * scale, a,
                            c_light=rnd.choice(["#8fb071", "#9fbf7f", "#7fa564"]), c_dark=rnd.choice(["#476f40", "#3e6338"])))
        if i % 2 == 0:                                       # flower cluster
            fx, fy = bx + rnd.uniform(-30, 30), by - rnd.uniform(10, 40)
            for _ in range(int(16 * scale + 6)):
                px, py = fx + rnd.gauss(0, 34 * scale), fy + rnd.gauss(0, 22 * scale)
                rr = rnd.uniform(7, 11) * scale
                for k in range(5):
                    a = 2 * math.pi * k / 5 + rnd.random()
                    out.append(P(smooth(ellipse_pts(px + math.cos(a) * rr * 0.6, py + math.sin(a) * rr * 0.6, rr * 0.55, rr * 0.3,
                                                    n=8, rot=a)), "#fbf6e6"))
                out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(rr * 0.22)}" fill="#e9d38c"/>')
    return "".join(out)


def lotus_leaf(doc, cx, cy, rx, ry, rot=0.0, seed=1):
    """Big lotus leaf: radial gradient light centre -> dark rim, radiating veins, wavy edge."""
    g = doc.rad([(0, "#c4d9a2"), (0.45, "#8fb57a"), (1, "#4f7d55")], cx=0.5, cy=0.45, r=0.6)
    pts = ellipse_pts(cx, cy, rx, ry, n=40, wob=0.04, seed=seed, rot=rot)
    out = [P(smooth(pts), g)]
    for k in range(16):
        a = 2 * math.pi * k / 16
        ex = cx + math.cos(a) * rx * 0.92 * math.cos(rot) - math.sin(a) * ry * 0.92 * math.sin(rot)
        ey = cy + math.cos(a) * rx * 0.92 * math.sin(rot) + math.sin(a) * ry * 0.92 * math.cos(rot)
        out.append(L(smooth([(cx, cy), ((cx + ex) / 2 + 4, (cy + ey) / 2 - 3), (ex, ey)], closed=False), "#e3eed0", 2.2, 0.55))
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(min(rx, ry) * 0.06)}" fill="#c9dca9"/>')
    out.append(P(smooth(pts), "none", extra='stroke="#3f6a47" stroke-width="3" opacity="0.5"'))
    return "".join(out)


def lotus_flower(doc, cx, cy, s, angle=0.0):
    """Lotus bloom seen from the side: petals white at the base, rose at the tips, each with a highlight."""
    out = []
    spec = [(-70, 0.78, 0.32), (70, 0.78, 0.32), (-42, 0.95, 0.34), (42, 0.95, 0.34),
            (-16, 1.02, 0.34), (16, 1.02, 0.34), (-56, 0.7, 0.3), (56, 0.7, 0.3), (0, 0.92, 0.36)]
    for deg, ln, wd in spec:
        a = math.radians(-90 + deg) + angle
        ca, sa = math.cos(a), math.sin(a)

        def T(u, v):
            return (cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)
        n = 10
        left = [T(ln * 160 * t, wd * 160 * math.sin(math.pi * min(1, t * 1.05)) ** 0.85 * (1 - 0.5 * t ** 2.4)) for t in [i / n for i in range(n + 1)]]
        right = [T(ln * 160 * t, -wd * 160 * math.sin(math.pi * min(1, t * 1.05)) ** 0.85 * (1 - 0.5 * t ** 2.4)) for t in [i / n for i in range(n + 1)]]
        tip = T(ln * 160, 0)
        base = T(0, 0)
        g = doc.lin([(0, "#fff8f2"), (0.55, "#f6cfc4"), (1, "#e2786c")],
                    x1=f(base[0]), y1=f(base[1]), x2=f(tip[0]), y2=f(tip[1]), units="userSpaceOnUse")
        out.append(P(smooth(left + right[::-1][1:-1]), g))
        hl = [T(ln * 160 * t, wd * 40 * math.sin(math.pi * t)) for t in (0.2, 0.45, 0.7)]
        out.append(L(smooth(hl, closed=False), "#ffffff", 5 * s, 0.6))
    out.append(P(smooth(ellipse_pts(cx, cy - 20 * s, 34 * s, 16 * s, n=12)), "#e8c75a"))
    return "".join(out)
