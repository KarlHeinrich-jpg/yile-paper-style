---
name: yile-paper-style
description: 按王毅乐（Yile Wang）已发表论文的语言与制图风格写作、润色和绘图。用于复刻或新画中国省级分级地图、SHAP 蜂群+条形组合图、SHAP 依赖图、多模型预测散点图，以及按 Systems、Scientific Reports、Sustainability、Frontiers 的论文风格写摘要、引言、结果、讨论、结论和审稿回复。触发词包括：按我论文风格画图、中国地图、SHAP 图、复刻论文插图、论文润色、写摘要、写引言、讨论、结论、图表规范、MDPI 风格。Use whenever the user asks to write or revise a paper in Yile Wang's voice, reproduce a figure from their Systems/Scientific Reports/Sustainability/Frontiers papers, or draw China provincial maps and SHAP plots in that exact style.
---

# Yile Paper Style

这个 skill 封装两件事：

1. **语言风格**：证据优先、因果克制、模块化推进、政策收尾的英文实证论文写法。
2. **制图风格**：Times New Roman 加粗、viridis SHAP、亮色五级中国地图、多面板预测散点。

所有默认值来自五篇论文的实际测量，不是泛化的“学术风”。先读参考文件，再动手。

## 何时使用

- 用户说“按我论文的风格写/改”“像我之前那篇 Systems/Scientific Reports 一样”。
- 要画或复刻：中国省级地图、SHAP summary、SHAP dependence、模型预测散点、多面板 ML 图。
- 要写/改：摘要、引言、数据与方法、结果、讨论、结论、cover letter、审稿回复。
- 要检查：句子节奏、因果措辞、拼写一致性、图表引用、期刊格式。

## 快速开始

```bash
cd ~/.agents/skills/yile-paper-style

# 重新生成四张 1:1 复刻预览图
python scripts/build_examples.py

# 中国地图（CSV: province, year, value）
python scripts/china_map.py \
  --data assets/data/epi_panel.csv \
  --out "$HOME/paper-style-output/fig06_china_epi_4panel.png" \
  --years 2003 2010 2015 2020 --value epi --label EPI

# SHAP 蜂群 + 条形
python scripts/shap_plots.py \
  --npz assets/data/shap_demo.npz --kind summary \
  --out "$HOME/paper-style-output/fig11_shap_combo.png"

# SHAP 依赖图（指定论文里的前六个特征）
python scripts/shap_plots.py \
  --npz assets/data/shap_demo.npz --kind dependence \
  --out "$HOME/paper-style-output/fig13_shap_dependence.png" \
  --features GDP EI PGPC FCR UR SSI

# 12 模型预测散点
python scripts/pred_scatter.py \
  --data assets/data/model_predictions.csv \
  --out "$HOME/paper-style-output/fig15_prediction_scatter.png"

# 语言风格体检
python scripts/style_lint.py manuscript.docx --journal mdpi
```

所有脚本同时写 PNG 和 PDF；输出目录会自动创建。**不要把用户图写到 skill 目录里**：`build_examples.py` 是唯一会写 `assets/previews/` 的脚本。**不要覆盖原始 PDF、ZIP 或任何 GitHub 仓库。**

## 画图决策树

| 要画的图 | 用什么 |
|---|---|
| 中国省级分级地图（2×2、3×2、3×3） | `scripts/china_map.py` |
| 单面板 SHAP 蜂群+条形 | `scripts/shap_plots.py::summary_combo` |
| 多面板 SHAP（区域/权重/稳健性） | `scripts/shap_plots.py::summary_grid` |
| SHAP 依赖图（2×3） | `scripts/shap_plots.py::dependence_grid` |
| 多模型 true-vs-predicted 散点 | `scripts/pred_scatter.py` |
| 研究框架/技术路线/泳道图 | `research-flowchart` skill（本 skill 提供字体/配色） |
| 相关系数热图、3D KDE、系数森林图 | 按 `references/figure-style.md` 第 8 节手写；暂无封装 |
| 三线表 | 按 `references/figure-style.md` 第 9 节 |

## 中国地图

### 数据契约

CSV 至少三列：

```csv
province,year,epi
北京,2003,0.272308
内蒙古,2010,0.301000
```

- `province` 可写简称（北京）或全称（北京市），脚本自动规范化。
- `year` 为整数；`epi` 为数值；缺失省份显示白色。
- 默认分级：`0–0.25 / 0.25–0.40 / 0.40–0.55 / 0.55–0.70 / 0.70–0.85`。
- 默认配色：`#38A800 / #8BD100 / #FFFF00 / #FF8000 / #FF0000`。

### 复用方式

