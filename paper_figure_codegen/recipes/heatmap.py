"""Heatmap recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "heatmap"
    required_data_kind = ["matrix", "wide_dataframe", "correlation_matrix"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("heatmap recipe not yet implemented")
