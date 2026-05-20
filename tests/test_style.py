import matplotlib.pyplot as plt

from paper_figure_codegen.core.style import apply_paper_style


class TestApplyPaperStyle:
    def test_sets_rcparams(self):
        apply_paper_style()
        assert plt.rcParams["pdf.fonttype"] == 42
        assert plt.rcParams["ps.fonttype"] == 42
        assert plt.rcParams["svg.fonttype"] == "none"
        assert plt.rcParams["savefig.bbox"] == "tight"

    def test_custom_font_size(self):
        apply_paper_style(font_size=14)
        assert plt.rcParams["font.size"] == 14

    def test_custom_linewidth(self):
        apply_paper_style(linewidth=2.0)
        assert plt.rcParams["axes.linewidth"] == 2.0

    def test_spines_top_right_hidden(self):
        apply_paper_style()
        assert plt.rcParams["axes.spines.top"] is False
        assert plt.rcParams["axes.spines.right"] is False

    def test_legend_no_frame(self):
        apply_paper_style()
        assert plt.rcParams["legend.frameon"] is False
