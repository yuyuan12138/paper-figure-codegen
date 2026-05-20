
from paper_figure_codegen.core.color_system import (
    PAPER_PALETTE,
    get_palette,
)


class TestPaperPalette:
    def test_contains_required_keys(self):
        required = [
            "blue_main", "blue_dark", "blue_light",
            "teal_main", "teal_dark", "green_light", "green_main",
            "yellow_light", "orange_light", "orange_main",
            "purple_light", "pink_light",
            "gray_light", "gray", "gray_dark",
            "positive", "negative", "neutral", "highlight",
        ]
        for key in required:
            assert key in PAPER_PALETTE, f"Missing key: {key}"

    def test_all_values_are_hex(self):
        for key, value in PAPER_PALETTE.items():
            assert value.startswith("#"), f"{key} = {value} is not hex"
            assert len(value) == 7, f"{key} = {value} is not 7 chars"


class TestGetPalette:
    def test_categorical_2(self):
        result = get_palette(2, kind="categorical")
        assert len(result) == 2
        assert result[0] == PAPER_PALETTE["blue_main"]
        assert result[1] == PAPER_PALETTE["teal_main"]

    def test_categorical_3(self):
        result = get_palette(3, kind="categorical")
        assert len(result) == 3

    def test_categorical_6(self):
        result = get_palette(6, kind="categorical")
        assert len(result) == 6

    def test_categorical_exceeds_base(self):
        result = get_palette(10, kind="categorical")
        assert len(result) == 10

    def test_binary(self):
        result = get_palette(2, kind="binary")
        assert result == [PAPER_PALETTE["blue_main"], PAPER_PALETTE["orange_main"]]

    def test_positive_negative(self):
        result = get_palette(3, kind="positive_negative")
        assert len(result) == 3
        assert result[0] == PAPER_PALETTE["orange_main"]
        assert result[2] == PAPER_PALETTE["blue_main"]

    def test_sequential(self):
        result = get_palette(0, kind="sequential")
        assert result == "Blues"

    def test_diverging(self):
        result = get_palette(0, kind="diverging")
        assert result == "RdBu_r"
