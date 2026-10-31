# 论文制图风格规范

本文件是 `assets/previews/` 中复刻图的规格说明。所有数值来自对原图的取色与测量，不是“看着差不多”。

## 1. 视觉基因

- **字体**：Times New Roman；几乎所有文字加粗（标题、轴标签、刻度、图例、图注）。
- **背景**：纯白；不透明；不加水印、不用 seaborn 默认灰底。
- **坐标轴**：完整四边框，黑色，线宽 1.6–2.0；刻度朝外，宽 1.6–2.0，长 5–8。
- **网格**：仅浅灰虚线，alpha 0.25–0.35，线宽 0.8–1.0；能不用就不用。
- **配色**：SHAP/密度用 viridis；地图用高饱和五级绿黄橙红；回归线蓝色、置信带浅蓝、1:1 线红色虚线。
- **多面板**：`(a)`, `(b)`, `(c)` 小写字母，Times New Roman 加粗，放在面板上方居中。
- **导出**：PNG 300 dpi + PDF 矢量；`bbox_inches="tight"`；字体嵌入（pdf.fonttype 42）。

## 2. Matplotlib 全局参数

`scripts/paper_style.py` 中的 `apply_style()` 已封装。核心值：

```python
font.family      = "Times New Roman"
font.weight      = "bold"
font.size        = 11–12        # 单栏 10–11；双栏 11–12；大图 12–14
axes.labelsize   = base + 2
axes.titlesize   = base + 4
xtick.labelsize  = base
ytick.labelsize  = base
legend.fontsize  = base
axes.linewidth   = 1.8
xtick.major.width= 1.8
ytick.major.width= 1.8
xtick.major.size = 7
ytick.major.size = 7
grid.linestyle   = "--"
grid.alpha       = 0.30
grid.linewidth   = 1.0
mathtext.fontset = "stix"       # 数学字体与 Times 匹配
savefig.dpi      = 300
pdf.fonttype     = 42
```

> `apply_style()` 会抑制 matplotlib font manager 的 cosmetic fallback 日志。Windows 自带 Times New Roman Bold；导出后用 `pdffonts fig.pdf` 确认嵌入的是 `TimesNewRomanPS-BoldMT`。如果换成其他字体，重新检查这一项。

## 3. 配色表

### 3.1 中国地图五级分类（从 Systems 2026 Fig. 6 取色）

| 类别 | 区间 | 颜色 |
|---|---|---|
| 1 | 0.0000–0.2500 | `#38A800` 深绿 |
| 2 | 0.2501–0.4000 | `#8BD100` 黄绿 |
| 3 | 0.4001–0.5500 | `#FFFF00` 黄 |
| 4 | 0.5501–0.7000 | `#FF8000` 橙 |
| 5 | 0.7001–0.8500 | `#FF0000` 红 |

省界 `#4D4D4D`，国界黑色，外发光 `#D5D5D5`；无数据省份白色填充、灰色描边。

### 3.2 顺序色阶（Sustainability 2026, 18, 1283 的 DEI/CEI 地图）

```python
BLUE_SEQ  = ["#E8F1F8", "#C6DBEF", "#9ECAE1", "#6BAED6", "#3182BD", "#08519C"]
GREEN_SEQ = ["#E5F5E0", "#C7E9C0", "#A1D99B", "#74C476", "#41AB5D", "#238B45", "#006D2C"]
```

### 3.3 机器学习图

| 元素 | 颜色 |
|---|---|
| SHAP / 密度 | `viridis` |
| 回归线 | `#1F77B4` |
| 95% 置信带 | `#A6CEE3`, alpha 0.40 |
| 1:1 线 | `#D62728`, dashed, lw 1.5 |
| LOWESS 趋势 | `#7F7F7F`, lw 2.2 |
| 中位数线 | 黑色 dashed, lw 1.1 |
| 阈值线 | `#F4A6A6` dotted, lw 1.3 |
| SHAP 条形 | viridis, alpha 0.30, 黑色描边 1.6 |

## 4. 中国省级地图

脚本：`scripts/china_map.py`；示例：`assets/previews/fig06_china_epi_4panel.png`。

### 4.1 版式

- 2×2 面板；每个面板 6.15 × 5.0 英寸；整图约 12.3 × 10 英寸。
- 每个面板包含：主地图、左下五级图例、右上指北针、右下南海小图、底部比例尺。
- 面板标题：`2003 EPI Value`，Times New Roman，斜体 + 加粗，18 pt，居中放在地图上方。
- 图例标题：`EPI`，斜体 + 加粗；图例文字 8.2 pt 加粗；色块黑边 0.55。
- 比例尺：`0 170 340 Miles`；按投影米制计算，340 miles = 547,176 m；放在地图下方白边。
- 指北针：四角星 + 圆环 + N/E/S/W；放在右上白边，避免压住陆地。
- 南海小图：右下角，约占面板宽 19.5%、高 28.5%；显示海南岛及南海诸岛，黑色虚线示意九段线；无坐标刻度、无标题。
- 主图范围：经度 73–135°E，纬度 17.5–54°N；投影 Albers（`lat_1=25, lat_2=47, lon_0=105`）；南海诸岛从主图裁掉，放入小图。
- 台湾作为省级面并入省界图层；无数据时浅灰填充，有数据时按数据着色；不添加文字标注。
- 无数据省份（台湾、西藏等）浅灰 `#E6E6E6` 填充，保留省界。

