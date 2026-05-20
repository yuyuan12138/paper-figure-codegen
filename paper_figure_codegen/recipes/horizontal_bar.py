"""Horizontal bar chart recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "horizontal_bar"
    required_data_kind = ["multi_series", "wide_dataframe", "grouped_table"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("horizontal_bar recipe not yet implemented")
