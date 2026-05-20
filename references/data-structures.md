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
