"""Seq 0 — Cold open: a matrix of noise, its eigenvalues drop and pile up into a semicircle."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, POS, NEG, BG
from common.narrative import Narrated

SP = load("spectra")


def matrix_image(M, cell=0.07, center=(0, 0.45, 0)):
    n = len(M)
    g = VGroup()
    for i in range(n):
        for j in range(n):
            v = max(-1.0, min(1.0, M[i][j] / 2.2))
            col = interpolate_color(BG, POS if v > 0 else NEG, abs(v) ** 0.7)
            g.add(Square(side_length=cell, stroke_width=0, fill_color=col, fill_opacity=1)
                  .move_to([center[0] + (j - n / 2 + 0.5) * cell, center[1] - (i - n / 2 + 0.5) * cell, 0]))
    return g


class ColdOpen(Narrated):
    def construct(self):
        M = SP["pixels"]["M"]
        eig = np.array(SP["pixels"]["eig"])
        img = matrix_image(M)
        frame = SurroundingRectangle(img, color=MUTED, buff=0.06, stroke_width=1.5)
        self.play(LaggedStart(*[FadeIn(s) for s in img], lag_ratio=0.0004), Create(frame), run_time=2.5)
        self.say(r"Fill a $60\times60$ table with random numbers: gold for positive, blue for negative. "
                 r"Make it symmetric: the entry in row $i$, column $j$ equals the one in row $j$, column $i$.",
                 extra=0.4)
        self.say(r"Pure noise. Nothing to see. But every such matrix has 60 \emph{eigenvalues}, "
                 r"60 special numbers hidden inside it.", extra=0.3)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 0.45, 0.15], x_length=10, y_length=3.2,
                  axis_config=axis_cfg(), x_axis_config={"include_numbers": True, "font_size": 24}
                  ).move_to([0, -0.3, 0])
        ax.y_axis.set_opacity(0)
        dots = VGroup(*[Dot(img.get_center() + 0.6 * np.array([np.cos(k), np.sin(1.7 * k), 0]), radius=0.06,
                            color=EIG) for k in range(len(eig))])
        self.play(FadeOut(VGroup(img, frame), scale=0.6), FadeIn(dots, scale=0.3), run_time=1.5)
        self.play(Create(ax), LaggedStart(*[d.animate.move_to(ax.c2p(l, 0)) for d, l in zip(dots, eig)],
                                         lag_ratio=0.02), run_time=2.5)
        self.say(r"Here they are, on a line. They do not spread out anyhow: let us stack them.", extra=0.2)
        # stack into a dot histogram
        bins = np.linspace(-2.2, 2.2, 12)
        w = bins[1] - bins[0]
        k = np.clip(np.digitize(eig, bins) - 1, 0, len(bins) - 2)
        h_unit = 0.45 / 12 * 1.0
        count = {}
        targets = []
        for kk in k:
            c = count.get(kk, 0); count[kk] = c + 1
            targets.append(ax.c2p(bins[kk] + w / 2, (c + 0.5) * 0.0215))
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=2)
        self.say(r"A hump, rounded on top, falling off steeply at the edges. With 60 eigenvalues it is rough\ldots",
                 extra=0.2)
        big = np.array(SP["single"]["4000"])
        H = hist(ax, big, 80, -2.2, 2.2, EIG, 0.6)
        lab = MathTex(r"N = 4000", font_size=34, color=EIG).move_to(ax.c2p(1.9, 0.38))
        self.say(r"\ldots so take a $4000\times4000$ matrix instead: 4000 eigenvalues.",
                 anims=[FadeOut(dots), FadeIn(H, shift=0.2 * UP), FadeIn(lab)], run_time=1.5)
        sc = semi_curve(ax)
        self.say(r"A perfect \emph{semicircle}. Out of pure noise, a shape as clean as a law of physics.",
                 anims=[Create(sc)], run_time=2, extra=0.6)
        self.say(r"And this is only the beginning: the same patterns show up in atomic nuclei, in chaotic "
                 r"billiards, and in the zeros of the Riemann zeta function.", extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(ax, H, sc, lab)), run_time=0.8)
        q = Tex(r"Random matrix theory:", font_size=50, color=FG)
        q2 = Tex(r"a happy marriage between \emph{probability} and \emph{linear algebra}.", font_size=42, color=SEMI)
        VGroup(q, q2).arrange(DOWN, buff=0.35).move_to([0, 0.5, 0])
        self.play(Write(q), run_time=1.2)
        self.play(FadeIn(q2, shift=0.15 * UP), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(VGroup(q, q2)), run_time=0.8)
        title = Tex(r"Random Matrices", font_size=70, color=FG)
        sub = Tex(r"Order from noise: level repulsion, Coulomb gases and the semicircle", font_size=34, color=MUTED)
        VGroup(title, sub).arrange(DOWN, buff=0.45)
        line = Line(LEFT * 4, RIGHT * 4, color=SEMI, stroke_width=2).next_to(title, DOWN, buff=0.22)
        self.play(Write(title), run_time=1.5)
        self.play(GrowFromCenter(line), FadeIn(sub, shift=0.1 * UP), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, sub, line)), run_time=1)
