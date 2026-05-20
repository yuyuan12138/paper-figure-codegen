"""Core modules for data parsing, color system, and style."""

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_parser import DataParser
from paper_figure_codegen.core.data_spec import DATA_KINDS, FigureDataSpec
from paper_figure_codegen.core.style import apply_paper_style

__all__ = [
    "PAPER_PALETTE",
    "get_palette",
    "DataParser",
    "DATA_KINDS",
    "FigureDataSpec",
    "apply_paper_style",
]