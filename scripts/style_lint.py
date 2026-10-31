# -*- coding: utf-8 -*-
"""Lightweight style checker for Yile Wang's empirical-paper voice.

Usage
-----
    python style_lint.py manuscript.md
    python style_lint.py manuscript.docx --journal mdpi
    python style_lint.py manuscript.txt --journal nature

It reports sentence rhythm, hedging density, over-claim words, spelling
consistency, abstract length, citation style and figure/table callouts.
It is deliberately conservative: warnings are prompts for a human read, not
automatic edits.
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

OVERCLAIM = [
    "prove", "proves", "proved", "obviously", "undoubtedly", "certainly",
    "always", "never", "completely", "definitely", "demonstrates causality",
    "causes", "leads to", "drives", "guarantees",
]
HEDGES = [
    "may", "might", "suggest", "suggests", "indicate", "indicates",
    "associated with", "likely", "potentially", "appears", "seems",
    "broadly", "generally", "relatively", "consistent with", "possible",
]
BOUNDARY = [
    "should not be interpreted", "cannot rule out", "not a direct causal",
    "causal evidence", "descriptive rather than causal",
    "association rather than causation", "does not imply", "not causal",
]
CONNECTORS = ["overall", "however", "therefore", "in contrast", "in addition",
              "at the same time", "specifically", "notably", "similarly",
              "meanwhile"]
AMERICAN = r"\b(analyze|analyzed|analyzing|modeling|normalize|normalization|characterize|summarize|behavior|favor|color|utilize)\b"
BRITISH = r"\b(analyse|analysed|modelling|normalisation|characterise|summarise|behaviour|favour|colour|utilise)\b"


def load_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\s*\|.*\|\s*$", " ", text, flags=re.M)  # markdown tables
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)
    return text


def split_sentences(text: str) -> list[str]:
    one = re.sub(r"\s+", " ", text)
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", one)
    return [s.strip() for s in sents if len(s.split()) >= 5]


def count_phrases(text: str, phrases: list[str]) -> dict[str, int]:
    low = text.lower()
    return {p: len(re.findall(r"\b" + re.escape(p) + r"\b", low)) for p in phrases}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--journal", choices=["generic", "mdpi", "nature", "frontiers"],
                        default="generic")
    args = parser.parse_args()

    raw = load_text(args.path)
    # drop back matter and reference list from prose statistics; match headings
    m = re.search(r"\n\s*(References|Author Contributions|Funding)\s*\n",
                  raw, flags=re.I)
    body = raw[:m.start()] if m else raw
    sents = split_sentences(body)
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", body)
    lens = [len(s.split()) for s in sents]
    mean_len = statistics.mean(lens) if lens else 0
    median_len = statistics.median(lens) if lens else 0
    long_share = 100 * sum(1 for x in lens if x > 40) / len(lens) if lens else 0

    low = body.lower()
    hedges = sum(low.count(h) for h in HEDGES)
    hedge_density = 1000 * hedges / max(len(words), 1)
    over = count_phrases(body, OVERCLAIM)
    boundary_hits = [p for p in BOUNDARY if p in low]
    connectors = count_phrases(body, CONNECTORS)
    amer = len(re.findall(AMERICAN, body, flags=re.I))
    brit = len(re.findall(BRITISH, body, flags=re.I))
    we = len(re.findall(r"\bwe\b", low))
    this_study = len(re.findall(r"\bthis study\b", low))
    fig_calls = len(re.findall(r"\b(?:Figure|Fig\.)\s*\d+", body))
    tab_calls = len(re.findall(r"\bTable\s*\d+", body))
    numeric_cites = len(re.findall(r"\[\d+(?:\s*[-,]\s*\d+)*\]", body))
    author_cites = len(re.findall(r"\([A-Z][A-Za-z]+\s+et al\.,?\s+\d{4}\)", body))
    r2_plain = len(re.findall(r"\bR2\b", body))
    r2_sup = body.count("R²") + body.count("R^2")

    abstract = ""
    m = re.search(r"\bAbstract\b(.*?)(Keywords|1\.?\s+Introduction|Introduction)",
                  raw, flags=re.S | re.I)
    if m:
        abstract = re.sub(r"\s+", " ", m.group(1)).strip()
    abs_words = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", abstract))

    print(f"# Style lint: {args.path}")
    print(f"Words: {len(words)} | Sentences: {len(sents)} | "
          f"Mean sentence: {mean_len:.1f} | Median: {median_len:.0f} | "
          f">40 words: {long_share:.1f}%")
    abs_label = abs_words if abs_words else "not found (check first paragraph)"
    print(f"Abstract words: {abs_label} | "
          f"Figure calls: {fig_calls} | Table calls: {tab_calls}")
    print(f"Hedges: {hedges} ({hedge_density:.1f}/1000 words) | "
          f"we: {we} | this study: {this_study}")
    print(f"Spelling: American {amer} / British {brit}")
    print(f"Citations: numeric {numeric_cites} / author-year {author_cites}")
    print(f"R2 plain: {r2_plain} | R²/R^2: {r2_sup}")
    print("Connectors: " + ", ".join(f"{k}={v}" for k, v in connectors.items() if v))

    warnings = []
    if mean_len > 30:
        warnings.append("Mean sentence length > 30 words; split long sentences.")
    if long_share > 12:
        warnings.append(f"{long_share:.1f}% of sentences exceed 40 words; tighten.")
    if hedge_density < 5:
        warnings.append("Hedging density < 5/1000 words; causal language may be too strong.")
    if not boundary_hits:
        warnings.append("No explicit causal-boundary phrase found; add one in Discussion/Conclusions.")
    if amer and brit:
        warnings.append("Mixed American and British spelling; choose one (-ize / -ise).")
    if r2_plain and not r2_sup:
        warnings.append("Use R² (or $R^2$) instead of plain R2 in prose and figures.")
    if fig_calls < 3:
        warnings.append("Few figure callouts; results paragraphs should point to figures/tables.")
    over_hits = {k: v for k, v in over.items() if v}
    if over_hits:
        warnings.append("Over-claim words found: " + ", ".join(f"{k}({v})" for k, v in over_hits.items()))

    if args.journal == "mdpi":
        if abs_words and not 150 <= abs_words <= 260:
            warnings.append(f"MDPI abstract is {abs_words} words; target 180–250.")
        if not numeric_cites:
            warnings.append("MDPI usually uses numeric [1] citations; none found.")
    elif args.journal == "nature":
        if abs_words and not 150 <= abs_words <= 230:
            warnings.append(f"Scientific Reports abstract is {abs_words} words; target ~200.")
        if author_cites and not numeric_cites:
            warnings.append("Scientific Reports uses superscript numeric citations; check citation style.")
    elif args.journal == "frontiers":
        if author_cites == 0 and numeric_cites == 0:
            warnings.append("No citations detected; check author-year style.")
        if not re.search(r"\b(Introduction|Methods|Results|Discussion):", abstract):
            warnings.append("Frontiers abstract is usually structured (Introduction/Methods/Results/Discussion).")

    print("\n## Warnings")
    if warnings:
        for w in warnings:
            print(f"- {w}")
    else:
        print("- None. Voice and formatting look consistent.")

    print("\n## Reading notes")
    print(f"- 'This study' / 'we' ratio: {this_study}:{we}. "
          "MDPI tolerates we; Nature/Frontiers prefer this study.")
    print(f"- Hedging examples found: {hedges}; boundary phrases: {len(boundary_hits)}.")
    print("- Check the abstract is one paragraph and has no citations/formulas.")

    severe = bool(over_hits or (hedge_density < 5) or (amer and brit))
    return 1 if severe else 0


if __name__ == "__main__":
    sys.exit(main())
