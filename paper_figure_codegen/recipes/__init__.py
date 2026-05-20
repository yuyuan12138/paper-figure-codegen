"""Recipe registry — lazy import and cache."""

_REGISTRY: dict[str, type] = {}
_IMPORTS_DONE = False

_MVP_RECIPES = [
    "grouped_bar",
    "stacked_bar",
    "horizontal_bar",
    "line_with_ci",
    "violin_box_scatter",
    "boxplot",
    "histogram_kde",
    "heatmap",
    "confusion_matrix",
    "scatter_regression",
    "multi_panel",
]

_V2_RECIPES = [
    "radar",
    "ternary",
    "eeg_topomap",
    "permutation_test",
    "raincloud",
    "flowchart_composite",
]

_ALL_RECIPES = _MVP_RECIPES + _V2_RECIPES

_MODULE_MAP = {
    "grouped_bar": "paper_figure_codegen.recipes.grouped_bar",
    "stacked_bar": "paper_figure_codegen.recipes.stacked_bar",
    "horizontal_bar": "paper_figure_codegen.recipes.horizontal_bar",
    "line_with_ci": "paper_figure_codegen.recipes.line_with_ci",
    "violin_box_scatter": "paper_figure_codegen.recipes.violin_box_scatter",
    "boxplot": "paper_figure_codegen.recipes.boxplot",
    "histogram_kde": "paper_figure_codegen.recipes.histogram_kde",
    "heatmap": "paper_figure_codegen.recipes.heatmap",
    "confusion_matrix": "paper_figure_codegen.recipes.confusion_matrix",
    "scatter_regression": "paper_figure_codegen.recipes.scatter_regression",
    "multi_panel": "paper_figure_codegen.recipes.multi_panel",
    "radar": "paper_figure_codegen.recipes.radar",
    "ternary": "paper_figure_codegen.recipes.ternary",
    "eeg_topomap": "paper_figure_codegen.recipes.eeg_topomap",
    "permutation_test": "paper_figure_codegen.recipes.permutation_test",
    "raincloud": "paper_figure_codegen.recipes.raincloud",
    "flowchart_composite": "paper_figure_codegen.recipes.flowchart_composite",
}


def _ensure_imports():
    global _IMPORTS_DONE
    if _IMPORTS_DONE:
        return
    import importlib
    for name, module_path in _MODULE_MAP.items():
        mod = importlib.import_module(module_path)
        cls = getattr(mod, "Recipe", None)
        if cls is not None:
            _REGISTRY[name] = cls
    _IMPORTS_DONE = True


def get_recipe(name: str):
    """Return a recipe class by plot type name."""
    _ensure_imports()
    if name not in _REGISTRY:
        raise KeyError(f"Unknown recipe: {name}. Available: {list(_REGISTRY.keys())}")
    return _REGISTRY[name]()


def list_recipes() -> list[str]:
    """Return list of all registered recipe names."""
    _ensure_imports()
    return list(_REGISTRY.keys())
