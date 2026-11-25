"""YouTube thumbnail (1280x720): a matrix of noise -> a perfect semicircle."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, POS, NEG, BG

SP = load("spectra")


class Thumbnail(Scene):
    def construct(self):
        M = np.array(SP["pixels"]["M"])[:40, :40]
        cell, c0 = 0.122, np.array([-4.15, -0.55, 0])
        img = VGroup()
        for i in range(40):
            for j in range(40):
                v = max(-1.0, min(1.0, M[i][j] / 2.0))
                col = interpolate_color(BG, POS if v > 0 else NEG, abs(v) ** 0.6)
                img.add(Square(cell, stroke_width=0, fill_color=col, fill_opacity=1)
                        .move_to(c0 + [(j - 19.5) * cell, -(i - 19.5) * cell, 0]))
        frame = SurroundingRectangle(img, color=MUTED, buff=0.05, stroke_width=2)
        ax = Axes(x_range=[-2.3, 2.3, 1], y_range=[0, 0.36, 0.1], x_length=6.0, y_length=4.4,
                  axis_config={"color": MUTED, "stroke_width": 3, "include_tip": False}).move_to([3.55, -0.55, 0])
        ax.y_axis.set_opacity(0)
        h = hist(ax, SP["single"]["4000"], 46, -2.2, 2.2, EIG, 0.85)
        sc = semi_curve(ax, SEMI, 9)
        arrow = Arrow([-1.45, -0.55, 0], [0.35, -0.55, 0], buff=0, color=FG, stroke_width=14,
                      max_tip_length_to_length_ratio=0.35)
        t1 = Tex(r"\textbf{PURE NOISE}", font_size=74, color=FG).move_to([-4.15, 2.75, 0])
        t2 = Tex(r"\textbf{PERFECT ORDER}", font_size=74, color=SEMI)
        for t, x in ((t1, -4.15), (t2, 3.55)):
            if t.width > 6.3:
                t.scale_to_fit_width(6.3)
            t.move_to([x, 2.75, 0])
        lab = Tex(r"eigenvalues", font_size=40, color=EIG).next_to(ax, DOWN, buff=0.25)
        lab2 = Tex(r"random matrix", font_size=40, color=MUTED).next_to(frame, DOWN, buff=0.25)
        self.add(img, frame, ax, h, sc, arrow, t1, t2, lab, lab2)
