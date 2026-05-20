# Code Generation Rules

## Required structure

Every generated script must follow:
1. Module docstring
2. Imports (pathlib, numpy, pandas, matplotlib)
3. Config section (OUTPUT_DIR, FIG_NAME, DPI, SAVE_FORMATS)
4. Style section (PAPER_PALETTE dict, apply_paper_style function)
5. Data loading (load_data function — real data or example with TODO)
6. Data validation (validate_data function)
7. Plotting function (plot_figure — returns fig)
8. Export function (save_figure)
9. main() entry point

## Naming conventions

- Functions: snake_case (plot_figure, load_data, save_figure)
- Constants: UPPER_SNAKE (OUTPUT_DIR, FIG_NAME, DPI)
- File names: figure_{type}.py

## Required behaviors

- All generated code must be directly runnable (`python script.py`)
- No dependency on user-local files unless user provides paths
- Example data with TODO comments when user hasn't provided real data
- Optional deps (scipy, sklearn, mne) in try/except with fallback
- Data validation before plotting
- Export PNG + PDF + SVG by default
- Modular functions, not monolithic main
