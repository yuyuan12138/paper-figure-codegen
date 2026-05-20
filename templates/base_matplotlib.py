"""Base matplotlib template for publication-quality scientific figures.

This template demonstrates the core structure for generating paper-ready plots:
- PAPER_PALETTE color system
- apply_paper_style configuration
- Data loading and validation
- Violin + box + scatter plot (signature visualization)
- Export to PNG, PDF, SVG
"""

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==============================================================================
# CONFIG
# ==============================================================================

OUTPUT_DIR = Path("outputs")
FIG_NAME = "figure_base"
DPI = 300
SAVE_FORMATS = ["png", "pdf", "svg"]

# ==============================================================================
# STYLE
# ==============================================================================

PAPER_PALETTE = {
    "blue_main": "#5B8DB8",
    "blue_dark": "#3E6F95",
    "blue_light": "#BFD8EA",
    "teal_main": "#6FA8A6",
    "teal_dark": "#4D8583",
    "green_light": "#CFE8D5",
    "green_main": "#9CCB9E",
    "yellow_light": "#F3E6B3",
    "orange_light": "#E8B77D",
    "orange_main": "#D99A5E",
    "purple_light": "#C9BEDF",
    "pink_light": "#E7C1C0",
    "gray_light": "#E8ECEF",
    "gray": "#BFC7CD",
    "gray_dark": "#66727C",
    "positive": "#6FA8A6",
    "negative": "#D99A5E",
    "neutral": "#BFC7CD",
    "highlight": "#F3C567",
}


def get_palette(n: int, kind: str = "categorical") -> List[str]:
    """Return a color palette appropriate for the given kind and group count."""
    categorical_base = [
        PAPER_PALETTE["blue_main"],
        PAPER_PALETTE["teal_main"],
        PAPER_PALETTE["green_main"],
        PAPER_PALETTE["yellow_light"],
        PAPER_PALETTE["orange_light"],
        PAPER_PALETTE["purple_light"],
    ]

    if kind == "categorical":
        if n <= len(categorical_base):
            return categorical_base[:n]
        return [plt.cm.tab20(i / n) for i in range(n)]

    if kind == "binary":
        return [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    if kind == "positive_negative":
        return [PAPER_PALETTE["orange_main"], PAPER_PALETTE["gray_light"], PAPER_PALETTE["blue_main"]]

    if kind == "sequential":
        return "Blues"

    if kind == "diverging":
        return "RdBu_r"

    raise ValueError(f"Unknown palette kind: {kind}")


def apply_paper_style(font_size: int = 12, linewidth: float = 1.2) -> None:
    """Apply publication-quality style to matplotlib defaults."""
    plt.rcParams.update({
        "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": font_size,
        "axes.linewidth": linewidth,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


# ==============================================================================
# DATA LOADING
# ==============================================================================

def load_data() -> Dict[str, np.ndarray]:
    """Load or generate example data.

    TODO: Replace with your actual data loading logic.
    Expected format: dict mapping group names to value arrays.
    """
    np.random.seed(42)

    # Example: 3 models × 4 seeds each
    data = {
        "Baseline": np.random.normal(0.75, 0.05, 30),
        "CNN": np.random.normal(0.82, 0.04, 30),
        "Transformer": np.random.normal(0.87, 0.03, 30),
    }

    return data


# ==============================================================================
# DATA VALIDATION
# ==============================================================================

def validate_data(data: Dict[str, np.ndarray]) -> None:
    """Validate that data has the expected structure."""
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary mapping group names to arrays")

    if len(data) == 0:
        raise ValueError("Data dictionary is empty")

    for name, values in data.items():
        if not isinstance(values, np.ndarray):
            raise ValueError(f"Values for '{name}' must be numpy arrays")
        if values.ndim != 1:
            raise ValueError(f"Values for '{name}' must be 1-dimensional")
        if len(values) == 0:
            raise ValueError(f"Values for '{name}' are empty")


# ==============================================================================
# PLOTTING
# ==============================================================================

def plot_figure(data: Dict[str, np.ndarray]) -> plt.Figure:
    """Create a violin + box + scatter plot comparing distributions across groups."""
    apply_paper_style()

    groups = list(data.keys())
    colors = get_palette(len(groups), kind="categorical")

    fig, ax = plt.subplots(figsize=(6, 4.5))

    # Prepare data for plotting
    positions = np.arange(len(groups))
    all_data = [data[group] for group in groups]

    # 1. Violin plots (half-violin)
    parts = ax.violinplot(
        all_data,
        positions=positions,
        widths=0.6,
        showmeans=False,
        showmedians=False,
        showextrema=False,
    )

    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_alpha(0.6)

    # 2. Box plots
    box = ax.boxplot(
        all_data,
        positions=positions,
        widths=0.3,
        patch_artist=True,
        showfliers=False,
        boxprops=dict(facecolor="white", edgecolor="gray", linewidth=1),
        medianprops=dict(color="gray", linewidth=1.5),
        whiskerprops=dict(color="gray", linewidth=1),
        capprops=dict(color="gray", linewidth=1),
    )

    # 3. Scatter points (jittered)
    for i, (group, values) in enumerate(data.items()):
        x_scatter = np.random.normal(i, 0.04, size=len(values))
        ax.scatter(x_scatter, values, color=colors[i], alpha=0.5, s=15, zorder=3)

    # Styling
    ax.set_xticks(positions)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Performance Score")
    ax.set_title("Model Performance Comparison")

    # Grid
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    # Remove spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout(pad=1.2)

    return fig


# ==============================================================================
# EXPORT
# ==============================================================================

def save_figure(fig: plt.Figure, name: str, output_dir: Path, dpi: int, formats: List[str]) -> None:
    """Save figure in multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        output_path = output_dir / f"{name}.{fmt}"
        fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
        print(f"Saved: {output_path}")


# ==============================================================================
# MAIN
# ==============================================================================

def main() -> None:
    """Generate and save the figure."""
    # Load data
    data = load_data()

    # Validate data
    validate_data(data)

    # Create plot
    fig = plot_figure(data)

    # Save figure
    save_figure(fig, FIG_NAME, OUTPUT_DIR, DPI, SAVE_FORMATS)

    plt.close(fig)


if __name__ == "__main__":
    main()
