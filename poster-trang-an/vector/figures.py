"""Flat-vector figures with realistic proportions (≈7.5 heads tall).

Local coordinates: feet at y=0, up is negative, facing +x. Placed with `place()`.
"""
import math

from scene import L, P
from svg_kit import ellipse_pts, f, smooth

SKIN, SKIN_SH, SKIN_HL = "#f1d3bf", "#ddb39b", "#f8e3d4"
HAIR, HAIR_HL = "#1b1716", "#463b37"
SHIRT, SHIRT_SH, SHIRT_LN = "#fbfaf6", "#e1ddd3", "#cfc9bc"
NAVY, NAVY_L, NAVY_D = "#2d3b5a", "#46597f", "#1e2840"


def T(pts, dx=0, dy=0, sx=1, sy=1):
    return [(dx + x * sx, dy + y * sy) for x, y in pts]


def rot(pts, ang, ox, oy):
    c, s = math.cos(ang), math.sin(ang)
    return [(ox + (x - ox) * c - (y - oy) * s, oy + (x - ox) * s + (y - oy) * c) for x, y in pts]


# ------------------------------------------------------------ head (profile, facing right)
PROFILE = [(-44, -10), (-40, -40), (-18, -56), (12, -56), (32, -42), (39, -22), (40, -8), (45, 2), (53, 15), (47, 19),
           (48, 25), (45, 29), (47, 34), (42, 40), (41, 47), (31, 55), (12, 53), (-6, 42), (-22, 26)]


def head(ox, oy, hair_style, old=False, sc=1.0):
    """Head centred at (ox, oy). Returns (back_hair, face_and_front_hair) so a ponytail can sit behind the body."""
    pts = T(PROFILE, ox, oy, sc, sc)
    back, front = [], []
    front.append(P(smooth(pts, tension=0.85), SKIN))
    front.append(P(smooth(T([(-30, 10), (-10, 34), (12, 48), (30, 52), (10, 40), (-8, 22)], ox, oy, sc, sc)), SKIN_SH, 0.55))  # jaw shade
    # ear
    front.append(P(smooth(ellipse_pts(ox - 8 * sc, oy + 6 * sc, 8 * sc, 12 * sc, n=10)), SKIN_SH))
    # closed, downcast eye with lashes; brow
    ex, ey = ox + 24 * sc, oy - 2 * sc
    front.append(L(f"M{f(ex - 10 * sc)},{f(ey)} Q{f(ex)},{f(ey + 6 * sc)} {f(ex + 9 * sc)},{f(ey + 1 * sc)}", "#3a2b26", 2.6 * sc))
    for k in range(3):
        front.append(L(f"M{f(ex - 6 * sc + k * 5 * sc)},{f(ey + 4 * sc)} l{f(-1 * sc)},{f(4 * sc)}", "#3a2b26", 1.4 * sc))
    front.append(L(f"M{f(ex - 10 * sc)},{f(ey - 12 * sc)} Q{f(ex + 2 * sc)},{f(ey - 17 * sc)} {f(ex + 12 * sc)},{f(ey - 12 * sc)}",
                   "#bdb5ad" if old else "#3e302b", 2.6 * sc))
    # nostril, lips, blush
    front.append(L(f"M{f(ox + 45 * sc)},{f(oy + 17 * sc)} q{f(-3 * sc)},{f(1 * sc)} {f(-4 * sc)},{f(-2 * sc)}", "#c49b86", 1.6 * sc))
    lip = "#b8645d" if old else "#cf6b66"
    front.append(P(smooth(T([(40, 26), (45, 26), (44.5, 29), (45, 33), (40, 32)], ox, oy, sc, sc)), lip, 0.85))
    front.append(P(smooth(ellipse_pts(ox + 22 * sc, oy + 18 * sc, 12 * sc, 7 * sc, n=10)), "#f0a39a", 0.4))
    if old:
        for a, b in (((30, 8), (34, 22)), ((18, -26), (32, -28)), ((28, 34), (34, 40))):
            front.append(L(f"M{f(ox + a[0] * sc)},{f(oy + a[1] * sc)} L{f(ox + b[0] * sc)},{f(oy + b[1] * sc)}", "#c9a08b", 1.4 * sc, 0.8))

    if hair_style == "ponytail":
        cap = [(36, -32), (24, -52), (0, -62), (-26, -58), (-46, -36), (-50, -8), (-40, 6), (-28, -4), (-14, -26), (6, -38), (24, -36)]
        tail = [(-40, -30), (-62, -18), (-74, 30), (-80, 100), (-70, 170), (-56, 210), (-52, 150), (-48, 80), (-40, 20), (-32, -14)]
        back.append(P(smooth(T(tail, ox, oy, sc, sc)), HAIR))
        for k in range(3):
            back.append(L(smooth(T([(-48 - k * 6, -6), (-62 - k * 4, 60), (-62 - k * 2, 150 - k * 20)], ox, oy, sc, sc), closed=False), HAIR_HL, 2.4 * sc, 0.7))
        front.append(P(smooth(T(cap, ox, oy, sc, sc)), HAIR))
        front.append(L(smooth(T([(30, -40), (40, -24), (40, -8)], ox, oy, sc, sc), closed=False), HAIR, 7 * sc))   # fringe wisp
        # ribbon bow at the tie
        bx, by = ox - 48 * sc, oy - 28 * sc
        for d in ((-1, -1), (1, -1)):
            front.append(P(smooth(T([(0, 0), (d[0] * 30, -18), (d[0] * 30, 12)], bx, by, sc, sc)), "#fbfaf6"))
        front.append(L(f"M{f(bx)},{f(by)} l{f(-8 * sc)},{f(34 * sc)} M{f(bx)},{f(by)} l{f(8 * sc)},{f(36 * sc)}", "#f1eee6", 5 * sc))
        front.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(6 * sc)}" fill="#e7e2d6"/>')
    elif hair_style == "long":
        mane = [(38, -30), (24, -54), (-2, -64), (-30, -58), (-50, -34), (-56, 10), (-60, 90), (-64, 180), (-58, 250), (-40, 266),
                (-30, 200), (-24, 120), (-18, 60), (-14, 20), (-10, -20), (10, -40), (26, -36)]
        back.append(P(smooth(T(mane[5:12] + [(-30, 200), (-20, 60)], ox, oy, sc, sc)), HAIR))
        front.append(P(smooth(T(mane, ox, oy, sc, sc)), HAIR))
        for k in range(4):
            front.append(L(smooth(T([(-10 - k * 9, -50), (-30 - k * 6, 20), (-38 - k * 5, 120), (-40 - k * 4, 220)], ox, oy, sc, sc), closed=False),
                           HAIR_HL, 2.2 * sc, 0.65))
        front.append(L(smooth(T([(32, -40), (42, -22), (41, -6)], ox, oy, sc, sc), closed=False), HAIR, 7 * sc))
        front.append(P(smooth(ellipse_pts(ox - 20 * sc, oy - 52 * sc, 14 * sc, 5 * sc, n=10, rot=-0.35)), "#c9a24e"))  # clip
    elif hair_style == "bun":
        cap = [(34, -34), (20, -54), (-4, -62), (-30, -56), (-46, -34), (-48, -6), (-36, 4), (-24, -10), (-6, -30), (14, -40), (28, -38)]
        front.append(P(smooth(ellipse_pts(ox - 52 * sc, oy - 28 * sc, 24 * sc, 22 * sc, n=14)), "#a8a198"))
        front.append(P(smooth(T(cap, ox, oy, sc, sc)), "#c3bdb4"))
        for k in range(4):
            front.append(L(smooth(T([(26 - k * 14, -50 + k * 3), (-6 - k * 8, -46), (-40, -30 + k * 6)], ox, oy, sc, sc), closed=False),
                           "#e6e1d9", 1.8 * sc, 0.8))
    return "".join(back), "".join(front)


