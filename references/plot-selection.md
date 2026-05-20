# Plot Type Selection

## Decision tree

1. Is the user comparing groups/methods? → grouped_bar, horizontal_bar
2. Is the user showing distributions? → violin_box_scatter, boxplot, histogram_kde, raincloud
3. Is the data a matrix? → heatmap, confusion_matrix
4. Is the user showing trends over time/epochs? → line_with_ci
5. Is the user showing relationships between variables? → scatter_regression
6. Is the user showing multi-metric profiles? → radar
7. Does the user need multiple subplots? → multi_panel

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
