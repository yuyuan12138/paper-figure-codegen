"""Violin, box, and scatter plot recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "violin_box_scatter"
    required_data_kind = ["multi_series", "long_dataframe", "raw_measurements"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("violin_box_scatter recipe not yet implemented")
