import pytest

from paper_figure_codegen.recipes import get_recipe, list_recipes


class TestRecipeRegistry:
    def test_list_recipes_returns_list(self):
        recipes = list_recipes()
        assert isinstance(recipes, list)
        assert len(recipes) > 0

    def test_get_unknown_recipe_raises(self):
        with pytest.raises(KeyError):
            get_recipe("nonexistent_plot")

    def test_list_recipes_includes_mvp_types(self):
        recipes = list_recipes()
        expected = [
            "grouped_bar", "stacked_bar", "horizontal_bar",
            "line_with_ci", "violin_box_scatter", "boxplot",
            "histogram_kde", "heatmap", "confusion_matrix",
            "scatter_regression", "multi_panel",
        ]
        for name in expected:
            assert name in recipes, f"Missing MVP recipe: {name}"
