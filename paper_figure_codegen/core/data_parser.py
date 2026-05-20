"""Parse raw user data into FigureDataSpec."""

from typing import Any

import numpy as np
import pandas as pd

from paper_figure_codegen.core.data_spec import FigureDataSpec, DATA_KINDS


class DataParser:
    """Identify data structure and produce a FigureDataSpec."""

    @staticmethod
    def parse(data: Any) -> FigureDataSpec:
        if isinstance(data, dict):
            return DataParser._parse_dict(data)
        if isinstance(data, (list, tuple)):
            return DataParser._parse_list(data)
        if isinstance(data, np.ndarray):
            return DataParser._parse_ndarray(data)
        if isinstance(data, pd.DataFrame):
            return DataParser._parse_dataframe(data)
        return FigureDataSpec(
            raw_input_type=type(data).__name__,
            data_kind="single_series",
            warnings=[f"Unknown data type: {type(data).__name__}"],
        )

    @staticmethod
    def _parse_dict(data: dict) -> FigureDataSpec:
        values = list(data.values())
        if all(isinstance(v, (list, tuple, np.ndarray)) for v in values):
            labels = list(data.keys())
            return FigureDataSpec(
                raw_input_type="dict_of_lists",
                data_kind="multi_series",
                groups=labels,
                values=np.array([np.asarray(v, dtype=float) for v in values]),
                labels=labels,
                suggested_plot_types=["grouped_bar", "violin_box_scatter", "boxplot", "line_with_ci"],
            )
        return FigureDataSpec(
            raw_input_type="dict",
            data_kind="single_series",
            values=np.array(list(data.values())),
            labels=list(data.keys()),
            suggested_plot_types=["bar", "horizontal_bar"],
        )

    @staticmethod
    def _parse_list(data) -> FigureDataSpec:
        arr = np.asarray(data, dtype=float)
        if arr.ndim == 1:
            return FigureDataSpec(
                raw_input_type="list",
                data_kind="single_series",
                values=arr,
                suggested_plot_types=["histogram_kde", "bar"],
            )
        if arr.ndim == 2:
            return FigureDataSpec(
                raw_input_type="list",
                data_kind="matrix",
                matrix=arr,
                suggested_plot_types=["heatmap", "confusion_matrix"],
            )
        return FigureDataSpec(
            raw_input_type="list",
            data_kind="single_series",
            values=arr,
            warnings=["High-dimensional array, treating as single_series"],
        )

    @staticmethod
    def _parse_ndarray(data: np.ndarray) -> FigureDataSpec:
        if data.ndim == 2:
            kind = "confusion_matrix" if DataParser._looks_like_confusion_matrix(data) else "matrix"
            return FigureDataSpec(
                raw_input_type="ndarray",
                data_kind=kind,
                matrix=data,
                suggested_plot_types=["heatmap", "confusion_matrix"],
            )
        return FigureDataSpec(
            raw_input_type="ndarray",
            data_kind="single_series",
            values=data,
            suggested_plot_types=["histogram_kde", "bar"],
        )

    @staticmethod
    def _parse_dataframe(df: pd.DataFrame) -> FigureDataSpec:
        if DataParser._is_ranking_table(df):
            label_col = df.columns[0]
            value_col = df.columns[1]
            return FigureDataSpec(
                raw_input_type="dataframe",
                data_kind="ranking_table",
                labels=df[label_col].tolist(),
                values=df[value_col].to_numpy(dtype=float),
                suggested_plot_types=["horizontal_bar"],
            )
        if DataParser._is_wide_dataframe(df):
            label_col = df.columns[0]
            metric_cols = df.columns[1:]
            return FigureDataSpec(
                raw_input_type="dataframe",
                data_kind="wide_dataframe",
                groups=df[label_col].tolist(),
                labels=metric_cols.tolist(),
                values=df[metric_cols].to_numpy(dtype=float),
                suggested_plot_types=["grouped_bar", "radar", "heatmap"],
            )
        return FigureDataSpec(
            raw_input_type="dataframe",
            data_kind="long_dataframe",
            suggested_plot_types=["grouped_bar", "violin_box_scatter", "boxplot", "line_with_ci"],
        )

    @staticmethod
    def _looks_like_confusion_matrix(arr: np.ndarray) -> bool:
        if arr.shape[0] != arr.shape[1]:
            return False
        try:
            row_sums = arr.sum(axis=1)
            return bool(np.allclose(row_sums, 1.0, atol=0.05))
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _is_ranking_table(df: pd.DataFrame) -> bool:
        if len(df.columns) != 2:
            return False
        first = df[df.columns[0]].dtype
        second = df[df.columns[1]].dtype
        is_string = first == object or str(first) == "string" or first.kind == "O" or first.kind == "U"
        return is_string and np.issubdtype(second, np.number)

    @staticmethod
    def _is_wide_dataframe(df: pd.DataFrame) -> bool:
        if len(df.columns) < 3:
            return False
        first = df[df.columns[0]].dtype
        rest_dtypes = [df[c].dtype for c in df.columns[1:]]
        is_string = first == object or str(first) == "string" or first.kind == "O" or first.kind == "U"

        # Check if all rest columns are numeric (handle string dtypes gracefully)
        all_numeric = True
        for dt in rest_dtypes:
            try:
                if not np.issubdtype(dt, np.number):
                    all_numeric = False
                    break
            except TypeError:
                all_numeric = False
                break

        return is_string and all_numeric
