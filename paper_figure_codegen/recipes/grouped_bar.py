"""Grouped bar chart recipe — model x metric comparison."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "grouped_bar"
    required_data_kind = ["multi_series", "wide_dataframe", "grouped_table"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()
        colors = get_palette(
            len(spec.groups) if spec.groups else 3, kind="categorical"
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
            methods = spec.groups
            metrics = spec.labels
            vals = spec.values
            rows = []
            for i, method in enumerate(methods):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                rows.append(f'        "{method}": [{row_vals}],')
            methods_str = ", ".join(f'"{m}"' for m in methods)
            metrics_str = ", ".join(f'"{m}"' for m in metrics)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    methods = [" + methods_str + "]\n"
                "    metrics = [" + metrics_str + "]\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    return methods, metrics, data"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    methods = ["Baseline", "Method A", "Ours"]\n'
            '    metrics = ["Accuracy", "F1", "AUC"]\n'
            "    data = {\n"
            '        "Baseline": [0.81, 0.79, 0.85],\n'
            '        "Method A": [0.84, 0.82, 0.88],\n'
            '        "Ours":     [0.88, 0.86, 0.91],\n'
            "    }\n"
            "    return methods, metrics, data"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    methods, metrics, data = data\n"
            "    if len(data) != len(methods):\n"
            '        raise ValueError(f"Expected {len(methods)} methods, got {len(data)}")\n'
            "    for name, vals in data.items():\n"
            "        if len(vals) != len(metrics):\n"
            '            raise ValueError(f"Method {name}: expected {len(metrics)} values, got {len(vals)}")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    methods, metrics, data = data\n"
            "\n"
            "    n_methods = len(methods)\n"
            "    n_metrics = len(metrics)\n"
            "    x = np.arange(n_metrics)\n"
            "    width = 0.8 / n_methods\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6, 4.5))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    for i, method in enumerate(methods):\n"
            "        offset = (i - n_methods / 2 + 0.5) * width\n"
            "        bars = ax.bar(x + offset, data[method], width, label=method, color=colors[i % len(colors)])\n"
            "        for bar in bars:\n"
            "            height = bar.get_height()\n"
            '            ax.annotate(f"{height:.2f}",\n'
            "                        xy=(bar.get_x() + bar.get_width() / 2, height),\n"
            "                        xytext=(0, 3), textcoords=\"offset points\",\n"
            "                        ha=\"center\", va=\"bottom\", fontsize=8)\n"
            "\n"
            "    ax.set_xticks(x)\n"
            "    ax.set_xticklabels(metrics)\n"
            '    ax.set_ylabel("Score")\n'
            '    ax.set_title("Method Comparison")\n'
            '    ax.legend(loc="upper right")\n'
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    y_min = min(min(v) for v in data.values())\n"
            "    ax.set_ylim(max(0, y_min - 0.05), 1.0)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
