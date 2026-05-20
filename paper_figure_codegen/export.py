"""Figure export helper — save to PNG, PDF, SVG."""

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt


def save_figure(
    fig: plt.Figure,
    name: str = "figure",
    output_dir: Path | str = "outputs",
    formats: List[str] | None = None,
    dpi: int = 300,
) -> List[Path]:
    """Save figure to multiple formats. Returns list of saved paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if formats is None:
        formats = ["png", "pdf", "svg"]
    saved = []
    for fmt in formats:
        path = output_dir / f"{name}.{fmt}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        saved.append(path)
    return saved