### 4.2 数据契约

CSV 至少三列：

```
province,year,epi
北京,2003,0.272308
...
```

- `province` 可以是简称（北京）或全称（北京市）；脚本自动规范化。
- `year` 为整数；`epi` 为数值。缺失值会显示为白色。
- 默认年份 `2003 2010 2015 2020`；可通过 `--years` 改。
- 默认分级 `[0, .25, .40, .55, .70, .85]`；超出 0.85 的值归入红色。若要改分级，改 `MAP_BREAKS` 与 `MAP_LABELS`。

### 4.3 复刻时的注意点

1. **不要用 `gdf.plot()` 直接画整张 Hainan**：它的 MultiPolygon 会延伸到 3.8°N，把主图拉长；主图必须按 bbox 裁剪。
2. **GeoJSON 可能有自相交**：先 `shapely.make_valid`，再 `intersection`。
3. **南海小图不要用主图投影**：用经纬度坐标、`aspect="equal"`，否则小岛会变形。
4. **图例不要用 `ax.legend`**：五级色块用 `Rectangle` + `text` 手动画，位置和行距才可控。
5. **比例尺必须按投影单位计算**：不要用固定 axes 比例，否则不同图幅长度不一致。

## 5. SHAP 蜂群 + 条形组合图

脚本：`scripts/shap_plots.py::summary_combo`；示例：`assets/previews/fig11_shap_combo.png`。

### 5.1 版式

- 单面板约 9.5 × 5.8 英寸；双面板约 16 × 5.8；2×2 约 15.6 × 10.4。
- 左侧蜂群：`shap.summary_plot(..., plot_type="dot", cmap="viridis")`；点大小 36–40，alpha 0.90。
- 右侧叠加条形：`ax.twiny()`，`barh`，高度 0.72，viridis 颜色，alpha 0.30，黑色描边 1.6；描边与填充共用 0.30 alpha，所以视觉上是灰色边（与原图一致）。若要纯黑边，需单独画边或给 edgecolor 设 RGBA。条形必须在蜂群点后面（`ax2.set_zorder(ax.get_zorder()-1)`，`ax.patch.set_visible(False)`）。
- 顶部轴：`Mean |SHAP Value| (Feature Importance)`，加粗 12–13 pt，从 0 开始。
- 底部轴：`SHAP Value`；左侧轴：`Features`。
- 零线：黑色实线 1.7，alpha 0.70。
- 网格：x 轴浅灰虚线；`shap.summary_plot` 还会自带每条特征行的浅灰横向引导线，属于预期效果。
- 颜色条：右侧，宽约 3.2%；只标 `High` / `Low`，标签 `Feature value` 旋转 270°。
- 特征排序：按 mean |SHAP| 从大到小；`shap.summary_plot` 默认已排序。

### 5.2 数据契约

```python
summary_combo(
    shap_values,        # (n_samples, n_features)，或 (n, lookback, n_features)
    feature_values,     # 同形状；用于蜂群着色
    feature_names,      # list[str]
    out_path="fig11_shap_combo.png",
)
```

- 3D 输入会沿 lookback 取平均，和论文 LSTM-SHAP 的做法一致。
- `feature_values` 必须是原始值（不是标准化值），否则 x 轴不可解释。
- 颜色条是“每特征 min–max 归一化”的示意，不是跨特征统一数值；不要在图注里把它解释成绝对值。

## 6. SHAP 依赖图

脚本：`scripts/shap_plots.py::dependence_grid`；示例：`assets/previews/fig13_shap_dependence.png`。

- 2×3 或 1×N 面板；每面板约 5.3 × 4.2 英寸。
- 散点：x = 特征值，y = SHAP 值，颜色 = 特征值（viridis），点大小 30–36，alpha 0.88。
- 趋势线：LOWESS（frac 0.70），灰色 2.2。
- 水平虚线：y=0，灰色。
- 垂直虚线：中位数，黑色。
- 垂直点线：阈值，浅红 `#F4A6A6`。
- 图例：三行 `Median: ...` / `Threshold: ...` / `Trend Fit`，白底、浅灰边框、字号 8–9。
- 阈值：默认取 LOWESS 曲线斜率绝对值最大的 x（“最陡转折点”）；可以用 `thresholds={"GDP": 30179.43, ...}` 手工覆盖。
- x 轴标签用特征简称（GDP、EI、PGPC…），加粗 12–14；y 轴统一 `SHAP`。

## 7. 多模型预测散点

脚本：`scripts/pred_scatter.py`；示例：`assets/previews/fig15_prediction_scatter.png`。

