"""Stylised flat-vector figures: two schoolgirls bowing, an old flower seller.

Each figure is drawn in local coordinates (feet at 0,0, up is negative y, facing right),
then placed with translate/scale (and mirrored for the old woman).
"""
from scene import L, P
from svg_kit import ellipse_pts, f, smooth

SKIN, SKIN_SH = "#f2d5c2", "#e2b9a2"
HAIR, HAIR_HL = "#1d1918", "#4c413c"
SHIRT, SHIRT_SH = "#fbfaf5", "#dcd7cc"
NAVY, NAVY_L, NAVY_D = "#2c3a58", "#43567d", "#1f2a42"


def _face(eye_x, eye_y, mouth_x, mouth_y, blush=True, lip="#c96a64", smile=0.0):
    out = [L(f"M{eye_x - 13},{eye_y - 2} Q{eye_x},{eye_y + 8} {eye_x + 12},{eye_y - 1}", "#3a2a26", 3.2),
           L(f"M{eye_x - 15},{eye_y - 3} L{eye_x - 21},{eye_y + 1}", "#3a2a26", 2.4),
           L(f"M{eye_x - 12},{eye_y - 22} Q{eye_x + 2},{eye_y - 28} {eye_x + 16},{eye_y - 21}", "#4a3a34", 3)]
    out.append(L(f"M{mouth_x - 9},{mouth_y} Q{mouth_x - 2},{mouth_y + 5 + smile} {mouth_x + 5},{mouth_y - 1}", lip, 4))
    if blush:
        out.append(P(smooth(ellipse_pts(eye_x - 6, eye_y + 26, 17, 9, n=12)), "#f0a39a", 0.45))
    return "".join(out)


def _head_profile(cx, cy):
    """Head facing right: skull ellipse + soft nose/chin profile."""
    prof = [(cx - 52, cy - 10), (cx - 44, cy - 52), (cx - 6, cy - 68), (cx + 36, cy - 56), (cx + 54, cy - 26),
            (cx + 58, cy - 4), (cx + 68, cy + 12), (cx + 58, cy + 18), (cx + 60, cy + 30), (cx + 54, cy + 38),
            (cx + 52, cy + 48), (cx + 30, cy + 64), (cx, cy + 62), (cx - 34, cy + 40)]
    return P(smooth(prof), SKIN)


