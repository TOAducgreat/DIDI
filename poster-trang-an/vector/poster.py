"""Poster vector 01 — "Một sớm bên Hồ Gươm" (Thanh lịch người Tràng An – Tiếp nối nếp Tràng An)."""
import math
import random

from PIL import ImageFont

import figures
import flora
import scene
from scene import L, P
from svg_kit import ROOT, H, W, Doc, ellipse_pts, f, font_css, paper_grain_overlay, paper_texture, render, smooth

HT, HB = 1060, 2300                # hero band
HORIZON = 1700
EDGE = 2050                        # lake edge / embankment
GROUND = 2220                      # where the figures stand
SON, SON_D = "#9c2e22", "#7a2219"
MOSS = "#24402f"
INK = "#3b332d"
INK2 = "#6b6058"

FONTS = ROOT / "fonts"


# ---------------------------------------------------------------- text helpers
def wrap(text, font_file, size, maxw):
    fnt = ImageFont.truetype(str(FONTS / font_file), size)
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if fnt.getlength(t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def para(doc, x, y, text, font_file, family, size, lh, maxw, fill, anchor="start", weight=400, style="normal"):
    for line in wrap(text, font_file, size, maxw):
        doc.text(x, y, line, size, family, fill, anchor=anchor, weight=weight, style=style)
        y += lh
    return y


def rule(doc, x0, x1, y, col=SON, w=2, op=0.8):
    doc.add(L(f"M{f(x0)},{f(y)} L{f(x1)},{f(y)}", col, w, op))


# ---------------------------------------------------------------- ornaments
def torn_paper(doc, x, y, w, h, rot=0, seed=1, col="#f7f0de", tape=True):
    rnd = random.Random(seed)
    pts = []
    for k in range(18):
        pts.append((x + w * k / 17, y + rnd.uniform(-6, 6)))
    for k in range(1, 12):
        pts.append((x + w + rnd.uniform(-6, 6), y + h * k / 11))
    for k in range(17, -1, -1):
        pts.append((x + w * k / 17, y + h + rnd.uniform(-10, 10)))
    for k in range(10, 0, -1):
        pts.append((x + rnd.uniform(-6, 6), y + h * k / 11))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + " Z"
    cx, cy = x + w / 2, y + h / 2
    sh = doc.blur(8)
    out = [f'<path d="{d}" fill="#5a4630" opacity="0.18" filter="{sh}" transform="translate(6,10)"/>',
           f'<path d="{d}" fill="{col}"/>',
           f'<path d="{d}" fill="none" stroke="#d8cbb0" stroke-width="2"/>']
    if tape:
        out.append(f'<rect x="{f(cx - 70)}" y="{f(y - 22)}" width="140" height="44" fill="#e9dfc4" opacity="0.75" '
                   f'transform="rotate({rnd.uniform(-6, 6):.1f},{f(cx)},{f(y)})"/>')
    return f'<g transform="rotate({rot},{f(cx)},{f(cy)})">{"".join(out)}</g>'


def note(doc, x, y, w, h, lines, rot, seed, size=62):
    doc.add(torn_paper(doc, x, y, w, h, rot=rot, seed=seed))
    cx, cy = x + w / 2, y + h / 2
    body = []
    ty = y + (h - (len(lines) - 1) * size * 1.12) / 2 + size * 0.35
    for ln in lines:
        body.append(f'<text x="{f(cx)}" y="{f(ty)}" font-family="Hand" font-weight="600" font-size="{size}" fill="{SON_D}" '
                    f'text-anchor="middle">{ln}</text>')
        ty += size * 1.12
    body.append(L(f"M{f(cx - w * 0.28)},{f(ty - size * 0.6)} Q{f(cx)},{f(ty - size * 0.3)} {f(cx + w * 0.28)},{f(ty - size * 0.7)}",
                  SON_D, 3, 0.7))
    doc.add(f'<g transform="rotate({rot},{f(cx)},{f(cy)})">{"".join(body)}</g>')


def lotus_mark(doc, cx, cy, s=1.0, col=SON):
    out = []
    for deg, ln in ((-60, 0.7), (60, 0.7), (-28, 0.9), (28, 0.9), (0, 1.0)):
        a = math.radians(-90 + deg)
        ca, sa = math.cos(a), math.sin(a)
        pts = [(cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)
               for u, v in ((0, 0), (14 * ln, 9), (34 * ln, 6), (42 * ln, 0), (34 * ln, -6), (14 * ln, -9))]
        out.append(L(smooth(pts), col, 2.2))
    out.append(L(f"M{f(cx - 44 * s)},{f(cy + 4 * s)} Q{f(cx)},{f(cy + 16 * s)} {f(cx + 44 * s)},{f(cy + 4 * s)}", col, 2.2))
    doc.add("".join(out))


# ---------------------------------------------------------------- icons for the four values
def icon_ao_dai(doc, cx, cy, s=1.0):
    g = doc.lin([(0, "#fbf8f0"), (1, "#e2dccd")])
    body = [(cx - 26 * s, cy - 70 * s), (cx + 26 * s, cy - 70 * s), (cx + 40 * s, cy - 40 * s), (cx + 30 * s, cy),
            (cx + 52 * s, cy + 80 * s), (cx - 52 * s, cy + 80 * s), (cx - 30 * s, cy), (cx - 40 * s, cy - 40 * s)]
    out = [P(smooth(body, tension=0.5), g), P(smooth(body, tension=0.5), "none", extra=f'stroke="{SON}" stroke-width="2.5"')]
    out.append(L(f"M{f(cx - 46 * s)},{f(cy - 52 * s)} L{f(cx - 70 * s)},{f(cy + 10 * s)} M{f(cx + 46 * s)},{f(cy - 52 * s)} L{f(cx + 70 * s)},{f(cy + 10 * s)}",
                 SON, 2.5))
    out.append(L(f"M{f(cx - 12 * s)},{f(cy - 70 * s)} L{f(cx - 12 * s)},{f(cy - 84 * s)} L{f(cx + 12 * s)},{f(cy - 84 * s)} L{f(cx + 12 * s)},{f(cy - 70 * s)}", SON, 2.5))
    out.append(L(f"M{f(cx)},{f(cy - 60 * s)} L{f(cx + 18 * s)},{f(cy + 76 * s)}", "#c9bfae", 2))
    doc.add("".join(out))


def icon_daisy(doc, cx, cy, s=1.0):
    doc.add(L(f"M{f(cx)},{f(cy + 10 * s)} Q{f(cx - 10 * s)},{f(cy + 50 * s)} {f(cx - 4 * s)},{f(cy + 86 * s)}", "#6f8e55", 4))
    doc.add(flora.leaf(doc, cx - 6 * s, cy + 52 * s, 44 * s, 10 * s, math.radians(-150), vein=False))
    doc.add(flora.daisy(cx, cy - 10 * s, 52 * s))
    doc.add(flora.daisy(cx + 50 * s, cy + 30 * s, 30 * s, tilt=0.8))


def icon_khue_van_cac(doc, cx, cy, s=1.0):
    red = doc.lin([(0, "#c4553c"), (1, "#963726")])
    out = [P(f"M{f(cx - 70 * s)},{f(cy - 40 * s)} L{f(cx + 70 * s)},{f(cy - 40 * s)} L{f(cx + 70 * s)},{f(cy + 30 * s)} L{f(cx - 70 * s)},{f(cy + 30 * s)} Z", red)]
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy - 5 * s)}" r="{f(26 * s)}" fill="#f4e7cc"/>')
    for k in range(12):
        a = math.pi * 2 * k / 12
        out.append(L(f"M{f(cx)},{f(cy - 5 * s)} L{f(cx + math.cos(a) * 24 * s)},{f(cy - 5 * s + math.sin(a) * 24 * s)}", "#963726", 2))
    for rx, ry, top in ((96, 18, -40), (84, 14, -80)):
        out.append(P(smooth([(cx - rx * s, cy + (top + 2) * s), (cx - (rx - 20) * s, cy + (top - ry) * s), (cx, cy + (top - ry - 8) * s),
                             (cx + (rx - 20) * s, cy + (top - ry) * s), (cx + rx * s, cy + (top + 2) * s), (cx + rx * s - 10, cy + (top + 8) * s),
                             (cx - rx * s + 10, cy + (top + 8) * s)], tension=0.6), "#8f3324"))
    out.append(P(f"M{f(cx - 44 * s)},{f(cy - 80 * s)} L{f(cx + 44 * s)},{f(cy - 80 * s)} L{f(cx + 44 * s)},{f(cy - 52 * s)} L{f(cx - 44 * s)},{f(cy - 52 * s)} Z", red))
    for x in (-60, -20, 20, 60):
        out.append(P(f"M{f(cx + (x - 9) * s)},{f(cy + 30 * s)} L{f(cx + (x + 9) * s)},{f(cy + 30 * s)} L{f(cx + (x + 9) * s)},{f(cy + 86 * s)} L{f(cx + (x - 9) * s)},{f(cy + 86 * s)} Z", "#e8dcc4"))
    doc.add("".join(out))


