"""Multi-panel figure recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "multi_panel"
    required_data_kind = ["mixed", "composite", "subfigures"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("multi_panel recipe not yet implemented")
