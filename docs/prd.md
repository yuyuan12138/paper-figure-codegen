# 科研绘图代码生成 Skill PRD v1.0

## 1. Skill 名称

**paper-figure-codegen**

定位：面向论文、组会、答辩、科研报告的**绘图代码自动生成 Skill**。
目标不是直接画一张固定图，而是让 AI 根据用户给的数据、需求描述或参考图风格，生成**可直接运行、可复用、可审稿修改的 Python 绘图代码**。

该设计参考了 `figures4papers` 的 Skill 化组织方式：其仓库将核心说明放在 `SKILL.md`，并将 API、常见模式、设计理论、教程、demo 等拆分到 `references/` 目录中，便于 AI coding agent 按需读取。([GitHub][1])

---

## 2. 核心目标

这个 Skill 需要解决三个问题：

1. **数据结构解析**
   自动判断用户给的是列表、DataFrame、CSV、Excel、JSON、矩阵、字典、多组实验结果、时间序列、混淆矩阵、EEG 通道数据等，并转成统一的 `FigureDataSpec`。

2. **颜色选择与视觉规范**
   根据图类型、变量含义、论文风格自动选择颜色。参考你上传图中的风格：低饱和蓝绿灰为主，浅黄/橙色强调，适合论文图、答辩图和多面板分析图。

3. **代码生成**
   生成结构清晰、可运行、可复用的 Python 脚本，包括：

   * 数据读取
   * 数据校验
   * 图形绘制
   * 风格设置
   * 导出 PNG / PDF / SVG
   * 可修改配置区

---

## 3. 使用场景

### 3.1 应该触发 Skill 的情况

用户提出以下需求时触发：

* “帮我画论文图”
* “根据这些数据生成绘图代码”
* “画箱线图/小提琴图/热力图/柱状图/折线图”
* “我有多个列表，画对比图”
* “画成论文风格”
* “根据这张图的风格生成代码”
* “生成 matplotlib 代码”
* “我要可直接运行的科研绘图脚本”

### 3.2 不适用场景

不优先处理：

* 交互式 Dashboard，例如 Plotly Dash、Streamlit、ECharts
* GIS 地图
* 纯 UI 图标设计
* Figma / Illustrator 信息图
* 复杂三维建模图
* 不需要代码、只要图片生成的请求

这与 `figures4papers` 中“主要面向 matplotlib、论文/报告/幻灯片图形，而不是交互式可视化或 Illustrator-first 工作流”的定位类似。([GitHub][2])

---

## 4. 输入与输出

## 4.1 输入类型

Skill 需要支持以下输入：

```text
1. 直接粘贴的数据
   - list
   - dict
   - JSON
   - Python array
   - pandas DataFrame 文本
   - markdown 表格

2. 文件型数据
   - CSV
   - XLSX
   - JSON
   - TXT
   - NPY / NPZ，可选

3. 需求描述
   - “画三个模型的 Accuracy/F1 对比柱状图”
   - “画多个 subject 的 PERS 分布小提琴图”
   - “画 normalized confusion matrix”
   - “画和上传图类似的多面板 figure”

4. 参考风格
   - 用户上传的图片
   - 已有论文图
   - 指定配色、字体、大小、导出格式
```

## 4.2 输出内容

默认输出一个完整 Python 脚本：

```text
figure_xxx.py
```

脚本必须包含：

```python
# 1. imports
# 2. global config
# 3. style config
# 4. data loading / example data
# 5. data validation
# 6. plotting function
# 7. save/export function
# 8. main()
```

默认导出：

```text
outputs/figure_xxx.png
outputs/figure_xxx.pdf
outputs/figure_xxx.svg
```

---

# 5. Skill 文件结构设计

推荐目录结构如下：

```text
paper-figure-codegen/
├── SKILL.md
├── references/
│   ├── data-structures.md
│   ├── plot-selection.md
│   ├── color-system.md
│   ├── codegen-rules.md
│   ├── plot-recipes.md
│   ├── style-guide.md
│   ├── export-policy.md
│   └── troubleshooting.md
├── templates/
│   ├── base_matplotlib.py
│   ├── multi_panel.py
│   ├── statistical_distribution.py
│   ├── heatmap_confusion_matrix.py
│   ├── eeg_topomap_optional.py
│   └── paper_dashboard.py
└── examples/
    ├── grouped_bar_example.py
    ├── violin_box_example.py
    ├── confusion_matrix_example.py
    ├── multi_panel_example.py
    └── time_series_example.py
```

