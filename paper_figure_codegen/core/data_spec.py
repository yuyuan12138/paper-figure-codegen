"""Unified data specification for figure generation."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

DATA_KINDS = [
    "single_series",
    "multi_series",
    "grouped_table",
    "long_dataframe",
    "wide_dataframe",
    "matrix",
    "confusion_matrix",
    "time_series",
    "distribution_groups",
    "ranking_table",
    "correlation_table",
    "eeg_channel_table",
    "multi_panel_spec",
]


@dataclass
class FigureDataSpec:
    """Unified description of user data for plot type selection and code generation."""

    raw_input_type: str
    data_kind: str
    x: Optional[Any] = None
    y: Optional[Any] = None
    groups: Optional[List[str]] = None
    values: Optional[Any] = None
    matrix: Optional[Any] = None
    labels: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    suggested_plot_types: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
