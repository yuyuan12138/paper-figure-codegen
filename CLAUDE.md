# Paper Image Skills

This project provides a Skill + Python package for generating publication-quality matplotlib plotting code.

## Using the Skill

When the user asks for plotting code, paper-style figures, or scientific visualizations, use the `paper-figure-codegen` skill:

1. Read `SKILL.md` first for the skill overview and rules
2. Read relevant `references/*.md` files as needed (data-structures, plot-selection, color-system, etc.)
3. Use the Python package (`paper_figure_codegen`) to generate code, or generate code directly following the templates

## Quick reference

- **17 plot types** available: grouped_bar, stacked_bar, horizontal_bar, line_with_ci, violin_box_scatter, boxplot, histogram_kde, heatmap, confusion_matrix, scatter_regression, multi_panel, radar, ternary, eeg_topomap, permutation_test, raincloud, flowchart_composite
- **CLI**: `paper-figure codegen --plot <type> --output <name>`
- **Python API**: `from paper_figure_codegen import get_recipe, FigureDataSpec`
- **Templates**: `templates/` has standalone runnable examples

## Project structure

- `SKILL.md` — AI Skill entry point (read this first)
- `references/` — Detailed reference docs for AI decision-making
- `paper_figure_codegen/` — Python package (core, recipes, templates, CLI)
- `templates/` — Standalone reference templates
- `examples/` — Runnable example scripts
- `tests/` — Test suite (74 tests)
