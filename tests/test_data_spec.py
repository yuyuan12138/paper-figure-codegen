import numpy as np
import pytest

from paper_figure_codegen.core.data_spec import (
    DATA_KINDS,
    FigureDataSpec,
)


class TestFigureDataSpec:
    def test_create_with_defaults(self):
        spec = FigureDataSpec(
            raw_input_type="dict_of_lists",
            data_kind="multi_series",
        )
        assert spec.raw_input_type == "dict_of_lists"
        assert spec.data_kind == "multi_series"
        assert spec.x is None
        assert spec.y is None
        assert spec.groups is None
        assert spec.values is None
        assert spec.matrix is None
        assert spec.labels is None
        assert spec.metadata == {}
        assert spec.suggested_plot_types == []
        assert spec.warnings == []

    def test_create_with_all_fields(self):
        spec = FigureDataSpec(
            raw_input_type="csv_path",
            data_kind="wide_dataframe",
            x=["Baseline", "Method A", "Ours"],
            y=None,
            groups=["Accuracy", "F1", "AUC"],
            values=np.array([[0.81, 0.79, 0.85], [0.88, 0.86, 0.91]]),
            labels=["Accuracy", "F1", "AUC"],
            metadata={"source": "results.csv"},
            suggested_plot_types=["grouped_bar", "radar", "heatmap"],
            warnings=["Missing 2 rows"],
        )
        assert spec.raw_input_type == "csv_path"
        assert spec.data_kind == "wide_dataframe"
        assert spec.values.shape == (2, 3)
        assert len(spec.suggested_plot_types) == 3
        assert len(spec.warnings) == 1

    def test_data_kinds_constant(self):
        assert "multi_series" in DATA_KINDS
        assert "confusion_matrix" in DATA_KINDS
        assert "wide_dataframe" in DATA_KINDS
        assert "ranking_table" in DATA_KINDS
        assert "eeg_channel_table" in DATA_KINDS
        assert len(DATA_KINDS) == 13