def icon_tea(doc, cx, cy, s=1.0):
    g = doc.lin([(0, "#fbf8f0"), (1, "#d9d3c4")], x1=0, y1=0, x2=1, y2=0)
    out = [P(f"M{f(cx - 64 * s)},{f(cy)} Q{f(cx - 60 * s)},{f(cy + 70 * s)} {f(cx)},{f(cy + 74 * s)} Q{f(cx + 60 * s)},{f(cy + 70 * s)} {f(cx + 64 * s)},{f(cy)} Z", g)]
    out.append(P(smooth(ellipse_pts(cx, cy, 64 * s, 14 * s, n=16)), "#b98a3c"))
    out.append(L(f"M{f(cx - 40 * s)},{f(cy + 36 * s)} Q{f(cx - 20 * s)},{f(cy + 26 * s)} {f(cx)},{f(cy + 36 * s)} Q{f(cx + 20 * s)},{f(cy + 46 * s)} {f(cx + 40 * s)},{f(cy + 36 * s)}", "#3f6ea0", 3))
    out.append(P(smooth(ellipse_pts(cx, cy + 82 * s, 84 * s, 12 * s, n=16)), "#e4ddcd"))
    for k in (-24, 0, 24):
        out.append(L(f"M{f(cx + k * s)},{f(cy - 14 * s)} q{f(-14 * s)},{f(-24 * s)} 0,{f(-46 * s)} q{f(14 * s)},{f(-22 * s)} 0,{f(-44 * s)}", "#b9b0a2", 3, 0.7))
    out.append(flora.lotus_flower(doc, cx + 92 * s, cy + 70 * s, 0.32 * s))
    doc.add("".join(out))


