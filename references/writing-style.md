# 论文语言风格画像

本文件从五篇论文中归纳：Systems 2026, 14, 319；Scientific Reports 2026, 16, 32263；Sustainability 2026, 18, 1283；Sustainability 2026, 18, 9871；Frontiers in Environmental Science 2026, 14, 1799258。默认面向英文实证论文（经济学 + 机器学习 + 空间分析），中文写作时保留同样的论证动作。

## 0. 一句话概括

**证据优先、因果克制、模块化推进、政策收尾。** 先用一句大背景把问题立起来，再用 “This study develops/constructs...” 交代研究设计，结果段用 “The results show/indicate...” 推进，讨论段用 “This suggests/may reflect...” 收住因果，最后用编号贡献与 First/Second/Third 政策含义结束。

## 1. 风格指纹（最像你的十个特征）

1. **第一句先立问题，不先报方法。** 摘要和引言的第一句通常是趋势、挑战或政策背景，而不是 “We propose a model”。
2. **“This study” 是主引擎。** Systems 一文出现 22 次，Scientific Reports 一文 27 次；MDPI 论文同时用 “we”，Nature 风格论文几乎不用 “we”。
3. **结果句高度公式化。** “The results show that...”, “The results indicate that...”, “As shown in Figure X...”, “Figure X compares...” 交替使用。
4. **因果语言非常克制。** 高频用 “associated with”, “contribute to”, “predictive correlate”, “explanatory contribution”；明确写 “should not be interpreted as causal evidence” 之类的边界。
5. **贡献写成编号清单。** (1)(2)(3) 每条先给一个名词短语标签，再解释 “This study develops... / This design helps...”。
6. **政策含义用 First/Second/Third。** 每一条都对应一个前面识别出的变量或区域类型，不写空泛口号。
7. **段落结构稳定：主题句 → 证据/数字 → 解释 → 限定。** 一个段落通常 4–8 句、80–180 词。
8. **限定词密集。** overall, generally, relatively, broadly, moderately, in the national sample, under this evaluation setting。
9. **美式拼写。** analyze, modeling, normalization, characterize, summarize, behavior；不混用 -ise/-our。
10. **图表引用密集、表注规范。** 每个结果段至少一次 “Figure X” 或 “Table X”，图注自足、句末带句号。

## 2. 宏观结构

| 部分 | 任务 | 典型长度 | 时态 | 人称 |
|---|---|---|---|---|
| Abstract | 背景 → 设计 → 数据/方法 → 结果 → 意义 | 180–250 词，一段 | 现在时 + 过去时 | 中性 |
| 1 Introduction | 背景 → 中国情境 → 文献三条线 → 缺口 → 本文 | 1,000–1,400 词 | 现在时为主 | this study / we |
| 2 Data and Methods | 数据、指标、公式、模型、评价指标 | 2,000–2,800 词 | 过去时为主 | this study / we |
| 3 Results | 图/表 → 模式 → 数字 → 解释 | 1,800–2,500 词 | 过去时 | 中性 |
| 4 Discussion | 机制、对照文献、稳健性、政策 | 1,500–2,200 词 | 现在时为主 | this study |
| 5 Conclusions | 总结 → 发现 → 含义 → 局限 → 未来 | 500–800 词 | 现在完成时 + 现在时 | this study |

MDPI 论文用数字编号（1., 1.1., 1.1.1.）；Scientific Reports 用不编号的 Introduction / Results / Discussion / Methods；Frontiers 用 1 Introduction、2 Literature review 之类的不带点的编号。**先看目标期刊，再决定编号。**

## 3. 摘要模板

五句法，一段，不引文献，不写公式：

1. **背景句**：一个趋势/挑战 + 为什么现在重要。
2. **设计句**：This study develops/constructs/examines + 一个框架/指数/模型。
3. **数据与方法句**：Using ... data (period), we first ... then ... / A ... model is used to ...
4. **结果句**：The results show/indicate that ... + 2–3 个具体发现 + 区域异质性。
5. **意义句**：These findings provide ... / Overall, the proposed framework provides ...

可直接套用的骨架：

