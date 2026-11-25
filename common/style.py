"""Shared visual identity for *Random Matrices* (same dark look as Routes to Chaos / Rare Events)."""
from manim import config, TexTemplate, ManimColor

BG = ManimColor("#0E1116")
FG = ManimColor("#E6E6E6")
MUTED = ManimColor("#7A8291")
EIG = ManimColor("#F2B544")      # eigenvalues, measured histograms
SEMI = ManimColor("#C792EA")     # the semicircle, theory curves
POI = ManimColor("#8FA8C8")      # Poisson / independent levels
GOE = ManimColor("#6CCB8B")      # beta = 1
GUE = ManimColor("#E85D75")      # beta = 2
GSE = ManimColor("#FF8A4C")      # beta = 4
FIELD = ManimColor("#5DA9E9")    # electric field
IID = ManimColor("#3F7FC8")      # "independent entries" bubble
INV = ManimColor("#E85D75")      # "rotation invariant" bubble
POS = ManimColor("#F2B544")      # positive matrix entries
NEG = ManimColor("#3F7FC8")      # negative matrix entries

TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{amsmath,amssymb}")


def setup():
    config.background_color = BG
    config.tex_template = TEX
