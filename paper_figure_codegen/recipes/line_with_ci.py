"""Line plot with confidence interval recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "line_with_ci"
    required_data_kind = ["multi_series", "long_dataframe", "summary_with_error"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("line_with_ci recipe not yet implemented")
