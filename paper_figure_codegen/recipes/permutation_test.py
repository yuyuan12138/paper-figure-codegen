"""Permutation test visualization recipe — statistical significance testing."""

import os

from jinja2 import Environment, FileSystemLoader

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes.base import BaseRecipe

_TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), keep_trailing_newline=True)


class Recipe(BaseRecipe):
    plot_type = "permutation_test"
    required_data_kind = ["single_series", "distribution_groups"]

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
        if spec.values is not None:
            # Assume first element is observed statistic, rest is null distribution
            vals = spec.values
            if vals.ndim == 1:
                observed = vals[0] if len(vals) > 0 else 0.5
                null_dist = vals[1:] if len(vals) > 1 else np.array([0.3, 0.4, 0.35, 0.45])
            else:
                observed = 0.65
                null_dist = vals.flatten()

            null_str = ", ".join(f"{v:.4f}" for v in null_dist)

            return (
                "\n"
                "    # TODO: Replace this example data with your real data.\n"
                f"    observed_statistic = {observed:.4f}\n"
                "    null_distribution = np.array([" + null_str + "])\n"
                "    return observed_statistic, null_distribution"
            )
        return (
            "\n"
            "    # TODO: Replace this example data with your real data.\n"
            "    np.random.seed(42)\n"
            "    observed_statistic = 0.65\n"
            "    null_distribution = np.random.normal(0.50, 0.08, 1000)\n"
            "    return observed_statistic, null_distribution"
        )

    def _build_validation(self) -> str:
        return (
            "\n"
            "    observed_statistic, null_distribution = data\n"
            "    if len(null_distribution) < 10:\n"
            '        raise ValueError(f"Null distribution too small: {len(null_distribution)} samples")\n'
            "    if not np.isfinite(observed_statistic):\n"
            '        raise ValueError(f"Observed statistic must be finite, got {observed_statistic}")'
        )

    def _build_plotting(self, spec: FigureDataSpec) -> str:
        return (
            "\n"
            "    apply_paper_style()\n"
            "    observed_statistic, null_distribution = data\n"
            "\n"
            "    fig, ax = plt.subplots(figsize=(7, 5))\n"
            "\n"
            "    # Calculate p-value (two-tailed)\n"
            "    p_value = np.mean(np.abs(null_distribution) >= np.abs(observed_statistic))\n"
            "\n"
            "    # Plot histogram of null distribution\n"
            "    n, bins, patches = ax.hist(null_distribution, bins=40, density=True,\n"
            "                                alpha=0.6, color='#5B8DB8', edgecolor='black', linewidth=0.8)\n"
            "\n"
            "    # Highlight the extreme regions\n"
            "    extreme_right = null_distribution >= observed_statistic\n"
            "    extreme_left = null_distribution <= -observed_statistic\n"
            "    ax.hist(null_distribution[extreme_right], bins=bins, density=True,\n"
            "            alpha=0.3, color='#E15759', label=f'p = {p_value:.3f}')\n"
            "    ax.hist(null_distribution[extreme_left], bins=bins, density=True,\n"
            "            alpha=0.3, color='#E15759')\n"
            "\n"
            "    # Vertical line for observed statistic\n"
            "    ax.axvline(observed_statistic, color='#E15759', linewidth=2.5,\n"
            "               linestyle='--', label=f'Observed = {observed_statistic:.3f}')\n"
            "    ax.axvline(-observed_statistic, color='#E15759', linewidth=2.5, linestyle='--')\n"
            "\n"
            "    # Annotate p-value\n"
            "    ax.text(0.95, 0.95, f'p = {p_value:.4f}',\n"
            "            transform=ax.transAxes, ha='right', va='top',\n"
            "            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),\n"
            "            fontsize=12, fontweight='bold')\n"
            "\n"
            "    ax.set_xlabel('Test Statistic')\n"
            "    ax.set_ylabel('Density')\n"
            '    ax.set_title("Permutation Test: Null Distribution vs. Observed")\n'
            "    ax.legend(loc='upper right')\n"
            "    ax.grid(axis='y', linestyle='--', linewidth=0.6, alpha=0.35)\n"
            "\n"
            "    fig.tight_layout(pad=1.2)\n"
            "    return fig"
        )
