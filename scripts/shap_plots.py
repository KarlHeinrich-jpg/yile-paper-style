# -*- coding: utf-8 -*-
"""Reusable SHAP figures in Yile Wang's published style.

Three entry points cover the figures used in Systems 2026, 14, 319:

``summary_combo``
    Beeswarm + horizontal importance bars on a twin top axis, viridis,
    translucent bars with black edges, "High/Low" colour bar.

``summary_grid``
    One ``summary_combo`` per panel (e.g. EWM / CRITIC / CV / DM).

``dependence_grid``
    Top-feature dependence panels with LOWESS trend, median line, automatic
    turning-point threshold and a three-entry legend.

All functions accept 2-D ``(n_samples, n_features)`` arrays.  A 3-D
``(n_samples, lookback, n_features)`` array is averaged over the lookback
dimension, which is what the published LSTM-SHAP figures do.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

import shap

from paper_style import TREND_GREY, apply_style, save_figure, style_ticks


def _prepare(shap_values, feature_values, feature_names=None):
    sv = np.asarray(shap_values, dtype=float)
    if sv.ndim == 4 and sv.shape[-1] == 1:
        sv = sv[..., 0]
    if sv.ndim == 3:
        sv = sv.mean(axis=1)
    if sv.ndim != 2:
        raise ValueError(f"SHAP values must be 2-D after aggregation, got {sv.shape}")
    n, p = sv.shape
    if feature_values is None:
        fv = np.zeros_like(sv)
    else:
        fv = np.asarray(feature_values, dtype=float)
        if fv.ndim == 3:
            fv = fv.mean(axis=1)
        if fv.shape != sv.shape:
            raise ValueError(f"feature_values {fv.shape} != shap_values {sv.shape}")
    if feature_names is None:
        feature_names = [f"F{i}" for i in range(p)]
    feature_names = [str(x) for x in feature_names]
    if len(feature_names) != p:
        raise ValueError("feature_names length does not match SHAP columns")
    return sv, fv, feature_names


def _add_colourbar(fig, cax, label="Feature value", fontsize=9):
    sm = cm.ScalarMappable(norm=Normalize(0, 1), cmap="viridis")
    cb = fig.colorbar(sm, cax=cax)
    cb.set_ticks([])
    cb.outline.set_linewidth(1.2)
    cb.set_label(label, rotation=270, labelpad=16, fontsize=fontsize,
                 fontweight="bold")
    cax.text(1.8, 1.0, "High", transform=cax.transAxes, ha="left",
             va="center", fontsize=fontsize - 1, fontweight="bold")
    cax.text(1.8, 0.0, "Low", transform=cax.transAxes, ha="left",
             va="center", fontsize=fontsize - 1, fontweight="bold")
    return cb


def _summary_on_ax(ax, sv, fv, names, title=None, max_display=None,
                   base_font=11, bar_alpha=0.30, point_size=38,
                   ylabel="Features", xlabel="SHAP Value",
                   top_label="Mean |SHAP Value| (Feature Importance)",
                   show_bars=True):
    """Draw one beeswarm + bar panel on an existing axis."""
    n, p = sv.shape
    keep = p if max_display is None else min(max_display, p)
    mean_abs_all = np.abs(sv).mean(axis=0)

    plt.sca(ax)
    shap.summary_plot(sv, fv, feature_names=names, max_display=keep,
                      plot_type="dot", cmap="viridis", show=False,
                      plot_size=None, color_bar=False, sort=True)
    # shap enlarges points; make them match the published figure
    for coll in ax.collections:
        try:
            coll.set_sizes([point_size])
            coll.set_alpha(0.90)
        except Exception:
            pass

    ax.set_xlabel(xlabel, fontsize=base_font + 2, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=base_font + 2, fontweight="bold")
    ax.tick_params(axis="both", width=1.8, length=6)
    style_ticks(ax, base_font)
    for spine in ax.spines.values():
        spine.set_linewidth(1.8)
        spine.set_color("black")
    ax.grid(True, axis="x", linestyle="--", alpha=0.30, linewidth=1.0)
    ax.axvline(0, color="black", linewidth=1.7, alpha=0.70, zorder=1)

    if show_bars:
        labels = [t.get_text() for t in ax.get_yticklabels()]
        ypos = ax.get_yticks()
        name_to_idx = {nm: i for i, nm in enumerate(names)}
        imp = [mean_abs_all[name_to_idx[l]] if l in name_to_idx
               else mean_abs_all[i] for i, l in enumerate(labels)]
        # only keep the visible ticks (shap may add blank ticks)
        mask = [l.strip() != "" for l in labels]
        labels = [l for l, m in zip(labels, mask) if m]
        ypos = [y for y, m in zip(ypos, mask) if m]
        imp = [v for v, m in zip(imp, mask) if m]
        colours = cm.viridis(np.linspace(0, 1, len(ypos)))
        ax2 = ax.twiny()
        ax2.set_zorder(ax.get_zorder() - 1)
        ax.patch.set_visible(False)
        ax2.barh(ypos, imp, height=0.72, color=colours, alpha=bar_alpha,
                 edgecolor="black", linewidth=1.6, zorder=0)
        ax2.set_xlim(left=0)
        ax2.set_xlabel(top_label, fontsize=base_font + 1, fontweight="bold",
                       labelpad=8)
        ax2.xaxis.set_label_position("top")
        ax2.xaxis.tick_top()
        ax2.tick_params(axis="x", width=1.8, length=5)
        style_ticks(ax2, base_font - 1)
        ax2.grid(False)
        for key, spine in ax2.spines.items():
            spine.set_visible(key == "top")
            if key == "top":
                spine.set_linewidth(1.8)
                spine.set_color("black")
    if title:
        ax.set_title(title, fontsize=base_font + 2, fontweight="bold", pad=22)
    return ax


def summary_combo(shap_values, feature_values=None, feature_names=None,
                  out_path=None, title=None, max_display=None,
                  figsize=(9.5, 5.8), base_font=11, colorbar=True,
                  **kwargs):
    """Single beeswarm + bar panel (published Figure 11 style)."""
    apply_style(base=base_font)
    sv, fv, names = _prepare(shap_values, feature_values, feature_names)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    _summary_on_ax(ax, sv, fv, names, title=title, max_display=max_display,
                   base_font=base_font, **kwargs)
    if colorbar:
        div = make_axes_locatable(ax)
        cax = div.append_axes("right", size="3.2%", pad=0.06)
        _add_colourbar(fig, cax, fontsize=base_font - 1)
    if out_path:
        save_figure(fig, out_path)
    return fig


def summary_grid(panels, out_path=None, ncols=2, figsize=None,
                 base_font=10, panel_titles=True):
    """Grid of summary panels.

    ``panels`` is a list of dicts with keys ``shap_values``, ``feature_values``,
    ``feature_names`` and optional ``title``.
    """
    apply_style(base=base_font)
    n = len(panels)
    ncols = min(ncols, n)
    nrows = int(np.ceil(n / ncols))
    if figsize is None:
        figsize = (7.8 * ncols, 5.2 * nrows)
    fig = plt.figure(figsize=figsize, dpi=300)
    outer = fig.add_gridspec(nrows, ncols, wspace=0.42, hspace=0.42)
    for i, panel in enumerate(panels):
        r, c = divmod(i, ncols)
        inner = outer[r, c].subgridspec(1, 2, width_ratios=[1, 0.035],
                                       wspace=0.05)
        ax = fig.add_subplot(inner[0])
        cax = fig.add_subplot(inner[1])
        sv, fv, names = _prepare(panel["shap_values"],
                                 panel.get("feature_values"),
                                 panel.get("feature_names"))
        _summary_on_ax(ax, sv, fv, names,
                       title=panel.get("title") if panel_titles else None,
                       max_display=panel.get("max_display"),
                       base_font=base_font - 1,
                       bar_alpha=panel.get("bar_alpha", 0.30),
                       point_size=panel.get("point_size", 30),
                       ylabel=panel.get("ylabel", "Features"),
                       xlabel=panel.get("xlabel", "SHAP Value"),
                       top_label=panel.get("top_label",
                                           "Mean |SHAP Value| (Feature Importance)"))
        _add_colourbar(fig, cax, fontsize=base_font - 2)
    if out_path:
        save_figure(fig, out_path)
    return fig


def _threshold_from_trend(x, y, frac=0.70):
    """x at the steepest point of a LOWESS curve (an interpretable turning point)."""
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        z = lowess(y, x, frac=frac, return_sorted=True)
        xs, ys = z[:, 0], z[:, 1]
    except Exception:
        order = np.argsort(x)
        xs, ys = x[order], y[order]
    if len(xs) < 3:
        return float(np.median(x))
    ux, idx = np.unique(xs, return_index=True)
    if len(ux) < 3:
        return float(np.median(x))
    slope = np.gradient(ys[idx], ux)
    return float(ux[int(np.nanargmax(np.abs(slope)))])


def dependence_grid(shap_values, feature_values, feature_names, out_path=None,
                    features=None, ncols=3, thresholds=None, figsize=None,
                    base_font=11, point_size=32, panel_labels=False):
    """Top-feature SHAP dependence panels (published Figure 13 style)."""
    apply_style(base=base_font)
    sv, fv, names = _prepare(shap_values, feature_values, feature_names)
    if features is None:
        order = np.argsort(np.abs(sv).mean(axis=0))[::-1]
        features = [names[i] for i in order[:6]]
    name_to_idx = {nm: i for i, nm in enumerate(names)}
    n = len(features)
    ncols = min(ncols, n)
    nrows = int(np.ceil(n / ncols))
    if figsize is None:
        figsize = (5.3 * ncols, 4.2 * nrows)
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, dpi=300)
    axes = np.atleast_1d(axes).ravel()

    for k, (ax, feat) in enumerate(zip(axes, features)):
        j = name_to_idx[feat]
        x = fv[:, j]
        y = sv[:, j]
        order = np.argsort(x)
        x, y = x[order], y[order]
        ax.scatter(x, y, c=x, cmap="viridis", s=point_size, alpha=0.88,
                   edgecolors="none", zorder=3)
        try:
            from statsmodels.nonparametric.smoothers_lowess import lowess
            z = lowess(y, x, frac=0.70, return_sorted=True)
            ax.plot(z[:, 0], z[:, 1], color=TREND_GREY, linewidth=2.2,
                    zorder=4)
        except Exception:
            coef = np.polyfit(x, y, 2)
            xx = np.linspace(x.min(), x.max(), 200)
            ax.plot(xx, np.polyval(coef, xx), color=TREND_GREY,
                    linewidth=2.2, zorder=4)
        med = float(np.median(x))
        thr = (float(thresholds[feat]) if thresholds and feat in thresholds
               else _threshold_from_trend(x, y))
        ax.axhline(0, color="#777777", linestyle="--", linewidth=1.0,
                   alpha=0.8, zorder=1)
        ax.axvline(med, color="black", linestyle="--", linewidth=1.1,
                   zorder=2)
        ax.axvline(thr, color="#F4A6A6", linestyle=":", linewidth=1.3,
                   zorder=2)
        handles = [
            Line2D([0], [0], color="black", linestyle="--", linewidth=1.1),
            Line2D([0], [0], color="#F4A6A6", linestyle=":", linewidth=1.3),
            Line2D([0], [0], color=TREND_GREY, linewidth=2.2),
        ]
        ax.legend(handles,
                  [f"Median: {med:,.2f}", f"Threshold: {thr:,.2f}", "Trend Fit"],
                  loc="best", fontsize=base_font - 2, frameon=True,
                  facecolor="white", edgecolor="#CCCCCC", framealpha=0.92,
                  handlelength=2.4, borderpad=0.4, labelspacing=0.3)
        ax.set_xlabel(feat, fontsize=base_font + 1, fontweight="bold")
        ax.set_ylabel("SHAP", fontsize=base_font + 1, fontweight="bold")
        ax.tick_params(width=1.6, length=5)
        style_ticks(ax, base_font - 1)
        for spine in ax.spines.values():
            spine.set_linewidth(1.6)
        if panel_labels:
            ax.text(-0.14, 1.04, f"({chr(97 + k)})", transform=ax.transAxes,
                    fontsize=base_font, fontweight="bold")
    for ax in axes[n:]:
        ax.axis("off")
    fig.subplots_adjust(wspace=0.30, hspace=0.34)
    if out_path:
        save_figure(fig, out_path)
    return fig


def _load_npz(path):
    d = np.load(path, allow_pickle=True)
    return d["shap_values"], d["feature_values"], list(d["feature_names"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--npz", required=True, help="NPZ with shap_values/feature_values/feature_names")
    parser.add_argument("--kind", choices=["summary", "dependence"], default="summary")
    parser.add_argument("--out", required=True)
    parser.add_argument("--features", nargs="*", default=None)
    args = parser.parse_args()
    sv, fv, names = _load_npz(args.npz)
    if args.kind == "summary":
        summary_combo(sv, fv, names, out_path=args.out)
    else:
        dependence_grid(sv, fv, names, out_path=args.out,
                        features=args.features)


if __name__ == "__main__":
    main()
