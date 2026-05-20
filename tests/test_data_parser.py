import numpy as np
import pandas as pd

from paper_figure_codegen.core.data_parser import DataParser


class TestDataParserDictOfLists:
    def test_multi_series(self):
        data = {
            "Model A": [0.72, 0.75, 0.78],
            "Model B": [0.69, 0.71, 0.74],
            "Model C": [0.80, 0.82, 0.83],
        }
        spec = DataParser.parse(data)
        assert spec.raw_input_type == "dict_of_lists"
        assert spec.data_kind == "multi_series"
        assert spec.labels == ["Model A", "Model B", "Model C"]
        assert "grouped_bar" in spec.suggested_plot_types
        assert "violin_box_scatter" in spec.suggested_plot_types

    def test_single_series(self):
        data = [1.2, 1.5, 1.3, 1.7, 1.4]
        spec = DataParser.parse(data)
        assert spec.data_kind == "single_series"
        assert "histogram_kde" in spec.suggested_plot_types


class TestDataParserMatrix:
    def test_confusion_matrix(self):
        matrix = np.array([
            [0.82, 0.10, 0.08],
            [0.15, 0.75, 0.10],
            [0.05, 0.12, 0.83],
        ])
        spec = DataParser.parse(matrix)
        assert spec.raw_input_type == "ndarray"
        assert spec.data_kind in ("matrix", "confusion_matrix")
        assert "heatmap" in spec.suggested_plot_types
        assert "confusion_matrix" in spec.suggested_plot_types


class TestDataParserLongDataFrame:
    def test_long_table(self):
        df = pd.DataFrame({
            "subject": ["S01", "S01", "S02", "S02"],
            "session": [1, 2, 1, 2],
            "emotion": ["happy", "sad", "happy", "sad"],
            "value": [0.61, 0.23, 0.58, 0.29],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "long_dataframe"
        assert "grouped_bar" in spec.suggested_plot_types


class TestDataParserWideDataFrame:
    def test_wide_table(self):
        df = pd.DataFrame({
            "method": ["Baseline", "Ours"],
            "Accuracy": [0.81, 0.88],
            "F1": [0.79, 0.86],
            "AUC": [0.85, 0.91],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "wide_dataframe"
        assert "grouped_bar" in spec.suggested_plot_types


class TestDataParserRankingTable:
    def test_ranking(self):
        df = pd.DataFrame({
            "feature": ["gamma", "beta", "alpha"],
            "importance": [0.36, 0.24, 0.19],
        })
        spec = DataParser.parse(df)
        assert spec.data_kind == "ranking_table"
        assert "horizontal_bar" in spec.suggested_plot_types
