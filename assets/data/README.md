# 示例数据说明

本目录中的 `epi_panel.csv`、`shap_demo.npz`、`model_predictions.csv` 是作者论文的示例数据。**公开 GitHub 仓库不包含这三个文件**，以免公开原始研究数据。代码、图库、边界文件和预览图不受影响。

要重新生成 `assets/previews/` 中的四张图，请在本目录准备以下文件。

## 1. `epi_panel.csv`

中国省级面板，至少三列：

```csv
province,year,epi
北京,2003,0.272308
内蒙古,2010,0.301000
台湾,2020,0.250000
```

- `province` 可用简称（北京、台湾）或全称（北京市、台湾省），脚本自动规范化。
- `year` 为整数；`epi` 为数值。
- 没有观测的省份（例如未纳入数据的台湾、西藏）会以浅灰填充、保留省界。
- 默认分级为 `0–0.25 / 0.25–0.40 / 0.40–0.55 / 0.55–0.70 / 0.70–0.85`；可在 `china_map.py` 的 `PALETTES` 或调用参数中改。

## 2. `shap_demo.npz`

用 NumPy 保存三个数组：

```python
import numpy as np
np.savez_compressed(
    "shap_demo.npz",
    shap_values=sv,        # (n_samples, n_features) 或 (n, lookback, n_features)
    feature_values=fv,     # 与 shap_values 同形状，原始特征值
    feature_names=names,   # 字符串数组，例如 ["GDP", "EI", ...]
)
```

- `shap_values` 可以是任意模型（XGBoost、CatBoost、LSTM 等）的 SHAP 矩阵。
- 3D 输入会沿 lookback 取平均，和论文 LSTM-SHAP 的做法一致。
- 可选数组：`y_true`、`y_pred`、`areas`、`years`，便于自己复核。

## 3. `model_predictions.csv`

多模型测试集预测，三列：

```csv
Model,True_Value,Predicted_Value
SSA-LSTM,0.119089,0.135633
LSTM,0.119089,0.141000
```

- 每个模型 60–120 行即可。
- `Model` 名称会直接作为面板标题；默认顺序在 `pred_scatter.py` 的 `main()` 里。

## 重新生成

```bash
cd C:\Users\93529\.agents\skills\yile-paper-style
python scripts/build_examples.py
```

如果文件缺失，脚本会打印缺失项并退出，不会写出半成品图。
