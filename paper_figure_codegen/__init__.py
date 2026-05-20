"""Paper Figure Codegen - Publication-quality plotting code generator."""

__version__ = "0.1.0"

from paper_figure_codegen.core.color_system import PAPER_PALETTE, get_palette
from paper_figure_codegen.core.data_parser import DataParser
from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.core.style import apply_paper_style
from paper_figure_codegen.export import save_figure
from paper_figure_codegen.recipes import get_recipe, list_recipes