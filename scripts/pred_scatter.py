# -*- coding: utf-8 -*-
"""Multi-model prediction scatter grid in the Systems 2026 style.

Each panel shows true versus predicted values coloured by a two-dimensional
Gaussian KDE, an OLS fit with a 95% confidence band, the 1:1 line, and a
three-line R2/MAE/RMSE box.  The grid shares one density colour bar and one
legend, exactly like the published Figure 15.

Usage
-----
    python pred_scatter.py --data assets/data/model_predictions.csv \
        --out assets/previews/fig15_prediction_scatter.png

The CSV needs columns ``Model``, ``True_Value`` and ``Predicted_Value``
(``model``, ``y_true``, ``y_pred`` are accepted as aliases).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from paper_style import BAND_BLUE, LINE_BLUE, ONE_TO_ONE, apply_style, save_figure, style_ticks


def _kde_colours(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Per-panel 2-D KDE, normalised to 0-1 for a stable visual scale."""
    try:
        xy = np.vstack([x, y])
        z = gaussian_kde(xy)(xy)
        if np.ptp(z) > 0:
            z = (z - z.min()) / np.ptp(z)
        return z
    except Exception:
        return np.zeros_like(x)


def _panel(ax, x, y, title, base_font=9, show_xlabel=True, show_ylabel=True):
    colours = _kde_colours(x, y)
    ax.scatter(x, y, c=colours, cmap="viridis", s=26, alpha=0.88,
               edgecolors="none", zorder=3)

    # OLS fit and 95% mean-confidence band
    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit()
    grid = np.linspace(x.min(), x.max(), 150)
    pred = res.get_prediction(sm.add_constant(grid)).summary_frame(alpha=0.05)
    ax.plot(grid, pred["mean"], color=LINE_BLUE, linewidth=2.0, zorder=4)
    ax.fill_between(grid, pred["mean_ci_lower"], pred["mean_ci_upper"],
                    color=BAND_BLUE, alpha=0.40, linewidth=0, zorder=2)

    lo = min(x.min(), y.min())
    hi = max(x.max(), y.max())
    pad = 0.05 * (hi - lo)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color=ONE_TO_ONE,
            linestyle="--", linewidth=1.5, zorder=1)
    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(lo - pad, hi + pad)

    r2 = r2_score(x, y)  # x = true values, y = predictions
    mae = mean_absolute_error(x, y)
    rmse = float(np.sqrt(mean_squared_error(x, y)))
    r2_disp = max(r2, 0.001)
    ax.text(0.045, 0.955,
            f"$R^2$ = {r2_disp:.3f}\n$MAE$ = {mae:.3f}\n$RMSE$ = {rmse:.3f}",
            transform=ax.transAxes, ha="left", va="top",
            fontsize=base_font - 0.5, fontweight="bold", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.72, pad=1.2))

    ax.set_title(title, fontsize=base_font + 1.2, fontweight="bold", pad=5)
    if show_xlabel:
        ax.set_xlabel("True Values", fontsize=base_font + 0.5,
                      fontweight="bold", labelpad=2)
    if show_ylabel:
        ax.set_ylabel("Predicted Values", fontsize=base_font + 0.5,
                      fontweight="bold", labelpad=2)
    ax.grid(True, linestyle="--", alpha=0.26, linewidth=0.8)
    ax.tick_params(width=1.2, length=4)
    style_ticks(ax, base_font - 1)
    for spine in ax.spines.values():
        spine.set_linewidth(1.3)
        spine.set_color("black")


def prediction_scatter_grid(data: pd.DataFrame | dict, out_path=None,
                            model_order=None, ncols=4, figsize=None,
                            base_font=9, title_prefix=True):
    """Draw the 4 x 3 prediction grid; return the figure."""
    apply_style(base=base_font)
    if isinstance(data, dict):
        frames = []
        for model, (y_true, y_pred) in data.items():
            frames.append(pd.DataFrame({"Model": model, "True_Value": y_true,
                                        "Predicted_Value": y_pred}))
        data = pd.concat(frames, ignore_index=True)
    df = data.rename(columns={"model": "Model", "y_true": "True_Value",
                              "y_pred": "Predicted_Value"})
    if model_order is None:
        model_order = list(dict.fromkeys(df["Model"].tolist()))
    n = len(model_order)
    ncols = min(ncols, n)
    nrows = int(np.ceil(n / ncols))
    if figsize is None:
        figsize = (4.15 * ncols, 3.15 * nrows)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, dpi=300)
    axes = np.atleast_1d(axes).ravel()
    for i, model in enumerate(model_order):
        sub = df[df["Model"] == model]
        x = sub["True_Value"].to_numpy(float)
        y = sub["Predicted_Value"].to_numpy(float)
        prefix = f"({chr(97 + i)}) " if title_prefix and i < 26 else ""
        r, c = divmod(i, ncols)
        _panel(axes[i], x, y, f"{prefix}{model}", base_font=base_font,
               show_xlabel=(r == nrows - 1), show_ylabel=(c == 0))
    for ax in axes[n:]:
        ax.axis("off")

    fig.subplots_adjust(left=0.055, right=0.905, top=0.965, bottom=0.11,
                        wspace=0.28, hspace=0.32)

    # shared density colour bar
    cax = fig.add_axes([0.922, 0.16, 0.013, 0.70])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(0, 1),
                                            cmap="viridis"), cax=cax)
    cb.set_ticks([])
    cb.outline.set_linewidth(1.2)
    cb.set_label("Density", rotation=270, labelpad=16, fontsize=base_font + 1,
                 fontweight="bold")

    handles = [
        Line2D([0], [0], color=LINE_BLUE, linewidth=2.4),
        Patch(facecolor=BAND_BLUE, alpha=0.55),
        Line2D([0], [0], color=ONE_TO_ONE, linestyle="--", linewidth=1.8),
    ]
    fig.legend(handles, ["Regression Line", "95% Confidence Interval", "1:1 Line"],
               loc="lower center", ncol=3, frameon=False,
               fontsize=base_font + 1, bbox_to_anchor=(0.46, -0.005),
               handlelength=3.2, columnspacing=3.0)
    if out_path:
        save_figure(fig, out_path)
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    df = pd.read_csv(args.data)
    order = ["SSA-LSTM", "LSTM", "GBDT", "RF", "SVR", "BP(MLP)", "XGBoost",
             "CatBoost", "ELM(EML)", "ANN(PyTorch)", "RNN", "Transformer"]
    order = [m for m in order if m in set(df["Model"])]
    prediction_scatter_grid(df, out_path=args.out, model_order=order or None)


if __name__ == "__main__":
    main()
