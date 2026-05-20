"""Paper Figure Codegen - Publication-quality plotting code generator."""

__version__ = "0.1.0"

from paper_figure_codegen.core.color_system import PAPER_PALETTE as PAPER_PALETTE
from paper_figure_codegen.core.color_system import get_palette as get_palette
from paper_figure_codegen.core.data_parser import DataParser as DataParser
from paper_figure_codegen.core.data_spec import FigureDataSpec as FigureDataSpec
from paper_figure_codegen.core.style import apply_paper_style as apply_paper_style
from paper_figure_codegen.export import save_figure as save_figure
from paper_figure_codegen.recipes import get_recipe as get_recipe
from paper_figure_codegen.recipes import list_recipes as list_recipes