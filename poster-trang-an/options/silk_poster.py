"""Bộ poster "Nét thanh lịch người Tràng An" — tranh lụa không khung trên nền gradient.

Mỗi bản là một `spec`; `render(spec)` dựng nền, ghép tranh, dàn chữ và xuất ra final/.
    python3 silk_poster.py            # dựng mọi bản đã có tranh
    python3 silk_poster.py 0 C        # chỉ dựng bản 0 và C
"""
import sys

from PIL import Image, ImageDraw

from brush import wash
from common import (CA_DAO, CLASS, NAMES, SCHOOL, SUB, TITLE, M, W, OUT_DIR,
                    Typesetter, font, p, paper, save, seal, seed)
from paint import ASSETS, lay, load, silk_tone, soft_mask

FINAL = OUT_DIR.parent / "final"
IVORY = (244, 238, 228)
INK, INK2, INK3 = (30, 28, 26), (98, 90, 84), (162, 150, 142)
SON = (166, 50, 38)

SPECS = {
    "0": dict(name="0-mac-nguyet", art="dan-tranh.png", crop=(0, 0.28, 1, 1), tone=(0.09, 0.05, 0.54, 0.25),
              bottom=(241, 222, 218), glow=(250, 245, 238), layout="image-top", width=1640,
              head=("Nº 01", "TRÀNG AN  ·  1010", "21°01'N  105°51'E"),
              side=("THĂNG LONG  ·  ĐÔNG ĐÔ  ·  HÀ NỘI", "TIẾNG ĐÀN  ·  HOA SEN  ·  VẦNG NGUYỆT"),
              mask=dict(inset=0.05, blur=0.09, roughness=0.7, fade_top=0.12, fade_bottom=0.2, fade_x=0.1, seed=3)),
    "A": dict(name="A-ho-guom", art="ho-guom.png", crop=(0, 0.24, 1, 0.99), tone=(0.1, 0.03, 0.9, 0.2),
              bottom=(222, 228, 234), glow=(246, 246, 244), layout="title-top", width=2140, top=1290,
              head=("Nº 02", "HỒ HOÀN KIẾM  ·  RẰM THÁNG TÁM", ""),
              mask=dict(inset=0.03, blur=0.08, roughness=0.7, fade_top=0.2, fade_bottom=0.14, fade_x=0.12, seed=5)),
    "B": dict(name="B-pho-co", art="ban-cong.png", crop=(0, 0.27, 1, 0.99), tone=(0.1, 0.03, 0.9, 0.22),
              bottom=(240, 224, 210), glow=(250, 244, 236), layout="image-top", width=2060, top=400, title_y=2220,
              head=("Nº 03", "BA SÁU PHỐ PHƯỜNG", "HÀ NỘI"),
              side=("PHỐ CỔ  ·  MÁI NGÓI  ·  HOA GIẤY", "THĂNG LONG  ·  KẺ CHỢ  ·  HÀ NỘI"),
              mask=dict(inset=0.03, blur=0.08, roughness=0.7, fade_top=0.14, fade_bottom=0.18, fade_x=0.1, seed=8)),
    "C": dict(name="C-xe-hoa", art="xe-hoa.png", crop=(0.075, 0.351, 0.927, 0.974), tone=(0.18, 0.05, 0.8, 0.25),
              bottom=(242, 230, 204), glow=(250, 244, 234), layout="title-top", width=1480,
              head=("Nº 04", "PHỐ CỔ  ·  HÀ NỘI", ""),
              mask=dict(inset=0.04, blur=0.09, roughness=0.7, fade_top=0.18, fade_bottom=0.12, fade_x=0.12, seed=11)),
    "D": dict(name="D-tra-sen", art="tra-sen.png", crop=(0, 0.16, 1, 0.98), tone=(0.55, 0.03, 0.95, 0.25),
              bottom=(224, 233, 224), glow=(248, 247, 240), layout="image-top", width=1600,
              head=("Nº 05", "TRÀ SEN  ·  TÂY HỒ", "HÀ NỘI"),
              side=("ƯỚP TRÀ  ·  SEN BÁCH DIỆP  ·  HỒ TÂY", "THƯỞNG TRÀ  ·  NẾP NHÀ  ·  HÀ NỘI"),
              mask=dict(inset=0.05, blur=0.09, roughness=0.7, fade_top=0.14, fade_bottom=0.2, fade_x=0.1, seed=4)),
}


def frac_box(im, f):
    return tuple(int(v * s) for v, s in zip(f, (im.width, im.height, im.width, im.height)))


def place_art(img, spec, top, max_bottom):
    src = load(spec["art"])
    bg = silk_tone(src, frac_box(src, spec["tone"]))
    crop = src.crop(frac_box(src, spec["crop"]))
    aw = spec["width"]
    ah = crop.height * aw / crop.width
    if top + ah > max_bottom:                       # keep the painting clear of the type below
        aw, ah = aw * (max_bottom - top) / ah, max_bottom - top
    art = crop.resize((p(int(aw)), p(int(ah))), Image.LANCZOS)
    lay(img, art, int(p(W / 2 - aw / 2)), int(p(top)), soft_mask(art.size, **spec["mask"]), bg)


