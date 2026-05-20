"""CLI entry point for paper-figure-codegen."""

import click

from paper_figure_codegen.recipes import get_recipe, list_recipes


@click.group()
def cli():
    """Paper Figure Codegen — publication-quality plotting code generator."""
    pass


@cli.command()
def list_plots():
    """List all available plot types."""
    recipes = list_recipes()
    click.echo("Available plot types:")
    for name in sorted(recipes):
        click.echo(f"  - {name}")


@cli.command()
@click.option("--plot", required=True, help="Plot type to generate")
@click.option("--output", default="figure_output", help="Output figure name")
@click.option("--groups", default=3, type=int, help="Number of groups (for example data)")
@click.option("--data", default=None, help="Path to data file (CSV/Excel)")
@click.option("--font-size", default=12, type=int, help="Font size")
@click.option("--dpi", default=300, type=int, help="DPI for output")
def codegen(plot, output, groups, data, font_size, dpi):
    """Generate plotting code for the specified plot type."""
    try:
        recipe = get_recipe(plot)
    except KeyError as e:
        raise click.BadParameter(str(e))

    import numpy as np
    from paper_figure_codegen.core.data_spec import FigureDataSpec

    if data:
        import pandas as pd
        from paper_figure_codegen.core.data_parser import DataParser
        if data.endswith(".csv"):
            df = pd.read_csv(data)
        elif data.endswith((".xlsx", ".xls")):
            df = pd.read_excel(data)
        else:
            raise click.BadParameter(f"Unsupported file format: {data}")
        spec = DataParser.parse(df)
    else:
        rng = np.random.default_rng(42)
        spec = FigureDataSpec(
            raw_input_type="example",
            data_kind="wide_dataframe",
            groups=[f"Method {i}" for i in range(groups)],
            labels=["Accuracy", "F1", "AUC"],
            values=rng.uniform(0.7, 0.95, size=(groups, 3)),
            suggested_plot_types=[plot],
        )

    code = recipe.generate_code(spec, font_size=font_size, dpi=dpi)
    code = code.replace(f"figure_{plot}", output)
    click.echo(code)


if __name__ == "__main__":
    cli()
