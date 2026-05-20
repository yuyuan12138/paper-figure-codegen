"""Radar chart recipe — multi-metric comparison on polar axes."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "radar"
    required_data_kind = ["wide_dataframe"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()
        colors = get_palette(
            len(spec.groups) if spec.groups else 2, kind="categorical"
        )

        data_loading_code = self._build_data_loading(spec)
        validation_code = self._build_validation()
        plotting_code = self._build_plotting(spec, colors)

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
        if spec.groups and spec.labels and spec.values is not None:
            method_names = spec.groups
            metric_names = spec.labels
            matrix = spec.values

            method_str = ", ".join(f'"{m}"' for m in method_names)
            metric_str = ", ".join(f'"{m}"' for m in metric_names)

            matrix_lines = []
            for row in matrix:
                row_vals = ", ".join(f"{v:.4f}" for v in row)
                matrix_lines.append(f"        [{row_vals}],")

            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    method_names = [" + method_str + "]\n"
                "    metric_names = [" + metric_str + "]\n"
                "    matrix = np.array([\n"
                + "\n".join(matrix_lines)
                + "\n"
                "    ])\n"
                "    return method_names, metric_names, matrix"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    method_names = ["Baseline", "Ours"]\n'
            '    metric_names = ["Accuracy", "Precision", "Recall", "F1", "AUC"]\n'
            "    matrix = np.array([\n"
            "        [0.75, 0.72, 0.68, 0.70, 0.78],\n"
            "        [0.88, 0.85, 0.82, 0.86, 0.91],\n"
            "    ])\n"
            "    return method_names, metric_names, matrix"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    method_names, metric_names, matrix = data\n"
            "    if matrix.shape[0] != len(method_names):\n"
            '        raise ValueError(f"Matrix rows ({matrix.shape[0]}) != method_names ({len(method_names)})")\n'
            "    if matrix.shape[1] != len(metric_names):\n"
            '        raise ValueError(f"Matrix cols ({matrix.shape[1]}) != metric_names ({len(metric_names)})")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    method_names, metric_names, matrix = data\n"
            "\n"
            "    # Close the radar polygon by appending first value\n"
            "    N = len(metric_names)\n"
            "    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()\n"
            "    angles += angles[:1]\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    for i, method in enumerate(method_names):\n"
            "        values = matrix[i].tolist()\n"
            "        values += values[:1]\n"
            "        ax.plot(angles, values, 'o-', linewidth=2, label=method,\n"
            "                color=colors[i % len(colors)])\n"
            "        ax.fill(angles, values, alpha=0.15, color=colors[i % len(colors)])\n"
            "\n"
            "    ax.set_xticks(angles[:-1])\n"
            "    ax.set_xticklabels(metric_names)\n"
            "    ax.set_ylim(0, 1)\n"
            "    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])\n"
            "    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'])\n"
            "    ax.grid(True, linestyle='--', linewidth=0.6, alpha=0.5)\n"
            "    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))\n"
            '    ax.set_title("Multi-Metric Comparison", pad=20)\n'
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