- 4×3 网格，每面板约 4.15 × 3.15 英寸；整图约 16.6 × 9.5。
- 散点：x = True，y = Predicted；颜色 = 二维高斯 KDE（每面板归一化到 0–1，viridis）；点大小 26，alpha 0.88。
- 回归线：OLS，蓝色 2.0；95% 均值置信带：浅蓝 alpha 0.40。
- 1:1 线：红色虚线 1.5，范围取 x/y 联合最小最大 + 5% padding。
- 统计框：左上角三行 `R² = ... / MAE = ... / RMSE = ...`，字号 8.5–9，白色半透明底。
- 负 R² 显示为 0.001（与论文表 5 的注释一致），图注里说明。
- 面板标题 `(a) SSA-LSTM`，加粗 10–11。
- 共享颜色条：右侧，标签 `Density`，旋转 270°，无刻度。
- 共享图例：底部三列 `Regression Line / 95% Confidence Interval / 1:1 Line`。
- 轴标签：y 只在第一列，x 只在最后一行，减少拥挤。

## 8. 其他常见图型

### 8.1 相关系数热图

- 发散色 `RdBu_r`，范围 −1 到 1，中心 0 白色；或 `coolwarm`。
- 单元格数字保留两位小数；字体 7–9 加粗。
- 不画网格；边框细黑线。
- 上三角/下三角可只保留一半；对角线为 1。

### 8.2 时间序列/收敛曲线

- 线宽 1.8–2.2；颜色用深绿/深蓝/橙色区分算法。
- 图例放右上或图外下方；不要遮挡曲线。
- y 轴标签写全（`Best Fitness (RMSE)`），不要只写 `Value`。

### 8.3 三维核密度（Scientific Reports Fig. 6）

- `mpl_toolkits.mplot3d`；视角 elev 25–35、azim −60 到 −45。
- 曲面用 `viridis` 或 `coolwarm`；网格线细、透明。
- 四个面板共享 z 轴范围；面板标题 `(a) National` 等。

### 8.4 框架图/技术路线图

论文 Fig. 1 是“四段式纵向泳道”：左侧竖排阶段名，右侧圆角矩形+箭头+迷你图。建议：

- 用 PowerPoint 或 `research-flowchart` skill 画，再用本 skill 的字体/配色统一。
- 阶段名：`Data sources and mechanism analysis` / `Indicator calculation and basic analysis` / `Optimization and driver analysis` / `Top, robustness, convergence analysis`。
- 圆角矩形填充用低饱和绿/蓝/橙（如 `#D9EAD3`, `#CFE2F3`, `#FCE5CD`），边框深灰 1 pt。
- 迷你图直接从本 skill 的预览图裁切嵌入，保证字体一致。
- 不要用 matplotlib 硬画复杂框架图；文字对齐和箭头会失控。

## 9. 表格风格

- 三线表：顶线 1.5 pt、表头下线 1.0 pt、底线 1.5 pt；无竖线。
- 表题在表上方，`Table 5. Comparison of ...`，句末句号。
- 表注在表下方：`Note: *** p < 0.01, ** p < 0.05, * p < 0.1.`；标准误在括号内。
- 数字右对齐；小数位数统一（RMSE/MAE 三位，R² 三位，百分比一位或两位）。
- 负 R² 在表注中说明“displayed as 0.001 for readability”。

## 10. 导出与验收

1. 同时导出 PNG 300 dpi 和 PDF；PDF 用于投稿，PNG 用于预览。
2. 检查字体是否嵌入：`pdffonts fig.pdf`（Git Bash 可用 `pdffonts`）。
3. 检查最小字号：印刷后不小于 7 pt；图中文字建议 8–12 pt。
4. 检查裁切：`bbox_inches="tight"` 后确认图例/颜色条/面板标签没有被切。
5. 1:1 复刻验收：
   - 取原图主色，计算与预览图的 RGB 距离（应 < 10）。
   - 对齐面板长宽比（误差 < 2%）。
   - 对比标题、图例、坐标轴位置；用 50% 透明度叠加检查。
   - 不追求每个数据点一致，但版式、配色、字号、图例顺序必须一致。

## 11. 常见坑

- **`shap.summary_plot` 会自己建 colorbar**：用 `color_bar=False`，再手动加，才能放进网格。
- **`twiny` 的条形会盖住散点**：必须把 `ax2` 的 zorder 降到主 axes 之下，并把主 axes 背景设为透明。
- **地图 GeoJSON 自相交**：先 `make_valid`；否则 `intersection` 会报 `TopologyException`。
- **Hainan 的 MultiPolygon 包含南海诸岛**：主图必须裁到 17.5°N 以上，否则图幅被拉到 3.8°N。
- **颜色条范围**：SHAP 的颜色是逐特征归一化，不要用全局数值解释。
- **中文字体**：本 skill 默认英文图；中文图把 `font.family` 改成 `SimSun`/`Source Han Serif`，数学仍用 STIX。
- **负 R²**：不要直接显示负值；按论文口径显示 0.001 并在图注说明。
