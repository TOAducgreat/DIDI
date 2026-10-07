"""Bản 0 — Mặc Nguyệt. Cả bộ poster nằm ở options/info_poster.py (nội dung: options/noi_dung.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "options"))
from info_poster import SPECS, render  # noqa: E402

render(SPECS["0"])
