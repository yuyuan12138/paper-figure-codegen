"""Flowchart composite recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "flowchart_composite"
    required_data_kind = ["diagram", "composite", "annotations"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("flowchart_composite recipe not yet implemented")
