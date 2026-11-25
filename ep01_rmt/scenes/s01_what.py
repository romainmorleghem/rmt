"""Seq 1 — What is a random matrix, and where does random matrix theory show up?"""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, GOE, GUE, POI, FIELD
from common.narrative import Narrated


class WhatIsIt(Narrated):
    def construct(self):
        self.chapter(r"1 \,$\cdot$\, What is a random matrix?")
        H = MathTex(r"H=\begin{pmatrix}2 & 1\\ 1 & 2\end{pmatrix}", font_size=52, color=FG).move_to([-3.8, 1.2, 0])
        ev = MathTex(r"H\,v = \lambda\, v", font_size=46, color=FG).move_to([2.6, 1.9, 0])
        e1 = MathTex(r"\lambda_1 = 1,\quad v_1=\begin{pmatrix}1\\-1\end{pmatrix}", font_size=36, color=EIG)
        e2 = MathTex(r"\lambda_2 = 3,\quad v_2=\begin{pmatrix}1\\1\end{pmatrix}", font_size=36, color=EIG)
        VGroup(e1, e2).arrange(DOWN, buff=0.3).next_to(ev, DOWN, buff=0.4)
        self.say(r"A matrix is a table of numbers. Ours are \emph{symmetric}: mirror images across the diagonal.",
                 anims=[Write(H)], run_time=1.2)
        self.say(r"Its eigenvalues are the special numbers $\lambda$ for which some vector $v$ is only stretched "
                 r"by $H$, not turned.", anims=[Write(ev)], run_time=1, extra=0.3)
        self.say(r"A symmetric matrix of size $N$ has $N$ real eigenvalues: its \emph{spectrum}. Here, 1 and 3.",
                 anims=[FadeIn(e1), FadeIn(e2)], run_time=1.2, extra=0.3)
        line = NumberLine(x_range=[-1, 5, 1], length=8, color=MUTED, include_numbers=True, font_size=24
                          ).move_to([0, -1.5, 0])
        d1, d2 = Dot(line.n2p(1), color=EIG, radius=0.1), Dot(line.n2p(3), color=EIG, radius=0.1)
        self.play(Create(line), FadeIn(d1, scale=2), FadeIn(d2, scale=2), run_time=1)
        self.say(r"Now draw the entries at random. The eigenvalues become random numbers too. "
                 r"But, as we will see, very special random numbers.", extra=0.3)
        rng = np.random.default_rng(4)
        for _ in range(4):
            a, b, d = rng.standard_normal(3)
            l = np.linalg.eigvalsh([[a + 2, b], [b, d + 2]])
            Hn = MathTex(r"H=\begin{pmatrix}%.2f & %.2f\\ %.2f & %.2f\end{pmatrix}" % (a + 2, b, b, d + 2),
                         font_size=52, color=FG).move_to(H)
            self.play(Transform(H, Hn), d1.animate.move_to(line.n2p(l[0])), d2.animate.move_to(line.n2p(l[1])),
                      FadeOut(VGroup(e1, e2)), run_time=0.8)
            self.wait(0.3)
        q = VGroup(Tex(r"\textbf{Two questions} for a large random matrix:", font_size=34, color=FG),
                   Tex(r"1. \ where do the eigenvalues lie? \ (their density)", font_size=32, color=SEMI),
                   Tex(r"2. \ how far apart are neighbours? \ (their spacings)", font_size=32, color=GOE)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, 0.9, 0])
        self.say(r"Random matrix theory asks two questions about large random matrices.",
                 anims=[FadeOut(ev), FadeIn(q, lag_ratio=0.3)], run_time=1.5, extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(H, q, line, d1, d2)), run_time=0.8)

        # --- where does it show up?
        self.chapter(r"1 \,$\cdot$\, Where does it show up?")
        axis = Arrow([-6.6, -1.0, 0], [6.8, -1.0, 0], color=MUTED, buff=0, stroke_width=3, tip_length=0.2)
        events = [
            (1928, r"Wishart", r"statistics:\\ covariance of data", POI),
            (1955, r"Wigner", r"energy levels\\ of heavy nuclei", EIG),
            (1962, r"Dyson", r"three symmetry classes,\\ a gas of charges", SEMI),
            (1972, r"Montgomery \& Dyson", r"zeros of the\\ Riemann zeta function", GUE),
            (1984, r"Bohigas, Giannoni, Schmit", r"quantum chaos", GOE),
            (2000, r"\ldots", r"disordered metals, optics,\\ wireless, finance\ldots", FIELD),
        ]
        x = lambda y: -6.0 + (y - 1925) * 12.2 / 75
        self.play(GrowArrow(axis), run_time=1)
        cards = VGroup()
        for i, (yr, who, what, col) in enumerate(events):
            p = Dot([x(yr), -1.0, 0], color=col, radius=0.08)
            yt = Tex(str(yr) if yr < 2000 else r"today", font_size=26, color=col).next_to(p, DOWN, buff=0.15)
            up = 0.9 if i % 2 == 0 else 2.3
            stem = Line(p.get_center(), [x(yr), -1.0 + up - 0.1, 0], color=col, stroke_width=1.5)
            c = VGroup(Tex(who, font_size=26, color=col), Tex(what, font_size=22, color=FG)).arrange(DOWN, buff=0.08)
            c.move_to([min(x(yr), 5.6), -1.0 + up + c.height / 2, 0])
            cards.add(VGroup(p, yt, stem, c))
        self.say(r"It started in statistics, with John Wishart's study of the correlations hidden in data tables.",
                 anims=[FadeIn(cards[0], shift=0.2 * UP)], run_time=1, extra=0.2)
        self.say(r"Then Eugene Wigner, in the 1950s. The energy levels of a heavy nucleus like uranium are far too "
                 r"complicated to compute, one by one.", anims=[FadeIn(cards[1], shift=0.2 * UP)], run_time=1)
        self.say(r"Wigner's bold idea: replace the unknown Hamiltonian by a \emph{random} symmetric matrix, and "
                 r"predict not the levels themselves, but their \emph{statistics}.", extra=0.5)
        self.say(r"Freeman Dyson classified the possible symmetries, and saw that the eigenvalues behave like a gas "
                 r"of electric charges (we will see why).", anims=[FadeIn(cards[2], shift=0.2 * UP)], run_time=1)
        self.say(r"In 1972, over tea, the number theorist Hugh Montgomery showed Dyson a formula for the zeros of the "
                 r"Riemann zeta function. Dyson recognised it: random matrix eigenvalues.",
                 anims=[FadeIn(cards[3], shift=0.2 * UP)], run_time=1, extra=0.3)
        self.say(r"In 1984, Bohigas, Giannoni and Schmit conjectured that \emph{any} quantum system whose classical "
                 r"motion is chaotic has random-matrix energy levels.", anims=[FadeIn(cards[4], shift=0.2 * UP)],
                 run_time=1, extra=0.3)
        self.say(r"And the list keeps growing. Let us see which random matrices to use, and why they are so universal.",
                 anims=[FadeIn(cards[5], shift=0.2 * UP)], run_time=1, extra=0.3)
        self.unsay()
        self.play(FadeOut(VGroup(axis, cards)), run_time=0.8)