def schoolgirl(doc, variant=0, bow=20):
    out = []
    # legs, socks, shoes
    for dx, col in ((-24, SKIN_SH), (8, SKIN)):
        out.append(P(smooth([(dx - 16, -260), (dx + 16, -260), (dx + 12, -120), (dx + 10, -30), (dx - 8, -30), (dx - 12, -120)]), col))
        out.append(P(smooth([(dx - 12, -112), (dx + 12, -112), (dx + 11, -26), (dx - 9, -26)]), "#f7f5ee"))
        out.append(L(f"M{dx - 12},{-104} L{dx + 12},{-104}", "#d9d4c8", 3))
        out.append(P(smooth([(dx - 14, -30), (dx + 16, -34), (dx + 40, -18), (dx + 40, -4), (dx - 14, -2)]), "#2a2522"))
        out.append(L(f"M{dx - 6},{-22} L{dx + 26},{-22}", "#4b443f", 2.5))
    # pleated skirt
    sk = doc.lin([(0, NAVY_L), (1, NAVY)], x1=0, y1=0, x2=1, y2=0)
    hem = [(-120, -238), (-80, -226), (-40, -232), (0, -224), (40, -232), (80, -224), (116, -236)]
    skirt = [(-58, -452), (56, -452)] + hem[::-1]
    out.append(P(smooth(skirt, tension=0.6), sk))
    for k in range(7):
        t = (k + 0.5) / 7
        xa, xb = -54 + 108 * t, -116 + 230 * t
        out.append(L(f"M{f(xa)},-446 L{f(xb)},-232", NAVY_D if k % 2 else NAVY_L, 3, 0.7))
    out.append(P(f"M-58,-452 L56,-452 L54,-436 L-56,-436 Z", NAVY_D))

    # upper body, bowing from the waist
    up = []
    # backpack
    bp = doc.lin([(0, "#3a4a66"), (1, "#26324a")], x1=0, y1=0, x2=1, y2=0)
    up.append(P(smooth([(-132, -630), (-60, -650), (-44, -600), (-46, -470), (-70, -440), (-130, -446), (-142, -540)]), bp))
    up.append(P(smooth([(-128, -560), (-78, -566), (-74, -470), (-124, -466)]), "#33425e"))
    up.append(L("M-122,-590 Q-96,-600 -66,-594", "#8494b4", 4, 0.8))
    # shirt torso
    torso = [(-58, -450), (-64, -540), (-54, -622), (-18, -648), (22, -650), (54, -628), (72, -570), (64, -510), (58, -450)]
    up.append(P(smooth(torso), SHIRT))
    up.append(P(smooth([(-58, -450), (-64, -540), (-54, -622), (-36, -636), (-38, -540), (-32, -452)]), SHIRT_SH, 0.8))
    up.append(L("M-30,-470 Q10,-500 50,-470", SHIRT_SH, 3, 0.7))
    # strap
    up.append(L("M-44,-470 Q-40,-560 -20,-640", "#26324a", 14))
    # school badge
    up.append(P(smooth(ellipse_pts(40, -586, 10, 12, n=10)), "#2f6a8a"))
    # neck + collar
    up.append(P(smooth([(-14, -680), (16, -680), (18, -640), (-12, -640)]), SKIN_SH))
    up.append(P("M-18,-650 L4,-632 L-4,-622 Z", SHIRT))
    up.append(P("M26,-652 L6,-632 L18,-622 Z", SHIRT))
    up.append(L("M-18,-650 L4,-632 L-4,-622 M26,-652 L6,-632 L18,-622", "#cfc9bc", 2))
    # head
    hx, hy = 8, -728
    up.append(_head_profile(hx, hy))
    up.append(P(smooth(ellipse_pts(hx - 14, hy + 4, 10, 14, n=10)), SKIN_SH))           # ear
    up.append(_face(hx + 30, hy - 2, hx + 50, hy + 36))
    # hair
    if variant == 0:
        hair = [(hx + 52, hy - 30), (hx + 30, hy - 62), (hx - 14, hy - 72), (hx - 56, hy - 48), (hx - 70, hy),
                (hx - 74, hy + 80), (hx - 84, hy + 170), (hx - 70, hy + 230), (hx - 56, hy + 180), (hx - 50, hy + 90),
                (hx - 30, hy + 30), (hx - 20, hy - 20), (hx + 10, hy - 40), (hx + 40, hy - 30)]
    else:
        hair = [(hx + 52, hy - 30), (hx + 28, hy - 64), (hx - 16, hy - 72), (hx - 58, hy - 46), (hx - 74, hy + 4),
                (hx - 86, hy + 90), (hx - 96, hy + 200), (hx - 76, hy + 270), (hx - 58, hy + 200), (hx - 44, hy + 100),
                (hx - 28, hy + 30), (hx - 18, hy - 20), (hx + 12, hy - 42), (hx + 42, hy - 28)]
    up.append(P(smooth(hair), HAIR))
    for k in range(3):
        up.append(L(smooth([(hx - 30 + k * 18, hy - 60 + k * 4), (hx - 50 + k * 10, hy - 20), (hx - 60 + k * 8, hy + 60 + k * 30)],
                           closed=False), HAIR_HL, 3, 0.7))
    up.append(L(f"M{hx + 40},{hy - 34} Q{hx + 52},{hy - 22} {hx + 50},{hy - 6}", HAIR, 8))       # fringe
    if variant == 0:                                                                           # ribbon bow
        bx, by = hx - 50, hy - 38
        up.append(P(f"M{bx},{by} L{bx - 34},{by - 22} L{bx - 30},{by + 18} Z", "#fbfaf5"))
        up.append(P(f"M{bx},{by} L{bx + 26},{by - 26} L{bx + 30},{by + 10} Z", "#fbfaf5"))
        up.append(L(f"M{bx},{by} L{bx - 12},{by + 40} M{bx},{by} L{bx + 8},{by + 44}", "#f1eee6", 6))
        up.append(L(f"M{bx - 34},{by - 22} L{bx - 30},{by + 18} M{bx + 26},{by - 26} L{bx + 30},{by + 10}", "#d9d4c8", 2))
    else:                                                                                      # hair clip
        up.append(P(smooth(ellipse_pts(hx - 40, hy - 52, 16, 6, n=10, rot=-0.5)), "#c9a24e"))
    # book held to the chest + near arm
    up.append(P(f"M26,-628 L104,-612 L96,-494 L18,-510 Z", "#2f5d5a"))
    up.append(P(f"M26,-628 L34,-626 L26,-508 L18,-510 Z", "#21433f"))
    up.append(L("M44,-598 L88,-590 M44,-584 L80,-578", "#d8b56a", 3))
    up.append(P(smooth([(10, -630), (34, -626), (40, -580), (12, -576)]), SHIRT))           # sleeve
    up.append(P(smooth([(14, -584), (36, -584), (34, -540), (40, -530), (84, -566), (96, -548), (46, -508), (24, -510),
                        (14, -540)], tension=0.5), SKIN))
    up.append(L("M18,-560 L20,-524", SKIN_SH, 5, 0.6))
    up.append(P(smooth(ellipse_pts(88, -556, 16, 12, n=10, rot=-0.6)), SKIN))
    out.append(f'<g transform="rotate({bow},0,-452)">{"".join(up)}</g>')
    return "".join(out)


