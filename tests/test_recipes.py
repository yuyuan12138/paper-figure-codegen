"""Test that each recipe generates executable Python code."""

import matplotlib
matplotlib.use("Agg")

import numpy as np
import pytest

from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.recipes import get_recipe


def _make_multi_series_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="multi_series",
        groups=["Baseline", "Method A", "Ours"],
        values=np.array([[0.72, 0.75, 0.74], [0.78, 0.79, 0.80], [0.84, 0.85, 0.86]]),
        labels=["Accuracy", "F1", "AUC"],
        suggested_plot_types=["grouped_bar"],
    )


def _make_wide_spec():
    return FigureDataSpec(
        raw_input_type="dataframe",
        data_kind="wide_dataframe",
        groups=["Baseline", "Ours"],
        labels=["Accuracy", "F1", "AUC"],
        values=np.array([[0.81, 0.79, 0.85], [0.88, 0.86, 0.91]]),
        suggested_plot_types=["grouped_bar"],
    )


class TestGroupedBarRecipe:
    def test_generate_code_returns_string(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert isinstance(code, str)
        assert len(code) > 100

    def test_generated_code_has_main(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "def main():" in code
        assert 'if __name__ == "__main__"' in code

    def test_generated_code_has_config(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "OUTPUT_DIR" in code
        assert "FIG_NAME" in code
        assert "DPI" in code

    def test_generated_code_has_palette(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        assert "PAPER_PALETTE" in code
        assert "#5B8DB8" in code

    def test_generated_code_executable(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        namespace = {}
        exec(code, namespace)
        assert "main" in namespace
        assert "plot_figure" in namespace

    def test_generated_code_runs(self):
        recipe = get_recipe("grouped_bar")
        code = recipe.generate_code(_make_wide_spec())
        namespace = {}
        exec(code, namespace)
        namespace["main"]()

    def test_validate_accepts_correct_data_kind(self):
        recipe = get_recipe("grouped_bar")
        warnings = recipe.validate(_make_wide_spec())
        assert len(warnings) == 0

    def test_validate_warns_on_wrong_data_kind(self):
        spec = FigureDataSpec(raw_input_type="list", data_kind="single_series")
        recipe = get_recipe("grouped_bar")
        warnings = recipe.validate(spec)
        assert len(warnings) > 0