---

# 6. SKILL.md 设计

`SKILL.md` 应该是 AI 第一个读取的文件，内容要短、明确、可执行。

## 6.1 SKILL.md 建议内容

```markdown
---
name: paper-figure-codegen
description: >
  Generate ready-to-run Python matplotlib code for publication-quality scientific figures.
  Use this skill when the user asks for plotting code, paper-style figures, multi-panel figures,
  statistical plots, heatmaps, model comparison plots, or figure styles similar to uploaded academic images.
---

# Paper Figure Code Generation Skill

Use this skill to generate immediately runnable Python plotting scripts for scientific papers, slides, and reports.

## Core tasks

1. Parse user data into a unified FigureDataSpec.
2. Select an appropriate plot type based on data structure and user intent.
3. Choose publication-ready colors using semantic color rules.
4. Generate complete Python code with reusable functions.
5. Save figures as PNG, PDF, and SVG.

## When to use

- The user asks for plotting code.
- The user provides lists, tables, CSV/Excel/JSON data, matrices, or experiment results.
- The user asks for paper-style visualizations.
- The user references a figure image and wants similar style.
- The user asks for boxplot, violin plot, bar plot, heatmap, confusion matrix, trend plot, radar plot, EEG-style topomap, or multi-panel figure.

## When not to use

- Interactive dashboards.
- Web visualization unless explicitly requested.
- Pure image generation without code.
- Non-data-driven illustrations.

## Required behavior

- Always generate runnable code.
- Prefer matplotlib + numpy + pandas.
- Do not require seaborn unless clearly beneficial.
- Use optional dependencies only with fallback.
- Include example data when the user has not provided real data.
- Include clear TODO comments for user-replaced paths or variables.
- Export high-resolution figures.
- Keep code modular.
- Validate data shapes before plotting.

## Related references

- references/data-structures.md
- references/plot-selection.md
- references/color-system.md
- references/codegen-rules.md
- references/plot-recipes.md
- references/style-guide.md
- references/export-policy.md
- references/troubleshooting.md
```

---

# 7. 数据结构解析模块

## 7.1 统一数据描述对象

Skill 内部需要先把用户数据转成统一结构：

```python
@dataclass
class FigureDataSpec:
    raw_input_type: str
    data_kind: str
    x: Optional[Any]
    y: Optional[Any]
    groups: Optional[Any]
    values: Optional[Any]
    matrix: Optional[Any]
    labels: Optional[Any]
    metadata: dict
    suggested_plot_types: list[str]
    warnings: list[str]
```

## 7.2 data_kind 类型

```text
single_series
multi_series
grouped_table
long_dataframe
wide_dataframe
matrix
confusion_matrix
time_series
distribution_groups
ranking_table
correlation_table
eeg_channel_table
multi_panel_spec
```

## 7.3 数据结构识别规则

### 规则 1：多个 list

输入：

```python
data = {
    "Model A": [0.72, 0.75, 0.78],
    "Model B": [0.69, 0.71, 0.74],
    "Model C": [0.80, 0.82, 0.83],
}
```

识别为：

```text
data_kind = multi_series
候选图 = boxplot, violin, line, grouped_bar
```

### 规则 2：二维矩阵

输入：

```python
matrix = [[0.82, 0.10, 0.08],
          [0.15, 0.75, 0.10],
          [0.05, 0.12, 0.83]]
```

识别为：

```text
data_kind = matrix 或 confusion_matrix
候选图 = heatmap, annotated_heatmap, confusion_matrix
```

### 规则 3：长表格

输入：

```text
subject,session,emotion,value
S01,1,happy,0.61
S01,1,sad,0.23
S02,2,happy,0.58
```

识别为：

```text
data_kind = long_dataframe
候选图 = grouped_bar, violin, boxplot, line, facet_plot
```

