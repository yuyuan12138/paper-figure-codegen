"""EEG topomap recipe — spatial visualization of channel data."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "eeg_topomap"
    required_data_kind = ["eeg_channel_table", "matrix"]

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
        if spec.labels and spec.values is not None and spec.metadata:
            channel_names = spec.labels
            values = spec.values
            x_pos = spec.metadata.get("x", [0.0] * len(channel_names))
            y_pos = spec.metadata.get("y", [0.0] * len(channel_names))

            channels_str = ", ".join(f'"{ch}"' for ch in channel_names)
            values_str = ", ".join(f"{v:.4f}" for v in values)
            x_str = ", ".join(f"{x:.4f}" for x in x_pos)
            y_str = ", ".join(f"{y:.4f}" for y in y_pos)

            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                "    channel_names = [" + channels_str + "]\n"
                "    values = np.array([" + values_str + "])\n"
                "    x_pos = np.array([" + x_str + "])\n"
                "    y_pos = np.array([" + y_str + "])\n"
                "    return channel_names, values, x_pos, y_pos"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            '    channel_names = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"]\n'
            "    values = np.array([0.21, 0.18, 0.15, 0.16, 0.12, 0.11, 0.09, 0.10, 0.07, 0.08])\n"
            "    x_pos = np.array([-0.3, 0.3, -0.4, 0.4, -0.2, 0.2, -0.15, 0.15, -0.1, 0.1])\n"
            "    y_pos = np.array([0.8, 0.8, 0.5, 0.5, 0.2, 0.2, -0.1, -0.1, -0.4, -0.4])\n"
            "    return channel_names, values, x_pos, y_pos"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    channel_names, values, x_pos, y_pos = data\n"
            "    if len(channel_names) != len(values):\n"
            '        raise ValueError(f"channel_names ({len(channel_names)}) != values ({len(values)})")\n'
            "    if len(channel_names) != len(x_pos):\n"
            '        raise ValueError(f"channel_names ({len(channel_names)}) != x_pos ({len(x_pos)})")\n'
            "    if len(channel_names) != len(y_pos):\n"
            '        raise ValueError(f"channel_names ({len(channel_names)}) != y_pos ({len(y_pos)})")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    channel_names, values, x_pos, y_pos = data\n"
            "\n"
            "    # Try to use MNE if available\n"
            "    try:\n"
            "        import mne\n"
            "        HAS_MNE = True\n"
            "    except ImportError:\n"
            "        HAS_MNE = False\n"
            "\n"
            "    # Try to use scipy for interpolation\n"
            "    try:\n"
            "        from scipy.interpolate import Rbf\n"
            "        HAS_SCIPY = True\n"
            "    except ImportError:\n"
            "        HAS_SCIPY = False\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 6))\n"
            "\n"
            "    if HAS_MNE:\n"
            "        # Use MNE's plot_topomap for professional visualization\n"
            "        info = mne.create_info(ch_names=channel_names, sfreq=256, ch_types='eeg')\n"
            "        for i, ch in enumerate(channel_names):\n"
            "            info['chs'][i]['loc'][:2] = [x_pos[i], y_pos[i]]\n"
            "        im, _ = mne.viz.plot_topomap(values, info, axes=ax, show=False,\n"
            "                                     cmap='RdBu_r', vmin=values.min(), vmax=values.max())\n"
            "    elif HAS_SCIPY:\n"
            "        # Fallback: interpolated scatter plot\n"
            "        xi = np.linspace(x_pos.min()-0.1, x_pos.max()+0.1, 100)\n"
            "        yi = np.linspace(y_pos.min()-0.1, y_pos.max()+0.1, 100)\n"
            "        zi_grid, yi_grid = np.meshgrid(xi, yi)\n"
            "        rbf = Rbf(x_pos, y_pos, values, function='multiquadric')\n"
            "        zi = rbf(zi_grid, yi_grid)\n"
            "        im = ax.pcolormesh(zi_grid, yi_grid, zi, cmap='RdBu_r',\n"
            "                          shading='auto', vmin=values.min(), vmax=values.max())\n"
            "        ax.scatter(x_pos, y_pos, c=values, cmap='RdBu_r', s=150,\n"
            "                   edgecolors='black', linewidth=1.5, vmin=values.min(), vmax=values.max())\n"
            "        for i, ch in enumerate(channel_names):\n"
            "            ax.annotate(ch, (x_pos[i], y_pos[i]), fontsize=9,\n"
            "                       ha='center', va='center', fontweight='bold', color='white')\n"
            "\n"
            "        # Draw head outline\n"
            "        head_circle = plt.Circle((0, 0), 0.5, fill=False, edgecolor='black', linewidth=2)\n"
            "        ax.add_patch(head_circle)\n"
            "    else:\n"
            "        # Ultimate fallback: simple scatter plot\n"
            "        im = ax.scatter(x_pos, y_pos, c=values, cmap='RdBu_r', s=300,\n"
            "                      edgecolors='black', linewidth=1.5, vmin=values.min(), vmax=values.max())\n"
            "        for i, ch in enumerate(channel_names):\n"
            "            ax.annotate(ch, (x_pos[i], y_pos[i]), fontsize=10,\n"
            "                       ha='center', va='center', fontweight='bold')\n"
            "\n"
            "        # Draw head outline\n"
            "        head_circle = plt.Circle((0, 0), 0.5, fill=False, edgecolor='black', linewidth=2)\n"
            "        ax.add_patch(head_circle)\n"
            "\n"
            "    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)\n"
            '    cbar.set_label("Power")\n'
            '    ax.set_title("EEG Topography", pad=20)\n'
            "    ax.set_aspect('equal')\n"
            "    ax.axis('off')\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
