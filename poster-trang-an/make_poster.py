"""Bản 0 — Mặc Nguyệt. Toàn bộ bộ poster nằm ở options/silk_poster.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "options"))
from silk_poster import SPECS, render  # noqa: E402

render(SPECS["0"])
