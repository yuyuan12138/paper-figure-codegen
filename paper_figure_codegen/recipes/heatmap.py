"""Heatmap recipe — matrix visualization with annotations."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "heatmap"
    required_data_kind = ["matrix", "correlation_table"]

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
            row_labels = spec.groups if spec.groups else [f"Row_{i}" for i in range(rows)]
            col_labels = spec.labels if spec.labels else [f"Col_{i}" for i in range(cols)]

            matrix_lines = []
            for row in matrix:
                row_vals = ", ".join(f"{v:.4f}" for v in row)
                matrix_lines.append(f"        [{row_vals}],")

            row_str = ", ".join(f'"{r}"' for r in row_labels)
            col_str = ", ".join(f'"{c}"' for c in col_labels)

            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    row_labels = [" + row_str + "]\n"
                "    col_labels = [" + col_str + "]\n"
                "    matrix = np.array([\n"
                + "\n".join(matrix_lines)
                + "\n"
                "    ])\n"
                "    return row_labels, col_labels, matrix"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    row_labels = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]\n'
            '    col_labels = ["Fz", "Cz", "Pz", "Oz"]\n'
            "    matrix = np.array([\n"
            "        [0.82, 0.75, 0.68, 0.52],\n"
            "        [0.45, 0.58, 0.62, 0.48],\n"
            "        [0.38, 0.42, 0.55, 0.65],\n"
            "        [0.28, 0.32, 0.38, 0.42],\n"
            "        [0.22, 0.25, 0.28, 0.32],\n"
            "    ])\n"
            "    return row_labels, col_labels, matrix"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    row_labels, col_labels, matrix = data\n"
            "    if matrix.shape[0] != len(row_labels):\n"
            '        raise ValueError(f"Matrix rows ({matrix.shape[0]}) != row_labels ({len(row_labels)})")\n'
            "    if matrix.shape[1] != len(col_labels):\n"
            '        raise ValueError(f"Matrix cols ({matrix.shape[1]}) != col_labels ({len(col_labels)})")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    row_labels, col_labels, matrix = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6, 5))\n"
            "\n"
            "    im = ax.imshow(matrix, cmap=\"Blues\", aspect=\"auto\", vmin=0, vmax=1)\n"
            "\n"
            "    ax.set_xticks(np.arange(len(col_labels)))\n"
            "    ax.set_yticks(np.arange(len(row_labels)))\n"
            "    ax.set_xticklabels(col_labels)\n"
            "    ax.set_yticklabels(row_labels)\n"
            "\n"
            "    for i in range(len(row_labels)):\n"
            "        for j in range(len(col_labels)):\n"
            "            value = matrix[i, j]\n"
            "            text_color = \"white\" if value < 0.5 else \"black\"\n"
            '            ax.annotate(f"{value:.2f}",\n'
            "                       xy=(j, i), ha=\"center\", va=\"center\",\n"
            "                       color=text_color, fontsize=10)\n"
            "\n"
            "    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)\n"
            '    cbar.set_label("Value")\n'
            '    ax.set_title("Band Power Across Electrode Sites")\n'
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