# ---------------------------------------------------------------- hero
def hero(doc):
    rnd = random.Random(1010)
    out = []
    out.append(scene.sky(doc, 0, HT - 120, W, HB, HORIZON, (1880, 1330, 70)))
    out.append(scene.cloud_swirl(1180, 1170, 1.3, op=0.45))
    out.append(scene.cloud_swirl(2200, 1240, 1.0, op=0.4, flip=True))
    out.append(scene.far_city(doc, 1250, W, HORIZON - 60, rnd))
    far_pal = [("#d3dcc2", "#b9c9a9", "#9fb492"), ("#cdd8bc", "#b0c3a0", "#97ae8b")]
    near_pal = [("#b7cc8f", "#86a96a", "#5a8452"), ("#a9c486", "#78a065", "#4f7a4c"), ("#c1d197", "#93b173", "#668e58")]
    out.append(scene.tree_band(doc, 1180, W + 100, HORIZON - 10, rnd, far_pal, 230, op=0.9, step=150))
    tower = scene.thap_rua(doc, 1980, HORIZON + 6, 0.62)
    out.append(scene.lake(doc, 0, W, HORIZON, EDGE, rnd))
    out.append(scene.reflection(tower, HORIZON + 10, op=0.2))
    out.append(scene.tree_band(doc, 1120, W + 100, HORIZON + 8, rnd, near_pal, 150, op=1, step=200))
    out.append(tower)
    out.append(scene.embankment(doc, 0, W, EDGE, HB - EDGE + 40))
    out.append(scene.old_house(doc, -20, 640, 1130, EDGE + 40, rnd))
    out.append(scene.bicycle(doc, 470, GROUND - 20, 0.95,
                             lambda d, cx, top, w, h: flora.daisy_heap(d, cx, top, w, h, seed=4, size=0.85)))
    # soft cast shadows on the pavement
    sh = doc.blur(10)
    for x, w in ((1000, 150), (1250, 150), (1650, 230)):
        out.append(f'<ellipse cx="{x}" cy="{GROUND + 4}" rx="{w}" ry="18" fill="#6d5b44" opacity="0.18" filter="{sh}"/>')
    # the story: two students bow to the flower seller
    out.append(figures.place(figures.schoolgirl(doc, 0, bow=30), 1000, GROUND, 1.0))
    out.append(figures.place(figures.schoolgirl(doc, 1, bow=25), 1260, GROUND + 6, 1.0))
    out.append(figures.place(figures.old_woman(doc), 1760, GROUND + 2, 0.94, mirror=True))
    # hoa sữa canopy over the top-left of the scene
    out.append(flora.hoa_sua_branch(doc, -60, HT + 40, 900, 0.18, seed=5, scale=1.0, droop=0.25))
    out.append(flora.hoa_sua_branch(doc, -40, HT + 260, 620, 0.05, seed=8, scale=0.85, droop=0.4))
    return "".join(out)


