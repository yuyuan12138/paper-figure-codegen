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
