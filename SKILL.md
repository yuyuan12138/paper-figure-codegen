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
