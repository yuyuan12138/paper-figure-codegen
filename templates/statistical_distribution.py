"""Statistical distribution analysis template.

This template demonstrates comprehensive statistical visualization:
- Histogram with KDE
- Q-Q plot for normality testing
- Box plot for distribution summary
- Cumulative distribution function
- Optional scipy integration with fallback
"""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np

# Optional scipy import
try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# ==============================================================================
# CONFIG
# ==============================================================================

OUTPUT_DIR = Path("outputs")
FIG_NAME = "figure_statistical"
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

def load_data() -> np.ndarray:
    """Load or generate example data.

    TODO: Replace with your actual data loading logic.
    Expected format: 1D numpy array of numeric values.
    """
    np.random.seed(42)

    # Example: slightly skewed distribution
    data = np.random.gamma(shape=2.0, scale=1.0, size=200)

    return data


# ==============================================================================
# STATISTICAL FUNCTIONS
# ==============================================================================

def compute_statistics(data: np.ndarray) -> Dict[str, float]:
    """Compute basic descriptive statistics."""
    return {
        "mean": np.mean(data),
        "std": np.std(data, ddof=1),
        "median": np.median(data),
        "q25": np.percentile(data, 25),
        "q75": np.percentile(data, 75),
        "min": np.min(data),
        "max": np.max(data),
    }


def compute_kde(data: np.ndarray, x_grid: np.ndarray) -> Optional[np.ndarray]:
    """Compute kernel density estimate.

    Returns None if scipy is not available.
    """
    if not HAS_SCIPY:
        return None

    kde = stats.gaussian_kde(data)
    return kde(x_grid)


def perform_normality_test(data: np.ndarray) -> Optional[Dict[str, float]]:
    """Perform Shapiro-Wilk test for normality.

    Returns None if scipy is not available.
    """
    if not HAS_SCIPY:
        return None

    statistic, p_value = stats.shapiro(data)
    return {"statistic": statistic, "p_value": p_value}


# ==============================================================================
# PLOTTING FUNCTIONS
# ==============================================================================

def plot_histogram(ax: plt.Axes, data: np.ndarray) -> None:
    """Panel A: Histogram with optional KDE overlay."""
    ax.hist(data, bins=30, color=PAPER_PALETTE["blue_main"], alpha=0.6,
           edgecolor="white", linewidth=0.5, density=True, label="Histogram")

    # Add KDE if scipy is available
    if HAS_SCIPY:
        x_grid = np.linspace(data.min(), data.max(), 200)
        kde = compute_kde(data, x_grid)
        if kde is not None:
            ax.plot(x_grid, kde, color=PAPER_PALETTE["blue_dark"],
                   linewidth=2, label="KDE")

    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, linestyle="--")


def plot_boxplot(ax: plt.Axes, data: np.ndarray) -> None:
    """Panel B: Box plot with statistics annotation."""
    box = ax.boxplot([data], labels=["Data"], patch_artist=True,
                     widths=0.5, showfliers=True,
                     boxprops=dict(facecolor=PAPER_PALETTE["teal_main"], alpha=0.7),
                     medianprops=dict(color="white", linewidth=2),
                     whiskerprops=dict(color="gray", linewidth=1.5),
                     capprops=dict(color="gray", linewidth=1.5))

    ax.set_ylabel("Value")
    ax.set_ylim(data.min() - 0.5, data.max() + 0.5)
    ax.grid(True, axis="y", alpha=0.3, linestyle="--")

    # Add statistics text
    stats = compute_statistics(data)
    textstr = f"Mean: {stats['mean']:.2f}\nMedian: {stats['median']:.2f}\nStd: {stats['std']:.2f}"
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=9,
           verticalalignment="top", horizontalalignment="right",
           bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))


def plot_qq(ax: plt.Axes, data: np.ndarray) -> None:
    """Panel C: Q-Q plot for normality assessment."""
    if not HAS_SCIPY:
        ax.text(0.5, 0.5, "scipy not available\nfor Q-Q plot",
               transform=ax.transAxes, ha="center", va="center",
               fontsize=10, color="gray")
        ax.set_xticks([])
        ax.set_yticks([])
        return

    stats.probplot(data, dist="norm", plot=ax)

    # Customize styling
    ax.get_lines()[0].set_color(PAPER_PALETTE["blue_main"])
    ax.get_lines()[0].set_marker("o")
    ax.get_lines()[0].set_markersize(4)
    ax.get_lines()[0].set_alpha(0.6)
    ax.get_lines()[1].set_color(PAPER_PALETTE["orange_main"])
    ax.get_lines()[1].set_linewidth(2)

    ax.set_title("Normal Q-Q Plot", fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")


def plot_cdf(ax: plt.Axes, data: np.ndarray) -> None:
    """Panel D: Empirical cumulative distribution function."""
    sorted_data = np.sort(data)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

    ax.plot(sorted_data, cdf, color=PAPER_PALETTE["green_main"],
           linewidth=2, drawstyle="steps-post")

    ax.set_xlabel("Value")
    ax.set_ylabel("Cumulative Probability")
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3, linestyle="--")

    # Add median line
    median = np.median(data)
    ax.axvline(median, color=PAPER_PALETTE["orange_main"],
              linestyle="--", linewidth=1.5, alpha=0.7, label=f"Median: {median:.2f}")
    ax.legend(loc="lower right", fontsize=9)


# ==============================================================================
# MAIN FIGURE
# ==============================================================================

def plot_figure(data: np.ndarray) -> plt.Figure:
    """Create a 2x2 statistical analysis figure."""
    apply_paper_style()

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Panel A: Histogram
    plot_histogram(axes[0, 0], data)
    axes[0, 0].text(-0.15, 1.05, "A", transform=axes[0, 0].transAxes,
                   fontsize=14, fontweight="bold", va="top")

    # Panel B: Boxplot
    plot_boxplot(axes[0, 1], data)
    axes[0, 1].text(-0.15, 1.05, "B", transform=axes[0, 1].transAxes,
                   fontsize=14, fontweight="bold", va="top")

    # Panel C: Q-Q plot
    plot_qq(axes[1, 0], data)
    axes[1, 0].text(-0.15, 1.05, "C", transform=axes[1, 0].transAxes,
                   fontsize=14, fontweight="bold", va="top")

    # Panel D: CDF
    plot_cdf(axes[1, 1], data)
    axes[1, 1].text(-0.15, 1.05, "D", transform=axes[1, 1].transAxes,
                   fontsize=14, fontweight="bold", va="top")

    fig.suptitle("Statistical Distribution Analysis", fontsize=14, fontweight="bold", y=0.995)

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
    """Generate and save the statistical figure."""
    # Load data
    data = load_data()

    # Create plot
    fig = plot_figure(data)

    # Print statistics
    stats = compute_statistics(data)
    print("\nDescriptive Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}")

    # Normality test if scipy available
    if HAS_SCIPY:
        normality = perform_normality_test(data)
        if normality:
            print("\nNormality Test (Shapiro-Wilk):")
            print(f"  Statistic: {normality['statistic']:.4f}")
            print(f"  p-value: {normality['p_value']:.4f}")

    # Save figure
    save_figure(fig, FIG_NAME, OUTPUT_DIR, DPI, SAVE_FORMATS)
    plt.close(fig)


if __name__ == "__main__":
    main()
