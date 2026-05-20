"""Permutation test visualization recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "permutation_test"
    required_data_kind = ["statistical", "distribution", "test_results"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("permutation_test recipe not yet implemented")
