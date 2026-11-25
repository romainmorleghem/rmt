"""Seq 7 — Recap: three ideas, and beta as a temperature (tridiagonal model, from a Poisson gas to a crystal)."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, POI, GOE, GUE, GSE, FIELD
from common.narrative import Narrated
from common.rmt import beta_tridiagonal, semicircle_cdf


class Recap(Narrated):
    def construct(self):
        self.chapter(r"Recap")
        cards = [(r"Level repulsion", r"P(s)\propto s^{\beta}", GOE, r"a small gap needs $\beta+1$ coincidences"),
                 (r"A gas of charges", r"\prod_{i<j}|\lambda_i-\lambda_j|^{\beta}\,e^{-\frac{\beta N}{4}\sum\lambda_i^2}",
                  FIELD, r"log repulsion, $\beta = 1/T$"),
                 (r"The semicircle", r"\rho(x)=\tfrac{1}{2\pi}\sqrt{4-x^2}", SEMI, r"force balance + complex field")]
        g = VGroup()
        for t, f, c, sub in cards:
            box = RoundedRectangle(corner_radius=0.15, width=4.2, height=2.3, stroke_color=c, stroke_width=2.5)
            inner = VGroup(Tex(t, font_size=32, color=c), MathTex(f, font_size=32, color=FG),
                           Tex(sub, font_size=22, color=MUTED)).arrange(DOWN, buff=0.22)
            g.add(VGroup(box, inner.move_to(box)))
        g.arrange(RIGHT, buff=0.3).move_to([0, 1.6, 0])
        for c, cap in zip(g, [r"Eigenvalues repel: the probability of a small gap vanishes like $s^\beta$.",
                              r"Their joint law is a gas of charges with logarithmic repulsion, at temperature "
                              r"$1/\beta$.",
                              r"For large $N$ the gas freezes into a semicircle, which we derived from electrostatics "
                              r"and complex analysis."]):
            self.say(cap, anims=[FadeIn(c, shift=0.2 * UP)], run_time=1, extra=0.3)
        rng = np.random.default_rng(9)
        rows = VGroup()
        betas = [(0.05, POI), (1, GOE), (2, GUE), (4, GSE), (40, FG)]
        for i, (b, col) in enumerate(betas):
            lam = np.sort(beta_tridiagonal(3000, b, rng))
            u = 3000 * semicircle_cdf(lam)
            m = np.argmin(abs(u - 1500))
            seg = u[m:m + 46] - u[m]
            y = -0.3 - 0.42 * i
            rows.add(VGroup(Line([-5.0, y, 0], [6.2, y, 0], color=MUTED, stroke_width=1),
                            *[Dot([-5.0 + 11.2 * v / 45, y, 0], radius=0.055, color=col) for v in seg if v <= 45],
                            MathTex(r"\beta=%g" % b, font_size=26, color=col).move_to([-6.0, y, 0])))
        self.say(r"$\beta$ can be any positive number: a tridiagonal matrix (Dumitriu--Edelman) samples "
                 r"the gas at any temperature: hot, independent points; cold, a crystal.",
                 anims=[FadeIn(rows, lag_ratio=0.2)], run_time=2.5, extra=0.6)
        self.say(r"Random matrices: a happy marriage between probability and linear algebra, with physics as the "
                 r"best man.", extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(g, rows)), FadeOut(self.chapter_tag), run_time=0.8)
        self.chapter_tag = None
        title = Tex(r"Random Matrices", font_size=60, color=FG)
        line = Line(LEFT * 4, RIGHT * 4, color=SEMI, stroke_width=2)
        web = Tex(r"Every step, with interactive simulations (any $N$, any $\beta$, the live Coulomb gas):\\ "
                  r"\texttt{romainmorleghem.github.io/rmt}", font_size=30, color=MUTED)
        code = Tex(r"Every number in this video is computed in the companion code.", font_size=26, color=MUTED)
        end = VGroup(title, line, web, code).arrange(DOWN, buff=0.4)
        self.play(Write(title), GrowFromCenter(line), run_time=1.5)
        self.play(FadeIn(web, shift=0.1 * UP), FadeIn(code), run_time=1)
        self.wait(4)
        self.play(FadeOut(end), run_time=1.2)