### 规则 4：宽表格

输入：

```text
method,Accuracy,F1,AUC
Baseline,0.81,0.79,0.85
Ours,0.88,0.86,0.91
```

识别为：

```text
data_kind = wide_dataframe
候选图 = grouped_bar, radar, heatmap
```

### 规则 5：排名数据

输入：

```text
feature,importance
gamma,0.36
beta,0.24
alpha,0.19
```

识别为：

```text
data_kind = ranking_table
候选图 = horizontal_bar, lollipop, coefficient_plot
```

### 规则 6：EEG 通道数据

输入：

```text
channel,band,value,x,y
Fp1,alpha,0.21,-0.3,0.8
Fp2,alpha,0.18,0.3,0.8
```

识别为：

```text
data_kind = eeg_channel_table
候选图 = topomap, channel_importance_bar, band_importance_heatmap
```

---

# 8. 图类型选择规则

根据你上传的图片，Skill 应该重点支持以下科研图类型：

## 8.1 对比类

适合模型、方法、实验组比较。

```text
bar
grouped_bar
stacked_bar
horizontal_bar
lollipop
coefficient_ranking
```

典型用途：

```text
模型指标对比
特征重要性排名
subject-level 排名
不同实验设置对比
```

## 8.2 分布类

对应你图里的 violin、box、raincloud 风格。

```text
boxplot
violinplot
box + scatter
raincloud
histogram
kde
permutation_distribution
```

典型用途：

```text
多个 subject 的分布
session 间分布差异
模型结果稳定性
统计检验结果展示
```

## 8.3 矩阵类

```text
heatmap
confusion_matrix
correlation_matrix
importance_matrix
channel_band_heatmap
```

典型用途：

```text
混淆矩阵
相关性矩阵
特征 × 频段重要性
subject × emotion 分布
```

## 8.4 趋势类

```text
line
trend_with_ci
session_curve
time_series
learning_curve
```

典型用途：

```text
session 变化
训练过程
指标随时间变化
多组趋势对比
```

## 8.5 关系类

```text
scatter
scatter_with_regression
bubble
bland_altman_optional
```

典型用途：

```text
两个指标之间关系
subject-level correlation
效应量与 p-value
```

## 8.6 多面板综合图

你上传的图中有大量多面板论文图，因此 Skill 必须支持：

```text
multi_panel_grid
dashboard_figure
figure_with_flowchart_and_plots
summary_panel
```

建议布局：

```text
A. 数据流程图
B. 主要结果图
C. 分布图
D. 排名图
E. 统计检验图
F. 补充分析图
```

---

# 9. 颜色系统设计

`figures4papers` 使用了语义色板，例如蓝色表示核心方法，绿色表示提升，红色表示对照，灰色表示背景。([GitHub][3])
你的参考图则更偏向：

```text
低饱和蓝
低饱和青绿
浅绿色
浅黄色
柔和橙色
灰蓝色
淡紫色
```

## 9.1 推荐默认色板

```python
PAPER_PALETTE = {
    # main cold colors
    "blue_main": "#5B8DB8",
    "blue_dark": "#3E6F95",
    "blue_light": "#BFD8EA",

    # green / teal
    "teal_main": "#6FA8A6",
    "teal_dark": "#4D8583",
    "green_light": "#CFE8D5",
    "green_main": "#9CCB9E",

    # warm accent
    "yellow_light": "#F3E6B3",
    "orange_light": "#E8B77D",
    "orange_main": "#D99A5E",

    # purple / pink
    "purple_light": "#C9BEDF",
    "pink_light": "#E7C1C0",

    # neutral
    "gray_light": "#E8ECEF",
    "gray": "#BFC7CD",
    "gray_dark": "#66727C",

    # semantic
    "positive": "#6FA8A6",
    "negative": "#D99A5E",
    "neutral": "#BFC7CD",
    "highlight": "#F3C567",
}
```

## 9.2 颜色选择规则

### 二分类

```python
["blue_main", "orange_main"]
```

用途：

```text
correct vs incorrect
positive vs negative
ours vs baseline
```

### 三分类

```python
["blue_main", "green_main", "orange_light"]
```

