"""Box plot recipe — statistical distribution comparison."""

import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "boxplot"
    required_data_kind = ["multi_series", "distribution_groups"]

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
        if spec.groups and spec.values is not None:
            group_names = spec.groups
            vals = spec.values
            rows = []
            for i, name in enumerate(group_names):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                rows.append(f'        "{name}": np.array([{row_vals}]),')
            groups_str = ", ".join(f'"{g}"' for g in group_names)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    group_names = [" + groups_str + "]\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    return group_names, data"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    group_names = ["Control", "Treatment A", "Treatment B"]\n'
            "    np.random.seed(42)\n"
            "    data = {\n"
            '        "Control": np.random.normal(0.50, 0.12, 40),\n'
            '        "Treatment A": np.random.normal(0.65, 0.10, 40),\n'
            '        "Treatment B": np.random.normal(0.72, 0.08, 40),\n'
            "    }\n"
            "    return group_names, data"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    group_names, data = data\n"
            "    if len(data) != len(group_names):\n"
            '        raise ValueError(f"Expected {len(group_names)} groups, got {len(data)}")\n'
            "    for name in group_names:\n"
            "        if name not in data:\n"
            '            raise ValueError(f"Group {name} not found in data")\n'
            "        if len(data[name]) < 5:\n"
            '            print(f"Warning: Group {name} has only {len(data[name])} samples")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    group_names, data = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(6.5, 5))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    box_plots = ax.boxplot(\n"
            "        [data[name] for name in group_names],\n"
            "        labels=group_names,\n"
            "        patch_artist=True,\n"
            "        showfliers=True,\n"
            "        boxprops=dict(linewidth=1.2),\n"
            "        whiskerprops=dict(linewidth=1.2),\n"
            "        capprops=dict(linewidth=1.2),\n"
            "        medianprops=dict(color=\"white\", linewidth=2.0),\n"
            "        flierprops=dict(marker=\"o\", markersize=4, markerfacecolor=\"none\", markeredgecolor=\"gray\"),\n"
            "    )\n"
            "\n"
            "    for patch, color in zip(box_plots[\"boxes\"], colors):\n"
            "        patch.set_facecolor(color)\n"
            "        patch.set_alpha(0.7)\n"
            "\n"
            "    ax.set_ylabel(\"Score\")\n"
            '    ax.set_title("Group Distribution Comparison")\n'
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
