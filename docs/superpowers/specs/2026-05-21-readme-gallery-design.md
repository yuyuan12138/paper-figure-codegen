# README Gallery Design

## Goal

Add example images for all 17 plot types to the README, presented as a gallery grid.

## Approach

1. Create 12 new example scripts (5 already exist) covering all 17 plot types
2. Run all scripts to generate PNG images into `docs/figures/`
3. Add a gallery grid section to README.md using an HTML table (3 columns)

## New Example Scripts

Existing (keep as-is): grouped_bar, confusion_matrix, multi_panel, time_series (line_with_ci), violin_box_scatter

New scripts to create in `examples/`:

- `stacked_bar_example.py`
- `horizontal_bar_example.py`
- `boxplot_example.py`
- `histogram_kde_example.py`
- `heatmap_example.py`
- `scatter_regression_example.py`
- `radar_example.py`
- `ternary_example.py`
- `eeg_topomap_example.py`
- `permutation_test_example.py`
- `raincloud_example.py`
- `flowchart_composite_example.py`

Each script:
- Uses `paper_figure_codegen` package or templates
- Generates data inline (no external files)
- Outputs PNG to `docs/figures/`
- Uniform size: ~6x4 inches, 150 DPI
- Graceful handling of optional deps (e.g., mne for eeg_topomap)

## Image Storage

- Directory: `docs/figures/`
- Format: PNG, 150 DPI
- Estimated total: ~4-7 MB (17 images)

## README Layout

Add a **Gallery** section with an HTML table grid (3 columns, 6 rows):

```
| grouped_bar | stacked_bar | horizontal_bar |
| line_with_ci | violin_box_scatter | boxplot |
| histogram_kde | heatmap | confusion_matrix |
| scatter_regression | multi_panel | radar |
| ternary | eeg_topomap | permutation_test |
| raincloud | flowchart_composite | |
```

Each cell: thumbnail image + type name label.

## Constraints

- No external data files required
- eeg_topomap skips gracefully if mne is not installed
- Images committed to repo for offline viewing
