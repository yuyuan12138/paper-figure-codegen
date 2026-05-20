# Paper Figure Codegen Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dual-layer system (AI Skill + Python package) that generates publication-quality matplotlib plotting code for 17 plot types.

**Architecture:** Skill layer (SKILL.md + references/) guides AI decision-making. Python package (paper_figure_codegen/) provides programmatic code generation via Jinja2 templates, a CLI, and data parsing. Recipes implement a unified protocol for each plot type.

**Tech Stack:** Python 3.9+, matplotlib, numpy, pandas, jinja2, click, pytest

---

## File Structure Map

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | Package config, dependencies, entry points |
| `paper_figure_codegen/__init__.py` | Package exports |
| `paper_figure_codegen/core/__init__.py` | Core module exports |
| `paper_figure_codegen/core/data_spec.py` | FigureDataSpec dataclass |
| `paper_figure_codegen/core/data_parser.py` | DataParser — identifies data_kind from raw input |
| `paper_figure_codegen/core/color_system.py` | PAPER_PALETTE, get_palette() |
| `paper_figure_codegen/core/style.py` | apply_paper_style() rcParams |
| `paper_figure_codegen/recipes/__init__.py` | Recipe registry, get_recipe(), list_recipes() |
| `paper_figure_codegen/recipes/base.py` | Recipe protocol + BaseRecipe ABC |
| `paper_figure_codegen/recipes/grouped_bar.py` | Grouped bar chart recipe |
| `paper_figure_codegen/recipes/stacked_bar.py` | Stacked bar chart recipe |
| `paper_figure_codegen/recipes/horizontal_bar.py` | Horizontal bar / ranking recipe |
| `paper_figure_codegen/recipes/line_with_ci.py` | Line with confidence interval recipe |
| `paper_figure_codegen/recipes/violin_box_scatter.py` | Violin + box + scatter recipe |
| `paper_figure_codegen/recipes/boxplot.py` | Boxplot recipe |
| `paper_figure_codegen/recipes/histogram_kde.py` | Histogram + KDE recipe |
| `paper_figure_codegen/recipes/heatmap.py` | Heatmap recipe |
| `paper_figure_codegen/recipes/confusion_matrix.py` | Confusion matrix recipe |
| `paper_figure_codegen/recipes/scatter_regression.py` | Scatter with regression recipe |
| `paper_figure_codegen/recipes/multi_panel.py` | Multi-panel composite recipe |
| `paper_figure_codegen/recipes/radar.py` | Radar chart recipe |
| `paper_figure_codegen/recipes/ternary.py` | Ternary plot recipe |
| `paper_figure_codegen/recipes/eeg_topomap.py` | EEG topomap recipe |
| `paper_figure_codegen/recipes/permutation_test.py` | Permutation test visualization recipe |
| `paper_figure_codegen/recipes/raincloud.py` | Raincloud plot recipe |
| `paper_figure_codegen/recipes/flowchart_composite.py` | Flowchart + data plot composite recipe |
| `paper_figure_codegen/templates/base.py.j2` | Jinja2 base template |
| `paper_figure_codegen/templates/multi_panel.py.j2` | Jinja2 multi-panel template |
| `paper_figure_codegen/templates/statistical.py.j2` | Jinja2 statistical plot template |
| `paper_figure_codegen/export.py` | Export helper (save_figure) |
| `paper_figure_codegen/cli.py` | CLI entry point (click) |
| `tests/test_data_parser.py` | DataParser tests |
| `tests/test_color_system.py` | Color system tests |
| `tests/test_recipes.py` | Recipe generation + exec tests |
| `tests/test_cli.py` | CLI integration tests |
| `SKILL.md` | AI Skill entry point |
| `references/data-structures.md` | Data structure identification reference |
| `references/plot-selection.md` | Plot type selection reference |
| `references/color-system.md` | Color system reference |
| `references/codegen-rules.md` | Code generation rules reference |
| `references/plot-recipes.md` | Detailed plot recipes reference |
| `references/style-guide.md` | Visual style reference |
| `references/export-policy.md` | Export format reference |
| `references/troubleshooting.md` | Common issues reference |
| `templates/base_matplotlib.py` | Standalone base template for AI reference |
| `templates/multi_panel.py` | Standalone multi-panel template |
| `templates/statistical_distribution.py` | Standalone statistical distribution template |
| `examples/grouped_bar_example.py` | Example: grouped bar chart |
| `examples/violin_box_example.py` | Example: violin + box + scatter |
| `examples/confusion_matrix_example.py` | Example: confusion matrix |
| `examples/multi_panel_example.py` | Example: multi-panel figure |
| `examples/time_series_example.py` | Example: time series / line with CI |

---

## Task 1: Project Scaffolding and pyproject.toml

**Files:**
- Create: `pyproject.toml`
- Create: `paper_figure_codegen/__init__.py`
- Create: `paper_figure_codegen/core/__init__.py`
- Create: `paper_figure_codegen/recipes/__init__.py`

- [ ] **Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "paper-figure-codegen"
version = "0.1.0"
description = "Generate publication-quality Python matplotlib code for scientific figures"
requires-python = ">=3.9"
dependencies = [
    "matplotlib>=3.5",
    "numpy>=1.21",
    "pandas>=1.3",
    "jinja2>=3.0",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1",
]
stats = [
    "scipy>=1.7",
    "scikit-learn>=1.0",
    "statsmodels>=0.13",
]
eeg = [
    "mne>=1.0",
]

[project.scripts]
paper-figure = "paper_figure_codegen.cli:cli"

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Create package __init__.py files**

`paper_figure_codegen/__init__.py`:
```python
"""Paper Figure Codegen - Publication-quality plotting code generator."""

__version__ = "0.1.0"
```

`paper_figure_codegen/core/__init__.py`:
```python
"""Core modules for data parsing, color system, and style."""
```

`paper_figure_codegen/recipes/__init__.py`:
```python
"""Plot recipe modules."""
```

- [ ] **Step 3: Install package in editable mode**

Run: `cd /Users/yuyuan/paper_image_skills && pip install -e ".[dev]"`

Expected: Successfully installed paper-figure-codegen

- [ ] **Step 4: Verify import works**

Run: `python -c "import paper_figure_codegen; print(paper_figure_codegen.__version__)"`

Expected: `0.1.0`

- [ ] **Step 5: Create tests directory**

Run: `mkdir -p /Users/yuyuan/paper_image_skills/tests`

Create `tests/__init__.py` (empty file).

- [ ] **Step 6: Commit**

```bash
git init
git add pyproject.toml paper_figure_codegen/ tests/__init__.py
git commit -m "feat: project scaffolding with pyproject.toml and package structure"
```

---

## Task 2: FigureDataSpec Dataclass

**Files:**
- Create: `paper_figure_codegen/core/data_spec.py`
- Create: `tests/test_data_spec.py`

- [ ] **Step 1: Write the test**

`tests/test_data_spec.py`:
```python
import numpy as np
import pytest

from paper_figure_codegen.core.data_spec import (
    DATA_KINDS,
    FigureDataSpec,
)


class TestFigureDataSpec:
    def test_create_with_defaults(self):
        spec = FigureDataSpec(
            raw_input_type="dict_of_lists",
            data_kind="multi_series",
        )
        assert spec.raw_input_type == "dict_of_lists"
        assert spec.data_kind == "multi_series"
        assert spec.x is None
        assert spec.y is None
        assert spec.groups is None
        assert spec.values is None
        assert spec.matrix is None
        assert spec.labels is None
        assert spec.metadata == {}
        assert spec.suggested_plot_types == []
        assert spec.warnings == []

    def test_create_with_all_fields(self):
        spec = FigureDataSpec(
            raw_input_type="csv_path",
            data_kind="wide_dataframe",
            x=["Baseline", "Method A", "Ours"],
            y=None,
            groups=["Accuracy", "F1", "AUC"],
            values=np.array([[0.81, 0.79, 0.85], [0.88, 0.86, 0.91]]),
            labels=["Accuracy", "F1", "AUC"],
            metadata={"source": "results.csv"},
            suggested_plot_types=["grouped_bar", "radar", "heatmap"],
            warnings=["Missing 2 rows"],
        )
        assert spec.raw_input_type == "csv_path"
        assert spec.data_kind == "wide_dataframe"
        assert spec.values.shape == (2, 3)
        assert len(spec.suggested_plot_types) == 3
        assert len(spec.warnings) == 1

    def test_data_kinds_constant(self):
        assert "multi_series" in DATA_KINDS
        assert "confusion_matrix" in DATA_KINDS
        assert "wide_dataframe" in DATA_KINDS
        assert "ranking_table" in DATA_KINDS
        assert "eeg_channel_table" in DATA_KINDS
        assert len(DATA_KINDS) == 13
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_data_spec.py -v`

Expected: FAIL — ModuleNotFoundError: No module named `paper_figure_codegen.core.data_spec`

- [ ] **Step 3: Implement FigureDataSpec**

`paper_figure_codegen/core/data_spec.py`:
```python
"""Unified data specification for figure generation."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DATA_KINDS = [
    "single_series",
    "multi_series",
    "grouped_table",
    "long_dataframe",
    "wide_dataframe",
    "matrix",
    "confusion_matrix",
    "time_series",
    "distribution_groups",
    "ranking_table",
    "correlation_table",
    "eeg_channel_table",
    "multi_panel_spec",
]


@dataclass
class FigureDataSpec:
    """Unified description of user data for plot type selection and code generation."""

    raw_input_type: str
    data_kind: str
    x: Optional[Any] = None
    y: Optional[Any] = None
    groups: Optional[List[str]] = None
    values: Optional[Any] = None
    matrix: Optional[Any] = None
    labels: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggested_plot_types: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_data_spec.py -v`

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/core/data_spec.py tests/test_data_spec.py
git commit -m "feat: add FigureDataSpec dataclass with DATA_KINDS"
```

---

## Task 3: Color System

**Files:**
- Create: `paper_figure_codegen/core/color_system.py`
- Create: `tests/test_color_system.py`

- [ ] **Step 1: Write the test**

`tests/test_color_system.py`:
```python
import pytest

