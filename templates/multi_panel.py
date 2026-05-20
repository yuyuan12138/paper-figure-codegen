"""Multi-panel figure template for composite scientific figures.

This template demonstrates how to create a 2x2 grid layout with:
- Panel labels (A, B, C, D)
- Different plot types in each panel
- Consistent styling across panels
- Shared axes where appropriate
"""

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# CONFIG
# ==============================================================================

OUTPUT_DIR = Path("outputs")
FIG_NAME = "figure_multi_panel"
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
# PLOTTING FUNCTIONS
# ==============================================================================

def plot_grouped_bar(ax: plt.Axes) -> None:
    """Panel A: Grouped bar chart."""
    np.random.seed(42)

    methods = ["Baseline", "CNN", "Transformer", "Ours"]
    metrics = ["Accuracy", "F1", "AUC"]

    # Example data: 4 methods × 3 metrics
    data = np.array([
        [0.81, 0.79, 0.85],
        [0.85, 0.83, 0.88],
        [0.87, 0.85, 0.90],
        [0.91, 0.89, 0.94],
    ])

    x = np.arange(len(metrics))
    width = 0.2
    colors = get_palette(len(methods), kind="categorical")

    for i, method in enumerate(methods):
        offset = (i - len(methods) / 2 + 0.5) * width
        bars = ax.bar(x + offset, data[i], width, label=method, color=colors[i])

        # Add value labels
        for bar, val in zip(bars, data[i]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                   f"{val:.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_ylabel("Score")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylim(0.7, 1.0)
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")


def plot_line_with_ci(ax: plt.Axes) -> None:
    """Panel B: Line plot with confidence interval."""
    np.random.seed(42)

    epochs = np.arange(1, 21)

    # Example learning curve data
    train_mean = 0.5 + 0.4 * (1 - np.exp(-epochs / 5))
    train_std = 0.05 * np.exp(-epochs / 10)

    val_mean = train_mean - 0.05 - 0.03 * np.sin(epochs / 3)
    val_std = 0.06 * np.exp(-epochs / 8)

    ax.plot(epochs, train_mean, color=PAPER_PALETTE["blue_main"], label="Train", linewidth=2)
    ax.fill_between(epochs, train_mean - train_std, train_mean + train_std,
                   color=PAPER_PALETTE["blue_main"], alpha=0.3)

    ax.plot(epochs, val_mean, color=PAPER_PALETTE["orange_main"], label="Validation", linewidth=2)
    ax.fill_between(epochs, val_mean - val_std, val_mean + val_std,
                   color=PAPER_PALETTE["orange_main"], alpha=0.3)

    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.set_xlim(0, 20)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, linestyle="--")


def plot_boxplot(ax: plt.Axes) -> None:
    """Panel C: Box plot comparing distributions."""
    np.random.seed(42)

    groups = ["Method A", "Method B", "Method C"]
    data = [
        np.random.normal(0.75, 0.08, 50),
        np.random.normal(0.82, 0.06, 50),
        np.random.normal(0.88, 0.05, 50),
    ]

    colors = get_palette(len(groups), kind="categorical")

    box = ax.boxplot(data, labels=groups, patch_artist=True, showfliers=True)

    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel("Performance")
    ax.set_ylim(0.5, 1.0)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")


def plot_heatmap(ax: plt.Axes) -> None:
    """Panel D: Heatmap."""
    np.random.seed(42)

    # Example correlation matrix
    data = np.corrcoef(np.random.randn(5, 50))

    labels = ["Feat1", "Feat2", "Feat3", "Feat4", "Feat5"]

    im = ax.imshow(data, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Correlation", fontsize=9)

    # Add annotations
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, f"{data[i, j]:.2f}",
                          ha="center", va="center", fontsize=8)

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)


# ==============================================================================
# MAIN FIGURE
# ==============================================================================

def plot_figure() -> plt.Figure:
    """Create a 2x2 multi-panel figure."""
    apply_paper_style()

    fig = plt.figure(figsize=(10, 8))

    # Create 2x2 grid with spacing
    grid = plt.GridSpec(2, 2, hspace=0.35, wspace=0.35, figure=fig)

    # Panel A: Grouped bar (top-left)
    ax_a = fig.add_subplot(grid[0, 0])
    plot_grouped_bar(ax_a)
    ax_a.text(-0.15, 1.05, "A", transform=ax_a.transAxes,
             fontsize=14, fontweight="bold", va="top")

    # Panel B: Line with CI (top-right)
    ax_b = fig.add_subplot(grid[0, 1])
    plot_line_with_ci(ax_b)
    ax_b.text(-0.15, 1.05, "B", transform=ax_b.transAxes,
             fontsize=14, fontweight="bold", va="top")

    # Panel C: Boxplot (bottom-left)
    ax_c = fig.add_subplot(grid[1, 0])
    plot_boxplot(ax_c)
    ax_c.text(-0.15, 1.05, "C", transform=ax_c.transAxes,
             fontsize=14, fontweight="bold", va="top")

    # Panel D: Heatmap (bottom-right)
    ax_d = fig.add_subplot(grid[1, 1])
    plot_heatmap(ax_d)
    ax_d.text(-0.15, 1.05, "D", transform=ax_d.transAxes,
             fontsize=14, fontweight="bold", va="top")

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
    """Generate and save the multi-panel figure."""
    fig = plot_figure()
    save_figure(fig, FIG_NAME, OUTPUT_DIR, DPI, SAVE_FORMATS)
    plt.close(fig)


if __name__ == "__main__":
    main()
