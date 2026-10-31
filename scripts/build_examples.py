# -*- coding: utf-8 -*-
"""Regenerate every preview figure from the bundled example data.

Run from anywhere:

    python scripts/build_examples.py

Outputs land in ``assets/previews``.  The script never writes to the source
papers, the ZIP archive, or any GitHub repository.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from china_map import plot_china_panels  # noqa: E402
from pred_scatter import prediction_scatter_grid  # noqa: E402
from shap_plots import dependence_grid, summary_combo  # noqa: E402

DATA = ROOT / "assets" / "data"
OUT = ROOT / "assets" / "previews"
REQUIRED = [
    DATA / "epi_panel.csv",
    DATA / "shap_demo.npz",
    DATA / "model_predictions.csv",
]


def _check_data() -> bool:
    missing = [p for p in REQUIRED if not p.exists()]
    if not missing:
        return True
    print("Example data not found. The public repository does not include the")
    print("author's research data; see assets/data/README.md for the schema.")
    for p in missing:
        print("  missing:", p.relative_to(ROOT))
    return False


def main() -> None:
    if not _check_data():
        return
    OUT.mkdir(parents=True, exist_ok=True)

    epi = pd.read_csv(DATA / "epi_panel.csv")
    plot_china_panels(epi, [2003, 2010, 2015, 2020],
                      OUT / "fig06_china_epi_4panel.png",
                      value_col="epi", legend_title="EPI",
                      title_suffix="EPI Value")

    shap = np.load(DATA / "shap_demo.npz", allow_pickle=True)
    sv = shap["shap_values"]
    fv = shap["feature_values"]
    names = list(shap["feature_names"])
    summary_combo(sv, fv, names, out_path=OUT / "fig11_shap_combo.png")
    dependence_grid(sv, fv, names, out_path=OUT / "fig13_shap_dependence.png",
                    features=["GDP", "EI", "PGPC", "FCR", "UR", "SSI"])

    pred = pd.read_csv(DATA / "model_predictions.csv")
    order = ["SSA-LSTM", "LSTM", "GBDT", "RF", "SVR", "BP(MLP)", "XGBoost",
             "CatBoost", "ELM(EML)", "ANN(PyTorch)", "RNN", "Transformer"]
    order = [m for m in order if m in set(pred["Model"])]
    prediction_scatter_grid(pred, out_path=OUT / "fig15_prediction_scatter.png",
                            model_order=order)
    make_contact_sheet()
    print("\nAll previews rebuilt in", OUT)


def make_contact_sheet() -> None:
    """2 x 2 overview of the four reproduced figures."""
    items = [
        ("Fig. 6  China EPI map", "fig06_china_epi_4panel.png"),
        ("Fig. 11  SHAP beeswarm + bars", "fig11_shap_combo.png"),
        ("Fig. 13  SHAP dependence", "fig13_shap_dependence.png"),
        ("Fig. 15  Prediction scatter", "fig15_prediction_scatter.png"),
    ]
    cell_w, cell_h, pad, label_h = 720, 560, 20, 34
    sheet = Image.new("RGB", (pad + 2 * (cell_w + pad),
                              pad + 2 * (cell_h + label_h + pad)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    for k, (label, name) in enumerate(items):
        img = Image.open(OUT / name).convert("RGB")
        img.thumbnail((cell_w, cell_h), Image.LANCZOS)
        r, c = divmod(k, 2)
        x0 = pad + c * (cell_w + pad)
        y0 = pad + r * (cell_h + label_h + pad)
        draw.text((x0 + 4, y0 + 4), label, fill="black", font=font)
        sheet.paste(img, (x0 + (cell_w - img.width) // 2,
                          y0 + label_h + (cell_h - img.height) // 2))
    out = OUT / "_contact_sheet.png"
    sheet.save(out, dpi=(300, 300))
    print(f"[saved] {out}")


if __name__ == "__main__":
    main()
