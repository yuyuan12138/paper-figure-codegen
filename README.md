# Paper Figure Codegen

Generate publication-quality Python matplotlib code for scientific figures. Dual-layer system: an **AI Skill** for intelligent decision-making + a **Python package** for programmatic code generation.

## Features

- **17 plot types**: grouped bar, stacked bar, horizontal bar, line with CI, violin+box+scatter, boxplot, histogram+KDE, heatmap, confusion matrix, scatter+regression, multi-panel, radar, ternary, EEG topomap, permutation test, raincloud, flowchart composite
- **Paper-style colors**: Low-saturation academic palette (blues, teals, greens with warm accents)
- **Ready-to-run code**: Every generated script includes data loading, validation, plotting, and export (PNG/PDF/SVG)
- **CLI and Python API**: Use from command line or import in your scripts

## Quick Start

### Install

```bash
pip install -e .
```

### CLI

```bash
# List available plot types
paper-figure list-plots

# Generate plotting code
paper-figure codegen --plot grouped_bar --output figure_comparison

# Generate with example data (no input file needed)
paper-figure codegen --plot violin_box_scatter --groups 4 --output figure_distribution

# Generate from CSV data
paper-figure codegen --plot grouped_bar --data results.csv --output figure_results
```

### Python API

```python
import numpy as np
from paper_figure_codegen import get_recipe, FigureDataSpec

spec = FigureDataSpec(
    raw_input_type="dataframe",
    data_kind="wide_dataframe",
    groups=["Baseline", "CNN", "Transformer", "Ours"],
    labels=["Accuracy", "F1", "AUC"],
    values=np.array([
        [0.81, 0.79, 0.85],
        [0.85, 0.83, 0.88],
        [0.87, 0.85, 0.90],
        [0.91, 0.89, 0.94],
    ]),
    suggested_plot_types=["grouped_bar"],
)

code = get_recipe("grouped_bar").generate_code(spec)
print(code)  # Complete Python script
```

### AI Skill (Claude Code)

Copy `SKILL.md` and `references/` into your project:

```bash
mkdir -p .claude/skills/paper-figure-codegen
cp SKILL.md .claude/skills/paper-figure-codegen/
cp -r references/ .claude/skills/paper-figure-codegen/
```

Then ask Claude Code to "generate plotting code for a grouped bar chart comparing model performance" and it will use the skill automatically.

## Plot Types

### MVP (11)

| Type | Use case |
|------|----------|
| `grouped_bar` | Model x metric comparison |
| `stacked_bar` | Category composition |
| `horizontal_bar` | Feature importance, ranking |
| `line_with_ci` | Learning curves, trends |
| `violin_box_scatter` | Distribution comparison |
| `boxplot` | Simple distribution |
| `histogram_kde` | Single variable shape |
| `heatmap` | Correlation, importance matrices |
| `confusion_matrix` | Classification results |
| `scatter_regression` | Variable relationships |
| `multi_panel` | Composite paper figures |

### Advanced (6)

| Type | Use case |
|------|----------|
| `radar` | Multi-metric profiles |
| `ternary` | Three-component compositions |
| `eeg_topomap` | Channel importance (requires mne) |
| `permutation_test` | Statistical test visualization |
| `raincloud` | Enhanced distribution |
| `flowchart_composite` | Method flow + results |

## Color System

Default palette uses low-saturation academic colors:

- **Blues**: `#5B8DB8`, `#3E6F95`, `#BFD8EA`
- **Teals**: `#6FA8A6`, `#4D8583`
- **Greens**: `#9CCB9E`, `#CFE8D5`
- **Warm accents**: `#F3E6B3` (yellow), `#E8B77D` (orange), `#D99A5E` (orange)
- **Semantic**: positive (teal), negative (orange), highlight (yellow)

## Generated Code Structure

Every generated script follows this layout:

```
1. Imports
2. Config (OUTPUT_DIR, FIG_NAME, DPI)
3. Style (PAPER_PALETTE, apply_paper_style)
4. Data loading (real or example with TODO)
5. Data validation
6. Plotting function
7. Export (PNG + PDF + SVG)
8. main()
```

## Project Structure

```
paper-figure-codegen/
├── SKILL.md                          # AI Skill entry point
├── references/                       # Reference docs for AI
├── paper_figure_codegen/             # Python package
│   ├── core/                         # DataSpec, DataParser, ColorSystem, Style
│   ├── recipes/                      # 17 plot type recipes
│   ├── templates/                    # Jinja2 code templates
│   ├── cli.py                        # CLI entry point
│   └── export.py                     # Export helper
├── templates/                        # Standalone reference templates
├── examples/                         # Runnable example scripts
├── tests/                            # Test suite (74 tests)
└── pyproject.toml
```

## Dependencies

**Required**: matplotlib, numpy, pandas, jinja2, click

**Optional**: scipy (statistical plots), scikit-learn (confusion matrix), mne (EEG topomap)

## License

MIT
