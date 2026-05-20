"""Ternary plot recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "ternary"
    required_data_kind = ["three_component", "composition_data"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("ternary recipe not yet implemented")
