"""Line plot with confidence interval recipe — time series with uncertainty bands."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "line_with_ci"
    required_data_kind = ["time_series", "multi_series"]

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
            series_names = spec.groups
            vals = spec.values
            n_epochs = len(vals[0])
            rows = []
            for i, name in enumerate(series_names):
                row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                rows.append('        "' + name + '": [' + row_vals + '],')
            series_str = ", ".join(f'"{s}"' for s in series_names)
            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    series_names = [" + series_str + "]\n"
                f"    epochs = list(range(1, {n_epochs + 1}))\n"
                "    data = {\n"
                + "\n".join(rows)
                + "\n"
                "    }\n"
                "    confidence_intervals = {\n"
                + "".join([
                    f'        "{name}": (np.array([0.65] * {n_epochs}), np.array([0.75] * {n_epochs})),\n'
                    if i == 0 else
                    f'        "{name}": (np.array([0.72] * {n_epochs}), np.array([0.82] * {n_epochs})),\n'
                    if i == 1 else
                    f'        "{name}": (np.array([0.80] * {n_epochs}), np.array([0.90] * {n_epochs})),\n'
                    for i, name in enumerate(series_names)
                ])
                + "    }\n"
                "    return series_names, epochs, data, confidence_intervals"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    series_names = ["Baseline", "Method A", "Ours"]\n'
            "    epochs = list(range(1, 51))\n"
            "    data = {\n"
            '        "Baseline": [0.70, 0.71, 0.68, 0.69, 0.70, 0.71, 0.70, 0.69, 0.70, 0.71,\n'
            '                      0.70, 0.69, 0.70, 0.71, 0.70, 0.69, 0.70, 0.71, 0.70, 0.69,\n'
            '                      0.70, 0.71, 0.70, 0.69, 0.70, 0.71, 0.70, 0.69, 0.70, 0.71,\n'
            '                      0.70, 0.69, 0.70, 0.71, 0.70, 0.69, 0.70, 0.71, 0.70, 0.69,\n'
            '                      0.70, 0.71, 0.70, 0.69, 0.70, 0.71, 0.70, 0.69, 0.70, 0.71],\n'
            '        "Method A": [0.77, 0.78, 0.76, 0.77, 0.78, 0.79, 0.78, 0.77, 0.78, 0.79,\n'
            '                     0.78, 0.77, 0.78, 0.79, 0.80, 0.79, 0.78, 0.77, 0.78, 0.79,\n'
            '                     0.80, 0.79, 0.78, 0.77, 0.78, 0.79, 0.80, 0.79, 0.78, 0.77,\n'
            '                     0.78, 0.79, 0.80, 0.79, 0.78, 0.77, 0.78, 0.79, 0.80, 0.79,\n'
            '                     0.78, 0.77, 0.78, 0.79, 0.80, 0.79, 0.78, 0.77, 0.78, 0.79],\n'
            '        "Ours":     [0.85, 0.86, 0.84, 0.85, 0.86, 0.87, 0.86, 0.85, 0.84, 0.85,\n'
            '                     0.86, 0.87, 0.86, 0.85, 0.84, 0.85, 0.86, 0.87, 0.88, 0.87,\n'
            '                     0.86, 0.85, 0.84, 0.85, 0.86, 0.87, 0.88, 0.87, 0.86, 0.85,\n'
            '                     0.84, 0.85, 0.86, 0.87, 0.88, 0.87, 0.86, 0.85, 0.84, 0.85,\n'
            '                     0.86, 0.87, 0.88, 0.87, 0.86, 0.85, 0.84, 0.85, 0.86, 0.87],\n'
            "    }\n"
            "    confidence_intervals = {\n"
            '        "Baseline": (np.array([0.65] * 50), np.array([0.75] * 50)),\n'
            '        "Method A": (np.array([0.72] * 50), np.array([0.82] * 50)),\n'
            '        "Ours": (np.array([0.80] * 50), np.array([0.90] * 50)),\n'
            "    }\n"
            "    return series_names, epochs, data, confidence_intervals"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    series_names, epochs, data, confidence_intervals = data\n"
            "    if len(data) != len(series_names):\n"
            '        raise ValueError(f"Expected {len(series_names)} series, got {len(data)}")\n'
            "    for name in series_names:\n"
            "        if name not in data:\n"
            '            raise ValueError(f"Series {name} not found in data")\n'
            "        if len(data[name]) != len(epochs):\n"
            '            raise ValueError(f"Series {name}: expected {len(epochs)} values, got {len(data[name])}")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    series_names, epochs, data, confidence_intervals = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 4.5))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    for i, name in enumerate(series_names):\n"
            "        color = colors[i % len(colors)]\n"
            "        values = data[name]\n"
            "        ax.plot(epochs, values, label=name, color=color, linewidth=2.0)\n"
            "        if name in confidence_intervals:\n"
            "            lower, upper = confidence_intervals[name]\n"
            "            ax.fill_between(epochs, lower, upper, color=color, alpha=0.2)\n"
            "\n"
            "    ax.set_xlabel(\"Training Epoch\")\n"
            '    ax.set_ylabel("Accuracy")\n'
            '    ax.set_title("Training Curve with 95% Confidence Interval")\n'
            '    ax.legend(loc="lower right")\n'
            "    ax.grid(linestyle=\"--\", linewidth=0.6, alpha=0.35)\n"
            "    ax.set_ylim(0.5, 1.0)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