```python
import pandas as pd
from china_map import plot_china_panels

df = pd.read_csv("my_panel.csv")
plot_china_panels(
    df, years=[2003, 2010, 2015, 2020],
    out_path="path/to/your/output/map.png",
    value_col="epi", legend_title="EPI", title_suffix="EPI Value",
)

# 顺序色阶（DEI/CEI 那种蓝/绿地图）
from china_map import PALETTES
colors, breaks, labels = PALETTES["blue"]
plot_china_panels(df, [2011, 2016, 2022], "path/to/your/output/dei_map.png",
                  palette=colors, breaks=breaks, labels=labels,
                  legend_title="DEI", title_suffix="DEI")
```

改顺序色阶（如 DEI/CEI 蓝绿地图）：用内置 `PALETTES["blue"]` / `PALETTES["green"]`，或传自己的 `palette/breaks/labels`。命令行可用 `--palette blue` 或 `--palette green`。改图幅/投影：改 `china_map.ALBERS` 与 `MAIN_BOX`。

### 必须保留的地图元素

- 左下五级色块图例（标题斜体）。
- 右上指北针。
- 右下南海小图（含海南岛与南海诸岛；九段线为示意）。
- 底部 `0 170 340 Miles` 比例尺。
- 台湾作为省级面并入省界图层；数据里没有台湾时按无数据浅灰显示，有台湾数据时按数据着色。不添加任何台湾文字标注。
- 无数据省份（台湾、西藏等）浅灰填充，但保留省界。

正式投稿若期刊要求官方边界，把 `_draw_inset` 里的示意九段线替换为有审图号的官方边界文件；不要直接删掉南海小图。

## SHAP 图

### 数据契约

```python
summary_combo(
    shap_values,       # (n_samples, n_features) 或 (n, lookback, n_features)
    feature_values,    # 同形状，原始值，用于蜂群着色
    feature_names,     # list[str]
    out_path="path/to/your/output/fig11_shap_combo.png",
)
```

- 3D 输入会沿 lookback 取平均，与论文 LSTM-SHAP 一致。
- 多分类模型：传目标类别的 SHAP 矩阵。
- 4D 且最后一维为 1：脚本会自动 squeeze。

### 从模型直接接到图

```python
import shap
from shap_plots import summary_combo

explainer = shap.TreeExplainer(model)
sv = explainer.shap_values(X_test)          # XGBoost / CatBoost / RF
summary_combo(sv, X_test, feature_names,
              out_path="path/to/your/output/shap_summary.png")
```

LSTM / 深度学习：

```python
sv = explainer.shap_values(X_test)          # (n, lookback, features)
summary_combo(sv, X_test.mean(axis=1), feature_names,
              out_path="path/to/your/output/shap_lstm.png")
```

多面板：

```python
from shap_plots import summary_grid
panels = [
    {"shap_values": sv_ewm, "feature_values": X, "feature_names": names,
     "title": "SHAP Summary (EWM)"},
    {"shap_values": sv_critic, "feature_values": X, "feature_names": names,
     "title": "SHAP Summary (CRITIC)"},
    {"shap_values": sv_cv, "feature_values": X, "feature_names": names,
     "title": "SHAP Summary (CV)"},
    {"shap_values": sv_dm, "feature_values": X, "feature_names": names,
     "title": "SHAP Summary (DM)"},
]
summary_grid(panels, out_path="path/to/your/output/shap_robustness.png", ncols=2)
```

依赖图：

```python
from shap_plots import dependence_grid
dependence_grid(sv, X, feature_names,
                features=["GDP", "EI", "PGPC", "FCR", "UR", "SSI"],
                out_path="path/to/your/output/shap_dependence.png",
                thresholds={"GDP": 30179.43, "EI": 0.99})  # 可选
```

不传 `thresholds` 时，阈值取 LOWESS 曲线斜率绝对值最大的 x（最陡转折点）。

## 预测散点

```python
import pandas as pd
from pred_scatter import prediction_scatter_grid

df = pd.read_csv("predictions.csv")  # Model, True_Value, Predicted_Value
prediction_scatter_grid(df, out_path="path/to/your/output/prediction_grid.png",
                        model_order=["SSA-LSTM", "LSTM", "GBDT", "RF"])
```

- 散点按二维 KDE 着色；回归线 OLS + 95% CI；红色 1:1 虚线。
- 负 R² 显示为 0.001；图注要说明。
- 共享颜色条与底部三列图例自动生成。

## 写作流程

1. **先读** `references/writing-style.md`，确认目标期刊与章节。
2. **定结构**：用五步摘要、五段引言、四拍结果、五段讨论、五段结论。
3. **写内容**：先给证据/数字，再解释；每个结果段至少一次图表引用。
4. **控因果**：默认用 “is associated with / contributes to / suggests / indicates”；讨论末尾加边界句。
5. **做体检**：`python scripts/style_lint.py draft.docx --journal mdpi`。
6. **再润色**：只改清楚度和一致性，不把口语化/公式化的“你的声音”改成通用 AI 腔。

