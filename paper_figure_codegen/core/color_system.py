"""Paper-style muted color palette and palette selection."""

from typing import List, Union

import matplotlib.pyplot as plt

PAPER_PALETTE = {
    "blue_main": "#5B8DB8",
    "blue_dark": "#3E6F95",
    "blue_light": "#BFD8EA",
    "teal_main": "#6FA8A6",
    "teal_dark": "#4D8583",
    "green_light": "#CFE8D5",
    "green_main": "#9CCB9E",
    "yellow_light": "#F3E6B3",
    "orange_light": "#E8B77D",
    "orange_main": "#D99A5E",
    "purple_light": "#C9BEDF",
    "pink_light": "#E7C1C0",
    "gray_light": "#E8ECEF",
    "gray": "#BFC7CD",
    "gray_dark": "#66727C",
    "positive": "#6FA8A6",
    "negative": "#D99A5E",
    "neutral": "#BFC7CD",
    "highlight": "#F3C567",
}

_CATEGORICAL_BASE = [
    PAPER_PALETTE["blue_main"],
    PAPER_PALETTE["teal_main"],
    PAPER_PALETTE["green_main"],
    PAPER_PALETTE["yellow_light"],
    PAPER_PALETTE["orange_light"],
    PAPER_PALETTE["purple_light"],
]


def get_palette(n: int, kind: str = "categorical") -> Union[List[str], str]:
    """Return a color palette appropriate for the given kind and group count."""
    if kind == "categorical":
        if n <= len(_CATEGORICAL_BASE):
            return _CATEGORICAL_BASE[:n]
        return [plt.cm.tab20(i / n) for i in range(n)]

    if kind == "binary":
        return [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    if kind == "positive_negative":
        return [PAPER_PALETTE["orange_main"], PAPER_PALETTE["gray_light"], PAPER_PALETTE["blue_main"]]

    if kind == "sequential":
        return "Blues"

    if kind == "diverging":
        return "RdBu_r"

    raise ValueError(f"Unknown palette kind: {kind}")