用途：

```text
neutral / sad / happy
low / medium / high
baseline / variant / ours
```

### 四到六分类

```python
["blue_main", "teal_main", "green_main", "yellow_light", "orange_light", "purple_light"]
```

### 连续数值

```text
sequential: light blue -> dark blue
diverging: orange -> gray -> blue
```

### 正负值

```text
正值：blue / teal
负值：orange
零附近：gray
```

### 显著性

```text
显著：深色 + marker
不显著：浅灰 + alpha
```

## 9.3 颜色分配函数

生成代码时应该内置：

```python
def get_palette(n: int, kind: str = "categorical"):
    if kind == "categorical":
        base = [
            PAPER_PALETTE["blue_main"],
            PAPER_PALETTE["teal_main"],
            PAPER_PALETTE["green_main"],
            PAPER_PALETTE["yellow_light"],
            PAPER_PALETTE["orange_light"],
            PAPER_PALETTE["purple_light"],
        ]
        if n <= len(base):
            return base[:n]
        return plt.cm.tab20(np.linspace(0, 1, n))

    if kind == "binary":
        return [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    if kind == "positive_negative":
        return [PAPER_PALETTE["orange_main"], PAPER_PALETTE["gray_light"], PAPER_PALETTE["blue_main"]]

    if kind == "sequential":
        return "Blues"

    if kind == "diverging":
        return "RdBu_r"
```

---

# 10. 代码生成规范

## 10.1 必须使用的基础依赖

