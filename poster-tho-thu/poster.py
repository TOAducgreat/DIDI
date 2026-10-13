"""Poster thơ "Sớm thu chín đỏ một cành hồng" – Phương Anh (Nhã An nữ sĩ).

Tranh: PlenX gpt-image-2 (assets/). Chữ, nền sơn mài sáng, khung và bố cục: dựng bằng SVG.
    python3 poster.py      ->  final/tho-thu-canh-hong.{svg,png,pdf}
"""
import base64
import io
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
ASSETS, FONTS, FINAL = ROOT / "assets", ROOT / "fonts", ROOT / "final"


def _find_chrome():
    """Chrome/Chromium/Edge for headless rendering; override with env POSTER_CHROME."""
    import os, shutil
    if os.environ.get("POSTER_CHROME"):
        return os.environ["POSTER_CHROME"]
    for c in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if Path(c).exists():
            return c
    for n in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge"):
        if shutil.which(n):
            return shutil.which(n)
    raise SystemExit("Không tìm thấy Chrome/Edge – đặt biến môi trường POSTER_CHROME tới file chạy của trình duyệt.")


CHROME = _find_chrome()
W, H = 2480, 3508

SON, SON_D = "#b8402c", "#8a2c1e"
INK = "#5a2a1e"
GOLD, GOLD_D = "#d4a24c", "#b07d2a"

POEM = [
    ["Sớm thu chín đỏ một cành hồng",
     "Thu hòa trong nắng biếc trời trong",
     "Thu khoe sắc thắm hoa đồng nội",
     "Thu thơm hương cốm với sen nồng."],
    ["Thu đem hoa sữa ngọt dịu lòng",
     "Thu thêm tĩnh lặng với mênh mông",
     "Thu lai thu khứ năm vẫn thế",
     "Thu để heo may trước thềm đông."],
    ["Trăng thu ngời sáng trời thái không",
     "Ánh thu lấp lánh giữa non sông",
     "Viên dung trăng thả thu man mác",
     "Thu lướt thành đô, tỏa ruộng đồng."],
    ["Bóng thu mải miết chí tang bồng",
     "Trúc thu tài đức dáng chẳng cong",
     "Ai gọi mùa thơ là thu liễm...",
     "Sớm thu chín đỏ một cành hồng!"],
]
SCENES = ["kho1-phong", "kho2-thu-ha-noi", "kho3-trang-thu", "kho4-truc"]


