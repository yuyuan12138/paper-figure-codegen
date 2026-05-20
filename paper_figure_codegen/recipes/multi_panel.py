"""Multi-panel figure recipe — composite subplots with panel labels."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "multi_panel"
    required_data_kind = ["multi_panel_spec", "multi_series"]

    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        palette = palette or self._default_palette()
        colors = get_palette(3, kind="categorical")

        data_loading_code = self._build_data_loading(spec)
        validation_code = self._build_validation()
        plotting_code = self._build_plotting(spec, colors)

        template = _env.get_template("multi_panel.py.j2")
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
            panel_names = spec.groups
            vals = spec.values
            rows = []
            for i, name in enumerate(panel_names):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i][:10])
                rows.append(f'        "{name}": np.array([{row_vals}, ...]),')
            panels_str = ", ".join(f'"{p}"' for p in panel_names)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    panel_names = [" + panels_str + "]\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    return panel_names, data"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    panel_names = ["Accuracy", "Loss", "F1-Score", "Precision"]\n'
            "    np.random.seed(42)\n"
            "    data = {\n"
            '        "Accuracy": np.array([0.72, 0.75, 0.78, 0.80, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87]),\n'
            '        "Loss": np.array([0.45, 0.38, 0.32, 0.28, 0.24, 0.21, 0.19, 0.17, 0.16, 0.15]),\n'
            '        "F1-Score": np.array([0.70, 0.73, 0.76, 0.78, 0.80, 0.82, 0.83, 0.84, 0.85, 0.86]),\n'
            '        "Precision": np.array([0.68, 0.71, 0.74, 0.76, 0.78, 0.80, 0.81, 0.82, 0.83, 0.84]),\n'
            "    }\n"
            "    return panel_names, data"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    panel_names, data = data\n"
            "    if len(data) != len(panel_names):\n"
            '        raise ValueError(f"Expected {len(panel_names)} panels, got {len(data)}")\n'
            "    for name in panel_names:\n"
            "        if name not in data:\n"
            '            raise ValueError(f"Panel {name} not found in data")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    panel_names, data = data\n"
            "\n"
            "    fig = plt.figure(figsize=(10, 7))\n"
            "    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.30)\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    axes = []\n"
            "    panel_labels = [\"A\", \"B\", \"C\", \"D\"]\n"
            "\n"
            "    for i, (panel_name, label) in enumerate(zip(panel_names, panel_labels)):\n"
            "        ax = fig.add_subplot(gs[i])\n"
            "        axes.append(ax)\n"
            "\n"
            "        values = data[panel_name]\n"
            "        x = np.arange(len(values))\n"
            "\n"
            "        if panel_name == \"Loss\":\n"
            "            color = PAPER_PALETTE[\"orange_main\"]\n"
            "        else:\n"
            "            color = colors[i % len(colors)]\n"
            "\n"
            "        ax.plot(x, values, marker=\"o\", color=color, linewidth=2.0, markersize=6)\n"
            "        ax.set_xlabel(\"Iteration\")\n"
            "        ax.set_ylabel(panel_name)\n"
            '        ax.set_title(f"{panel_name} Over Time")\n'
            "        ax.grid(linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "\n"
            "        ax.text(-0.12, 1.02, label, transform=ax.transAxes,\n"
            "                fontsize=14, fontweight=\"bold\", va=\"bottom\", ha=\"right\")\n"
            "\n"
            "    return fig"
        )
