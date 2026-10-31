# 复刻预览图

这四张图是“版式复刻”，不是把原 PDF 的像素直接贴回来。它们由本 skill 的脚本从示例数据重新绘制，字体、配色、面板布局、图例顺序按原图对齐。

| 文件 | 对应原图 | 数据 | 说明 |
|---|---|---|---|
| `fig06_china_epi_4panel.png/.pdf` | Systems 2026, Fig. 6 | `assets/data/epi_panel.csv` | 2003/2010/2015/2020；五级绿黄橙红；南海小图、指北针、比例尺 |
| `fig11_shap_combo.png/.pdf` | Systems 2026, Fig. 11（左） | `assets/data/shap_demo.npz` | 由保存的 LSTM checkpoint 计算 SHAP；蜂群 + 条形；viridis |
| `fig13_shap_dependence.png/.pdf` | Systems 2026, Fig. 13 | `assets/data/shap_demo.npz` | GDP/EI/PGPC/FCR/UR/SSI；LOWESS、中位数、阈值 |
| `fig15_prediction_scatter.png/.pdf` | Systems 2026, Fig. 15 | `assets/data/model_predictions.csv` | 12 模型；密度着色；OLS + 95% CI；1:1 线；R² 与原图一致 |
| `_contact_sheet.png` | — | 上面四张 | 2×2 总览，方便快速检查 |

## 重新生成

```bash
cd C:\Users\93529\.agents\skills\yile-paper-style
python scripts/build_examples.py
```

## 说明

- **地图**：省界来自 `assets/geo/china_provinces.geojson`（31 个省级单元，含西藏），并叠加 `assets/geo/taiwan_province.geojson` 的台湾省多边形。台湾作为省级面加入；无数据时浅灰显示，不加文字标注。南海诸岛用海南 MultiPolygon 的岛礁部分；九段线是示意线，正式投稿请替换为官方边界文件。
- **SHAP**：`shap_demo.npz` 由 `best_SSA_LSTM_checkpoint_manual_split.pth` 在 2020–2022 测试窗口上计算，沿 lookback 取平均。数值与论文正文可能略有差异，但特征排序和方向一致。
- **预测散点**：直接使用原项目 `Model_Comparison_12Models_manual_split.xlsx` 的 `Test_Predictions_Long`，所以 R²/MAE/RMSE 与论文表 5 对应。
- **负 R²**：按论文口径显示为 0.001；正式图注请加一句“Values below zero are displayed as 0.001 for readability.”
- **颜色**：地图五级色为 `#38A800 / #8BD100 / #FFFF00 / #FF8000 / #FF0000`；SHAP/密度为 viridis。

## 验收

- 主色 RGB 距离 < 10；
- 面板长宽比误差 < 2%；
- 标题、图例、坐标轴、颜色条位置与原图一致；
- 负 R²、图例顺序、面板字母顺序无遗漏。
