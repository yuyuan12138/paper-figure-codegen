"""EEG topomap recipe — placeholder."""

from paper_figure_codegen.recipes.base import BaseRecipe


class Recipe(BaseRecipe):
    plot_type = "eeg_topomap"
    required_data_kind = ["spatial", "eeg_data", "topography"]

    def generate_code(self, spec, palette=None, font_size=12, dpi=300):
        raise NotImplementedError("eeg_topomap recipe not yet implemented")
