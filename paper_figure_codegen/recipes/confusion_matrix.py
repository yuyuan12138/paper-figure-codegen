"""Confusion matrix recipe — classification performance visualization."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "confusion_matrix"
    required_data_kind = ["confusion_matrix", "matrix"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()

        data_loading_code = self._build_data_loading(spec)
        validation_code = self._build_validation()
        plotting_code = self._build_plotting(spec)

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
        if spec.values is not None and len(spec.values.shape) == 2:
            matrix = spec.values
            rows, cols = matrix.shape
            class_names = spec.groups if spec.groups else [f"Class_{i}" for i in range(rows)]

            matrix_lines = []
            for row in matrix:
                row_vals = ", ".join(f"{v:.4f}" for v in row)
                matrix_lines.append(f"        [{row_vals}],")

            classes_str = ", ".join(f'"{c}"' for c in class_names)

            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    class_names = [" + classes_str + "]\n"
                "    matrix = np.array([\n"
                + "\n".join(matrix_lines)
                + "\n"
                "    ])\n"
                "    return class_names, matrix"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    class_names = ["N1", "N2", "N3", "REM", "Awake"]\n'
            "    matrix = np.array([\n"
            "        [0.72, 0.12, 0.08, 0.05, 0.03],\n"
            "        [0.10, 0.68, 0.14, 0.06, 0.02],\n"
            "        [0.06, 0.12, 0.74, 0.05, 0.03],\n"
            "        [0.04, 0.06, 0.06, 0.80, 0.04],\n"
            "        [0.02, 0.02, 0.02, 0.04, 0.90],\n"
            "    ])\n"
            "    return class_names, matrix"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    class_names, matrix = data\n"
            "    if matrix.shape[0] != matrix.shape[1]:\n"
            '        raise ValueError(f"Confusion matrix must be square, got {matrix.shape}")\n'
            "    if len(class_names) != matrix.shape[0]:\n"
            '        raise ValueError(f"Class names ({len(class_names)}) != matrix size ({matrix.shape[0]})")\n'
            "    for i, row in enumerate(matrix):\n"
            "        row_sum = row.sum()\n"
            "        if not (0.95 <= row_sum <= 1.05):\n"
            '            print(f"Warning: Row {i} ({class_names[i]}) sums to {row_sum:.3f}, expected ~1.0")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    class_names, matrix = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6, 5.5))\n"
            "\n"
            "    im = ax.imshow(matrix, cmap=\"Blues\", aspect=\"auto\", vmin=0, vmax=1)\n"
            "\n"
            "    ax.set_xticks(np.arange(len(class_names)))\n"
            "    ax.set_yticks(np.arange(len(class_names)))\n"
            "    ax.set_xticklabels(class_names)\n"
            "    ax.set_yticklabels(class_names)\n"
            "\n"
            "    for i in range(len(class_names)):\n"
            "        for j in range(len(class_names)):\n"
            "            value = matrix[i, j]\n"
            "            text_color = \"white\" if value < 0.6 else \"black\"\n"
            "            if i == j:\n"
            "                font_weight = \"bold\"\n"
            "            else:\n"
            "                font_weight = \"normal\"\n"
            '            ax.annotate(f"{value:.0%}",\n'
            "                       xy=(j, i), ha=\"center\", va=\"center\",\n"
            "                       color=text_color, fontsize=10, fontweight=font_weight)\n"
            "\n"
            '    ax.set_xlabel("Predicted Label")\n'
            '    ax.set_ylabel("True Label")\n'
            '    ax.set_title("Confusion Matrix (Normalized per True Class)")\n'
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
