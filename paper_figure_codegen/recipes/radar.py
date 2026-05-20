"""Radar chart recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "radar"
    required_data_kind = ["multi_series", "wide_dataframe", "normalized_dimensions"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("radar recipe not yet implemented")