> **[Context]** remains an important challenge for sustainable development in China, with pronounced regional disparities and evolving temporal dynamics that require **[what is missing]**. This study develops a **[framework/index/model]** that combines **[method 1]**, **[method 2]**, and **[method 3]**. Using **[data]** for China (**period**), we first **[step 1]**, then **[step 2]**. The results show that **[finding 1]**; **[finding 2]**; and **[finding 3]**, with notable regional heterogeneity. Overall, the proposed framework provides **[theoretical/practical value]** and offers a useful empirical reference for **[policy/management]**.

注意：
- 摘要里 **不要** 出现 “This paper is organized as follows”。
- 摘要里 **不要** 引用文献或公式。
- 关键词 5–6 个，MDPI 用分号分隔，首字母大写（专有名词除外）。

## 4. 引言模板

五段式漏斗。每段一个功能，不要在一段里同时做文献综述和贡献声明。

**第 1 段：全球背景。**
> In the context of global energy transition and sustainable development [1], **[problem]** has emerged as a critical issue that requires urgent attention worldwide [2].

**第 2 段：中国情境与政策。**
> This is especially true in China, where, despite **[progress]**, **[problem]** remains a pressing concern in certain regions [3]. The Chinese government has made **[policy goal]** a key policy objective, implementing **[measures]**, achieving significant progress. However, **[remaining gap]**.

**第 3 段：文献三条线。**
> Existing studies on **[topic]** can generally be divided into three strands. The first strand focuses on **[conceptual/measurement]**. ... The second strand pays more attention to **[spatial/dynamic]**. ... The third strand focuses on **[drivers/factors]**. ...

**第 4 段：缺口。**
> However, several gaps remain. First, **[gap 1]**. Second, **[gap 2]**. Third, **[gap 3]**. These gaps motivate the present study.

**第 5 段：本文与贡献。**
> To fill these gaps, this study **[design]**. The contributions of this study can be summarized as follows: (1) **[label]**: This study develops ... (2) **[label]**: This design helps ... (3) **[label]**: The results provide ...

**引言的语气**：先承认已有研究，再指出 “less understood / remains limited / has not been systematically examined”，不要用 “no one has studied” 这种绝对化表达。

## 5. 数据与方法模板

顺序固定：数据来源 → 样本与变量 → 指标构建 → 模型 → 评价指标 → 稳健性设计。

常用句式：

- 数据：
  > The data used in this study were collected from **[sources]**. The sample spans **[period]** and covers **[units]**.
- 变量：
  > Following **[literature]**, **[variable]** is measured as **[definition]**. The descriptive statistics are reported in Table **[X]**.
- 指标：
  > The entropy weight method is used to construct the composite index. The calculation steps are as follows. First, ... Second, ... Finally, ...
- 公式：
  > where \(x_{ij}\) denotes the value of the \(j\)-th indicator for province \(i\), and \(w_j\) is the corresponding weight.
- 模型：
  > The SSA-LSTM model consists of two components: SSA is used to optimize the hyperparameters of LSTM, and LSTM is used to capture the temporal dependence in the panel sequence.
- 评价：
  > The model is evaluated by RMSE, MAE, and \(R^2\). Lower RMSE and MAE and higher \(R^2\) indicate better predictive performance.
- 稳健性：
  > To examine whether the results depend on a single weighting method, we reconstruct the index using CRITIC, CV, DM, and PCA.

**方法段的三个习惯**：
1. 每个公式后面都要解释符号，不要只摆公式。
2. 每个模型选择都要给理由（“because it captures nonlinearity / avoids subjective weighting / is robust to outliers”）。
3. 方法段末尾用一句话交代评价口径（“under the chronologically ordered training/validation/testing framework”）。

## 6. 结果模板

一个结果段通常四拍：

1. **指图**：Figure X shows / As shown in Figure X / Figure X compares ...
2. **描述模式**：从高到低、从东到西、从早到晚，给出具体数字或排序。
3. **解释**：indicating / suggesting / implying + 一个克制的机制。
4. **限定**：in the national sample / under this specification / this pattern is broadly consistent with ...

示例（你的原句节奏）：

