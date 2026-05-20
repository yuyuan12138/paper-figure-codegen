"""Confusion matrix recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "confusion_matrix"
    required_data_kind = ["matrix", "wide_dataframe", "classification_results"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("confusion_matrix recipe not yet implemented")