def title_block(img, T, y, size=1.0):
    """Title + subtitle (vermilion) + seal + ornament + ca dao; y = baseline of the title."""
    cx = W / 2
    T.put(TITLE, font("PlayfairDisplay[wght].ttf", 214 * size, 400), cx, y, INK, track=1, anchor="c")
    sy = y + 196 * size
    sw = T.put(SUB, font("PlayfairDisplay-Italic[wght].ttf", 150 * size, 400), cx, sy, SON, anchor="c")
    seal(img, cx + sw / 2 + 90, sy - 46 * size, 104, SON, ["Tràng", "An"], font("PlayfairDisplay[wght].ttf", 26, 500))
    d = ImageDraw.Draw(img)
    oy = sy + 94
    d.line([(p(cx - 220), p(oy)), (p(cx - 26), p(oy))], fill=INK3, width=2)
    d.line([(p(cx + 26), p(oy)), (p(cx + 220), p(oy))], fill=INK3, width=2)
    d.ellipse([p(cx - 7), p(oy - 7), p(cx + 7), p(oy + 7)], fill=SON)
    cf = font("PlayfairDisplay-Italic[wght].ttf", 42, 400)
    T.put(CA_DAO[0], cf, cx, oy + 94, INK2, anchor="c")
    T.put(CA_DAO[1], cf, cx, oy + 152, INK2, anchor="c")
    return oy + 152


def render(spec):
    seed(sum(map(ord, spec["name"])))
    img = paper(spec["bottom"], top=IVORY, grain=3.0, vignette=14, fibres=700, fibre_col=(212, 202, 190))
    cx = W / 2
    T = Typesetter(img)

    if spec["layout"] == "image-top":
        wash(img, [], spec["glow"], alpha=0.85, blur=70, ellipses=[(cx - 660, 560, cx + 660, 1880)])
        ty = spec.get("title_y", 2500)
        place_art(img, spec, spec.get("top", 250), ty - 100)
        T = Typesetter(img)
        title_block(img, T, ty)
    else:
        title_block(img, T, 560, size=0.93)
        wash(img, [], spec["glow"], alpha=0.7, blur=90, ellipses=[(cx - 820, 1150, cx + 820, 2950)])
        place_art(img, spec, spec.get("top", 1070), 3080)
        T = Typesetter(img)

    # header
    d = ImageDraw.Draw(img)
    hf = font("BeVietnamPro-Light.ttf", 24)
    left, mid, right = spec["head"]
    T.put(left, hf, M, 240, INK2, track=8)
    if mid:
        T.put(mid, hf, cx if right else W - M, 240, INK2, track=8, anchor="c" if right else "r")
    if right:
        T.put(right, hf, W - M, 240, INK2, track=8, anchor="r")
    d.line([(p(M), p(282)), (p(W - M), p(282))], fill=INK3, width=2)
    if spec.get("side"):
        vf = font("BeVietnamPro-Light.ttf", 22)
        T.vertical(spec["side"][0], vf, M + 6, 1300, INK2, track=9)
        T.vertical(spec["side"][1], vf, W - M - 6, 1300, INK2, track=9)

    # credits
    d = ImageDraw.Draw(img)
    by = 3200
    d.line([(p(M), p(by)), (p(W - M), p(by))], fill=INK3, width=2)
    lab = font("BeVietnamPro-Light.ttf", 20)
    T.put("THỰC HIỆN", lab, M, by + 70, INK2, track=7)
    T.put("ĐƠN VỊ", lab, W - M, by + 70, INK2, track=7, anchor="r")
    nf = font("BeVietnamPro-Medium.ttf", 36)
    lf = font("BeVietnamPro-Light.ttf", 31)
    T.put(NAMES[0], nf, M, by + 132, INK)
    T.put(NAMES[1], nf, M, by + 188, INK)
    T.put(CLASS, lf, W - M, by + 132, INK, anchor="r")
    T.put(SCHOOL, lf, W - M, by + 188, INK, anchor="r")

    return save(img, spec["name"], FINAL)


def contact_sheet(keys):
    names = [SPECS[k]["name"] for k in keys if (FINAL / f"{SPECS[k]['name']}.png").exists()]
    thumbs = [Image.open(FINAL / f"{n}.png").resize((620, 877), Image.LANCZOS) for n in names]
    sheet = Image.new("RGB", (40 + 660 * len(thumbs), 957), (228, 224, 218))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (40 + 660 * i, 40))
    sheet.save(FINAL / "tong-hop.png")
    print("saved", FINAL / "tong-hop.png")


if __name__ == "__main__":
    keys = sys.argv[1:] or list(SPECS)
    for k in keys:
        if not (ASSETS / SPECS[k]["art"]).exists():
            print(f"skip {k}: thiếu tranh assets/{SPECS[k]['art']}")
            continue
        render(SPECS[k])
    contact_sheet(list(SPECS))
