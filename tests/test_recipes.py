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


# ===== Spec Helpers =====


def _make_stacked_spec():
    return FigureDataSpec(
        raw_input_type="dataframe",
        data_kind="wide_dataframe",
        groups=["Session 1", "Session 2", "Session 3", "Session 4"],
        labels=["Deep", "Light", "REM", "Awake"],
        values=np.array([
            [0.25, 0.15, 0.30, 0.30],
            [0.30, 0.10, 0.35, 0.25],
            [0.20, 0.20, 0.25, 0.35],
            [0.15, 0.25, 0.20, 0.40],
        ]),
        suggested_plot_types=["stacked_bar"],
    )


def _make_ranking_spec():
    return FigureDataSpec(
        raw_input_type="dict",
        data_kind="ranking_table",
        labels=["Band Power Delta", "Band Power Theta", "Spectral Entropy", "Hjorth Parameters"],
        values=np.array([0.125, 0.098, 0.076, 0.065]),
        suggested_plot_types=["horizontal_bar"],
    )


def _make_time_series_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="time_series",
        groups=["Baseline", "Method A", "Ours"],
        values=np.array([
            [0.70] * 10,
            [0.77] * 10,
            [0.85] * 10,
        ]),
        suggested_plot_types=["line_with_ci"],
    )


def _make_single_series_spec():
    return FigureDataSpec(
        raw_input_type="array",
        data_kind="single_series",
        values=np.random.normal(0.65, 0.15, 50),
        suggested_plot_types=["histogram_kde"],
    )


def _make_matrix_spec():
    return FigureDataSpec(
        raw_input_type="array_2d",
        data_kind="matrix",
        groups=["Delta", "Theta", "Alpha", "Beta", "Gamma"],
        labels=["Fz", "Cz", "Pz", "Oz"],
        values=np.array([
            [0.82, 0.75, 0.68, 0.52],
            [0.45, 0.58, 0.62, 0.48],
            [0.38, 0.42, 0.55, 0.65],
            [0.28, 0.32, 0.38, 0.42],
            [0.22, 0.25, 0.28, 0.32],
        ]),
        suggested_plot_types=["heatmap"],
    )


def _make_confusion_matrix_spec():
    return FigureDataSpec(
        raw_input_type="array_2d",
        data_kind="confusion_matrix",
        groups=["N1", "N2", "N3", "REM", "Awake"],
        values=np.array([
            [0.72, 0.12, 0.08, 0.05, 0.03],
            [0.10, 0.68, 0.14, 0.06, 0.02],
            [0.06, 0.12, 0.74, 0.05, 0.03],
            [0.04, 0.06, 0.06, 0.80, 0.04],
            [0.02, 0.02, 0.02, 0.04, 0.90],
        ]),
        suggested_plot_types=["confusion_matrix"],
    )


def _make_scatter_spec():
    return FigureDataSpec(
        raw_input_type="array_2d",
        data_kind="single_series",
        values=np.array([
            np.random.uniform(0.4, 0.9, 30),
            np.random.uniform(0.3, 0.8, 30),
        ]),
        suggested_plot_types=["scatter_regression"],
    )


def _make_multi_panel_spec():
    return FigureDataSpec(
        raw_input_type="dict_of_lists",
        data_kind="multi_panel_spec",
        groups=["Accuracy", "Loss", "F1-Score", "Precision"],
        values=np.array([
            [0.72, 0.75, 0.78, 0.80, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87],
            [0.45, 0.38, 0.32, 0.28, 0.24, 0.21, 0.19, 0.17, 0.16, 0.15],
            [0.70, 0.73, 0.76, 0.78, 0.80, 0.82, 0.83, 0.84, 0.85, 0.86],
            [0.68, 0.71, 0.74, 0.76, 0.78, 0.80, 0.81, 0.82, 0.83, 0.84],
        ]),
        suggested_plot_types=["multi_panel"],
    )


# ===== Test Classes =====


class TestStackedBarRecipe:
    def test_generate_code(self):
        recipe = get_recipe("stacked_bar")
        spec = _make_stacked_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code

    def test_executable(self):
        recipe = get_recipe("stacked_bar")
        spec = _make_stacked_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestHorizontalBarRecipe:
    def test_generate_code(self):
        recipe = get_recipe("horizontal_bar")
        spec = _make_ranking_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "feature_importance" in code

    def test_executable(self):
        recipe = get_recipe("horizontal_bar")
        spec = _make_ranking_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestLineWithCIRecipe:
    def test_generate_code(self):
        recipe = get_recipe("line_with_ci")
        spec = _make_time_series_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "fill_between" in code

    def test_executable(self):
        recipe = get_recipe("line_with_ci")
        spec = _make_time_series_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestViolinBoxScatterRecipe:
    def test_generate_code(self):
        recipe = get_recipe("violin_box_scatter")
        spec = _make_multi_series_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "violinplot" in code
        assert "boxplot" in code
        assert "scatter" in code

    def test_executable(self):
        recipe = get_recipe("violin_box_scatter")
        spec = _make_multi_series_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestBoxplotRecipe:
    def test_generate_code(self):
        recipe = get_recipe("boxplot")
        spec = _make_multi_series_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "boxplot" in code

    def test_executable(self):
        recipe = get_recipe("boxplot")
        spec = _make_multi_series_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestHistogramKDERecipe:
    def test_generate_code(self):
        recipe = get_recipe("histogram_kde")
        spec = _make_single_series_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "hist" in code

    def test_executable(self):
        recipe = get_recipe("histogram_kde")
        spec = _make_single_series_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestHeatmapRecipe:
    def test_generate_code(self):
        recipe = get_recipe("heatmap")
        spec = _make_matrix_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "imshow" in code

    def test_executable(self):
        recipe = get_recipe("heatmap")
        spec = _make_matrix_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestConfusionMatrixRecipe:
    def test_generate_code(self):
        recipe = get_recipe("confusion_matrix")
        spec = _make_confusion_matrix_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "Blues" in code

    def test_executable(self):
        recipe = get_recipe("confusion_matrix")
        spec = _make_confusion_matrix_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestScatterRegressionRecipe:
    def test_generate_code(self):
        recipe = get_recipe("scatter_regression")
        spec = _make_scatter_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "scatter" in code
        assert "polyfit" in code

    def test_executable(self):
        recipe = get_recipe("scatter_regression")
        spec = _make_scatter_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()


class TestMultiPanelRecipe:
    def test_generate_code(self):
        recipe = get_recipe("multi_panel")
        spec = _make_multi_panel_spec()
        code = recipe.generate_code(spec)
        assert "def main():" in code
        assert "PAPER_PALETTE" in code
        assert "GridSpec" in code

    def test_executable(self):
        recipe = get_recipe("multi_panel")
        spec = _make_multi_panel_spec()
        code = recipe.generate_code(spec)
        namespace = {}
        exec(code, namespace)
        namespace["main"]()