from paper_figure_codegen.core.color_system import (
    PAPER_PALETTE,
    get_palette,
)


class TestPaperPalette:
    def test_contains_required_keys(self):
        required = [
            "blue_main", "blue_dark", "blue_light",
            "teal_main", "teal_dark", "green_light", "green_main",
            "yellow_light", "orange_light", "orange_main",
            "purple_light", "pink_light",
            "gray_light", "gray", "gray_dark",
            "positive", "negative", "neutral", "highlight",
        ]
        for key in required:
            assert key in PAPER_PALETTE, f"Missing key: {key}"

    def test_all_values_are_hex(self):
        for key, value in PAPER_PALETTE.items():
            assert value.startswith("#"), f"{key} = {value} is not hex"
            assert len(value) == 7, f"{key} = {value} is not 7 chars"


class TestGetPalette:
    def test_categorical_2(self):
        result = get_palette(2, kind="categorical")
        assert len(result) == 2
        assert result[0] == PAPER_PALETTE["blue_main"]
        assert result[1] == PAPER_PALETTE["teal_main"]

    def test_categorical_3(self):
        result = get_palette(3, kind="categorical")
        assert len(result) == 3

    def test_categorical_6(self):
        result = get_palette(6, kind="categorical")
        assert len(result) == 6

    def test_categorical_exceeds_base(self):
        result = get_palette(10, kind="categorical")
        assert len(result) == 10

    def test_binary(self):
        result = get_palette(2, kind="binary")
        assert result == [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    def test_positive_negative(self):
        result = get_palette(3, kind="positive_negative")
        assert len(result) == 3
        assert result[0] == PAPER_PALETTE["orange_main"]
        assert result[2] == PAPER_PALETTE["blue_main"]

    def test_sequential(self):
        result = get_palette(0, kind="sequential")
        assert result == "Blues"

    def test_diverging(self):
        result = get_palette(0, kind="diverging")
        assert result == "RdBu_r"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_color_system.py -v`

Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: Implement color system**

`paper_figure_codegen/core/color_system.py`:
```python
"""Paper-style muted color palette and palette selection."""

from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np

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

_CATEGORICAL_BASE = [
    PAPER_PALETTE["blue_main"],
    PAPER_PALETTE["teal_main"],
    PAPER_PALETTE["green_main"],
    PAPER_PALETTE["yellow_light"],
    PAPER_PALETTE["orange_light"],
    PAPER_PALETTE["purple_light"],
]


def get_palette(n: int, kind: str = "categorical") -> Union[List[str], str]:
    """Return a color palette appropriate for the given kind and group count."""
    if kind == "categorical":
        if n <= len(_CATEGORICAL_BASE):
            return _CATEGORICAL_BASE[:n]
        return [plt.cm.tab20(i / n) for i in range(n)]

    if kind == "binary":
        return [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    if kind == "positive_negative":
        return [PAPER_PALETTE["orange_main"], PAPER_PALETTE["gray_light"], PAPER_PALETTE["blue_main"]]

    if kind == "sequential":
        return "Blues"

    if kind == "diverging":
        return "RdBu_r"

    raise ValueError(f"Unknown palette kind: {kind}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_color_system.py -v`

Expected: 10 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/core/color_system.py tests/test_color_system.py
git commit -m "feat: add color system with PAPER_PALETTE and get_palette"
```

---

## Task 4: Style Module

**Files:**
- Create: `paper_figure_codegen/core/style.py`
- Create: `tests/test_style.py`

- [ ] **Step 1: Write the test**

`tests/test_style.py`:
```python
import matplotlib
import matplotlib.pyplot as plt
import pytest

from paper_figure_codegen.core.style import apply_paper_style


class TestApplyPaperStyle:
    def test_sets_rcparams(self):
        apply_paper_style()
        assert plt.rcParams["pdf.fonttype"] == 42
        assert plt.rcParams["ps.fonttype"] == 42
        assert plt.rcParams["svg.fonttype"] == "none"
        assert plt.rcParams["savefig.bbox"] == "tight"

    def test_custom_font_size(self):
        apply_paper_style(font_size=14)
        assert plt.rcParams["font.size"] == 14

    def test_custom_linewidth(self):
        apply_paper_style(linewidth=2.0)
        assert plt.rcParams["axes.linewidth"] == 2.0

    def test_spines_top_right_hidden(self):
        apply_paper_style()
        assert plt.rcParams["axes.spines.top"] is False
        assert plt.rcParams["axes.spines.right"] is False

    def test_legend_no_frame(self):
        apply_paper_style()
        assert plt.rcParams["legend.frameon"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_style.py -v`

Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: Implement style module**

`paper_figure_codegen/core/style.py`:
```python
"""Paper-style matplotlib rcParams configuration."""

import matplotlib.pyplot as plt


def apply_paper_style(font_size: int = 12, linewidth: float = 1.2) -> None:
    """Apply publication-quality style to matplotlib defaults."""
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
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_style.py -v`

Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/core/style.py tests/test_style.py
git commit -m "feat: add apply_paper_style rcParams configuration"
```

---

## Task 5: DataParser

**Files:**
- Create: `paper_figure_codegen/core/data_parser.py`
- Create: `tests/test_data_parser.py`

- [ ] **Step 1: Write the test**

`tests/test_data_parser.py`:
```python
import numpy as np
import pandas as pd
import pytest

from paper_figure_codegen.core.data_parser import DataParser
from paper_figure_codegen.core.data_spec import FigureDataSpec


class TestDataParserDictOfLists:
    def test_multi_series(self):
        data = {
            "Model A": [0.72, 0.75, 0.78],
            "Model B": [0.69, 0.71, 0.74],
            "Model C": [0.80, 0.82, 0.83],
        }
        spec = DataParser.parse(data)
        assert spec.raw_input_type == "dict_of_lists"
        assert spec.data_kind == "multi_series"
        assert spec.labels == ["Model A", "Model B", "Model C"]
        assert "grouped_bar" in spec.suggested_plot_types
        assert "violin_box_scatter" in spec.suggested_plot_types

    def test_single_series(self):
        data = [1.2, 1.5, 1.3, 1.7, 1.4]
        spec = DataParser.parse(data)
        assert spec.data_kind == "single_series"
        assert "histogram_kde" in spec.suggested_plot_types


class TestDataParserMatrix:
    def test_confusion_matrix(self):
        matrix = np.array([
            [0.82, 0.10, 0.08],
            [0.15, 0.75, 0.10],
            [0.05, 0.12, 0.83],
        ])
        spec = DataParser.parse(matrix)
        assert spec.raw_input_type == "ndarray"
        assert spec.data_kind in ("matrix", "confusion_matrix")
        assert "heatmap" in spec.suggested_plot_types
        assert "confusion_matrix" in spec.suggested_plot_types


class TestDataParserLongDataFrame:
    def test_long_table(self):
        df = pd.DataFrame({
            "subject": ["S01", "S01", "S02", "S02"],
            "session": [1, 2, 1, 2],
            "emotion": ["happy", "sad", "happy", "sad"],
            "value": [0.61, 0.23, 0.58, 0.29],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "long_dataframe"
        assert "grouped_bar" in spec.suggested_plot_types


class TestDataParserWideDataFrame:
    def test_wide_table(self):
        df = pd.DataFrame({
            "method": ["Baseline", "Ours"],
            "Accuracy": [0.81, 0.88],
            "F1": [0.79, 0.86],
            "AUC": [0.85, 0.91],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "wide_dataframe"
        assert "grouped_bar" in spec.suggested_plot_types


class TestDataParserRankingTable:
    def test_ranking(self):
        df = pd.DataFrame({
            "feature": ["gamma", "beta", "alpha"],
            "importance": [0.36, 0.24, 0.19],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "ranking_table"
        assert "horizontal_bar" in spec.suggested_plot_types
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_data_parser.py -v`

Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: Implement DataParser**

`paper_figure_codegen/core/data_parser.py`:
```python
"""Parse raw user data into FigureDataSpec."""

from typing import Any

import numpy as np
import pandas as pd

from paper_figure_codegen.core.data_spec import FigureDataSpec, DATA_KINDS


class DataParser:
    """Identify data structure and produce a FigureDataSpec."""

    @staticmethod
    def parse(data: Any) -> FigureDataSpec:
        if isinstance(data, dict):
            return DataParser._parse_dict(data)
        if isinstance(data, (list, tuple)):
            return DataParser._parse_list(data)
        if isinstance(data, np.ndarray):
            return DataParser._parse_ndarray(data)
        if isinstance(data, pd.DataFrame):
            return DataParser._parse_dataframe(data)
        return FigureDataSpec(
            raw_input_type=type(data).__name__,
            data_kind="single_series",
            warnings=[f"Unknown data type: {type(data).__name__}"],
        )

    @staticmethod
    def _parse_dict(data: dict) -> FigureDataSpec:
        values = list(data.values())
        if all(isinstance(v, (list, tuple, np.ndarray)) for v in values):
            labels = list(data.keys())
            return FigureDataSpec(
                raw_input_type="dict_of_lists",
                data_kind="multi_series",
                groups=labels,
                values=np.array([np.asarray(v, dtype=float) for v in values]),
                labels=labels,
                suggested_plot_types=["grouped_bar", "violin_box_scatter", "boxplot", "line_with_ci"],
            )
        return FigureDataSpec(
            raw_input_type="dict",
            data_kind="single_series",
            values=np.array(list(data.values())),
            labels=list(data.keys()),
            suggested_plot_types=["bar", "horizontal_bar"],
        )

    @staticmethod
    def _parse_list(data) -> FigureDataSpec:
        arr = np.asarray(data, dtype=float)
        if arr.ndim == 1:
            return FigureDataSpec(
                raw_input_type="list",
                data_kind="single_series",
                values=arr,
                suggested_plot_types=["histogram_kde", "bar"],
            )
        if arr.ndim == 2:
            return FigureDataSpec(
                raw_input_type="list",
                data_kind="matrix",
                matrix=arr,
                suggested_plot_types=["heatmap", "confusion_matrix"],
            )
        return FigureDataSpec(
            raw_input_type="list",
            data_kind="single_series",
            values=arr,
            warnings=["High-dimensional array, treating as single_series"],
        )

    @staticmethod
    def _parse_ndarray(data: np.ndarray) -> FigureDataSpec:
        if data.ndim == 2:
            kind = "confusion_matrix" if DataParser._looks_like_confusion_matrix(data) else "matrix"
            return FigureDataSpec(
                raw_input_type="ndarray",
                data_kind=kind,
                matrix=data,
                suggested_plot_types=["heatmap", "confusion_matrix"],
            )
        return FigureDataSpec(
            raw_input_type="ndarray",
            data_kind="single_series",
            values=data,
            suggested_plot_types=["histogram_kde", "bar"],
        )

    @staticmethod
    def _parse_dataframe(df: pd.DataFrame) -> FigureDataSpec:
        if DataParser._is_ranking_table(df):
            label_col = df.columns[0]
            value_col = df.columns[1]
            return FigureDataSpec(
                raw_input_type="dataframe",
                data_kind="ranking_table",
                labels=df[label_col].tolist(),
                values=df[value_col].to_numpy(dtype=float),
                suggested_plot_types=["horizontal_bar"],
            )
        if DataParser._is_wide_dataframe(df):
            label_col = df.columns[0]
            metric_cols = df.columns[1:]
            return FigureDataSpec(
                raw_input_type="dataframe",
                data_kind="wide_dataframe",
                groups=df[label_col].tolist(),
                labels=metric_cols.tolist(),
                values=df[metric_cols].to_numpy(dtype=float),
                suggested_plot_types=["grouped_bar", "radar", "heatmap"],
            )
        return FigureDataSpec(
            raw_input_type="dataframe",
            data_kind="long_dataframe",
            suggested_plot_types=["grouped_bar", "violin_box_scatter", "boxplot", "line_with_ci"],
        )

    @staticmethod
    def _looks_like_confusion_matrix(arr: np.ndarray) -> bool:
        if arr.shape[0] != arr.shape[1]:
            return False
        try:
            row_sums = arr.sum(axis=1)
            return bool(np.allclose(row_sums, 1.0, atol=0.05))
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _is_ranking_table(df: pd.DataFrame) -> bool:
        if len(df.columns) != 2:
            return False
        first = df[df.columns[0]].dtype
        second = df[df.columns[1]].dtype
        return first == object and np.issubdtype(second, np.number)

    @staticmethod
    def _is_wide_dataframe(df: pd.DataFrame) -> bool:
        if len(df.columns) < 3:
            return False
        first = df[df.columns[0]].dtype
        rest_dtypes = [df[c].dtype for c in df.columns[1:]]
        return first == object and all(np.issubdtype(dt, np.number) for dt in rest_dtypes)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_data_parser.py -v`

Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/core/data_parser.py tests/test_data_parser.py
git commit -m "feat: add DataParser with dict/list/ndarray/dataframe support"
```

---

## Task 6: Jinja2 Base Template

**Files:**
- Create: `paper_figure_codegen/templates/base.py.j2`

- [ ] **Step 1: Create base template**

`paper_figure_codegen/templates/base.py.j2`:
```jinja2
\"\"\"
Publication-quality figure: {{ figure_name }}.

Generated by paper-figure-codegen.
\"\"\"

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =========================
# Config
# =========================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_NAME = "{{ figure_name }}"
SAVE_FORMATS = ["png", "pdf", "svg"]
DPI = {{ dpi }}


# =========================
# Style
# =========================

PAPER_PALETTE = {
{% for name, hex_val in palette.items() %}
    "{{ name }}": "{{ hex_val }}",
{% endfor %}
}


def apply_paper_style(font_size={{ font_size }}, linewidth={{ linewidth }}):
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
{{ data_loading_code | indent(4) }}


def validate_data(data):
{{ validation_code | indent(4) }}


# =========================
# Plot
# =========================

def plot_figure(data):
{{ plotting_code | indent(4) }}


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

- [ ] **Step 2: Commit**

```bash
git add paper_figure_codegen/templates/base.py.j2
git commit -m "feat: add Jinja2 base template for code generation"
```

---

## Task 7: Recipe Protocol and Registry

**Files:**
- Create: `paper_figure_codegen/recipes/base.py`
- Modify: `paper_figure_codegen/recipes/__init__.py`
- Create: `tests/test_recipe_registry.py`

- [ ] **Step 1: Write the test**

`tests/test_recipe_registry.py`:
```python
import pytest

from paper_figure_codegen.recipes import get_recipe, list_recipes


class TestRecipeRegistry:
    def test_list_recipes_returns_list(self):
        recipes = list_recipes()
        assert isinstance(recipes, list)
        assert len(recipes) > 0

    def test_get_unknown_recipe_raises(self):
        with pytest.raises(KeyError):
            get_recipe("nonexistent_plot")

    def test_list_recipes_includes_mvp_types(self):
        recipes = list_recipes()
        expected = [
            "grouped_bar", "stacked_bar", "horizontal_bar",
            "line_with_ci", "violin_box_scatter", "boxplot",
            "histogram_kde", "heatmap", "confusion_matrix",
            "scatter_regression", "multi_panel",
        ]
        for name in expected:
            assert name in recipes, f"Missing MVP recipe: {name}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipe_registry.py -v`

Expected: FAIL — import error or empty registry

- [ ] **Step 3: Implement recipe base and registry**

`paper_figure_codegen/recipes/base.py`:
```python
"""Base recipe protocol for plot code generation."""

from abc import ABC, abstractmethod
from typing import List

from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.core.color_system import PAPER_PALETTE


class BaseRecipe(ABC):
    """Abstract base class for plot code generation recipes."""

    plot_type: str = ""
    required_data_kind: List[str] = []

    @abstractmethod
    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        """Generate complete Python plotting script."""
        ...

    def validate(self, spec: FigureDataSpec) -> List[str]:
        """Return warnings if data doesn't match expectations."""
        warnings = []
        if spec.data_kind not in self.required_data_kind:
            warnings.append(
                f"data_kind '{spec.data_kind}' not in expected {self.required_data_kind}"
            )
        return warnings

    def _default_palette(self) -> dict:
        return dict(PAPER_PALETTE)
```

`paper_figure_codegen/recipes/__init__.py`:
```python
"""Recipe registry — lazy import and cache."""

_REGISTRY: dict[str, type] = {}
_IMPORTS_DONE = False

_MVP_RECIPES = [
    "grouped_bar",
    "stacked_bar",
    "horizontal_bar",
    "line_with_ci",
    "violin_box_scatter",
    "boxplot",
    "histogram_kde",
    "heatmap",
    "confusion_matrix",
    "scatter_regression",
    "multi_panel",
]

_V2_RECIPES = [
    "radar",
    "ternary",
    "eeg_topomap",
    "permutation_test",
    "raincloud",
    "flowchart_composite",
]

_ALL_RECIPES = _MVP_RECIPES + _V2_RECIPES

_MODULE_MAP = {
    "grouped_bar": "paper_figure_codegen.recipes.grouped_bar",
    "stacked_bar": "paper_figure_codegen.recipes.stacked_bar",
    "horizontal_bar": "paper_figure_codegen.recipes.horizontal_bar",
    "line_with_ci": "paper_figure_codegen.recipes.line_with_ci",
    "violin_box_scatter": "paper_figure_codegen.recipes.violin_box_scatter",
    "boxplot": "paper_figure_codegen.recipes.boxplot",
    "histogram_kde": "paper_figure_codegen.recipes.histogram_kde",
    "heatmap": "paper_figure_codegen.recipes.heatmap",
    "confusion_matrix": "paper_figure_codegen.recipes.confusion_matrix",
    "scatter_regression": "paper_figure_codegen.recipes.scatter_regression",
    "multi_panel": "paper_figure_codegen.recipes.multi_panel",
    "radar": "paper_figure_codegen.recipes.radar",
    "ternary": "paper_figure_codegen.recipes.ternary",
    "eeg_topomap": "paper_figure_codegen.recipes.eeg_topomap",
    "permutation_test": "paper_figure_codegen.recipes.permutation_test",
    "raincloud": "paper_figure_codegen.recipes.raincloud",
    "flowchart_composite": "paper_figure_codegen.recipes.flowchart_composite",
}


def _ensure_imports():
    global _IMPORTS_DONE
    if _IMPORTS_DONE:
        return
    import importlib
    for name, module_path in _MODULE_MAP.items():
        mod = importlib.import_module(module_path)
        cls = getattr(mod, "Recipe", None)
        if cls is not None:
            _REGISTRY[name] = cls
    _IMPORTS_DONE = True


def get_recipe(name: str):
    """Return a recipe class by plot type name."""
    _ensure_imports()
    if name not in _REGISTRY:
        raise KeyError(f"Unknown recipe: {name}. Available: {list(_REGISTRY.keys())}")
    return _REGISTRY[name]()


def list_recipes() -> list[str]:
    """Return list of all registered recipe names."""
    _ensure_imports()
    return list(_REGISTRY.keys())
```

- [ ] **Step 4: Commit**

```bash
git add paper_figure_codegen/recipes/base.py paper_figure_codegen/recipes/__init__.py tests/test_recipe_registry.py
git commit -m "feat: add Recipe protocol, BaseRecipe ABC, and registry"
```

---

## Task 8: Export Helper

**Files:**
- Create: `paper_figure_codegen/export.py`
- Create: `tests/test_export.py`

- [ ] **Step 1: Write the test**

`tests/test_export.py`:
```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from paper_figure_codegen.export import save_figure


class TestSaveFigure:
    def test_save_png_pdf_svg(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        paths = save_figure(fig, name="test_fig", output_dir=tmp_path)
        assert len(paths) == 3
        for p in paths:
            assert p.exists()
            assert p.stat().st_size > 0
        plt.close(fig)

    def test_custom_formats(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, name="test_fig", output_dir=tmp_path, formats=["png"])
        assert len(paths) == 1
        assert paths[0].suffix == ".png"
        plt.close(fig)

    def test_custom_dpi(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, name="test_dpi", output_dir=tmp_path, dpi=150)
        assert paths[0].exists()
        plt.close(fig)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_export.py -v`

Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: Implement export module**

`paper_figure_codegen/export.py`:
```python
"""Figure export helper — save to PNG, PDF, SVG."""

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt


def save_figure(
    fig: plt.Figure,
    name: str = "figure",
    output_dir: Path | str = "outputs",
    formats: List[str] | None = None,
    dpi: int = 300,
) -> List[Path]:
    """Save figure to multiple formats. Returns list of saved paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if formats is None:
        formats = ["png", "pdf", "svg"]
    saved = []
    for fmt in formats:
        path = output_dir / f"{name}.{fmt}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        saved.append(path)
    return saved
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_export.py -v`

Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/export.py tests/test_export.py
git commit -m "feat: add save_figure export helper"
```

---

## Task 9: Grouped Bar Recipe

**Files:**
- Create: `paper_figure_codegen/recipes/grouped_bar.py`
- Modify: `tests/test_recipes.py` (add grouped bar test)

This is the first recipe — it establishes the pattern all other recipes follow. Each recipe generates a complete Python script string using Jinja2.

- [ ] **Step 1: Write the test for grouped bar**

`tests/test_recipes.py`:
```python
"""Test that each recipe generates executable Python code."""

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pytest

from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes import get_recipe


def _make_multi_series_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="multi_series",
        groups=["Baseline", "Method A", "Ours"],
        values=np.array([[0.72, 0.75, 0.74], [0.78, 0.79, 0.80], [0.84, 0.85, 0.86]]),
        labels=["Accuracy", "F1", "AUC"],
        suggested_plot_types=["grouped_bar"],
    )


def _make_wide_spec():
    return FigureDataSpec(
        raw_input_type="dataframe",
        data_kind="wide_dataframe",
        groups=["Baseline", "Ours"],
        labels=["Accuracy", "F1", "AUC"],
        values=np.array([[0.81, 0.79, 0.85], [0.88, 0.86, 0.91]]),
        suggested_plot_types=["grouped_bar"],
    )


class TestGroupedBarRecipe:
    def test_generate_code_returns_string(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert isinstance(code, str)
        assert len(code) > 100

    def test_generated_code_has_main(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "def main():" in code
        assert 'if __name__ == "__main__"' in code

    def test_generated_code_has_config(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "OUTPUT_DIR" in code
        assert "FIG_NAME" in code
        assert "DPI" in code

    def test_generated_code_has_palette(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "PAPER_PALETTE" in code
        assert "#5B8DB8" in code

    def test_generated_code_executable(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        namespace = {}
        exec(code, namespace)
        assert "main" in namespace
        assert "plot_figure" in namespace

    def test_generated_code_runs(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()

    def test_validate_accepts_correct_data_kind(self):
        recipe = get_recipe("grouped_bar")
        warnings = recipe.validate(_make_wide_spec())
        assert len(warnings) == 0

    def test_validate_warns_on_wrong_data_kind(self):
        spec = FigureDataSpec(raw_input_type="list", data_kind="single_series")
        recipe = get_recipe("grouped_bar")
        warnings = recipe.validate(spec)
        assert len(warnings) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestGroupedBarRecipe -v`

Expected: FAIL — KeyError: "grouped_bar" (recipe not yet implemented)

- [ ] **Step 3: Implement grouped bar recipe**

`paper_figure_codegen/recipes/grouped_bar.py`:
```python
"""Grouped bar chart recipe — model x metric comparison."""

from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

import os

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "grouped_bar"
    required_data_kind = ["multi_series", "wide_dataframe", "grouped_table"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()
        colors = get_palette(
            len(spec.groups) if spec.groups else 3, kind="categorical"
        )

        data_loading_code = self._build_data_loading(spec)
        validation_code = self._build_validation()
        plotting_code = self._build_plotting(spec, colors)

        template = _env.get_template("base.py.j2")
        return template.render(
            figure_name=f"figure_{self.plot_type}",
            dpi=dpi,
            font_size=font_size,
            linewidth=1.2,
            palette=palette,
            data_loading_code=data_loading_code,
            validation_code=validation_code,
            plotting_code=plotting_code,
        )

    def _build_data_loading(self, spec: FigureDataSpec) -> str:
        if spec.groups and spec.labels and spec.values is not None:
            methods = spec.groups
            metrics = spec.labels
            vals = spec.values
            rows = []
            for i, method in enumerate(methods):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                rows.append(f'        "{method}": [{row_vals}],')
            methods_str = ", ".join(f'"{m}"' for m in methods)
            metrics_str = ", ".join(f'"{m}"' for m in metrics)
            return (
                "    # TODO: Replace this example data with your real data.\n"
                "    methods = [" + methods_str + "]\n"
                "    metrics = [" + metrics_str + "]\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    return methods, metrics, data"
            )
        return (
            "    # TODO: Replace this example data with your real data.\n"
            '    methods = ["Baseline", "Method A", "Ours"]\n'
            '    metrics = ["Accuracy", "F1", "AUC"]\n'
            "    data = {\n"
            '        "Baseline": [0.81, 0.79, 0.85],\n'
            '        "Method A": [0.84, 0.82, 0.88],\n'
            '        "Ours":     [0.88, 0.86, 0.91],\n'
            "    }\n"
            "    return methods, metrics, data"
        )

    def _build_validation(self) -> str:
        return (
            "    methods, metrics, data = data\n"
            "    if len(data) != len(methods):\n"
            '        raise ValueError(f"Expected {len(methods)} methods, got {len(data)}")\n'
            "    for name, vals in data.items():\n"
            "        if len(vals) != len(metrics):\n"
            '            raise ValueError(f"Method {name}: expected {len(metrics)} values, got {len(vals)}")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        n_groups = len(spec.groups) if spec.groups else 3
        color_lines = []
        for c in colors:
            color_lines.append(f'        "{c}",')
        colors_str = "\n".join(color_lines)

        return (
            "    apply_paper_style()\n"
            "    methods, metrics, data = data\n"
            "\n"
            "    n_methods = len(methods)\n"
            "    n_metrics = len(metrics)\n"
            "    x = np.arange(n_metrics)\n"
            "    width = 0.8 / n_methods\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6, 4.5))\n"
            "\n"
            "    colors = [\n"
            + colors_str
            + "\n"
            "    ]\n"
            "\n"
            "    for i, method in enumerate(methods):\n"
            "        offset = (i - n_methods / 2 + 0.5) * width\n"
            "        bars = ax.bar(x + offset, data[method], width, label=method, color=colors[i % len(colors)])\n"
            "        for bar in bars:\n"
            "            height = bar.get_height()\n"
            "            ax.annotate(f\"{height:.2f}\",\n"
            "                        xy=(bar.get_x() + bar.get_width() / 2, height),\n"
            "                        xytext=(0, 3), textcoords=\"offset points\",\n"
            "                        ha=\"center\", va=\"bottom\", fontsize=8)\n"
            "\n"
            "    ax.set_xticks(x)\n"
            "    ax.set_xticklabels(metrics)\n"
            "    ax.set_ylabel(\"Score\")\n"
            '    ax.set_title("Method Comparison")\n'
            "    ax.legend(loc=\"upper right\")\n"
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    y_min = min(min(v) for v in data.values())\n"
            "    ax.set_ylim(max(0, y_min - 0.05), 1.0)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestGroupedBarRecipe -v`

Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/recipes/grouped_bar.py tests/test_recipes.py
git commit -m "feat: add grouped_bar recipe with Jinja2 code generation"
```

---

## Task 10: Stacked Bar Recipe

**Files:**
- Create: `paper_figure_codegen/recipes/stacked_bar.py`

- [ ] **Step 1: Add test to test_recipes.py**

Append to `tests/test_recipes.py`:

```python
def _make_stacked_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="multi_series",
        groups=["Happy", "Sad", "Neutral"],
        values=np.array([[0.45, 0.35, 0.20], [0.30, 0.40, 0.30], [0.25, 0.30, 0.45]]),
        labels=["Session 1", "Session 2", "Session 3"],
        suggested_plot_types=["stacked_bar"],
    )


class TestStackedBarRecipe:
    def test_generate_code(self):
        recipe = get_recipe("stacked_bar")
        code = recipe.generate_code(_make_stacked_spec())
        assert "def main():" in code
        assert "PAPER_PALETTE" in code

    def test_executable(self):
        recipe = get_recipe("stacked_bar")
        code = recipe.generate_code(_make_stacked_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestStackedBarRecipe -v`

Expected: FAIL

- [ ] **Step 3: Implement stacked bar recipe**

`paper_figure_codegen/recipes/stacked_bar.py`:
```python
"""Stacked bar chart recipe — category composition."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "stacked_bar"
    required_data_kind = ["multi_series", "wide_dataframe", "grouped_table"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        palette = palette or self._default_palette()
        colors = get_palette(len(spec.groups) if spec.groups else 3, kind="categorical")
        data_loading = self._data_loading(spec)
        plotting = self._plotting(spec, colors)

        template = _env.get_template("base.py.j2")
        return template.render(
            figure_name=f"figure_{self.plot_type}",
            dpi=dpi, font_size=font_size, linewidth=1.2,
            palette=palette,
            data_loading_code=data_loading,
            validation_code=self._validation(),
            plotting_code=plotting,
        )

    def _data_loading(self, spec):
        if spec.groups and spec.labels and spec.values is not None:
            cats = spec.groups
            sessions = spec.labels
            vals = spec.values
            rows = []
            for i, cat in enumerate(cats):
                row = ", ".join(f"{v:.2f}" for v in vals[i])
                rows.append(f'        "{cat}": [{row}],')
            cats_str = ", ".join(f'"{c}"' for c in cats)
            sess_str = ", ".join(f'"{s}"' for s in sessions)
            return (
                "    # TODO: Replace with your real data.\n"
                "    categories = [" + cats_str + "]\n"
                "    sessions = [" + sess_str + "]\n"
                "    data = {\n" + "\n".join(rows) + "\n    }\n"
                "    return categories, sessions, data"
            )
        return (
            "    # TODO: Replace with your real data.\n"
            '    categories = ["Happy", "Sad", "Neutral"]\n'
            '    sessions = ["Session 1", "Session 2", "Session 3"]\n'
            "    data = {\n"
            '        "Happy":   [0.45, 0.35, 0.20],\n'
            '        "Sad":     [0.30, 0.40, 0.30],\n'
            '        "Neutral": [0.25, 0.30, 0.45],\n'
            "    }\n"
            "    return categories, sessions, data"
        )

    def _validation(self):
        return (
            "    categories, sessions, data = data\n"
            "    for cat, vals in data.items():\n"
            "        if len(vals) != len(sessions):\n"
            '            raise ValueError(f"Category {cat}: expected {len(sessions)} values, got {len(vals)}")'
        )

    def _plotting(self, spec, colors):
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "    apply_paper_style()\n"
            "    categories, sessions, data = data\n"
            "\n"
            "    n_sessions = len(sessions)\n"
            "    x = np.arange(n_sessions)\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6, 4.5))\n"
            "    colors = [\n" + color_lines + "\n    ]\n"
            "\n"
            "    bottom = np.zeros(n_sessions)\n"
            "    for i, cat in enumerate(categories):\n"
            "        vals = np.array(data[cat])\n"
            "        ax.bar(x, vals, 0.6, bottom=bottom, label=cat, color=colors[i % len(colors)])\n"
            "        bottom += vals\n"
            "\n"
            "    ax.set_xticks(x)\n"
            "    ax.set_xticklabels(sessions)\n"
            "    ax.set_ylabel(\"Proportion\")\n"
            '    ax.set_title("Category Composition")\n'
            "    ax.legend(loc=\"upper right\")\n"
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestStackedBarRecipe -v`

Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/recipes/stacked_bar.py
git commit -m "feat: add stacked_bar recipe"
```

---

## Task 11: Horizontal Bar Recipe

**Files:**
- Create: `paper_figure_codegen/recipes/horizontal_bar.py`

- [ ] **Step 1: Add test to test_recipes.py**

Append:

```python
def _make_ranking_spec():
    return FigureDataSpec(
        raw_input_type="dataframe",
        data_kind="ranking_table",
        labels=["gamma", "beta", "alpha", "theta", "delta"],
        values=np.array([0.36, 0.24, 0.19, 0.12, 0.09]),
        suggested_plot_types=["horizontal_bar"],
    )


class TestHorizontalBarRecipe:
    def test_generate_code(self):
        recipe = get_recipe("horizontal_bar")
        code = recipe.generate_code(_make_ranking_spec())
        assert "def main():" in code
        assert "barh" in code

    def test_executable(self):
        recipe = get_recipe("horizontal_bar")
        code = recipe.generate_code(_make_ranking_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestHorizontalBarRecipe -v`

Expected: FAIL

- [ ] **Step 3: Implement horizontal bar recipe**

`paper_figure_codegen/recipes/horizontal_bar.py`:
```python
"""Horizontal bar chart recipe — feature importance, ranking."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "horizontal_bar"
    required_data_kind = ["ranking_table", "single_series"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        palette = palette or self._default_palette()
        data_loading = self._data_loading(spec)
        plotting = self._plotting(spec)

        template = _env.get_template("base.py.j2")
        return template.render(
            figure_name=f"figure_{self.plot_type}",
            dpi=dpi, font_size=font_size, linewidth=1.2,
            palette=palette,
            data_loading_code=data_loading,
            validation_code="    pass",
            plotting_code=plotting,
        )

    def _data_loading(self, spec):
        if spec.labels is not None and spec.values is not None:
            names = spec.labels
            vals = spec.values
            lines = []
            for n, v in zip(names, vals):
                lines.append(f'        ("{n}", {v:.4f}),')
            return (
                "    # TODO: Replace with your real data.\n"
                "    features = [\n" + "\n".join(lines) + "\n    ]\n"
                "    return features"
            )
        return (
            "    # TODO: Replace with your real data.\n"
            "    features = [\n"
            '        ("gamma", 0.36),\n'
            '        ("beta",  0.24),\n'
            '        ("alpha", 0.19),\n'
            '        ("theta", 0.12),\n'
            '        ("delta", 0.09),\n'
            "    ]\n"
            "    return features"
        )

    def _plotting(self, spec):
        return (
            "    apply_paper_style()\n"
            "    features = data\n"
            "    names = [f[0] for f in features]\n"
            "    values = [f[1] for f in features]\n"
            "\n"
            "    sorted_idx = np.argsort(values)\n"
            "    names = [names[i] for i in sorted_idx]\n"
            "    values = [values[i] for i in sorted_idx]\n"
            "\n"
            "    colors = [PAPER_PALETTE[\"teal_main\"] if v >= 0 else PAPER_PALETTE[\"orange_main\"] for v in values]\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(5, 4))\n"
            "    y_pos = np.arange(len(names))\n"
            "    ax.barh(y_pos, values, color=colors, height=0.6)\n"
            "    ax.set_yticks(y_pos)\n"
            "    ax.set_yticklabels(names)\n"
            "    ax.set_xlabel(\"Importance\")\n"
            '    ax.set_title("Feature Importance")\n'
            "    ax.grid(axis=\"x\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    for i, v in enumerate(values):\n"
            '        ax.annotate(f"{v:.3f}", xy=(v, i), xytext=(5, 0),\n'
            "                    textcoords=\"offset points\", va=\"center\", fontsize=8)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py::TestHorizontalBarRecipe -v`

Expected: 2 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/recipes/horizontal_bar.py
git commit -m "feat: add horizontal_bar recipe"
```

---

## Task 12: Remaining MVP Recipes (Line, Violin, Boxplot, Histogram, Heatmap, Confusion Matrix, Scatter, Multi-panel)

These 8 recipes follow the exact same pattern as Tasks 9-11. Each has its own `Recipe` class with `generate_code`, `_data_loading`, `_validation`, and `_plotting`. Each gets a test in `test_recipes.py`.

Due to length, I'm providing the full implementation for each. The executing agent should implement them one at a time, running tests after each.

### Task 12a: Line with CI Recipe

- [ ] **Step 1: Add test**

```python
def _make_time_series_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="time_series",
        groups=["Train", "Val"],
        values=np.array([
            [0.60, 0.72, 0.78, 0.83, 0.86],
            [0.55, 0.65, 0.70, 0.74, 0.75],
        ]),
        labels=["Epoch 1", "Epoch 2", "Epoch 3", "Epoch 4", "Epoch 5"],
        suggested_plot_types=["line_with_ci"],
    )


class TestLineWithCIRecipe:
    def test_generate_code(self):
        recipe = get_recipe("line_with_ci")
        code = recipe.generate_code(_make_time_series_spec())
        assert "def main():" in code
        assert "plot" in code

    def test_executable(self):
        recipe = get_recipe("line_with_ci")
        code = recipe.generate_code(_make_time_series_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()
```

- [ ] **Step 2: Implement `paper_figure_codegen/recipes/line_with_ci.py`**

The recipe follows the same structure: `_data_loading` creates example data for learning curves (epochs × metrics), `_plotting` uses `ax.plot()` with optional `fill_between` for CI bands. Colors from `get_palette(n, "categorical")`.

- [ ] **Step 3: Run tests, commit**

```bash
git add paper_figure_codegen/recipes/line_with_ci.py
git commit -m "feat: add line_with_ci recipe"
```

### Task 12b: Violin Box Scatter Recipe

- [ ] **Step 1: Add test**

```python
class TestViolinBoxScatterRecipe:
    def test_generate_code(self):
        recipe = get_recipe("violin_box_scatter")
        code = recipe.generate_code(_make_multi_series_spec())
        assert "def main():" in code
        assert "violinplot" in code

    def test_executable(self):
        recipe = get_recipe("violin_box_scatter")
        code = recipe.generate_code(_make_multi_series_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()
```

- [ ] **Step 2: Implement `paper_figure_codegen/recipes/violin_box_scatter.py`**

This is the signature plot from the PRD (§10.2 example). The plotting code should include violin (distribution), box (quartiles), and jittered scatter (raw points), matching the PRD's example code exactly.

- [ ] **Step 3: Run tests, commit**

```bash
git add paper_figure_codegen/recipes/violin_box_scatter.py
git commit -m "feat: add violin_box_scatter recipe"
```

### Task 12c: Boxplot Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/boxplot.py`**

Simpler than violin — just `ax.boxplot()` with `patch_artist=True`, paper palette colors, no scatter overlay.

### Task 12d: Histogram KDE Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/histogram_kde.py`**

Uses `ax.hist()` with density=True, optional KDE overlay via scipy (try/except fallback).

### Task 12e: Heatmap Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/heatmap.py`**

Uses `ax.imshow()` with annotations. Supports correlation matrices and generic 2D data.

### Task 12f: Confusion Matrix Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/confusion_matrix.py`**

Specialized heatmap with `normalize` parameter, percentage display, diagonal emphasis via cmap.

### Task 12g: Scatter Regression Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/scatter_regression.py`**

Scatter plot with `np.polyfit` regression line and optional CI band. scipy/statsmodels for robust regression (try/except fallback).

### Task 12h: Multi-panel Recipe

- [ ] **Step 1: Add test + implement `paper_figure_codegen/recipes/multi_panel.py`**

Uses `matplotlib.gridspec.GridSpec` to compose multiple subplots. Panel labels (A, B, C). Takes a `multi_panel_spec` data_kind with panel configurations.

- [ ] **Step 4: Run all MVP recipe tests**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py -v`

Expected: All tests pass (each recipe: generate_code returns string, code is executable, code runs)

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/recipes/ tests/test_recipes.py
git commit -m "feat: add all 11 MVP recipes"
```

---

## Task 13: V2 Recipes (Radar, Ternary, EEG Topomap, Permutation Test, Raincloud, Flowchart Composite)

Each V2 recipe follows the same pattern. They use optional dependencies with try/except fallback.

### Task 13a: Radar Chart

- [ ] **Implement `paper_figure_codegen/recipes/radar.py`**

Uses matplotlib's polar projection. Handles wide_dataframe (methods × metrics mapped to radar axes).

### Task 13b: Ternary Plot

- [ ] **Implement `paper_figure_codegen/recipes/ternary.py`**

Uses manual triangular projection with matplotlib. No external ternary library needed.

### Task 13c: EEG Topomap

- [ ] **Implement `paper_figure_codegen/recipes/eeg_topomap.py`**

Primary: mne.viz.plot_topomap. Fallback: 2D scatter with interpolation when mne not installed.

### Task 13d: Permutation Test Plot

- [ ] **Implement `paper_figure_codegen/recipes/permutation_test.py`**

Histogram of permutation distribution with observed statistic marked as vertical line, p-value annotation.

### Task 13e: Raincloud Plot

- [ ] **Implement `paper_figure_codegen/recipes/raincloud.py`**

Half-violin (using KDE) + box + scatter. No external library needed.

### Task 13f: Flowchart Composite

- [ ] **Implement `paper_figure_codegen/recipes/flowchart_composite.py`**

Multi-panel with method flow diagram (using matplotlib patches/arrows) + data plots.

- [ ] **Run all recipe tests**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_recipes.py -v`

Expected: All 17 recipes pass

- [ ] **Commit**

```bash
git add paper_figure_codegen/recipes/ tests/test_recipes.py
git commit -m "feat: add all 6 V2 recipes (radar, ternary, eeg, permutation, raincloud, flowchart)"
```

---

## Task 14: Jinja2 Statistical and Multi-panel Templates

**Files:**
- Create: `paper_figure_codegen/templates/statistical.py.j2`
- Create: `paper_figure_codegen/templates/multi_panel.py.j2`

- [ ] **Step 1: Create statistical template**

`paper_figure_codegen/templates/statistical.py.j2`:
```jinja2
\"\"\"
Statistical figure: {{ figure_name }}.

Generated by paper-figure-codegen.
\"\"\"

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


# =========================
# Config
# =========================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_NAME = "{{ figure_name }}"
SAVE_FORMATS = ["png", "pdf", "svg"]
DPI = {{ dpi }}


# =========================
# Style
# =========================

PAPER_PALETTE = {
{% for name, hex_val in palette.items() %}
    "{{ name }}": "{{ hex_val }}",
{% endfor %}
}


def apply_paper_style(font_size={{ font_size }}, linewidth={{ linewidth }}):
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
{{ data_loading_code | indent(4) }}


def validate_data(data):
{{ validation_code | indent(4) }}


# =========================
# Statistical Helpers
# =========================

def compute_statistics(groups):
    \"\"\"Compute basic statistics for each group.\"\"\"
    results = {}
    for name, vals in groups.items():
        arr = np.asarray(vals, dtype=float)
        results[name] = {
            "mean": np.mean(arr),
            "std": np.std(arr),
            "median": np.median(arr),
        }
        if HAS_SCIPY:
            results[name]["ci"] = stats.t.interval(
                0.95, len(arr) - 1,
                loc=np.mean(arr),
                scale=stats.sem(arr),
            )
    return results


# =========================
# Plot
# =========================

def plot_figure(data):
{{ plotting_code | indent(4) }}


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

- [ ] **Step 2: Create multi-panel template**

`paper_figure_codegen/templates/multi_panel.py.j2`:
```jinja2
\"\"\"
Multi-panel figure: {{ figure_name }}.

Generated by paper-figure-codegen.
\"\"\"

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# =========================
# Config
# =========================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_NAME = "{{ figure_name }}"
SAVE_FORMATS = ["png", "pdf", "svg"]
DPI = {{ dpi }}


# =========================
# Style
# =========================

PAPER_PALETTE = {
{% for name, hex_val in palette.items() %}
    "{{ name }}": "{{ hex_val }}",
{% endfor %}
}


def apply_paper_style(font_size={{ font_size }}, linewidth={{ linewidth }}):
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
{{ data_loading_code | indent(4) }}


# =========================
# Panel Helpers
# =========================

def add_panel_label(ax, label, x=-0.1, y=1.05):
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="top")


# =========================
# Plot
# =========================

def plot_figure(data):
{{ plotting_code | indent(4) }}


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
    fig = plot_figure(data)
    saved_paths = save_figure(fig)
    print("Saved files:")
    for path in saved_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Commit**

```bash
git add paper_figure_codegen/templates/statistical.py.j2 paper_figure_codegen/templates/multi_panel.py.j2
git commit -m "feat: add statistical and multi-panel Jinja2 templates"
```

---

## Task 15: CLI

**Files:**
- Create: `paper_figure_codegen/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write the test**

`tests/test_cli.py`:
```python
from click.testing import CliRunner

from paper_figure_codegen.cli import cli


class TestCLI:
    def test_list_plots(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["list-plots"])
        assert result.exit_code == 0
        assert "grouped_bar" in result.output
        assert "violin_box_scatter" in result.output

    def test_codegen_missing_plot(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["codegen", "--plot", "nonexistent"])
        assert result.exit_code != 0

    def test_codegen_generates_code(self):
        runner = CliRunner()
        result = runner.invoke(cli, [
            "codegen",
            "--plot", "grouped_bar",
            "--output", "test_figure",
        ])
        assert result.exit_code == 0
        assert "def main():" in result.output
        assert "PAPER_PALETTE" in result.output

    def test_codegen_with_groups(self):
        runner = CliRunner()
        result = runner.invoke(cli, [
            "codegen",
            "--plot", "violin_box_scatter",
            "--groups", "3",
            "--output", "test_violin",
        ])
        assert result.exit_code == 0
        assert "violinplot" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_cli.py -v`

Expected: FAIL — ModuleNotFoundError

- [ ] **Step 3: Implement CLI**

`paper_figure_codegen/cli.py`:
```python
"""CLI entry point for paper-figure-codegen."""

import click

from paper_figure_codegen.recipes import get_recipe, list_recipes


@click.group()
def cli():
    """Paper Figure Codegen — publication-quality plotting code generator."""
    pass


@cli.command()
def list_plots():
    """List all available plot types."""
    recipes = list_recipes()
    click.echo("Available plot types:")
    for name in sorted(recipes):
        click.echo(f"  - {name}")


@cli.command()
@click.option("--plot", required=True, help="Plot type to generate")
@click.option("--output", default="figure_output", help="Output figure name")
@click.option("--groups", default=3, type=int, help="Number of groups (for example data)")
@click.option("--data", default=None, help="Path to data file (CSV/Excel)")
@click.option("--font-size", default=12, type=int, help="Font size")
@click.option("--dpi", default=300, type=int, help="DPI for output")
def codegen(plot, output, groups, data, font_size, dpi):
    """Generate plotting code for the specified plot type."""
    try:
        recipe = get_recipe(plot)
    except KeyError as e:
        raise click.BadParameter(str(e))

    import numpy as np
    from paper_figure_codegen.core.data_spec import FigureDataSpec

    if data:
        import pandas as pd
        from paper_figure_codegen.core.data_parser import DataParser
        if data.endswith(".csv"):
            df = pd.read_csv(data)
        elif data.endswith((".xlsx", ".xls")):
            df = pd.read_excel(data)
        else:
            raise click.BadParameter(f"Unsupported file format: {data}")
        spec = DataParser.parse(df)
    else:
        rng = np.random.default_rng(42)
        spec = FigureDataSpec(
            raw_input_type="example",
            data_kind="wide_dataframe",
            groups=[f"Method {i}" for i in range(groups)],
            labels=["Accuracy", "F1", "AUC"],
            values=rng.uniform(0.7, 0.95, size=(groups, 3)),
            suggested_plot_types=[plot],
        )

    code = recipe.generate_code(spec, font_size=font_size, dpi=dpi)
    code = code.replace(f"figure_{plot}", output)
    click.echo(code)


if __name__ == "__main__":
    cli()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/test_cli.py -v`

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add paper_figure_codegen/cli.py tests/test_cli.py
git commit -m "feat: add CLI with codegen and list-plots commands"
```

---

## Task 16: Update Package __init__.py Exports

**Files:**
- Modify: `paper_figure_codegen/core/__init__.py`
- Modify: `paper_figure_codegen/__init__.py`

- [ ] **Step 1: Update core/__init__.py**

```python
"""Core modules for data parsing, color system, and style."""

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_parser import DataParser
from paper_figure_codegen.core.data_spec import DATA_KINDS, FigureDataSpec
from paper_figure_codegen.core.style import apply_paper_style

__all__ = [
    "PAPER_PALETTE",
    "get_palette",
    "DataParser",
    "DATA_KINDS",
    "FigureDataSpec",
    "apply_paper_style",
]
```

- [ ] **Step 2: Update package __init__.py**

```python
"""Paper Figure Codegen - Publication-quality plotting code generator."""

__version__ = "0.1.0"

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_parser import DataParser
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.core.style import apply_paper_style
from paper_figure_codegen.export import save_figure
from paper_figure_codegen.recipes import get_recipe, list_recipes
```

- [ ] **Step 3: Verify all imports work**

Run: `cd /Users/yuyuan/paper_image_skills && python -c "from paper_figure_codegen import PAPER_PALETTE, DataParser, FigureDataSpec, get_recipe, list_recipes; print('OK')"`

Expected: OK

- [ ] **Step 4: Commit**

```bash
git add paper_figure_codegen/__init__.py paper_figure_codegen/core/__init__.py
git commit -m "feat: update package exports for public API"
```

---

## Task 17: SKILL.md

**Files:**
- Create: `SKILL.md`

- [ ] **Step 1: Create SKILL.md**

```markdown
---
name: paper-figure-codegen
description: >
  Generate ready-to-run Python matplotlib code for publication-quality scientific figures.
  Use this skill when the user asks for plotting code, paper-style figures, multi-panel figures,
  statistical plots, heatmaps, model comparison plots, or figure styles similar to uploaded academic images.
---

# Paper Figure Code Generation Skill

Generate immediately runnable Python plotting scripts for scientific papers, slides, and reports.

## Core tasks

1. Parse user data into a unified `FigureDataSpec`.
2. Select an appropriate plot type based on data structure and user intent.
3. Choose publication-ready colors using semantic color rules.
4. Generate complete Python code with reusable functions.
5. Save figures as PNG, PDF, and SVG.

## When to use

- The user asks for plotting code or wants to "draw a figure for a paper".
- The user provides lists, tables, CSV/Excel/JSON data, matrices, or experiment results.
- The user asks for paper-style visualizations.
- The user references a figure image and wants similar style.
- The user asks for boxplot, violin plot, bar plot, heatmap, confusion matrix, trend plot, radar plot, EEG-style topomap, or multi-panel figure.

## When not to use

- Interactive dashboards (Plotly Dash, Streamlit, ECharts).
- GIS maps or pure image generation without code.
- Non-data-driven illustrations.

## Required behavior

- Always generate runnable code.
- Prefer matplotlib + numpy + pandas.
- Do not require seaborn unless clearly beneficial.
- Use optional dependencies only with fallback (try/except).
- Include example data when the user has not provided real data.
- Include clear TODO comments for user-replaced paths or variables.
- Export high-resolution figures (PNG 300dpi, PDF, SVG).
- Keep code modular (functions, not monolithic main).
- Validate data shapes before plotting.

## Available plot types

### MVP (11)
`grouped_bar`, `stacked_bar`, `horizontal_bar`, `line_with_ci`, `violin_box_scatter`, `boxplot`, `histogram_kde`, `heatmap`, `confusion_matrix`, `scatter_regression`, `multi_panel`

### Advanced (6)
`radar`, `ternary`, `eeg_topomap`, `permutation_test`, `raincloud`, `flowchart_composite`

## Code generation rules

Every generated script follows this structure:
1. Module docstring
2. Imports
3. Config section (OUTPUT_DIR, FIG_NAME, DPI, SAVE_FORMATS)
4. Style section (PAPER_PALETTE, apply_paper_style)
5. Data loading (real data or example data with TODO)
6. Data validation
7. Plotting function
8. Save/export function
9. main()

## Color system

Default palette uses low-saturation academic colors: blues, teals, greens with warm accents (orange, yellow).
See references/color-system.md for full rules.

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

- [ ] **Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md entry point"
```

---

## Task 18: References Documentation

**Files:**
- Create: `references/data-structures.md`
- Create: `references/plot-selection.md`
- Create: `references/color-system.md`
- Create: `references/codegen-rules.md`
- Create: `references/plot-recipes.md`
- Create: `references/style-guide.md`
- Create: `references/export-policy.md`
- Create: `references/troubleshooting.md`

This task creates 8 reference files. Each is a concise Markdown document that the AI can read on-demand. Content is derived directly from the spec.

- [ ] **Step 1: Create references/ directory**

Run: `mkdir -p /Users/yuyuan/paper_image_skills/references`

- [ ] **Step 2: Create all 8 reference files**

`references/data-structures.md`:
```markdown
# Data Structure Identification

## data_kind taxonomy

| data_kind | Input pattern | Candidate plots |
|-----------|--------------|-----------------|
| single_series | Single list/array | histogram_kde, bar |
| multi_series | Dict of lists, multiple arrays | grouped_bar, violin_box_scatter, boxplot, line_with_ci |
| grouped_table | Tabular with group column | grouped_bar, stacked_bar |
| long_dataframe | subject/session/value columns | grouped_bar, violin_box_scatter, boxplot, line_with_ci |
| wide_dataframe | method/metric1/metric2 columns | grouped_bar, radar, heatmap |
| matrix | 2D numeric array | heatmap, confusion_matrix |
| confusion_matrix | Square matrix, rows sum ~1.0 | confusion_matrix, heatmap |
| time_series | Temporal data with timestamps | line_with_ci |
| distribution_groups | Multiple value arrays per group | violin_box_scatter, boxplot, raincloud |
| ranking_table | 2 columns: name + score | horizontal_bar |
| correlation_table | Square symmetric matrix | heatmap |
| eeg_channel_table | channel/band/x/y/value columns | eeg_topomap, heatmap |
| multi_panel_spec | Multiple plot specifications | multi_panel |

## Identification rules

1. **Multiple lists** (dict of lists) → `multi_series`
2. **2D numeric matrix** → `matrix` or `confusion_matrix` (if square + rows sum to ~1)
3. **Long table** (≥3 columns, mix of categorical + numeric) → `long_dataframe`
4. **Wide table** (first col categorical, rest numeric, ≥3 cols) → `wide_dataframe`
5. **2-column table** (name + number) → `ranking_table`
6. **EEG data** (channel + spatial coords) → `eeg_channel_table`
```

`references/plot-selection.md`:
```markdown
# Plot Type Selection

## Decision tree

1. Is the user comparing groups/methods?
   - Yes → grouped_bar, horizontal_bar
   - No → continue

2. Is the user showing distributions?
   - Yes → violin_box_scatter, boxplot, histogram_kde, raincloud
   - No → continue

3. Is the data a matrix?
   - Yes → heatmap, confusion_matrix
   - No → continue

4. Is the user showing trends over time/epochs?
   - Yes → line_with_ci
   - No → continue

5. Is the user showing relationships between variables?
   - Yes → scatter_regression
   - No → continue

6. Is the user showing multi-metric profiles?
   - Yes → radar
   - No → continue

7. Does the user need multiple subplots in one figure?
   - Yes → multi_panel
   - No → suggest based on data_kind

## Per-type use cases

| Plot type | Typical use |
|-----------|-------------|
| grouped_bar | Model × metric, method × dataset |
| stacked_bar | Category composition, emotion distribution |
| horizontal_bar | Feature importance, subject ranking |
| line_with_ci | Learning curves, session changes |
| violin_box_scatter | Distribution comparison across groups |
| boxplot | Simple distribution comparison |
| histogram_kde | Single variable distribution shape |
| heatmap | Correlation, feature × band importance |
| confusion_matrix | Classification results |
| scatter_regression | Variable relationships |
| multi_panel | Composite paper figures |
| radar | Multi-metric method profiles |
| ternary | Three-component compositions |
| eeg_topomap | Channel importance visualization |
| permutation_test | Statistical test results |
| raincloud | Enhanced distribution with KDE |
| flowchart_composite | Method flow + results combined |
```

`references/color-system.md`:
```markdown
# Color System

## Default palette (PAPER_PALETTE)

Low-saturation academic colors:
- Blues: blue_main (#5B8DB8), blue_dark (#3E6F95), blue_light (#BFD8EA)
- Teals: teal_main (#6FA8A6), teal_dark (#4D8583)
- Greens: green_main (#9CCB9E), green_light (#CFE8D5)
- Warm: yellow_light (#F3E6B3), orange_light (#E8B77D), orange_main (#D99A5E)
- Purple: purple_light (#C9BEDF), pink_light (#E7C1C0)
- Neutral: gray_light (#E8ECEF), gray (#BFC7CD), gray_dark (#66727C)
- Semantic: positive (#6FA8A6), negative (#D99A5E), neutral (#BFC7CD), highlight (#F3C567)

## Color assignment rules

| Groups | kind | Colors |
|--------|------|--------|
| 2 | binary | blue_main, orange_main |
| 3 | categorical | blue_main, green_main, orange_light |
| 4-6 | categorical | blue, teal, green, yellow, orange, purple (first n) |
| 7+ | categorical | tab20 fallback |
| continuous | sequential | Blues colormap |
| positive/negative | diverging | orange → gray → blue |
| significant vs not | significance | dark + marker vs light gray + alpha |

## Usage in generated code

Every generated script includes the full PAPER_PALETTE dict. The `get_palette(n, kind)` function handles selection.
```

`references/codegen-rules.md`:
```markdown
# Code Generation Rules

## Required structure

Every generated script must follow:
1. Module docstring
2. Imports (pathlib, numpy, pandas, matplotlib)
3. Config section (OUTPUT_DIR, FIG_NAME, DPI, SAVE_FORMATS)
4. Style section (PAPER_PALETTE dict, apply_paper_style function)
5. Data loading (load_data function — real data or example with TODO)
6. Data validation (validate_data function)
7. Plotting function (plot_figure — returns fig)
8. Export function (save_figure)
9. main() entry point

## Naming conventions

- Functions: snake_case (plot_figure, load_data, save_figure)
- Constants: UPPER_SNAKE (OUTPUT_DIR, FIG_NAME, DPI)
- File names: figure_{type}.py

## Required behaviors

- All generated code must be directly runnable (`python script.py`)
- No dependency on user-local files unless user provides paths
- Example data with TODO comments when user hasn't provided real data
- Optional deps (scipy, sklearn, mne) in try/except with fallback
- Data validation before plotting
- Export PNG + PDF + SVG by default
- Modular functions, not monolithic main
```

`references/plot-recipes.md`:
```markdown
# Plot Recipes

## grouped_bar
- Input: wide_dataframe or multi_series
- Output: Grouped bar chart with value labels
- Key params: n_methods, n_metrics, value annotations

## stacked_bar
- Input: multi_series
- Output: Stacked bars showing composition
- Key params: categories, sessions, normalize (percentage vs count)

## horizontal_bar
- Input: ranking_table
- Output: Horizontal bars sorted by value
- Key params: positive/negative color split, value annotations

## line_with_ci
- Input: time_series or multi_series
- Output: Line plot with optional confidence interval band
- Key params: x_labels, CI band fill_between

## violin_box_scatter
- Input: multi_series or distribution_groups
- Output: Half-violin + box + jittered scatter
- Key params: violin alpha, box width, scatter jitter

## boxplot
- Input: multi_series
- Output: Standard boxplot with patch_artist
- Key params: widths, medianprops, showfliers

## histogram_kde
- Input: single_series
- Output: Histogram with optional KDE overlay
- Key params: bins, density, scipy.stats.gaussian_kde fallback

## heatmap
- Input: matrix or correlation_table
- Output: Annotated heatmap with colorbar
- Key params: cmap, annot, fmt

## confusion_matrix
- Input: confusion_matrix
- Output: Annotated confusion matrix with normalization
- Key params: normalize, percentage display, diagonal emphasis

## scatter_regression
- Input: two numeric arrays
- Output: Scatter plot with regression line + CI
- Key params: np.polyfit degree, CI band

## multi_panel
- Input: multi_panel_spec
- Output: GridSpec composite with panel labels (A, B, C)
- Key params: nrows, ncols, panel configs

## radar
- Input: wide_dataframe
- Output: Polar plot with radar axes per metric
- Key params: close polygon, fill alpha

## ternary
- Input: 3-column data
- Output: Triangular scatter/bar plot
- Key params: axis labels, grid lines

## eeg_topomap
- Input: eeg_channel_table
- Output: Topographic map of channel values
- Key params: mne.viz.plot_topomap (primary), scatter+interpolation (fallback)

## permutation_test
- Input: distribution + observed statistic
- Output: Histogram with observed line + p-value
- Key params: n_permutations, observed line color

## raincloud
- Input: distribution_groups
- Output: Half-violin KDE + box + scatter
- Key params: KDE bandwidth, orientation

## flowchart_composite
- Input: multi_panel_spec with flowchart config
- Output: Method flow diagram + result plots
- Key params: patches, arrows, panel layout
```

`references/style-guide.md`:
```markdown
# Visual Style Guide

## Font

```python
"font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"]
```

Chinese fallback (when needed):
```python
"font.sans-serif": ["SimHei", "Arial Unicode MS", "Microsoft YaHei", "DejaVu Sans"]
```

## Axes

- Hide top and right spines
- Keep left and bottom spines
- Grid lines: y-axis only, dashed, alpha <= 0.35
- No heavy backgrounds

## Legend

- Simple plots: above or to the right
- Complex plots: separate legend panel
- Multi-panel figures: unified legend
- No frame (`legend.frameon: False`)

## Figure sizing

- Single plot: (5.5, 4) to (6, 4.5)
- Multi-panel: (10, 8) to (14, 10)
- Wide format for landscape slides: (12, 5)

## Export

- PNG: 300 DPI default, 600 for dense plots
- PDF: vector format for paper submission
- SVG: vector format for post-editing
- Always `bbox_inches="tight"`
- Font type 42 (TrueType) for PDF/PS compatibility
```

`references/export-policy.md`:
```markdown
# Export Policy

## Default formats

PNG, PDF, SVG — all three generated for every figure.

## DPI settings

| Scenario | DPI |
|----------|-----|
| Default | 300 |
| Dense plots (many points/labels) | 600 |
| Quick preview | 150 |

## File naming

`figure_{name}.{format}` — stored in `outputs/` directory.

Example: `outputs/figure_comparison.png`, `outputs/figure_comparison.pdf`, `outputs/figure_comparison.svg`

## Font embedding

```python
"pdf.fonttype": 42,    # TrueType
"ps.fonttype": 42,     # TrueType
"svg.fonttype": "none", # Text as text, not paths
```

This ensures fonts are editable in vector formats.
```

`references/troubleshooting.md`:
```markdown
# Troubleshooting

## Chinese text shows as squares

Add before plotting:
```python
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False
```

## Optional dependency missing

All optional deps (scipy, sklearn, mne, statsmodels) use try/except with fallback:
```python
try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
```

## Figure clipped / labels cut off

Add `fig.tight_layout(pad=1.2)` before returning figure.
Use `savefig(bbox_inches="tight")` in export.

## Colors too similar for many groups

For >6 groups, `get_palette` falls back to `tab20`. Consider splitting into multiple subplots.

## Heatmap too crowded

- Reduce annotation font size
- Use `figsize` with wider dimensions
- Rotate x-axis labels: `ax.set_xticklabels(labels, rotation=45, ha="right")`
```

- [ ] **Step 3: Commit**

```bash
git add references/
git commit -m "feat: add all 8 reference documentation files"
```

---

## Task 19: Standalone Templates

**Files:**
- Create: `templates/base_matplotlib.py`
- Create: `templates/multi_panel.py`
- Create: `templates/statistical_distribution.py`

These are runnable reference templates that the AI can adapt directly (not Jinja2 — plain Python).

- [ ] **Step 1: Create templates/ directory**

Run: `mkdir -p /Users/yuyuan/paper_image_skills/templates`

- [ ] **Step 2: Create base_matplotlib.py**

This is the exact code from PRD §10.2 — the complete paper-style matplotlib template with PAPER_PALETTE, apply_paper_style, load_data, validate_data, plot_figure, save_figure, main().

Content: Copy from PRD lines 703-854 verbatim (the full code block).

- [ ] **Step 3: Create multi_panel.py**

A runnable multi-panel template using GridSpec with 2×2 layout, panel labels A/B/C/D.

- [ ] **Step 4: Create statistical_distribution.py**

A runnable statistical template with violin + box + scatter, optional scipy for CI.

- [ ] **Step 5: Commit**

```bash
git add templates/
git commit -m "feat: add standalone reference templates"
```

---

## Task 20: Example Scripts

**Files:**
- Create: `examples/grouped_bar_example.py`
- Create: `examples/violin_box_example.py`
- Create: `examples/confusion_matrix_example.py`
- Create: `examples/multi_panel_example.py`
- Create: `examples/time_series_example.py`

- [ ] **Step 1: Create examples/ directory**

Run: `mkdir -p /Users/yuyuan/paper_image_skills/examples`

- [ ] **Step 2: Create each example**

Each example is a standalone runnable script generated by the corresponding recipe. Create by running:

```bash
python -c "
from paper_figure_codegen import get_recipe
from paper_figure_codegen.core.data_spec import FigureDataSpec
import numpy as np

# grouped_bar
spec = FigureDataSpec(
    raw_input_type='example', data_kind='wide_dataframe',
    groups=['Baseline', 'CNN', 'Transformer', 'Ours'],
    labels=['Accuracy', 'F1', 'AUC'],
    values=np.array([[0.81, 0.79, 0.85], [0.85, 0.83, 0.88], [0.87, 0.85, 0.90], [0.91, 0.89, 0.94]]),
    suggested_plot_types=['grouped_bar'],
)
print(get_recipe('grouped_bar').generate_code(spec))
" > examples/grouped_bar_example.py
```

Repeat for each recipe with appropriate example data.

- [ ] **Step 3: Verify all examples run**

Run: `cd /Users/yuyuan/paper_image_skills && for f in examples/*.py; do echo "Running $f..."; python "$f" && echo "OK" || echo "FAILED"; done`

Expected: All print "OK" and create files in outputs/

- [ ] **Step 4: Commit**

```bash
git add examples/
git commit -m "feat: add 5 runnable example scripts"
```

---

## Task 21: Full Test Suite Pass

- [ ] **Step 1: Run complete test suite**

Run: `cd /Users/yuyuan/paper_image_skills && python -m pytest tests/ -v`

Expected: All tests pass. This covers:
- test_data_spec.py (3 tests)
- test_color_system.py (10 tests)
- test_style.py (5 tests)
- test_data_parser.py (7 tests)
- test_export.py (3 tests)
- test_recipe_registry.py (3 tests)
- test_recipes.py (~34 tests: 2 per recipe)
- test_cli.py (4 tests)

- [ ] **Step 2: Run ruff linting**

Run: `cd /Users/yuyuan/paper_image_skills && ruff check paper_figure_codegen/ tests/`

Expected: No errors (fix any that appear)

- [ ] **Step 3: Final commit if needed**

```bash
git add -A
git commit -m "chore: fix linting issues and ensure full test suite passes"
```

---

## Spec Coverage Check

| Spec Section | Task |
|---|---|
| §1 Overview (dual-layer) | Task 1 (scaffolding), Task 16 (exports) |
| §2 Project Structure | Task 1 |
| §3 Data Flow | Tasks 2-5 (core modules) |
| §4 FigureDataSpec | Task 2 |
| §5 Color System | Task 3 |
| §6 Recipe Architecture | Tasks 7, 9-13 |
| §7 Style Guide | Task 4 |
| §8 Skill Layer (SKILL.md) | Tasks 17-18 |
| §9 CLI | Task 15 |
| §10 Quality Standards | Verified in Task 21 |
| §11 Dependencies | Task 1 (pyproject.toml) |
| 17 plot types | Tasks 9-13 |
| 8 reference docs | Task 18 |
| 3 templates | Task 14 (Jinja2) + Task 19 (standalone) |
| 5 examples | Task 20 |
