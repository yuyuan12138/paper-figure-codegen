from click.testing import CliRunner

from paper_figure_codegen.cli import cli


class TestCLI:
    def test_list_plots(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["list-plots"])
        assert result.exit_code == 0
        assert "grouped_bar" in result.output
        assert "violin_box_scatter" in result.output

    def test_codegen_missing_plot(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["codegen", "--plot", "nonexistent"])
        assert result.exit_code != 0

    def test_codegen_generates_code(self):
        runner = CliRunner()
        result = runner.invoke(cli, [
            "codegen",
            "--plot", "grouped_bar",
            "--output", "test_figure",
        ])
        assert result.exit_code == 0
        assert "def main():" in result.output
        assert "PAPER_PALETTE" in result.output

    def test_codegen_with_groups(self):
        runner = CliRunner()
        result = runner.invoke(cli, [
            "codegen",
            "--plot", "violin_box_scatter",
            "--groups", "3",
            "--output", "test_violin",
        ])
        assert result.exit_code == 0
        assert "violinplot" in result.output