def old_woman(doc, stoop=12):
    """Flower seller in a rust áo bà ba, grey bun, holding a basket of daisies (facing right)."""
    from flora import daisy_heap
    out = []
    # wide black trousers + sandals
    tr = doc.lin([(0, "#3a3533"), (1, "#24201f")], x1=0, y1=0, x2=1, y2=0)
    out.append(P(smooth([(-54, -340), (52, -340), (64, -120), (58, -24), (8, -24), (2, -180), (-4, -24), (-58, -24), (-64, -120)], tension=0.5), tr))
    for dx in (-30, 34):
        out.append(P(smooth([(dx - 30, -26), (dx + 34, -28), (dx + 44, -10), (dx - 30, -6)]), "#6b4b35"))
        out.append(P(smooth([(dx - 18, -40), (dx + 18, -40), (dx + 20, -24), (dx - 18, -24)]), SKIN_SH))
    up = []
    shirt = doc.lin([(0, "#a54a35"), (1, "#7d3426")], x1=0, y1=0, x2=1, y2=1)
    body = [(-64, -330), (-70, -440), (-62, -540), (-20, -572), (24, -574), (60, -548), (72, -470), (70, -330), (60, -300),
            (-58, -300)]
    up.append(P(smooth(body, tension=0.7), shirt))
    for k in range(40):                                                       # printed dots
        x = -56 + (k * 37) % 120
        y = -560 + (k * 53) % 250
        up.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#d3826a" opacity="0.6"/>')
    up.append(P(smooth([(-64, -330), (-70, -440), (-62, -540), (-40, -556), (-44, -440), (-38, -304)]), "#6a2c20", 0.5))
    up.append(L("M8,-570 L14,-300", "#6a2c20", 3, 0.6))
    for y in (-520, -470, -420, -370):
        up.append(f'<circle cx="16" cy="{y}" r="5" fill="#e8d6b8"/>')
    # neck + head (older, gentle smile)
    hx, hy = 6, -634
    up.append(P(smooth([(-12, -592), (18, -592), (18, -560), (-12, -560)]), SKIN_SH))
    up.append(_head_profile(hx, hy))
    up.append(_face(hx + 30, hy - 2, hx + 48, hy + 34, smile=3, lip="#b6655c"))
    up.append(L(f"M{hx + 22},{hy + 12} Q{hx + 30},{hy + 18} {hx + 40},{hy + 14}", "#c99a86", 2, 0.8))   # cheek line
    up.append(L(f"M{hx + 10},{hy - 34} Q{hx + 26},{hy - 38} {hx + 40},{hy - 32}", "#c99a86", 2, 0.7))   # brow crease
    hair = [(hx + 50, hy - 28), (hx + 26, hy - 64), (hx - 18, hy - 72), (hx - 56, hy - 46), (hx - 62, hy - 4),
            (hx - 40, hy + 8), (hx - 20, hy - 24), (hx + 10, hy - 40), (hx + 40, hy - 26)]
    up.append(P(smooth(hair), "#bdb7ae"))
    up.append(P(smooth(ellipse_pts(hx - 66, hy - 24, 30, 26, n=14)), "#a9a299"))               # bun
    for k in range(4):
        up.append(L(smooth([(hx + 30 - k * 20, hy - 56 + k * 4), (hx - 10 - k * 12, hy - 50), (hx - 46, hy - 26 + k * 6)],
                           closed=False), "#e3ded6", 2.4, 0.8))
    # arms reaching to the basket
    up.append(L("M24,-530 Q20,-460 58,-424 Q96,-412 120,-424", "#7f3527", 30))
    up.append(L("M24,-530 Q20,-460 58,-424", "#b0563f", 4, 0.6))
    up.append(P(smooth(ellipse_pts(126, -424, 18, 14, n=10)), SKIN))
    out.append(f'<g transform="rotate({stoop},0,-320)">{"".join(up)}</g>')
    # basket held in front (not rotated, so it sits level)
    bk = doc.lin([(0, "#dcb26c"), (1, "#9e6e36")], x1=0, y1=0, x2=0, y2=1)
    bx, by = 190, -360
    out.append(P(smooth([(bx - 130, by - 20), (bx + 130, by - 20), (bx + 110, by + 70), (bx - 110, by + 70)], tension=0.4), bk))
    for k in range(1, 6):
        yy = by - 20 + 90 * k / 6
        out.append(L(f"M{bx - 128 + k * 4},{yy} L{bx + 128 - k * 4},{yy}", "#8a5f2e", 2.5, 0.6))
    for k in range(-6, 7):
        out.append(L(f"M{bx + k * 20},{by - 18} L{bx + k * 17},{by + 68}", "#b88545", 2, 0.5))
    out.append(daisy_heap(doc, bx, by - 14, 128, 92, seed=9, size=1.15))
    out.append(P(smooth(ellipse_pts(bx - 120, by - 16, 22, 16, n=10)), SKIN))                  # hand on rim
    return "".join(out)


def place(inner, x, y, s=1.0, mirror=False):
    m = -s if mirror else s
    return f'<g transform="translate({f(x)},{f(y)}) scale({f(m)},{f(s)})">{inner}</g>'
