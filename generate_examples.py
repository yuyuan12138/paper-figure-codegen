"""Generate all example scripts using the recipe system."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from paper_figure_codegen.recipes import get_recipe
from paper_figure_codegen.core.data_spec import FigureDataSpec
import numpy as np

# Example 1: grouped_bar
spec1 = FigureDataSpec(
    raw_input_type='example',
    data_kind='wide_dataframe',
    groups=['Baseline', 'CNN', 'Transformer', 'Ours'],
    labels=['Accuracy', 'F1', 'AUC'],
    values=np.array([
        [0.81, 0.79, 0.85],
        [0.85, 0.83, 0.88],
        [0.87, 0.85, 0.90],
        [0.91, 0.89, 0.94]
    ]),
)

code1 = get_recipe('grouped_bar').generate_code(spec1)
with open('examples/grouped_bar_example.py', 'w') as f:
    f.write(code1)
print("Generated examples/grouped_bar_example.py")

# Example 2: violin_box_scatter
np.random.seed(42)
spec2 = FigureDataSpec(
    raw_input_type='example',
    data_kind='multi_series',
    groups=['Model A', 'Model B', 'Model C'],
    values=[
        np.random.normal(0.75, 0.08, 50),
        np.random.normal(0.82, 0.06, 50),
        np.random.normal(0.88, 0.05, 50),
    ],
)

code2 = get_recipe('violin_box_scatter').generate_code(spec2)
with open('examples/violin_box_example.py', 'w') as f:
    f.write(code2)
print("Generated examples/violin_box_example.py")

# Example 3: confusion_matrix
spec3 = FigureDataSpec(
    raw_input_type='example',
    data_kind='confusion_matrix',
    matrix=np.array([
        [45, 5, 2, 0],
        [3, 48, 4, 1],
        [1, 3, 46, 5],
        [0, 2, 3, 50],
    ]),
    labels=['Class A', 'Class B', 'Class C', 'Class D'],
)

code3 = get_recipe('confusion_matrix').generate_code(spec3)
with open('examples/confusion_matrix_example.py', 'w') as f:
    f.write(code3)
print("Generated examples/confusion_matrix_example.py")

# Example 4: multi_panel
spec4 = FigureDataSpec(
    raw_input_type='example',
    data_kind='multi_panel_spec',
    metadata={
        'panels': [
            {'type': 'grouped_bar', 'position': (0, 0)},
            {'type': 'line_with_ci', 'position': (0, 1)},
            {'type': 'boxplot', 'position': (1, 0)},
            {'type': 'heatmap', 'position': (1, 1)},
        ],
        'nrows': 2,
        'ncols': 2,
    },
)

code4 = get_recipe('multi_panel').generate_code(spec4)
with open('examples/multi_panel_example.py', 'w') as f:
    f.write(code4)
print("Generated examples/multi_panel_example.py")

# Example 5: line_with_ci (time series)
epochs = np.arange(1, 21)
spec5 = FigureDataSpec(
    raw_input_type='example',
    data_kind='time_series',
    x=epochs,
    groups=['Train', 'Validation'],
    values=[
        0.5 + 0.4 * (1 - np.exp(-epochs / 5)),  # Train mean
        0.5 + 0.35 * (1 - np.exp(-epochs / 5)) - 0.03 * np.sin(epochs / 3),  # Validation mean
    ],
    labels=[f'Epoch {i}' for i in epochs],
)

code5 = get_recipe('line_with_ci').generate_code(spec5)
with open('examples/time_series_example.py', 'w') as f:
    f.write(code5)
print("Generated examples/time_series_example.py")

print("\nAll examples generated successfully!")
