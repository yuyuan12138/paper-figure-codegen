"""Ternary plot recipe — three-component composition visualization."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "ternary"
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
            len(spec.groups) if spec.groups else 1, kind="categorical"
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
            '    group_names = ["Sample A", "Sample B", "Sample C", "Sample D"]\n'
            "    np.random.seed(42)\n"
            "    data = {\n"
            '        "Sample A": np.array([0.6, 0.3, 0.1]),\n'
            '        "Sample B": np.array([0.2, 0.5, 0.3]),\n'
            '        "Sample C": np.array([0.15, 0.25, 0.6]),\n'
            '        "Sample D": np.array([0.33, 0.34, 0.33]),\n'
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
            "        comps = data[name]\n"
            "        if len(comps) != 3:\n"
            '            raise ValueError(f"Ternary plot requires exactly 3 components, got {len(comps)}")\n'
            "        if not np.isclose(comps.sum(), 1.0, atol=0.01):\n"
            '            print(f"Warning: {name} components sum to {comps.sum():.3f}, not 1.0")'
        )

    def _build_plotting(self, spec: FigureDataSpec, colors: list) -> str:
        color_lines = "\n".join(f'        "{c}",' for c in colors)
        return (
            "\n"
            "    apply_paper_style()\n"
            "    group_names, data = data\n"
            "\n"
            "    # Ternary coordinate transform: (a, b, c) -> (x, y)\n"
            "    # where a, b, c are proportions summing to 1\n"
            "    def ternary_to_xy(a, b, c):\n"
            "        total = a + b + c\n"
            "        x = 0.5 * (2 * b + c) / total\n"
            "        y = (np.sqrt(3) / 2) * c / total\n"
            "        return x, y\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 6))\n"
            "\n"
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    # Draw triangle outline\n"
            "    triangle_x = [0, 1, 0.5, 0]\n"
            "    triangle_y = [0, 0, np.sqrt(3)/2, 0]\n"
            "    ax.plot(triangle_x, triangle_y, 'k-', linewidth=1.5)\n"
            "\n"
            "    # Draw grid lines\n"
            "    for i in range(1, 10):\n"
            "        alpha = i / 10.0\n"
            "        # Lines from A vertex to opposite side\n"
            "        ax.plot([alpha * 0.5, 0.5], [alpha * np.sqrt(3)/2, np.sqrt(3)/2],\n"
            "                'k--', linewidth=0.5, alpha=0.3)\n"
            "        # Lines from B vertex to opposite side\n"
            "        ax.plot([alpha, alpha], [0, np.sqrt(3)/2 * (1-alpha)],\n"
            "                'k--', linewidth=0.5, alpha=0.3)\n"
            "        # Lines from C vertex to opposite side\n"
            "        ax.plot([0, 1 - alpha * 0.5], [alpha * np.sqrt(3)/2, 0],\n"
            "                'k--', linewidth=0.5, alpha=0.3)\n"
            "\n"
            "    # Plot data points\n"
            "    for i, name in enumerate(group_names):\n"
            "        a, b, c = data[name]\n"
            "        x, y = ternary_to_xy(a, b, c)\n"
            "        ax.scatter(x, y, s=200, color=colors[i % len(colors)],\n"
            "                   edgecolors='black', linewidth=1.5, label=name, zorder=5)\n"
            "\n"
            "    # Vertex labels\n"
            "    ax.text(-0.08, -0.05, 'Component A', fontsize=11, ha='right', fontweight='bold')\n"
            "    ax.text(1.08, -0.05, 'Component B', fontsize=11, ha='left', fontweight='bold')\n"
            "    ax.text(0.5, np.sqrt(3)/2 + 0.05, 'Component C',\n"
            "            fontsize=11, ha='center', fontweight='bold')\n"
            "\n"
            "    ax.set_xlim(-0.15, 1.15)\n"
            "    ax.set_ylim(-0.15, np.sqrt(3)/2 + 0.15)\n"
            "    ax.set_aspect('equal')\n"
            "    ax.axis('off')\n"
            "    ax.legend(loc='upper right', frameon=True, fontsize=10)\n"
            '    ax.set_title("Ternary Composition Plot", pad=20)\n'
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