写作时优先保留这些“签名动作”：

- “This study develops/constructs...” 开方法。
- “The results show/indicate...” 开结果。
- “Overall / In contrast / At the same time” 做转折。
- “These findings provide several practical implications for policymakers. First, ... Second, ... Third, ...”
- “Several limitations remain. Future research can extend this framework by...”

## 1:1 复刻流程

1. 用 `pymupdf` 把参考页渲染到 200 dpi，裁出原图。
2. 用 PIL 取主色、量长宽比、字号、图例顺序。
3. 选最接近的模板；按数据契约接数据。
4. 对齐字体、颜色、坐标轴、图例、留白。
5. 50% 透明度叠加对比；主色 RGB 距离 < 10，长宽比误差 < 2%。
6. 导出 PNG 300 dpi + PDF，记录到 `references/figure-catalog.md`。

不要“凭感觉”复刻；先量再画。

## 风格硬规则

- 字体 Times New Roman；标题、轴标签、刻度、图例加粗。
- 白底；完整四边框；网格只用浅灰虚线。
- 地图五级色必须用上面的精确 hex；SHAP/密度用 viridis。
- SHAP 条形 alpha 0.30、黑边 1.6，且必须在蜂群点后面。
- 预测散点：蓝回归线、浅蓝 95% CI、红色 1:1 虚线。
- 数据图内不放图表标题；只放 `(a)`/模型名。
- 负 R² → 0.001，并在图注说明。
- 结果段不写 “proves/causes”；用 “associated with/suggests/indicates”。
- 美式拼写；MDPI 用数字引用 [1]。
- 图注在图下、表题在表上、句末句号。

## 期刊适配

| 项目 | MDPI Systems/Sustainability | Scientific Reports | Frontiers |
|---|---|---|---|
| 章节 | 1., 1.1., 1.1.1. | 不编号 | 1, 2.1（不带点） |
| 摘要 | 一段 180–250 词 | 一段约 200 词 | Introduction/Methods/Results/Discussion |
| 关键词 | 5–6，分号 | 通常无 | 5–8，逗号 |
| 引用 | [1] | 上标数字 | 作者-年份 |
| 图注 | Figure 6. | Fig. 5. | FIGURE 3 |
| 人称 | we + this study | this study | this paper + this study |

详细规则见 `references/journal-profiles.md`。

## 质量检查

```bash
python scripts/build_examples.py
python scripts/style_lint.py draft.docx --journal mdpi
```

检查清单：

- [ ] 四张预览图能重新生成，且与原图版式一致。
- [ ] 地图有图例、指北针、比例尺、南海小图。
- [ ] SHAP 条形在点后面，顶部轴从 0 开始。
- [ ] 预测散点负 R² 已按 0.001 处理并注释。
- [ ] 摘要 180–250 词、一段、无引用/公式。
- [ ] 结果段有图表引用；讨论有因果边界句。
- [ ] 拼写一致（-ize / -or）。
- [ ] 没有改动任何 GitHub 仓库或原始数据。

## 边界与安全

- **只读输入**：原始 PDF、ZIP、仓库数据一律只读；输出写到用户指定目录。
- **不改 GitHub 仓库**：本 skill 的脚本在其自身目录运行；不要 `git add/commit/push` 用户的项目。
- **不编数据**：演示数据必须标注 `demo`；没有真实数据时不要伪造结果。
- **不删地图元素**：南海小图、九段线、指北针、比例尺是中国地图完整性的组成部分；正式投稿用官方边界文件替换示意线。
- **不覆盖原图**：复刻图另存新文件，保留原图用于对比。

## 文件地图

```
yile-paper-style/
├── SKILL.md
├── references/
│   ├── writing-style.md      # 语言风格、章节模板、句式库、自检
│   ├── figure-style.md       # 制图规格、颜色、地图/SHAP/散点细节
│   ├── figure-catalog.md     # 五篇论文插图清单与模板映射
│   └── journal-profiles.md   # MDPI / Nature / Frontiers 格式差异
├── scripts/
│   ├── paper_style.py        # rcParams、palette、保存、省名规范化
│   ├── china_map.py          # 中国省级地图（图例/指北针/比例尺/南海小图）
│   ├── shap_plots.py         # SHAP 组合、网格、依赖图
│   ├── pred_scatter.py       # 多模型预测散点
│   ├── style_lint.py         # 语言风格体检
│   └── build_examples.py     # 一键重生成四张预览图
└── assets/
    ├── geo/                  # 中国省界 + 台湾省多边形
    ├── data/                 # EPI、SHAP、模型预测示例数据
    └── previews/             # 四张 1:1 复刻图（PNG + PDF）
```
