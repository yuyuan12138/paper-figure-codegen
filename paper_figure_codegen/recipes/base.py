"""Base recipe protocol for plot code generation."""

from abc import ABC, abstractmethod
from typing import List

from paper_figure_codegen.core.data_spec import FigureDataSpec
from paper_figure_codegen.core.color_system import PAPER_PALETTE


class BaseRecipe(ABC):
    """Abstract base class for plot code generation recipes."""

    plot_type: str = ""
    required_data_kind: List[str] = []

    @abstractmethod
    def generate_code(
        self,
        spec: FigureDataSpec,
        palette: dict | None = None,
        font_size: int = 12,
        dpi: int = 300,
    ) -> str:
        """Generate complete Python plotting script."""
        ...

    def validate(self, spec: FigureDataSpec) -> List[str]:
        """Return warnings if data doesn't match expectations."""
        warnings = []
        if spec.data_kind not in self.required_data_kind:
            warnings.append(
                f"data_kind '{spec.data_kind}' not in expected {self.required_data_kind}"
            )
        return warnings

    def _default_palette(self) -> dict:
        return dict(PAPER_PALETTE)