# ------------------------------------------------------------ schoolgirl
def schoolgirl(doc, variant=0, bow=18):
    out = []
    WAIST = -505
    # --- legs (behind skirt)
    for dx, col, sk in ((-14, SKIN_SH, 0), (10, SKIN, 1)):
        leg = [(dx - 14, -350), (dx + 14, -350), (dx + 16, -280), (dx + 21, -205), (dx + 14, -120), (dx + 9, -44),
               (dx - 5, -44), (dx - 7, -120), (dx - 12, -215), (dx - 14, -285)]
        out.append(P(smooth(leg, tension=0.7), col))
        out.append(P(smooth([(dx - 7, -118), (dx + 12, -118), (dx + 9, -36), (dx - 5, -36)]), "#f8f6f0"))
        out.append(L(f"M{dx - 6},-110 L{dx + 11},-110", "#dcd7cb", 2))
        shoe = [(dx - 8, -40), (dx + 12, -42), (dx + 34, -24), (dx + 36, -6), (dx - 8, -4)]
        out.append(P(smooth(shoe, tension=0.6), "#26211f"))
        out.append(L(f"M{dx - 2},-26 L{dx + 22},-26", "#4b433e", 2))
        out.append(L(f"M{dx + 6},-8 L{dx + 34},-8", "#120f0e", 3))
    # --- skirt
    sk = doc.lin([(0, NAVY_L), (0.5, NAVY), (1, NAVY_D)], x1=0, y1=0, x2=1, y2=0)
    hem = [(84, -300), (54, -290), (24, -297), (-4, -288), (-34, -296), (-62, -288), (-88, -298)]
    skirt = [(-32, WAIST), (32, WAIST)] + hem
    out.append(P(smooth(skirt, tension=0.55), sk))
    for k in range(8):
        t = (k + 0.5) / 8
        xa, xb = -30 + 60 * t, -82 + 162 * t
        out.append(L(f"M{f(xa)},{WAIST + 8} L{f(xb * 1.04)},-294", NAVY_D if k % 2 else NAVY_L, 2.4, 0.75))
    out.append(P(f"M-33,{WAIST} L33,{WAIST} L32,{WAIST + 14} L-33,{WAIST + 14} Z", NAVY_D))

    # --- upper body (bows from the waist)
    up = []
    hx, hy = 14, -742
    hair_back, face = head(hx, hy, "ponytail" if variant == 0 else "long")
    # backpack
    bp = doc.lin([(0, "#425274"), (1, "#283550")], x1=0, y1=0, x2=1, y2=0)
    up.append(P(smooth([(-40, -664), (-94, -650), (-112, -580), (-104, -510), (-80, -488), (-38, -500)], tension=0.7), bp))
    up.append(P(smooth([(-96, -600), (-60, -606), (-56, -520), (-92, -516)], tension=0.6), "#34446a"))
    up.append(L("M-92,-560 L-60,-562", "#8a9abd", 3))
    up.append(hair_back)
    # torso: fitted short-sleeve blouse
    torso = [(-30, WAIST + 4), (-34, -560), (-38, -628), (-26, -664), (2, -676), (26, -668), (40, -642), (44, -604),
             (40, -560), (34, WAIST + 4)]
    up.append(P(smooth(torso, tension=0.7), SHIRT))
    up.append(P(smooth([(-30, WAIST + 4), (-34, -560), (-38, -628), (-26, -664), (-14, -664), (-18, -600), (-14, WAIST + 4)]), SHIRT_SH, 0.8))
    up.append(L(f"M-26,{WAIST + 2} Q4,{WAIST - 14} 34,{WAIST + 2}", SHIRT_LN, 2))
    up.append(L("M24,-664 Q30,-620 26,-560", SHIRT_LN, 2, 0.7))                                        # placket
    for y in (-640, -610, -580):
        up.append(f'<circle cx="27" cy="{y}" r="3" fill="{SHIRT_LN}"/>')
    up.append(P(smooth(ellipse_pts(36, -630, 7, 9, n=10)), "#356f8e"))                                  # badge
    # strap over the shoulder
    up.append(L("M-30,-520 Q-26,-600 -6,-668", "#2a3753", 11))
    # neck + Peter-Pan collar
    up.append(P(smooth([(-4, -706), (16, -706), (20, -666), (-8, -664)]), SKIN_SH))
    up.append(P(smooth([(-14, -672), (8, -660), (6, -650), (-18, -660)]), SHIRT))
    up.append(P(smooth([(30, -674), (8, -660), (12, -648), (34, -662)]), SHIRT))
    up.append(L("M-14,-672 L8,-660 L30,-674", SHIRT_LN, 1.6))
    up.append(face)
    # history book held against the chest, near arm wrapped around it
    book_d = "M30,-640 L86,-628 L78,-536 L22,-548 Z"
    up.append(P(book_d, "#2e5c58"))
    up.append(P("M22,-548 L30,-640 L36,-638 L28,-547 Z", "#1f413e"))
    up.append(L("M44,-612 L74,-606 M44,-598 L66,-594", "#d8b56a", 2.4))
    up.append(f'<text x="52" y="-570" font-family="Hand" font-size="14" fill="#d8b56a" transform="rotate(8,52,-570)">Lịch sử</text>')
    up.append(P(smooth([(-2, -664), (24, -662), (28, -620), (2, -616)]), SHIRT))                        # sleeve
    up.append(L("M-2,-664 L2,-616 M24,-662 L28,-620", SHIRT_LN, 1.5, 0.7))
    arm = [(4, -618), (24, -620), (24, -572), (34, -560), (76, -580), (82, -566), (34, -540), (14, -546), (6, -580)]
    up.append(P(smooth(arm, tension=0.55), SKIN))
    up.append(L("M8,-600 L10,-560", SKIN_SH, 4, 0.5))
    hand = [(70, -588), (86, -592), (92, -578), (84, -566), (72, -568)]
    up.append(P(smooth(hand), SKIN))
    up.append(L("M78,-586 L88,-584 M78,-578 L90,-576", SKIN_SH, 1.4, 0.7))
    out.append(f'<g transform="rotate({bow},0,{WAIST})">{"".join(up)}</g>')
    return "".join(out)