def hero_mask(doc):
    rnd = random.Random(7)
    top = HT - 110
    pts = [(0, top), (W, top)]
    for k in range(60, -1, -1):
        pts.append((W * k / 60, HB + rnd.uniform(-16, 16)))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in pts) + " Z"
    g = doc.lin([(0, "#000"), (0.14, "#fff"), (1, "#fff")])
    return doc.mask(f'<path d="{d}" fill="{g}"/>')


# ---------------------------------------------------------------- page
def build():
    doc = Doc()
    paper_texture(doc)
    cx = W / 2

    # corner flowers at the very top
    doc.add(flora.hoa_sua_branch(doc, W + 60, -60, 520, math.pi - 0.62, seed=11, scale=0.9, droop=-0.25))
    doc.add(flora.hoa_sua_branch(doc, -80, -30, 560, 0.5, seed=12, scale=0.8, droop=0.3))

    # header
    doc.text(cx, 200, "HÀ NỘI XƯA VÀ NAY", 34, "BeVN", SON, weight=500, ls=14)
    rule(doc, cx - 640, cx - 330, 190)
    rule(doc, cx + 330, cx + 640, 190)
    tg = doc.lin([(0, "#b23a2a"), (1, "#7e2419")])
    doc.text(cx, 470, "THANH LỊCH", 250, "PlayfairSC", tg, weight=900, ls=4)
    doc.text(cx, 690, "NGƯỜI TRÀNG AN", 200, "PlayfairSC", MOSS, weight=900, ls=2)
    doc.text(cx, 800, "TIẾP NỐI NẾP TRÀNG AN", 46, "BeVN", SON, weight=500, ls=16)
    rule(doc, cx - 1000, cx - 560, 786)
    rule(doc, cx + 560, cx + 1000, 786)
    lotus_mark(doc, cx, 852, 0.9)
    doc.text(cx, 925, "Nghìn năm văn hiến hun đúc nên nét thanh lịch – tuổi trẻ hôm nay tiếp nối", 42, "Playfair", INK, style="italic")
    doc.text(cx, 980, "bằng lời hay, ý đẹp và những việc làm tử tế.", 42, "Playfair", INK, style="italic")

    # hero illustration
    doc.add(f'<g mask="{hero_mask(doc)}">{hero(doc)}</g>')

    # handwritten notes on torn paper
    note(doc, 90, 1120, 460, 280, ["Hiểu lịch sử", "để thêm yêu", "Hà Nội."], -7, seed=3, size=58)
    note(doc, 2010, 1960, 400, 260, ["Hà Nội hôm nay", "vẫn đẹp,", "vẫn văn hóa."], 6, seed=4, size=50)

    # story strip
    sy = 2400
    doc.text(cx, sy, "MỘT SỚM BÊN HỒ GƯƠM", 40, "BeVN", MOSS, weight=500, ls=12)
    rule(doc, 170, cx - 420, sy - 12, MOSS, 2, 0.5)
    rule(doc, cx + 420, W - 170, sy - 12, MOSS, 2, 0.5)
    story = [
        ("01", "Sáng sớm", "Trên đường đến trường, hai cô nữ sinh đi dọc bờ Hồ Gươm. Mặt hồ còn phảng phất sương, Tháp Rùa ửng nắng mai."),
        ("02", "Lời chào", "Gặp bà cụ bán hoa, hai em dừng lại, khoanh tay cúi đầu: “Chúng cháu chào bà ạ!”. Lời chào nhỏ mà ấm cả góc phố."),
        ("03", "Bó hoa", "Hai em đón bó cúc họa mi bằng cả hai tay, nói lời cảm ơn, rồi mang mùa thu Hà Nội vào lớp học."),
    ]
    colw = (W - 340 - 2 * 90) / 3
    for i, (no, head, body) in enumerate(story):
        x = 170 + i * (colw + 90)
        doc.text(x, sy + 120, no, 96, "Hand", SON, anchor="start", weight=700)
        doc.text(x + 160, sy + 104, head, 50, "Playfair", MOSS, anchor="start", style="italic", weight=600)
        para(doc, x, sy + 180, body, "BeVietnamPro-Light.ttf", "BeVN", 30, 46, colw, INK, weight=300)
        if i:
            doc.add(L(f"M{f(x - 45)},{sy + 60} L{f(x - 45)},{sy + 360}", "#c9bba0", 2))

    # four values
    vy = 2860
    doc.add(f'<rect x="150" y="{vy - 70}" width="{W - 300}" height="420" rx="18" fill="#f6eedb" opacity="0.65"/>')
    doc.text(cx, vy - 16, "NẾP TRÀNG AN HÔM NAY", 36, "BeVN", SON, weight=500, ls=12)
    vals = [
        (icon_ao_dai, "Ăn mặc chỉn chu", "Gọn gàng, giản dị, hợp hoàn cảnh – tôn trọng mình và người đối diện."),
        (icon_daisy, "Lời nói nhẹ nhàng", "Biết chào hỏi, cảm ơn, xin lỗi; nói khẽ nơi công cộng."),
        (icon_khue_van_cac, "Kính trên nhường dưới", "Lễ phép với người lớn tuổi, nhường nhịn bạn bè, giữ gìn nếp nhà."),
        (icon_tea, "Yêu cái đẹp nhỏ bé", "Một bó hoa, một chén trà, một góc phố sạch – đẹp từ điều giản dị."),
    ]
    cw = (W - 300) / 4
    for i, (icon, head, body) in enumerate(vals):
        x = 150 + i * cw + cw / 2
        icon(doc, x, vy + 90, 0.85)
        doc.text(x, vy + 230, head, 40, "Playfair", SON_D, style="italic", weight=600)
        para(doc, x, vy + 280, body, "BeVietnamPro-Light.ttf", "BeVN", 27, 38, cw - 80, INK, anchor="middle", weight=300)

    # ca dao + credits
    doc.text(cx, 3300, "“Chẳng thơm cũng thể hoa nhài, dẫu không thanh lịch cũng người Tràng An.”", 42, "Playfair", MOSS, style="italic")
    lotus_mark(doc, cx, 3342, 0.6, SON)
    doc.text(cx, 3404, "Đặng Vũ Hà Châu  ·  Nguyễn Thụy Anh", 38, "Playfair", INK, weight=600)
    doc.text(cx, 3450, "Lớp 10 Chuyên Sử 1  ·  Trường THPT chuyên Hà Nội – Amsterdam", 28, "BeVN", INK2, weight=400, ls=2)

    paper_grain_overlay(doc)
    return doc


if __name__ == "__main__":
    render(build().svg(font_css()), "vector-01-mot-som-ben-ho-guom")
