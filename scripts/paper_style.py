# -*- coding: utf-8 -*-
"""Shared visual language for Yile Wang's journal figures.

The defaults in this module are measured from the published figures in
Systems 2026, 14, 319 and Scientific Reports 2026, 16, 32263:

* Times New Roman, almost everything bold, generous type sizes.
* White background, full box axes, light dashed guide lines.
* viridis for SHAP and density; a five-class bright green-to-red ramp for maps.
* 300 dpi PNG plus a vector PDF for every figure.

Import this module before creating figures.  ``apply_style()`` is idempotent.
"""

from __future__ import annotations

from pathlib import Path
import logging

import matplotlib as mpl
import matplotlib.pyplot as plt

FONT = "Times New Roman"

# --- China map ramp sampled from the published Figure 6 ---------------------
MAP_COLORS = ["#38A800", "#8BD100", "#FFFF00", "#FF8000", "#FF0000"]
MAP_BREAKS = [0.0, 0.25, 0.40, 0.55, 0.70, 0.85]
MAP_LABELS = [
    "0.0000 — 0.2500",
    "0.2501 — 0.4000",
    "0.4001 — 0.5500",
    "0.5501 — 0.7000",
    "0.7001 — 0.8500",
]

# Sequential ramps used in the Sustainability (18, 1283) map figure.
BLUE_SEQ = ["#E8F1F8", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"]
GREEN_SEQ = ["#E5F5E0", "#C7E9C0", "#A1D99B", "#74C476", "#41AB5D", "#238B45", "#006D2C"]

# Prediction / model-comparison figures.
LINE_BLUE = "#1F77B4"
BAND_BLUE = "#A6CEE3"
ONE_TO_ONE = "#D62728"
TREND_GREY = "#7F7F7F"

PROVINCE_SHORT_TO_FULL = {
    "北京": "北京市", "天津": "天津市", "河北": "河北省", "山西": "山西省",
    "内蒙古": "内蒙古自治区", "辽宁": "辽宁省", "吉林": "吉林省", "黑龙江": "黑龙江省",
    "上海": "上海市", "江苏": "江苏省", "浙江": "浙江省", "安徽": "安徽省",
    "福建": "福建省", "江西": "江西省", "山东": "山东省", "河南": "河南省",
    "湖北": "湖北省", "湖南": "湖南省", "广东": "广东省", "广西": "广西壮族自治区",
    "海南": "海南省", "重庆": "重庆市", "四川": "四川省", "贵州": "贵州省",
    "云南": "云南省", "西藏": "西藏自治区", "陕西": "陕西省", "甘肃": "甘肃省",
    "青海": "青海省", "宁夏": "宁夏回族自治区", "新疆": "新疆维吾尔自治区",
}


def normalize_province(name: object) -> str:
    """Return the full provincial name used by the bundled GeoJSON."""
    s = str(name).strip().replace(" ", "")
    if s in PROVINCE_SHORT_TO_FULL:
        return PROVINCE_SHORT_TO_FULL[s]
    if s.endswith(("省", "市", "自治区", "特别行政区")):
        return s
    return PROVINCE_SHORT_TO_FULL.get(s, s)


def apply_style(base: float = 12, bold: bool = True) -> None:
    """Apply the house style.  Call once at the top of every plotting script."""
    # Times New Roman Bold is present on this machine; the font manager still
    # emits a cosmetic fallback notice for a few mathtext glyphs.
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    weight = "bold" if bold else "normal"
    mpl.rcParams.update({
        "font.family": FONT,
        "font.weight": weight,
        "font.size": base,
        "axes.labelweight": weight,
        "axes.titleweight": weight,
        "axes.labelsize": base + 2,
        "axes.titlesize": base + 4,
        "xtick.labelsize": base,
        "ytick.labelsize": base,
        "legend.fontsize": base,
        "axes.linewidth": 1.8,
        "axes.edgecolor": "black",
        "axes.unicode_minus": False,
        "xtick.major.width": 1.8,
        "ytick.major.width": 1.8,
        "xtick.major.size": 7,
        "ytick.major.size": 7,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "grid.linestyle": "--",
        "grid.alpha": 0.30,
        "grid.linewidth": 1.0,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "mathtext.fontset": "stix",
        "mathtext.default": "it",
    })


def save_figure(fig: plt.Figure, out_path: str | Path, dpi: int = 300,
                pdf: bool = True, tight: bool = True) -> list[Path]:
    """Save a PNG and (by default) a vector PDF next to it."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = []
    fig.savefig(out_path, dpi=dpi, bbox_inches="tight" if tight else None,
                facecolor="white")
    written.append(out_path)
    if pdf:
        pdf_path = out_path.with_suffix(".pdf")
        fig.savefig(pdf_path, bbox_inches="tight" if tight else None,
                    facecolor="white")
        written.append(pdf_path)
    for p in written:
        print(f"[saved] {p}")
    return written


def panel_label(ax: plt.Axes, label: str, x: float = 0.5, y: float = 1.02,
                fontsize: float | None = None, **kwargs) -> None:
    """Add the bold (a)/(b) panel label used above every subplot."""
    ax.text(x, y, label, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=fontsize, fontweight="bold", **kwargs)


def style_ticks(ax: plt.Axes, size: float | None = None) -> None:
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontweight("bold")
        if size is not None:
            tick.set_fontsize(size)
