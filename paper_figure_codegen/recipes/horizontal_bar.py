"""Horizontal bar chart recipe — feature importance or rankings."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "horizontal_bar"
    required_data_kind = ["ranking_table", "single_series"]

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
        if spec.labels and spec.values is not None:
            features = spec.labels
            vals = spec.values
            feature_lines = []
            for i, feat in enumerate(features):
                feature_lines.append(f'        "{feat}": {vals[i]:.4f},')
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    feature_importance = {\n"
                + "\n".join(feature_lines)
                + "\n"
                "    }\n"
                "    return feature_importance"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            "    feature_importance = {\n"
            '        "Band Power Delta": 0.125,\n'
            '        "Band Power Theta": 0.098,\n'
            '        "Band Power Alpha": 0.087,\n'
            '        "Spectral Entropy": 0.076,\n'
            '        "Hjorth Parameters": 0.065,\n'
            '        "Fractal Dimension": 0.054,\n'
            '        "Connectivity Strength": -0.043,\n'
            '        "Phase Lag Index": -0.032,\n'
            "    }\n"
            "    return feature_importance"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    feature_importance = data\n"
            "    if not feature_importance:\n"
            '        raise ValueError("feature_importance dictionary is empty")\n'
            "    for name, val in feature_importance.items():\n"
            "        if not isinstance(val, (int, float)):\n"
            '            raise ValueError(f"Feature {name}: value must be numeric, got {type(val)}")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    feature_importance = data\n"
            "\n"
            "    features = list(feature_importance.keys())\n"
            "    values = list(feature_importance.values())\n"
            "\n"
            "    sorted_indices = sorted(range(len(values)), key=lambda i: values[i])\n"
            "    sorted_features = [features[i] for i in sorted_indices]\n"
            "    sorted_values = [values[i] for i in sorted_indices]\n"
            "\n"
            "    colors = [PAPER_PALETTE[\"positive\"] if v >= 0 else PAPER_PALETTE[\"negative\"] for v in sorted_values]\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 5))\n"
            "    y_pos = np.arange(len(sorted_features))\n"
            "\n"
            "    bars = ax.barh(y_pos, sorted_values, color=colors, edgecolor=\"white\", height=0.7)\n"
            "\n"
            "    ax.set_yticks(y_pos)\n"
            "    ax.set_yticklabels(sorted_features)\n"
            '    ax.set_xlabel("Importance Score")\n'
            '    ax.set_title("Feature Importance Rankings")\n'
            "    ax.axvline(x=0, color=\"gray\", linestyle=\"-\", linewidth=1.0)\n"
            "    ax.grid(axis=\"x\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    for bar, val in zip(bars, sorted_values):\n"
            "        width = bar.get_width()\n"
            "        offset = 0.02 if width >= 0 else -0.02\n"
            '        ax.annotate(f"{val:.3f}",\n'
            "                    xy=(width + offset, bar.get_y() + bar.get_height() / 2),\n"
            "                    xytext=(4, 0), textcoords=\"offset points\",\n"
            "                    ha=\"left\" if width >= 0 else \"right\", va=\"center\", fontsize=9)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
