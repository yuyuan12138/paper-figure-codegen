"""Paper-style matplotlib rcParams configuration."""

import matplotlib.pyplot as plt


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
