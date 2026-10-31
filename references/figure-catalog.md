# 论文插图清单与模板映射

本文件把五篇论文的插图分成“已复刻 / 有模板 / 需另配工具”三类，方便以后按图索骥。

## 1. 已复刻（`assets/previews/`）

| 预览文件 | 对应原图 | 类型 | 说明 |
|---|---|---|---|
| `fig06_china_epi_4panel.png/.pdf` | Systems 2026, Fig. 6 | 中国省级分级地图 2×2 | 2003/2010/2015/2020；五级绿黄橙红；含台湾省级面；南海小图、指北针、比例尺 |
| `fig11_shap_combo.png/.pdf` | Systems 2026, Fig. 11（左） | SHAP 蜂群 + 条形组合 | 真实 LSTM checkpoint 计算的 SHAP 值；版式、配色、坐标轴与原图一致 |
| `fig13_shap_dependence.png/.pdf` | Systems 2026, Fig. 13 | SHAP 依赖图 2×3 | GDP/EI/PGPC/FCR/UR/SSI；LOWESS、中位数、阈值 |
| `fig15_prediction_scatter.png/.pdf` | Systems 2026, Fig. 15 | 12 模型预测散点 4×3 | 使用原文 `Test_Predictions_Long`，R²/MAE/RMSE 与原图逐项一致 |

> 复刻图的版式、字体、配色、图例顺序按原图；SHAP 数值来自保存的 `best_SSA_LSTM_checkpoint_manual_split.pth`，与论文正文的 SHAP 数值可能有小幅差异，但特征排序与方向一致。

## 2. 有模板、换数据即可复用

| 原图 | 类型 | 使用函数 | 备注 |
|---|---|---|---|
| Systems Fig. 11 右（no urban） | 双面板 SHAP 组合 | `summary_grid(panels, ncols=2)` | 两个 panel 字典，各自 `shap_values/feature_values/feature_names/title` |
| Systems Fig. 14 | 2×2 SHAP 稳健性 | `summary_grid(panels, ncols=2)` | EWM/CRITIC/CV/DM 四套 SHAP 值 |
| Systems Fig. 12 | 双面板预测散点 | `prediction_scatter_grid(df, ncols=2)` | 传入两个模型的 true/pred |
| Scientific Reports Fig. 7–9 | 全国/区域 SHAP | `summary_combo` / `summary_grid` | 区域面板可用 `title="Eastern Region"` |
| Scientific Reports Fig. 11 | 2×3 依赖图 | `dependence_grid` | 特征名按论文顺序传入 |
| Sustainability 18, 1283 Fig. 2 | DEI/CEI 地图 3×2 | `plot_china_panels(..., palette=PALETTES["blue"])` | 内置 `PALETTES["blue"]` / `PALETTES["green"]`；也可传自定义 `palette/breaks/labels` |
| Sustainability 18, 1283 Fig. 6 | 3D 核密度 | 暂无封装 | 用 `mpl_toolkits.mplot3d`；参考 `figure-style.md` 8.3 |
| fenvs Fig. 9 | Pearson 热图 | 暂无封装 | `imshow` + `RdBu_r`，中心 0；参考 `figure-style.md` 8.1 |
| fenvs Fig. 12 | 散点矩阵 | 暂无封装 | `pd.plotting.scatter_matrix` 或 `seaborn.pairplot`，需改成 Times 加粗 |

## 3. 需要专门工具（本 skill 不硬画）

| 原图 | 类型 | 建议 |
|---|---|---|
| Systems Fig. 1 | 四段式纵向泳道框架图 | 用 `research-flowchart` skill 或 PowerPoint；字体/配色用本 skill |
| Systems Fig. 2 | 能源贫困影响因素示意图 | 用 `research-flowchart` 或 draw.io |
| Systems Fig. 3–5 | SSA-LSTM 流程/结构图 | 用 `research-flowchart`；模型结构可用 `matplotlib` 方框+箭头 |
| Scientific Reports Fig. 1–2 | 研究框架/方法示意 | `research-flowchart` |
| Sustainability 18, 1283 Fig. 1 | 框架 + 迷你地图 | `research-flowchart` + 本 skill 地图裁切 |
| Sustainability 18, 9871 Fig. 1 | 概念模型（路径图） | PowerPoint / draw.io / TikZ |
| Sustainability 18, 9871 Fig. 2–5 | 系数图（点+95% CI） | 可用 `matplotlib errorbar`；森林图风格，暂无封装 |
| Scientific Reports Fig. 5 | 冷热点地图 3×3 | `china_map.py` 改 diverging 红蓝色阶与 3×3 布局；需改图例为连续色条 |
| Scientific Reports Fig. 6 | 3D 核密度 2×2 | `mpl_toolkits.mplot3d` |
| Sustainability 18, 1283 Fig. 5 | LISA 聚类地图 | `geopandas` + 分类色（红/蓝/灰）；需单独写分类图例 |

## 4. 图形语言速查

| 图型 | 关键识别特征 |
|---|---|
| 中国地图 | 亮绿→黄→橙→红五级；左下色块图例；右上指北针；右下南海小图；底部 0/170/340 Miles |
| SHAP 组合 | 左侧 viridis 蜂群；右侧半透明 viridis 条形；顶部 Mean |SHAP| 轴；右侧 High/Low 色条 |
| SHAP 依赖 | 散点按特征值着色；灰色 LOWESS；黑色中位数虚线；浅红阈值点线；三行图例 |
| 预测散点 | 密度着色；蓝色回归线+浅蓝置信带；红色 1:1 虚线；左上 R²/MAE/RMSE；底部三列图例 |
| 框架图 | 四段纵向泳道；左侧竖排阶段名；圆角矩形；低饱和填充；嵌入迷你图 |
| 系数图 | 点估计+95% CI；零线；变量按大小排序；常用于 TWFE/回归系数 |
| 3D 核密度 | 年份× resilience× density 曲面；viridis/coolwarm；四区域面板 |

## 5. 原始文件位置

- `C:\Users\93529\Desktop\systems-14-00319.pdf`
- `C:\Users\93529\Desktop\sr-WL,YW.pdf`
- `C:\Users\93529\Desktop\sustainability-18-09871.pdf`
- `C:\Users\93529\Desktop\10-论文文件\成果列表\fenvs-14-1799258.pdf`
- `C:\Users\93529\Desktop\10-论文文件\成果列表\sustainability-18-01283-with-cover.pdf`
- 代码与数据：`C:\Users\93529\Desktop\10-论文文件\成果列表\能源贫困预测.zip`（已解压到工作区只读分析，未改动原压缩包）

## 6. 复刻优先级

如果时间有限，优先复刻这四类，因为它们占你论文图表的绝大多数：

1. 中国省级地图（Fig. 6 / Fig. 2 / Fig. 5）
2. SHAP 蜂群+条形（Fig. 11 / Fig. 7–9）
3. SHAP 依赖图（Fig. 13 / Fig. 11）
4. 多模型预测散点（Fig. 12 / Fig. 15）

框架图、3D 核密度、系数图属于“锦上添花”，用专门工具画更快。
