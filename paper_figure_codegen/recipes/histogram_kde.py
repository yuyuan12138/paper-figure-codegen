"""Histogram with KDE recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "histogram_kde"
    required_data_kind = ["single_series", "long_dataframe", "raw_measurements"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("histogram_kde recipe not yet implemented")