```python
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

可选依赖：

```python
scipy
sklearn
mne
statsmodels
```

要求：

```text
可选依赖必须 try/except。
没有安装时给出 fallback。
不能让脚本因为可选依赖缺失直接崩溃。
```

## 10.2 标准代码结构

生成的代码必须采用这个结构：

```python
"""
Publication-quality figure script.

Generated by paper-figure-codegen skill.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# Config
# =========================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_NAME = "figure_result"
SAVE_FORMATS = ["png", "pdf", "svg"]
DPI = 300


# =========================
# Style
# =========================

PAPER_PALETTE = {
    "blue_main": "#5B8DB8",
    "teal_main": "#6FA8A6",
    "green_main": "#9CCB9E",
    "yellow_light": "#F3E6B3",
    "orange_light": "#E8B77D",
    "orange_main": "#D99A5E",
    "purple_light": "#C9BEDF",
    "gray_light": "#E8ECEF",
    "gray": "#BFC7CD",
    "gray_dark": "#66727C",
}


def apply_paper_style(font_size=12, linewidth=1.2):
    plt.rcParams.update({
        "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": font_size,
        "axes.linewidth": linewidth,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
    })


# =========================
# Data
# =========================

def load_data():
    # Replace this example data with your own data.
    data = {
        "Baseline": [0.72, 0.75, 0.74, 0.76],
        "Method A": [0.78, 0.79, 0.80, 0.81],
        "Ours": [0.84, 0.85, 0.86, 0.87],
    }
    return data


def validate_data(data):
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError(f"All groups must have the same length, got lengths: {lengths}")


# =========================
# Plot
# =========================

def plot_figure(data):
    apply_paper_style(font_size=12)

    labels = list(data.keys())
    values = [np.asarray(v, dtype=float) for v in data.values()]

    fig, ax = plt.subplots(figsize=(5.5, 4))

    colors = [
        PAPER_PALETTE["blue_main"],
        PAPER_PALETTE["green_main"],
        PAPER_PALETTE["orange_light"],
    ]

    parts = ax.violinplot(values, showmeans=False, showmedians=False, showextrema=False)

    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(colors[i % len(colors)])
        body.set_edgecolor("black")
        body.set_alpha(0.65)
        body.set_linewidth(0.8)

    box = ax.boxplot(
        values,
        widths=0.18,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "black", "linewidth": 1.2},
        boxprops={"facecolor": "white", "edgecolor": "black", "linewidth": 1.0},
        whiskerprops={"color": "black", "linewidth": 1.0},
        capprops={"color": "black", "linewidth": 1.0},
    )

    rng = np.random.default_rng(42)
    for i, y in enumerate(values, start=1):
        x = rng.normal(i, 0.035, size=len(y))
        ax.scatter(
            x,
            y,
            s=18,
            color=colors[i - 1],
            edgecolor="white",
            linewidth=0.4,
            alpha=0.85,
            zorder=3,
        )

    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=0)
    ax.set_ylabel("Score")
    ax.set_title("Distribution Comparison")

    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.35)

    fig.tight_layout(pad=1.2)
    return fig


# =========================
# Export
# =========================

def save_figure(fig, name=FIG_NAME):
    saved_paths = []
    for fmt in SAVE_FORMATS:
        path = OUTPUT_DIR / f"{name}.{fmt}"
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        saved_paths.append(path)
    return saved_paths


def main():
    data = load_data()
    validate_data(data)
    fig = plot_figure(data)
    saved_paths = save_figure(fig)
    print("Saved files:")
    for path in saved_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
```

---

# 11. 图形配方库

## 11.1 grouped bar

适用：

```text
模型 × 指标
方法 × 数据集
消融实验
```

必须包含：

```text
误差条可选
数值标注可选
legend 放在图外或上方
y 轴从合理范围开始
```

## 11.2 stacked bar

适用：

```text
类别组成比例
情绪分布
session 内样本构成
```

必须包含：

```text
每一组总和校验
支持百分比
支持 absolute count
```

## 11.3 violin + box + scatter

适用：

```text
分布比较
多个 subject
多个 session
多个模型 seed
```

必须包含：

```text
violin 表示分布
box 表示四分位
scatter 表示原始点
median 标注可选
```

## 11.4 confusion matrix

适用：

```text
分类模型结果
情绪识别结果
多分类任务
```

必须包含：

```text
normalize 参数
百分比显示
自动选择 cmap
支持 diagonal emphasis
```

## 11.5 ranking bar

适用：

```text
feature importance
subject ranking
region importance
coefficient ranking
```

必须包含：

```text
横向条形图
自动排序
正负颜色区分
数值标注
```

## 11.6 EEG topomap optional

适用：

```text
通道重要性
频段分析
脑区可视化
```

实现策略：

```text
优先使用 mne
如果没有 mne，则用二维散点 + 插值近似 topography
```

## 11.7 multi-panel figure

适用：

```text
完整论文主图
方法流程 + 实验结果
A/B/C/D 子图组合
```

必须包含：

```text
GridSpec
panel label: A, B, C
统一字体
统一颜色语义
统一导出
```

---

# 12. 绘图风格规范

参考 `figures4papers` 的做法，论文图应采用极简坐标轴、无边框 legend、清晰字体、可编辑 vector text，并默认导出高分辨率图片。([GitHub][4])

## 12.1 字体

```python
"font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
```

中文图可使用：

```python
"font.sans-serif": ["SimHei", "Arial Unicode MS", "Microsoft YaHei", "DejaVu Sans"]
```

## 12.2 坐标轴

```text
默认隐藏 top/right spine
保留 left/bottom spine
网格线只用于 y 轴，且 alpha <= 0.35
不要使用过重背景
```

## 12.3 图例

```text
简单图：legend 放在上方或右侧
复杂图：单独 legend panel
多面板图：统一 legend
```

## 12.4 导出

```text
PNG: 300 dpi
PDF: 论文投稿
SVG: 后期编辑
复杂密集图: 600 dpi
```

---

# 13. 用户交互策略

## 13.1 数据足够时

直接生成代码，不反复追问。

例如用户给出：

```python
data = [[...], [...], [...]]
labels = ["A", "B", "C"]
```

Skill 应直接输出：

```text
完整 Python 脚本
```

## 13.2 数据不足时

仍然生成可运行模板，使用示例数据，并在代码里写：

```python
# TODO: Replace this example data with your real data.
```

## 13.3 只有图像参考时

根据参考图生成风格模板：

```text
多面板布局
低饱和配色
论文风格 rcParams
常见 plot function
```

不应该假装知道真实数据。

## 13.4 需要澄清的情况

只有当以下信息会明显改变图类型时才追问：

```text
用户没有说明 x/y 含义
矩阵不知道是否为 confusion matrix
分类标签和数值列无法判断
多文件数据关系不明确
```

---

# 14. 质量验收标准

生成的代码必须满足：

```text
1. 可以直接运行
2. 不依赖用户本地特殊文件，除非用户明确给了路径
3. 有示例数据或读取接口
4. 有清晰配置区
5. 有函数封装
6. 有数据校验
7. 有导出函数
8. 默认输出 PNG + PDF + SVG
9. 风格适合论文/答辩
10. 颜色语义统一
11. 不生成一次性杂乱代码
12. 不把所有逻辑堆在 main 里
```

---

# 15. Skill 内部决策流程

```text
Step 1: 读取用户需求
        ↓
Step 2: 判断是否为绘图代码生成任务
        ↓
Step 3: 解析数据结构
        ↓
Step 4: 判断候选图类型
        ↓
Step 5: 选择最合适图类型
        ↓
Step 6: 选择颜色系统
        ↓
Step 7: 生成完整 Python 脚本
        ↓
Step 8: 加入数据校验和导出逻辑
        ↓
Step 9: 给出使用说明
```

---

# 16. Prompt 模板

## 16.1 用户调用模板

```text
请使用 paper-figure-codegen skill 生成一份可直接运行的 Python 绘图代码。

数据如下：
<粘贴数据>

绘图目标：
<说明想画什么>

风格要求：
论文风格，参考上传图片中的低饱和蓝绿橙配色，导出 png/pdf/svg。
```

## 16.2 Agent 内部执行提示

```text
You are using the paper-figure-codegen skill.

Tasks:
1. Parse the user's data into a FigureDataSpec.
2. Infer the best plot type from the data structure and user intent.
3. Use the paper-style muted palette.
4. Generate a complete runnable Python script.
5. Include validation, style config, plotting function, export function, and main().
6. Export PNG, PDF, and SVG.
7. If data is missing, include example data and TODO comments.
```

---

# 17. 第一版必须实现的图类型

MVP 建议先做这些，马上可用：

```text
1. grouped_bar
2. stacked_bar
3. horizontal_ranking_bar
4. line_with_ci
5. violin_box_scatter
6. boxplot
7. histogram_kde
8. heatmap
9. confusion_matrix
10. scatter_with_regression
11. multi_panel_grid
```

第二版再做：

```text
1. radar
2. ternary plot
3. EEG topomap
4. permutation test plot
5. raincloud plot
6. flowchart + data plot composite
```

---

# 18. 最小可用 Skill 骨架

最终你可以先写这几个文件：

```text
paper-figure-codegen/
├── SKILL.md
├── references/
│   ├── data-structures.md
│   ├── color-system.md
│   ├── plot-recipes.md
│   └── codegen-rules.md
└── templates/
    └── base_matplotlib.py
```

其中优先级：

```text
1. SKILL.md
2. codegen-rules.md
3. data-structures.md
4. color-system.md
5. plot-recipes.md
6. base_matplotlib.py
```

---

# 19. PRD 总结

这个 Skill 的核心不是“会画很多图”，而是形成一个稳定流程：

```text
用户数据/需求
→ 数据结构解析
→ 图类型选择
→ 颜色语义映射
→ 论文风格代码模板
→ 可运行绘图脚本
→ 多格式导出
```

你的上传图可以作为 Skill 的视觉目标：**多面板、低饱和、信息密度高、统计图为主、论文可用**。
`figures4papers` 可以作为 Skill 文件组织和风格规范参考：`SKILL.md + references/ + demos/templates` 的结构非常适合你现在要做的绘图代码生成工具。

[1]: https://github.com/ChenLiu-1996/figures4papers "GitHub - ChenLiu-1996/figures4papers: My Python scripts to make high-quality figures for publications in top AI conferences and journals. · GitHub"
[2]: https://raw.githubusercontent.com/ChenLiu-1996/figures4papers/main/scientific-figure-making/SKILL.md "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/ChenLiu-1996/figures4papers/main/scientific-figure-making/references/api.md "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/ChenLiu-1996/figures4papers/main/scientific-figure-making/references/design-theory.md "raw.githubusercontent.com"