> Figure 13 shows the dependency patterns for the top six features. Overall, the relationship between feature values and SHAP contributions differs across variables. For GDP, the SHAP dependence pattern becomes increasingly negative as GDP rises, indicating that higher GDP levels are generally associated with lower model-predicted EPI. In contrast, EI exhibits predominantly positive SHAP contributions that increase with EI, suggesting that higher energy intensity is associated with higher model-predicted EPI.

注意：
- **不要** 在结果段写 “this proves” 或 “this demonstrates causality”。
- 比较不同模型时，先给指标，再给 “indicating improved out-of-sample prediction capability”。
- 稳健性结果用 “remains stable / broadly consistent / does not fundamentally alter”，不要写 “perfectly robust”。

## 7. 讨论模板

讨论不是结果复述，而是回答 “为什么会这样、和谁对话、有什么边界”。

**第 1 段：重申核心发现。**
> The findings reveal that **[core pattern]**. This pattern is consistent with **[literature]**, which suggests that **[mechanism]**.

**第 2 段：可能机制。**
> One possible explanation is that **[mechanism 1]**. Another explanation relates to **[mechanism 2]**. At the same time, **[alternative explanation]** cannot be ruled out.

**第 3 段：区域/群体异质性。**
> The regional results further show that the eastern region places more weight on **[factor 1]**, the western region highlights **[factor 2]**, while the central region gives greater importance to **[factor 3]**.

**第 4 段：政策含义。**
> These findings provide several practical implications for policymakers. First, **[implication 1]**. Second, **[implication 2]**. Third, **[implication 3]**.

**第 5 段：边界与局限。**
> Several limitations remain. The analysis is based on historical data and does not explicitly incorporate **[limitation]**. Future research can extend this framework by **[extension]**.

## 8. 结论模板

结论 = 摘要的“完成时”版本，不要引入新结果。

1. **研究回顾**：This study develops/constructs ... 
2. **主要发现**：The results show that ... ; The SHAP results indicate that ... ; The robustness analyses suggest that ...
3. **政策含义**：First/Second/Third（可与讨论合并，但结论里要更短）。
4. **局限**：Several limitations remain.
5. **未来**：Future research can ...

结论段的高频收尾：
> Overall, this study contributes a **[framework]** that combines **[A]**, **[B]**, and **[C]**. This integrated design improves the transparency and practical interpretability of **[topic]** compared with using **[single method]** alone.

## 9. 句子级规则

### 9.1 长度与节奏
- 平均句长 20–28 词；中位数 17–23 词。
- 超过 45 词的句子要拆。你的论文里长句多为“主句 + 两个从句 + 一个限定”，拆成两句更清楚。
- 一段只做一个论证动作：描述、解释、比较、限定，不要四件事挤在一段。

### 9.2 主语选择
- MDPI（Systems、Sustainability）：可以用 “we”，但 “This study” 仍然是主引擎。
- Scientific Reports：尽量不用 “we”，用 “This study / The analysis / The results”。
- Frontiers：可以用 “this paper / this study”，少用 “we”。

### 9.3 时态
- Methods：过去时（were collected, was used, were trained）。
- Results：过去时（showed, indicated, was concentrated）。
- Discussion：现在时（suggests, implies, remains）。
- Conclusions：现在完成时 + 现在时（has shown, remains, should）。

### 9.4 因果语言阶梯

| 强度 | 表达 | 使用场景 |
|---|---|---|
| 强因果（少用） | causes, leads to, drives, proves | 只有实验/准实验设计才用 |
| 中等（常用） | is associated with, contributes to, is linked to, predicts | 面板回归、SHAP、相关性 |
| 弱（高频） | may reflect, suggests, indicates, is consistent with, potentially | 机制解释、异质性讨论 |
| 边界（必备） | should not be interpreted as causal evidence; cannot rule out; is descriptive rather than causal | 讨论/稳健性 |

你的默认档位：**中等 + 弱 + 边界**。只有政策建议段可以稍微加强，但也要用 “can be used as / may help”。

### 9.5 连接词
高频且够用：Overall, However, Therefore, In contrast, In addition, At the same time, Specifically, Notably, Similarly, Meanwhile。
不要每段都用 “Moreover/Furthermore”；你的论文里这两个词反而很少。

## 10. 高频短语库

**指缺口**
- However, ... remains less understood.
- Few studies have systematically examined ...
- Existing studies often focus on ..., leaving ... underexplored.
- These gaps motivate the present study.

