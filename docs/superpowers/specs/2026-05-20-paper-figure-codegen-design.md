# Paper Figure Codegen - Design Spec

**Date:** 2026-05-20
**Status:** Approved
**Scope:** Full implementation (17 plot types), Skill + Python package, English docs

---

## 1. Overview

A dual-layer system for generating publication-quality Python plotting code:

- **Skill layer** (SKILL.md + references/) — AI reads to make intelligent decisions about plot type, color, and style
- **Python package** (paper_figure_codegen/) — Programmatic code generation, CLI, data parsing, testable logic

Target users: researchers writing papers, preparing slides, or creating reports who need ready-to-run matplotlib scripts.

---

## 2. Project Structure

```
paper_image_skills/
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
├── paper_figure_codegen/
│   ├── __init__.py
│   ├── cli.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_spec.py
│   │   ├── data_parser.py
│   │   ├── color_system.py
│   │   └── style.py
│   ├── recipes/
│   │   ├── __init__.py
│   │   ├── grouped_bar.py
│   │   ├── stacked_bar.py
│   │   ├── horizontal_bar.py
│   │   ├── line_with_ci.py
│   │   ├── violin_box_scatter.py
│   │   ├── boxplot.py
│   │   ├── histogram_kde.py
│   │   ├── heatmap.py
│   │   ├── confusion_matrix.py
│   │   ├── scatter_regression.py
│   │   ├── multi_panel.py
│   │   ├── radar.py
│   │   ├── ternary.py
│   │   ├── eeg_topomap.py
│   │   ├── permutation_test.py
│   │   ├── raincloud.py
│   │   └── flowchart_composite.py
│   ├── templates/
│   │   ├── base.py.j2
│   │   ├── multi_panel.py.j2
│   │   └── statistical.py.j2
│   └── export.py
├── templates/
│   ├── base_matplotlib.py
│   ├── multi_panel.py
│   └── statistical_distribution.py
├── examples/
│   ├── grouped_bar_example.py
│   ├── violin_box_example.py
│   ├── confusion_matrix_example.py
│   ├── multi_panel_example.py
│   └── time_series_example.py
├── tests/
│   ├── test_data_parser.py
│   ├── test_color_system.py
│   ├── test_recipes.py
│   └── test_cli.py
├── pyproject.toml
└── docs/
    └── prd.md
```

### Layer responsibilities

| Layer | Path | Role |
|-------|------|------|
| Skill | SKILL.md, references/ | AI decision-making: plot type selection, color strategy, style guidance |
| Package | paper_figure_codegen/ | Programmatic code generation, CLI, data parsing, testable logic |
| Templates | paper_figure_codegen/templates/ | Jinja2 templates for code rendering |
| Examples | examples/ | Standalone runnable scripts for reference |

---

## 3. Core Data Flow

```
User Input (data / description / image)
    → DataParser.parse() → FigureDataSpec
    → PlotSelector.select(spec) → plot_type + recipe
    → ColorSystem.assign(plot_type, n_groups, semantic) → palette
    → Recipe.generate_code(spec, palette, style) → complete Python script
    → Exporter.save() → PNG + PDF + SVG
```

---

## 4. FigureDataSpec

```python
@dataclass
class FigureDataSpec:
    raw_input_type: str           # "dict_of_lists", "csv_path", "matrix", etc.
    data_kind: str                # "multi_series", "confusion_matrix", etc.
    x: Optional[Any] = None
    y: Optional[Any] = None
    groups: Optional[List[str]] = None
    values: Optional[np.ndarray] = None
    matrix: Optional[np.ndarray] = None
    labels: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggested_plot_types: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
```

### data_kind values

`single_series`, `multi_series`, `grouped_table`, `long_dataframe`, `wide_dataframe`, `matrix`, `confusion_matrix`, `time_series`, `distribution_groups`, `ranking_table`, `correlation_table`, `eeg_channel_table`, `multi_panel_spec`

### Identification rules

| Input pattern | data_kind | Candidate plots |
|---------------|-----------|-----------------|
| Multiple lists (dict of lists) | multi_series | boxplot, violin, line, grouped_bar |
| 2D numeric matrix | matrix / confusion_matrix | heatmap, annotated_heatmap, confusion_matrix |
| Long table (subject, session, value) | long_dataframe | grouped_bar, violin, boxplot, line, facet |
| Wide table (method, metric1, metric2) | wide_dataframe | grouped_bar, radar, heatmap |
| Feature importance (feature, score) | ranking_table | horizontal_bar, lollipop, coefficient_plot |
| EEG channels (channel, band, x, y, value) | eeg_channel_table | topomap, channel_importance_bar |

---

## 5. Color System

### Default palette

```python
PAPER_PALETTE = {
    "blue_main": "#5B8DB8",
    "blue_dark": "#3E6F95",
    "blue_light": "#BFD8EA",
    "teal_main": "#6FA8A6",
    "teal_dark": "#4D8583",
    "green_light": "#CFE8D5",
    "green_main": "#9CCB9E",
    "yellow_light": "#F3E6B3",
    "orange_light": "#E8B77D",
    "orange_main": "#D99A5E",
    "purple_light": "#C9BEDF",
    "pink_light": "#E7C1C0",
    "gray_light": "#E8ECEF",
    "gray": "#BFC7CD",
    "gray_dark": "#66727C",
    "positive": "#6FA8A6",
    "negative": "#D99A5E",
    "neutral": "#BFC7CD",
    "highlight": "#F3C567",
}
```

