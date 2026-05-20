"""Stacked bar chart recipe — proportional composition across categories."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "stacked_bar"
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
            len(spec.labels) if spec.labels else 3, kind="categorical"
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
            categories = spec.groups
            stacks = spec.labels
            vals = spec.values
            rows = []
            for i, cat in enumerate(categories):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                rows.append(f'        "{cat}": [{row_vals}],')
            cats_str = ", ".join(f'"{c}"' for c in categories)
            stacks_str = ", ".join(f'"{s}"' for s in stacks)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    categories = [" + cats_str + "]\n"
                "    stack_labels = [" + stacks_str + "]\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    return categories, stack_labels, data"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    categories = ["Session 1", "Session 2", "Session 3", "Session 4"]\n'
            '    stack_labels = ["Deep", "Light", "REM", "Awake"]\n'
            "    data = {\n"
            '        "Session 1": [0.25, 0.15, 0.30, 0.30],\n'
            '        "Session 2": [0.30, 0.10, 0.35, 0.25],\n'
            '        "Session 3": [0.20, 0.20, 0.25, 0.35],\n'
            '        "Session 4": [0.15, 0.25, 0.20, 0.40],\n'
            "    }\n"
            "    return categories, stack_labels, data"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    categories, stack_labels, data = data\n"
            "    if len(data) != len(categories):\n"
            '        raise ValueError(f"Expected {len(categories)} categories, got {len(data)}")\n'
            "    for name, vals in data.items():\n"
            "        if len(vals) != len(stack_labels):\n"
            '            raise ValueError(f"Category {name}: expected {len(stack_labels)} values, got {len(vals)}")\n'
            "        total = sum(vals)\n"
            "        if not (0.99 <= total <= 1.01):\n"
            '            print(f"Warning: {name} values sum to {total:.3f}, expected ~1.0")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    categories, stack_labels, data = data\n"
            "\n"
            "    n_categories = len(categories)\n"
            "    x = np.arange(n_categories)\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 4.5))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    bottoms = np.zeros(n_categories)\n"
            "    bars_list = []\n"
            "    for i, label in enumerate(stack_labels):\n"
            "        values = [data[cat][i] for cat in categories]\n"
            "        bars = ax.bar(x, values, label=label, color=colors[i % len(colors)], bottom=bottoms)\n"
            "        bars_list.append(bars)\n"
            "        bottoms += values\n"
            "\n"
            "    ax.set_xticks(x)\n"
            "    ax.set_xticklabels(categories)\n"
            '    ax.set_ylabel("Proportion")\n'
            '    ax.set_title("Sleep Stage Composition by Session")\n'
            '    ax.legend(loc="upper right")\n'
            "    ax.grid(axis=\"y\", linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "    ax.set_ylim(0, 1.0)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
