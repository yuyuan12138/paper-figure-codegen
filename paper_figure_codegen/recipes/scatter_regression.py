"""Scatter plot with regression line recipe — correlation analysis."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "scatter_regression"
    required_data_kind = ["single_series"]

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
        if spec.values is not None and spec.values.shape[0] >= 2:
            x_vals = spec.values[0]
            y_vals = spec.values[1]
            x_str = ", ".join(f"{v:.4f}" for v in x_vals)
            y_str = ", ".join(f"{v:.4f}" for v in y_vals)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    np.random.seed(42)\n"
                f"    x = np.array([{x_str}])\n"
                f"    y = np.array([{y_str}])\n"
                "    return x, y"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            "    np.random.seed(42)\n"
            "    x = np.random.uniform(0.4, 0.9, 50)\n"
            "    y = 0.7 * x + 0.2 + np.random.normal(0, 0.05, 50)\n"
            "    y = np.clip(y, 0, 1)\n"
            "    return x, y"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    x, y = data\n"
            "    if len(x) != len(y):\n"
            '        raise ValueError(f"x and y must have same length: {len(x)} != {len(y)}")\n'
            "    if len(x) < 5:\n"
            '        print(f"Warning: Only {len(x)} samples, regression may be unreliable")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    x, y = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6.5, 5))\n"
            "\n"
            "    color = PAPER_PALETTE[\"blue_main\"]\n"
            "    ax.scatter(x, y, color=color, alpha=0.6, s=50, edgecolors=\"white\", linewidth=0.8)\n"
            "\n"
            "    coeffs = np.polyfit(x, y, 1)\n"
            "    slope, intercept = coeffs\n"
            "    x_line = np.array([x.min(), x.max()])\n"
            "    y_line = slope * x_line + intercept\n"
            "    ax.plot(x_line, y_line, color=PAPER_PALETTE[\"blue_dark\"], linewidth=2.5,\n"
            "            label=f\"y = {slope:.2f}x + {intercept:.2f}\")\n"
            "\n"
            "    correlation = np.corrcoef(x, y)[0, 1]\n"
            '    ax.text(0.05, 0.95, f"r = {correlation:.3f}",\n'
            "            transform=ax.transAxes, va=\"top\", ha=\"left\",\n"
            "            bbox=dict(boxstyle=\"round\", facecolor=\"white\", alpha=0.8),\n"
            "            fontsize=11)\n"
            "\n"
            "    ax.set_xlabel(\"X Variable\")\n"
            '    ax.set_ylabel("Y Variable")\n'
            '    ax.set_title("Correlation with Linear Regression")\n'
            "    ax.legend(loc=\"lower right\")\n"
            "    ax.grid(linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
