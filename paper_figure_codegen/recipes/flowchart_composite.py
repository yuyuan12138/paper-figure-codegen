"""Flowchart composite recipe — multi-panel with flow diagram and data plots."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "flowchart_composite"
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
        if spec.groups and spec.values is not None:
            panel_names = spec.groups
            vals = spec.values
            # Check if values is a 2D array where each row corresponds to a panel
            if vals.ndim == 2 and vals.shape[0] == len(panel_names):
                rows = []
                for i, name in enumerate(panel_names):
                    row_vals = ", ".join(f"{v:.4f}" for v in vals[i])
                    rows.append(f'        "{name}": np.array([{row_vals}]),')
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
            '    panel_names = ["Method Overview", "Training Loss", "Accuracy", "Inference Time"]\n'
            "    np.random.seed(42)\n"
            "    data = {\n"
            '        "Method Overview": np.array([0.0]),\n'
            '        "Training Loss": np.array([0.85, 0.72, 0.58, 0.45, 0.35, 0.28, 0.22, 0.18]),\n'
            '        "Accuracy": np.array([0.65, 0.72, 0.78, 0.82, 0.85, 0.87, 0.88, 0.89]),\n'
            '        "Inference Time": np.array([12.5, 8.3, 5.2, 3.8, 2.9, 2.4, 2.1, 1.9]),\n'
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
            "    colors = [\n"
            + color_lines
            + "\n"
            "    ]\n"
            "\n"
            "    # Create multi-panel figure\n"
            "    fig = plt.figure(figsize=(12, 8))\n"
            "    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)\n"
            "\n"
            "    # Panel A: Flowchart (Method Overview)\n"
            "    ax_flow = fig.add_subplot(gs[0, 0])\n"
            "    ax_flow.set_xlim(0, 10)\n"
            "    ax_flow.set_ylim(0, 10)\n"
            "    ax_flow.axis('off')\n"
            "    ax_flow.text(5, 9.5, 'A', fontsize=14, fontweight='bold', ha='left')\n"
            "\n"
            "    # Draw flowchart boxes\n"
            "    from matplotlib.patches import Rectangle, FancyArrowPatch\n"
            "    box_color = '#5B8DB8'\n"
            "    arrow_color = '#707070'\n"
            "\n"
            "    # Input box\n"
            "    rect1 = Rectangle((2, 8), 6, 1, facecolor=box_color, edgecolor='black', linewidth=1.5)\n"
            "    ax_flow.add_patch(rect1)\n"
            "    ax_flow.text(5, 8.5, 'Input Data', ha='center', va='center',\n"
            "                fontsize=11, fontweight='bold', color='white')\n"
            "\n"
            "    # Feature extraction box\n"
            "    rect2 = Rectangle((2, 6), 6, 1, facecolor=box_color, edgecolor='black', linewidth=1.5)\n"
            "    ax_flow.add_patch(rect2)\n"
            "    ax_flow.text(5, 6.5, 'Feature Extraction', ha='center', va='center',\n"
            "                fontsize=11, fontweight='bold', color='white')\n"
            "\n"
            "    # Model box\n"
            "    rect3 = Rectangle((2, 4), 6, 1, facecolor=box_color, edgecolor='black', linewidth=1.5)\n"
            "    ax_flow.add_patch(rect3)\n"
            "    ax_flow.text(5, 4.5, 'Model Processing', ha='center', va='center',\n"
            "                fontsize=11, fontweight='bold', color='white')\n"
            "\n"
            "    # Output box\n"
            "    rect4 = Rectangle((2, 2), 6, 1, facecolor=colors[1], edgecolor='black', linewidth=1.5)\n"
            "    ax_flow.add_patch(rect4)\n"
            "    ax_flow.text(5, 2.5, 'Output', ha='center', va='center',\n"
            "                fontsize=11, fontweight='bold', color='white')\n"
            "\n"
            "    # Arrows\n"
            "    arrow1 = FancyArrowPatch((5, 8), (5, 7), arrowstyle='->',\n"
            "                             mutation_scale=20, color=arrow_color, linewidth=2)\n"
            "    arrow2 = FancyArrowPatch((5, 6), (5, 5), arrowstyle='->',\n"
            "                             mutation_scale=20, color=arrow_color, linewidth=2)\n"
            "    arrow3 = FancyArrowPatch((5, 4), (5, 3), arrowstyle='->',\n"
            "                             mutation_scale=20, color=arrow_color, linewidth=2)\n"
            "    ax_flow.add_patch(arrow1)\n"
            "    ax_flow.add_patch(arrow2)\n"
            "    ax_flow.add_patch(arrow3)\n"
            "\n"
            "    # Panel B: Training Loss\n"
            "    ax_loss = fig.add_subplot(gs[0, 1])\n"
            "    ax_loss.text(-0.1, 1.05, 'B', transform=ax_loss.transAxes,\n"
            "                 fontsize=14, fontweight='bold', va='top')\n"
            "    loss_data = data['Training Loss']\n"
            "    epochs = np.arange(1, len(loss_data) + 1)\n"
            "    ax_loss.plot(epochs, loss_data, 'o-', color=colors[0],\n"
            "                linewidth=2, markersize=6)\n"
            "    ax_loss.set_xlabel('Epoch')\n"
            "    ax_loss.set_ylabel('Loss')\n"
            "    ax_loss.set_title('Training Loss')\n"
            "    ax_loss.grid(True, linestyle='--', linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    # Panel C: Accuracy\n"
            "    ax_acc = fig.add_subplot(gs[0, 2])\n"
            "    ax_acc.text(-0.1, 1.05, 'C', transform=ax_acc.transAxes,\n"
            "                fontsize=14, fontweight='bold', va='top')\n"
            "    acc_data = data['Accuracy']\n"
            "    ax_acc.plot(epochs, acc_data, 'o-', color=colors[1],\n"
            "               linewidth=2, markersize=6)\n"
            "    ax_acc.set_xlabel('Epoch')\n"
            "    ax_acc.set_ylabel('Accuracy')\n"
            "    ax_acc.set_title('Validation Accuracy')\n"
            "    ax_acc.set_ylim(0.5, 1.0)\n"
            "    ax_acc.grid(True, linestyle='--', linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    # Panel D: Inference Time\n"
            "    ax_time = fig.add_subplot(gs[1, :])\n"
            "    ax_time.text(-0.02, 1.05, 'D', transform=ax_time.transAxes,\n"
            "                 fontsize=14, fontweight='bold', va='top')\n"
            "    time_data = data['Inference Time']\n"
            "    ax_time.plot(epochs, time_data, 'o-', color=colors[2],\n"
            "                linewidth=2, markersize=6)\n"
            "    ax_time.set_xlabel('Epoch')\n"
            "    ax_time.set_ylabel('Time (ms)')\n"
            "    ax_time.set_title('Inference Time')\n"
            "    ax_time.grid(True, linestyle='--', linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    fig.suptitle('Method Overview and Performance', fontsize=14, fontweight='bold', y=0.98)\n"
            "\n"
            "    return fig"
        )