### Color assignment rules

| n groups | kind | Colors |
|----------|------|--------|
| 2 | binary | blue_main, orange_main |
| 3 | categorical | blue_main, green_main, orange_light |
| 4-6 | categorical | blue, teal, green, yellow, orange, purple (first n) |
| continuous | sequential | Blues colormap |
| positive/negative | diverging | orange → gray → blue |
| significant vs not | significance | dark + marker vs light gray + alpha |

### get_palette function

```python
def get_palette(n: int, kind: str = "categorical"):
    if kind == "categorical":
        base = [blue, teal, green, yellow, orange, purple]
        return base[:n] if n <= len(base) else plt.cm.tab20(...)
    if kind == "binary":
        return [blue_main, orange_main]
    if kind == "positive_negative":
        return [orange_main, gray_light, blue_main]
    if kind == "sequential":
        return "Blues"
    if kind == "diverging":
        return "RdBu_r"
```

---

## 6. Recipe Architecture

### Protocol

```python
class Recipe(Protocol):
    plot_type: str
    required_data_kind: List[str]

    def generate_code(self, spec: FigureDataSpec, palette, style) -> str: ...
    def validate(self, spec: FigureDataSpec) -> List[str]: ...
```

### Recipe list

**MVP (11):**
1. grouped_bar — model × metric comparison
2. stacked_bar — category composition
3. horizontal_bar — feature importance, ranking
4. line_with_ci — trends, learning curves
5. violin_box_scatter — distribution comparison
6. boxplot — simple distribution
7. histogram_kde — single distribution shape
8. heatmap — correlation, importance matrices
9. confusion_matrix — classification results
10. scatter_regression — relationships between variables
11. multi_panel — composite figures (GridSpec)

**V2 (6):**
12. radar — multi-metric profiles
13. ternary — three-component compositions
14. eeg_topomap — channel importance visualization
15. permutation_test — statistical test visualization
16. raincloud — enhanced distribution
17. flowchart_composite — method flow + results

### Generated code structure (every recipe)

```python
# 1. Module docstring
# 2. Imports
# 3. Config section (OUTPUT_DIR, FIG_NAME, DPI, SAVE_FORMATS)
# 4. Style section (PAPER_PALETTE, apply_paper_style)
# 5. Data loading (real data or example data with TODO)
# 6. Data validation
# 7. Plotting function
# 8. Save/export function
# 9. main()
```

---

## 7. Style Guide

### Font

```python
"font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
```

Chinese fallback (optional):
```python
"font.sans-serif": ["SimHei", "Arial Unicode MS", "Microsoft YaHei", "DejaVu Sans"]
```

### Axes

- Hide top/right spine
- Grid only on y-axis, alpha <= 0.35
- No heavy backgrounds

### Legend

- Simple plots: legend above or right
- Complex plots: separate legend panel
- Multi-panel: unified legend

### Export

| Format | DPI | Use case |
|--------|-----|----------|
| PNG | 300 (default), 600 (dense) | Quick preview |
| PDF | vector | Paper submission |
| SVG | vector | Post-editing |

---

## 8. Skill Layer (SKILL.md + references/)

### SKILL.md content

- Skill name: `paper-figure-codegen`
- Description: Generate ready-to-run Python matplotlib code for publication-quality scientific figures
- Trigger conditions: plotting code requests, paper-style figures, multi-panel figures, statistical plots, heatmaps, model comparison plots
- Exclusions: interactive dashboards, web visualization, pure image generation
- Required behaviors: always generate runnable code, prefer matplotlib + numpy + pandas, optional deps with fallback, include example data when missing

### references/ files

| File | Content |
|------|---------|
| data-structures.md | Data structure identification rules, data_kind taxonomy, candidate plots per kind |
| plot-selection.md | Decision tree for plot type, per-type use cases |
| color-system.md | Color rules, semantic mapping, get_palette usage |
| codegen-rules.md | Code structure, naming conventions, required modules |
| plot-recipes.md | Detailed recipes for all 17 plot types |
| style-guide.md | Font, axes, legend, grid visual specs |
| export-policy.md | Format, DPI, naming, batch export |
| troubleshooting.md | Common issues (font missing, dep absent, clipped labels) |

---

## 9. CLI

```bash
# Generate from data file
paper-figure codegen --data results.csv --plot grouped_bar --output figure_comparison

# Generate from description (with example data)
paper-figure codegen --plot violin --groups 3 --output figure_distribution

# List available plot types
paper-figure list-plots

# Generate multi-panel
paper-figure codegen --plot multi_panel --config panels.yaml
```

---

## 10. Quality Standards

1. Every generated script must run with `python script.py`
2. No dependency on user-local files unless user provides paths
3. Example data or read interface included
4. Clear config section at top of generated script
5. Function encapsulation (not all logic in main)
6. Data validation before plotting
7. Export function (PNG + PDF + SVG by default)
8. Paper/slide-suitable style
9. Unified color semantics
10. No disposable messy code
11. Optional dependencies (scipy, sklearn, mne) use try/except with fallback
12. Test coverage: each recipe tested to confirm generated code is executable via exec()

---

## 11. Dependencies

### Required

- Python >= 3.9
- matplotlib
- numpy
- pandas
- jinja2
- click (CLI)

### Optional

- scipy (statistical tests, KDE)
- scikit-learn (confusion matrix normalization)
- mne (EEG topomap)
- statsmodels (regression, CI)

### Dev

- pytest
- ruff (linting)
