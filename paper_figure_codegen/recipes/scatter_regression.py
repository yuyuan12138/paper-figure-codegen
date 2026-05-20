"""Scatter plot with regression recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "scatter_regression"
    required_data_kind = ["two_series", "long_dataframe", "correlation_data"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("scatter_regression recipe not yet implemented")
