"""Raincloud plot recipe — half-violin, box, and scatter combination."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "raincloud"
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
            '        "Control": np.random.normal(0.50, 0.12, 50),\n'
            '        "Treatment A": np.random.normal(0.65, 0.10, 50),\n'
            '        "Treatment B": np.random.normal(0.72, 0.08, 50),\n'
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
            "    fig, ax = plt.subplots(figsize=(8, 6))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    # Create raincloud plot for each group\n"
            "    for i, (group_name, group_data) in enumerate(zip(group_names, [data[name] for name in group_names])):\n"
            "        color = colors[i % len(colors)]\n"
            "        x_pos = i + 1\n"
            "\n"
            "        # 1. Half-violin (top) - using KDE\n"
            "        if HAS_SCIPY:\n"
            "            kde = gaussian_kde(group_data)\n"
            "            y_range = np.linspace(group_data.min(), group_data.max(), 200)\n"
            "            density = kde(y_range)\n"
            "            # Scale density to match violin width\n"
            "            density_scaled = density * 0.3 / density.max()\n"
            "            ax.fill_betweenx(y_range, x_pos - density_scaled, x_pos,\n"
            "                           alpha=0.5, color=color)\n"
            "            ax.plot([x_pos - density_scaled.max(), x_pos],\n"
            "                   [group_data.mean(), group_data.mean()],\n"
            "                   color=color, linewidth=1)\n"
            "        else:\n"
            "            # Fallback: simple violin using matplotlib\n"
            "            parts = ax.violinplot([group_data], positions=[x_pos],\n"
            "                                 vert=True, widths=0.5,\n"
            "                                 showmeans=False, showmedians=False,\n"
            "                                 showextrema=False)\n"
            "            for pc in parts['bodies']:\n"
            "                pc.set_facecolor(color)\n"
            "                pc.set_alpha(0.5)\n"
            "\n"
            "        # 2. Box plot (middle)\n"
            "        box_stats = ax.boxplot([group_data], positions=[x_pos], widths=0.15,\n"
            "                                patch_artist=True, showfliers=False,\n"
            "                                boxprops=dict(facecolor='white',\n"
            "                                             edgecolor='gray', linewidth=1.2),\n"
            "                                whiskerprops=dict(color='gray', linewidth=1.2),\n"
            "                                capprops=dict(color='gray', linewidth=1.2),\n"
            "                                medianprops=dict(color='black', linewidth=1.5))\n"
            "\n"
            "        # 3. Scatter (bottom) - strip plot with jitter\n"
            "        y_jitter = np.random.normal(0, 0.02, size=len(group_data))\n"
            "        ax.scatter(x_pos + y_jitter, group_data, color=color,\n"
            "                  alpha=0.6, s=25, edgecolors='white', linewidth=0.5, zorder=3)\n"
            "\n"
            "    # Formatting\n"
            "    ax.set_xticks(np.arange(1, len(group_names) + 1))\n"
            "    ax.set_xticklabels(group_names)\n"
            "    ax.set_ylabel('Value')\n"
            '    ax.set_title("Raincloud Plot: Distribution Comparison")\n'
            "    ax.grid(axis='y', linestyle='--', linewidth=0.6, alpha=0.35)\n"
            "    ax.set_xlim(0.5, len(group_names) + 0.5)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