**指贡献**
- This study develops a ... framework that combines ...
- This design helps distinguish ... from ...
- The results provide provincial-level evidence on ...
- This integrated design improves the transparency and practical interpretability of ...

**指结果**
- The results show that ...
- The results indicate that ...
- As shown in Figure X, ...
- Figure X compares ...
- ... is concentrated in ...
- ... exhibits a clear ... pattern.
- ... remains stable across ...

**指解释**
- This indicates that ...
- This suggests that ...
- A possible explanation is that ...
- This pattern is broadly consistent with ...
- ... may reflect ...
- ... cannot be ruled out.

**指政策**
- These findings provide several practical implications for policymakers.
- First, ... Second, ... Third, ...
- ... can be used as a provincial early-warning and monitoring tool.
- Policy attention may focus on ...
- ... should be prioritized in ...

**指局限**
- Several limitations remain.
- The analysis is based on historical data and does not explicitly incorporate ...
- Future research can extend this framework by ...

## 11. 图表引用与标题

- 正文：`Figure 6 shows ...`、`As shown in Table 5 ...`、`Figure 11 compares ...`。句首大写 Figure/Table。
- 图注：`Figure 6. Heat maps of EPI values for specific years.` 句末句号；自足，不依赖正文。
- 表注：表题在表上方；显著性注释在表下方（`Note: *** p < 0.01 ...`）。
- 多面板：`(a)`, `(b)`, `(c)`，小写字母，面板标题加粗。
- 公式：`Equation (2)` 或 `Eq. (2)`；变量斜体，矩阵/向量加粗。

## 12. 期刊适配

| 项目 | MDPI Systems / Sustainability | Scientific Reports | Frontiers |
|---|---|---|---|
| 章节编号 | 1., 1.1., 1.1.1. | 不编号 | 1, 2.1（不带点） |
| 摘要 | 一段，180–250 词 | 一段，约 200 词 | 结构化：Introduction / Methods / Results / Discussion |
| 关键词 | 5–6 个，分号 | 通常不单列 | 5–8 个，逗号 |
| 引用 | 数字 [1] | 上标数字 | 作者-年份 (Zheng et al., 2025) |
| 图注 | `Figure 6.` | `Fig. 5.` | `FIGURE 3` |
| 人称 | we + this study | this study（少用 we） | this paper + this study |
| 文末 | Author Contributions / Funding / Data Availability / Conflicts of Interest | Data availability / Acknowledgements | Data availability / Author contributions / Funding / Conflict of interest |

**同一个研究投不同期刊时，只改格式层，不改论证层。** 不要把 Scientific Reports 的 “this study” 全改成 “we” 而不调整句法；也不要把 MDPI 的编号带进 Nature 风格稿件。

## 13. 自检清单

- [ ] 摘要是否 180–250 词、一段、无引用、无公式？
- [ ] 引言是否有“三条文献线 + 三个 gap + 编号贡献”？
- [ ] 每个结果段是否先指图/表，再给模式，再解释？
- [ ] 是否至少有一次明确的因果边界声明？
- [ ] 政策建议是否每条都对应一个实证发现？
- [ ] 是否混用了 -ise/-ize、behaviour/behavior、modelling/modeling？
- [ ] 是否有 “proves / obviously / clearly / undoubtedly / always / never” 等过度断言？
- [ ] 图注是否自足、句末有句号？
- [ ] 表题是否在表上方、注释在表下方？
- [ ] 数字与单位是否统一（%、亿元、万人、R²、95% CI）？

## 14. 不要做的事

1. 不要用 “This paper proves that ...” —— 你的论文从不这样写。
2. 不要在结果段堆砌 “significant” 而不给统计口径。
3. 不要把 “associated with” 改写成 “drives/causes”，除非设计支持。
4. 不要在一段里同时写文献、方法、结果、政策。
5. 不要用 “very / a lot of / huge / amazing” 这类口语强化词。
6. 不要为了“高级”而堆从句；你的风格是清楚，不是炫技。
7. 不要在摘要里写 “The rest of this paper is organized as follows”。
8. 不要把政策建议写成口号；每条都要落到变量、区域或工具上。