def b64(im, fmt="PNG"):
    buf = io.BytesIO()
    im.save(buf, fmt, **({"quality": 92} if fmt == "JPEG" else {}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def find(name):
    for ext in (".png", ".jpg", ".webp"):
        p = ASSETS / f"{name}{ext}"
        if p.exists():
            return p
    raise FileNotFoundError(name)


def cut_branch():
    """Cut the persimmon branch off its plain cream background (soft alpha by colour distance)."""
    im = Image.open(find("canh-hong")).convert("RGB")
    a = np.asarray(im, np.float32)
    corners = np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3),
                              a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    alpha = np.clip((dist - 10) / 34, 0, 1)
    alpha_im = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    out = im.convert("RGBA")
    out.putalpha(alpha_im)
    return out


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def build():
    rnd = random.Random(1410)
    defs, body = [], []

    # ---------------- background: bright lacquer, soft gradients, gold leaf
    defs.append('<linearGradient id="bg" x1="0" y1="0" x2="0.25" y2="1">'
                '<stop offset="0" stop-color="#fdf6e6"/><stop offset="0.45" stop-color="#fbe6d2"/>'
                '<stop offset="0.8" stop-color="#f8e0b8"/><stop offset="1" stop-color="#f3d39a"/></linearGradient>')
    defs.append('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="120"/></filter>')
    defs.append('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
                'baseFrequency="0.9" numOctaves="2" seed="5"/><feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.4  '
                '0 0 0 0 0.25  0 0 0 0.06 0"/></filter>')
    defs.append('<filter id="crackle" x="0" y="0" width="100%" height="100%"><feTurbulence type="turbulence" '
                'baseFrequency="0.012 0.02" numOctaves="3" seed="9"/><feColorMatrix values="0 0 0 0 0.85  '
                '0 0 0 0 0.62  0 0 0 0 0.3  0 0 0 0.35 -0.12"/></filter>')
    defs.append(f'<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6dc93"/>'
                f'<stop offset="0.5" stop-color="{GOLD}"/><stop offset="1" stop-color="#f1cf7c"/></linearGradient>')
    defs.append('<linearGradient id="title" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c9482e"/>'
                '<stop offset="0.5" stop-color="#e07a3c"/><stop offset="1" stop-color="#c9482e"/></linearGradient>')
    defs.append('<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="14" '
                'stdDeviation="18" flood-color="#9c5a2a" flood-opacity="0.22"/></filter>')
    defs.append('<filter id="halo" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="34"/></filter>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    for cx, cy, r, col, op in ((300, 900, 700, "#a8d8c8", 0.35), (2200, 500, 650, "#f7b9a0", 0.45),
                               (500, 2600, 800, "#f6c98a", 0.35), (2100, 2900, 700, "#a9d6cf", 0.3),
                               (1300, 1700, 600, "#fbd2c0", 0.3)):
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{op}" filter="url(#soft)"/>')
    body.append(f'<rect width="{W}" height="{H}" filter="url(#crackle)" opacity="0.5"/>')
    for _ in range(140):                                         # scattered gold-leaf flakes
        x, y = rnd.uniform(60, W - 60), rnd.uniform(60, H - 60)
        s = rnd.uniform(4, 16)
        pts = " ".join(f"{x + math.cos(a) * s * rnd.uniform(0.5, 1.2):.1f},{y + math.sin(a) * s * rnd.uniform(0.4, 1.0):.1f}"
                       for a in [k * 2 * math.pi / 6 + rnd.random() * 0.4 for k in range(6)])
        body.append(f'<polygon points="{pts}" fill="url(#gold)" opacity="{rnd.uniform(0.35, 0.8):.2f}"/>')
    # double gold border
    for inset, sw in ((56, 6), (78, 2)):
        body.append(f'<rect x="{inset}" y="{inset}" width="{W - 2 * inset}" height="{H - 2 * inset}" rx="26" '
                    f'fill="none" stroke="url(#gold)" stroke-width="{sw}"/>')

    # ---------------- persimmon branch: right side, running through all four stanzas
    br = cut_branch()
    bh = 3080
    bw = bh * br.width / br.height
    bx, by = 1420, 250                       # part of the branch bleeds past the right edge, as if hanging into the page
    defs.append(f'<clipPath id="page"><rect x="80" y="80" width="{W - 160}" height="{H - 160}" rx="24"/></clipPath>')
    body.append(f'<g clip-path="url(#page)" filter="url(#shadow)"><image href="{b64(br)}" x="{bx}" y="{by}" '
                f'width="{bw:.0f}" height="{bh}" preserveAspectRatio="none"/></g>')

    # ---------------- title
    body.append('<text x="200" y="300" font-family="Charm" font-weight="700" font-size="138" fill="url(#title)">'
                'Sớm thu chín đỏ</text>')
    body.append('<text x="420" y="455" font-family="Charm" font-weight="700" font-size="138" fill="url(#title)">'
                'một cành hồng</text>')
    body.append(f'<path d="M210,500 Q620,470 1050,500" fill="none" stroke="url(#gold)" stroke-width="4"/>')
    body.append(f'<text x="214" y="572" font-family="BeVN" font-weight="300" font-size="34" letter-spacing="10" '
                f'fill="{INK}">THƠ · PHƯƠNG ANH (NHÃ AN NỮ SĨ)</text>')

    # ---------------- four stanzas: scene on the left, verse beside it
    top, pitch = 660, 690
    sw_, sh_ = 760, 570
    for i, (scene, verses) in enumerate(zip(SCENES, POEM)):
        y = top + i * pitch
        x = 150
        im = Image.open(find(scene)).convert("RGB")
        r = max(sw_ / im.width, sh_ / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, t = (im.width - sw_) // 2, (im.height - sh_) // 2
        im = im.crop((l, t, l + sw_, t + sh_))
        cid = f"sc{i}"
        defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{sw_}" height="{sh_}" rx="34"/></clipPath>')
        body.append(f'<rect x="{x}" y="{y}" width="{sw_}" height="{sh_}" rx="34" fill="#fff8ec" filter="url(#shadow)"/>')
        body.append(f'<image href="{b64(im, "JPEG")}" x="{x}" y="{y}" width="{sw_}" height="{sh_}" clip-path="url(#{cid})"/>')
        body.append(f'<rect x="{x}" y="{y}" width="{sw_}" height="{sh_}" rx="34" fill="none" stroke="url(#gold)" stroke-width="5"/>')
        body.append(f'<rect x="{x + 14}" y="{y + 14}" width="{sw_ - 28}" height="{sh_ - 28}" rx="24" fill="none" '
                    f'stroke="#fff6e2" stroke-width="2" opacity="0.8"/>')
        # stanza number seal
        body.append(f'<circle cx="{x + sw_ - 8}" cy="{y + 8}" r="38" fill="{SON}"/>')
        body.append(f'<text x="{x + sw_ - 8}" y="{y + 22}" font-family="Charm" font-weight="700" font-size="42" '
                    f'fill="#fff4e0" text-anchor="middle">{"一二三四"[i] if False else i + 1}</text>')
        # verse, on a soft cream halo so leaves behind never touch the letters
        tx = x + sw_ + 52
        ty = y + 128
        body.append(f'<rect x="{tx - 40}" y="{ty - 90}" width="720" height="{3 * 112 + 140}" rx="60" '
                    f'fill="#fdf3e2" opacity="0.82" filter="url(#halo)"/>')
        for j, line in enumerate(verses):
            first, rest = (line.split(" ", 1) + [""])[:2]
            body.append(f'<text x="{tx}" y="{ty + j * 112}" font-family="Charm" font-size="54" fill="{INK}">'
                        f'<tspan fill="{SON}" font-weight="700" font-size="64">{esc(first)}</tspan> {esc(rest)}</text>')

    # ---------------- footer: author, date, seal
    fy = 3390
    body.append(f'<text x="150" y="{fy}" font-family="Charm" font-weight="700" font-size="58" fill="{SON_D}">'
                f'Phương Anh <tspan font-weight="400" font-size="46" fill="{INK}">(Nhã An nữ sĩ)</tspan></text>')
    body.append(f'<text x="1000" y="{fy}" font-family="BeVN" font-weight="300" font-size="36" letter-spacing="6" '
                f'fill="{INK}">14 / 10 / 2026</text>')
    body.append(f'<g transform="rotate(-4,1390,{fy - 22})"><rect x="1340" y="{fy - 72}" width="100" height="100" rx="8" fill="{SON}"/>'
                f'<rect x="1348" y="{fy - 64}" width="84" height="84" rx="5" fill="none" stroke="#fbe8d0" stroke-width="2"/>'
                f'<text x="1390" y="{fy - 30}" font-family="Charm" font-weight="700" font-size="30" fill="#fbe8d0" text-anchor="middle">Nhã</text>'
                f'<text x="1390" y="{fy + 6}" font-family="Charm" font-weight="700" font-size="30" fill="#fbe8d0" text-anchor="middle">An</text></g>')

    body.append(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')

    css = "".join(f"@font-face{{font-family:'{n}';src:url('{b64_font(fn)}');font-weight:{w};}}"
                  for n, fn, w in (("Charm", "Charm-Regular.ttf", 400), ("Charm", "Charm-Bold.ttf", 700),
                                   ("BeVN", "BeVietnamPro-Light.ttf", 300), ("BeVN", "BeVietnamPro-Regular.ttf", 400)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<style>{css}</style><defs>{"".join(defs)}</defs>{"".join(body)}</svg>')


def b64_font(fn):
    return "data:font/ttf;base64," + base64.b64encode((FONTS / fn).read_bytes()).decode()


def render(svg, name="tho-thu-canh-hong"):
    FINAL.mkdir(exist_ok=True)
    sp = FINAL / f"{name}.svg"
    sp.write_text(svg, encoding="utf-8")
    png = FINAL / f"{name}.png"
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--disable-gpu",
                    f"--window-size={W},{H + 400}", "--force-device-scale-factor=1", "--virtual-time-budget=10000",
                    f"--screenshot={png}", sp.as_uri()], check=True, capture_output=True)
    im = Image.open(png).convert("RGB").crop((0, 0, W, H))
    im.save(png, dpi=(300, 300))
    im.save(png.with_suffix(".pdf"), resolution=300)
    print("saved", png)


if __name__ == "__main__":
    render(build())
