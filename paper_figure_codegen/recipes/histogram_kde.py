"""Histogram with KDE recipe — distribution visualization."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "histogram_kde"
    required_data_kind = ["single_series"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()
        colors = get_palette(1, kind="categorical")

        data_loading_code = self._build_data_loading(spec)
        validation_code = self._build_validation()
        plotting_code = self._build_plotting(spec, colors)

        template = _env.get_template("statistical.py.j2")
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
        if spec.values is not None and spec.values.flatten().size > 0:
            vals = spec.values.flatten()
            vals_str = ", ".join(f"{v:.4f}" for v in vals)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    np.random.seed(42)\n"
                f"    data = np.array([{vals_str}])\n"
                "    return data"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            "    np.random.seed(42)\n"
            "    data = np.random.normal(0.65, 0.15, 200)\n"
            "    data = np.clip(data, 0, 1)\n"
            "    return data"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    if len(data) == 0:\n"
            '        raise ValueError("data array is empty")\n'
            "    if len(data) < 10:\n"
            '        print(f"Warning: Only {len(data)} samples, histogram may be unreliable")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 4.5))\n"
            "\n"
            "    color = PAPER_PALETTE[\"blue_main\"]\n"
            "    n, bins, patches = ax.hist(data, bins=30, density=True,\n"
            "                                color=color, alpha=0.6, edgecolor=\"white\", linewidth=0.8)\n"
            "\n"
            "    if HAS_SCIPY:\n"
            "        kde = gaussian_kde(data)\n"
            "        x_range = np.linspace(data.min(), data.max(), 200)\n"
            "        ax.plot(x_range, kde(x_range), color=PAPER_PALETTE[\"blue_dark\"],\n"
            "                linewidth=2.5, label=\"KDE\")\n"
            "        ax.legend(loc=\"upper right\")\n"
            "    else:\n"
            "        print(\"scipy not available, skipping KDE curve\")\n"
            "\n"
            "    ax.set_xlabel(\"Value\")\n"
            '    ax.set_ylabel("Density")\n'
            '    ax.set_title("Distribution with Histogram and KDE")\n'
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
