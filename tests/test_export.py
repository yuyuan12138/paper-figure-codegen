import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from paper_figure_codegen.export import save_figure


class TestSaveFigure:
    def test_save_png_pdf_svg(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        paths = save_figure(fig, name="test_fig", output_dir=tmp_path)
        assert len(paths) == 3
        for p in paths:
            assert p.exists()
            assert p.stat().st_size > 0
        plt.close(fig)

    def test_custom_formats(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, name="test_fig", output_dir=tmp_path, formats=["png"])
        assert len(paths) == 1
        assert paths[0].suffix == ".png"
        plt.close(fig)

    def test_custom_dpi(self, tmp_path):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        paths = save_figure(fig, name="test_dpi", output_dir=tmp_path, dpi=150)
        assert paths[0].exists()
        plt.close(fig)