# ------------------------------------------------------------ old flower seller
def old_woman(doc, stoop=16):
    from flora import daisy_heap
    out = []
    WAIST = -400
    tr = doc.lin([(0, "#3b3634"), (1, "#221e1d")], x1=0, y1=0, x2=1, y2=0)
    out.append(P(smooth([(-40, WAIST + 10), (40, WAIST + 10), (50, -200), (46, -30), (6, -30), (2, -200), (-4, -30), (-44, -30),
                         (-50, -200)], tension=0.5), tr))
    out.append(L("M2,-380 L4,-40", "#151211", 2, 0.6))
    for dx in (-24, 26):
        out.append(P(smooth([(dx - 14, -40), (dx + 14, -40), (dx + 16, -24), (dx - 14, -24)]), SKIN_SH))
        out.append(P(smooth([(dx - 22, -26), (dx + 30, -28), (dx + 40, -10), (dx - 22, -4)], tension=0.6), "#6b4b35"))
        out.append(L(f"M{dx - 8},-26 L{dx + 14},-34", "#4e3626", 3))

    up = []
    hx, hy = 16, -606
    _, face = head(hx, hy, "bun", old=True, sc=0.98)
    # conical hat hanging on her back
    hat = doc.lin([(0, "#efdcae"), (1, "#c9a96b")])
    up.append(P(f"M-60,-600 L-130,-430 L-10,-470 Z", hat))
    for k in range(1, 5):
        t = k / 5
        up.append(L(f"M{f(-60 - 70 * t)},{f(-600 + 170 * t)} L{f(-60 + 50 * t)},{f(-600 + 130 * t)}", "#b8955a", 1.8, 0.7))
    up.append(L("M-60,-600 Q-20,-560 4,-566", "#8a6a3c", 2))
    # áo bà ba: loose, rust with a small print
    shirt = doc.lin([(0, "#a8503a"), (1, "#7b3326")], x1=0, y1=0, x2=1, y2=1)
    body = [(-44, WAIST + 30), (-50, -470), (-44, -540), (-22, -566), (10, -570), (36, -556), (48, -500), (50, -440), (52, WAIST + 30)]
    up.append(P(smooth(body, tension=0.7), shirt))
    for k in range(46):
        x = -40 + (k * 37) % 88
        y = -556 + (k * 53) % 180
        up.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="#d58a70" opacity="0.55"/>')
    up.append(P(smooth([(-44, WAIST + 30), (-50, -470), (-44, -540), (-30, -556), (-32, -470), (-26, WAIST + 30)]), "#5f271c", 0.45))
    up.append(L("M14,-566 L18,-372", "#62291d", 2.5, 0.7))
    for y in (-540, -500, -460, -420):
        up.append(f'<circle cx="17" cy="{y}" r="4" fill="#ead9bb"/>')
    up.append(P(smooth([(-6, -566), (24, -566), (22, -540), (-4, -540)]), SKIN_SH))
    up.append(face)
    # far arm (behind) and near arm reaching to the basket
    up.append(L("M30,-540 Q40,-470 92,-436 L132,-430", "#6a2b20", 26))
    up.append(L("M2,-540 Q4,-460 60,-416 L118,-404", "#913f2e", 28))
    up.append(L("M4,-520 Q6,-462 50,-428", "#b45a42", 3, 0.6))
    out.append(f'<g transform="rotate({stoop},0,{WAIST})">{"".join(up)}</g>')
    # basket (level), held at the rim by both hands
    bk = doc.lin([(0, "#dcb26c"), (1, "#9e6e36")], x1=0, y1=0, x2=0, y2=1)
    bx, by = 210, -330
    out.append(P(smooth([(bx - 120, by - 18), (bx + 120, by - 18), (bx + 100, by + 66), (bx - 100, by + 66)], tension=0.35), bk))
    for k in range(1, 6):
        yy = by - 18 + 84 * k / 6
        out.append(L(f"M{bx - 118 + k * 4},{yy} L{bx + 118 - k * 4},{yy}", "#8a5f2e", 2.2, 0.6))
    for k in range(-6, 7):
        out.append(L(f"M{bx + k * 18},{by - 16} L{bx + k * 15},{by + 64}", "#b88545", 1.8, 0.5))
    out.append(L(f"M{bx - 120},{by - 18} L{bx + 120},{by - 18}", "#c79a55", 6))
    out.append(daisy_heap(doc, bx, by - 14, 116, 86, seed=9, size=1.1))
    for hx2, hy2 in ((bx - 112, by - 14), (bx - 92, by - 6)):
        out.append(P(smooth(ellipse_pts(hx2, hy2, 14, 11, n=10)), SKIN))
    return "".join(out)


def place(inner, x, y, s=1.0, mirror=False):
    m = -s if mirror else s
    return f'<g transform="translate({f(x)},{f(y)}) scale({f(m)},{f(s)})">{inner}</g>'
