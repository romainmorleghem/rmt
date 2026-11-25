"""Seq 2 — The Gaussian ensembles: the intersection of 'independent entries' and 'rotation invariance';
proof for 2x2 (Maxwell's argument); the three values of beta."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, GOE, GUE, GSE, IID, INV
from common.narrative import Narrated


class Ensembles(Narrated):
    def construct(self):
        self.chapter(r"2 \,$\cdot$\, Which random matrix?")
        self.say(r"Which random matrix should we use? There are two natural wishes.", extra=0.2)
        cL = Circle(radius=2.25, color=IID, fill_color=IID, fill_opacity=0.15, stroke_width=3).move_to([-1.5, 0.55, 0])
        cR = Circle(radius=2.25, color=INV, fill_color=INV, fill_opacity=0.15, stroke_width=3).move_to([1.5, 0.55, 0])
        tL = VGroup(Tex(r"\textbf{Independent}", font_size=30, color=IID), Tex(r"\textbf{entries}", font_size=30, color=IID),
                    Tex(r"each entry drawn", font_size=22, color=FG), Tex(r"on its own", font_size=22, color=FG)
                    ).arrange(DOWN, buff=0.08).move_to([-2.4, 0.75, 0])
        tR = VGroup(Tex(r"\textbf{Rotation}", font_size=30, color=INV), Tex(r"\textbf{invariant}", font_size=30, color=INV),
                    Tex(r"no preferred", font_size=22, color=FG), Tex(r"basis", font_size=22, color=FG)
                    ).arrange(DOWN, buff=0.08).move_to([2.4, 0.75, 0])
        self.say(r"Wish 1: \emph{independent entries}. Each number in the table is drawn on its own, like a coin "
                 r"flip. Easy to simulate.", anims=[DrawBorderThenFill(cL), FadeIn(tL)], run_time=1.5, extra=0.2)
        self.say(r"Wish 2: \emph{rotation invariance}. In physics, the basis in which we write a Hamiltonian is "
                 r"arbitrary: $H$ and $OHO^{\mathsf T}$ (the same matrix in a rotated basis) should be equally likely.",
                 anims=[DrawBorderThenFill(cR), FadeIn(tR)], run_time=1.5, extra=0.4)
        mid = VGroup(Tex(r"Gaussian", font_size=28, color=FG), Tex(r"ensembles", font_size=28, color=FG)
                     ).arrange(DOWN, buff=0.06).move_to([0, 0.55, 0])
        self.say(r"Can we have both? Yes, but only in one way. The overlap of the two bubbles contains exactly "
                 r"the \emph{Gaussian} ensembles (Porter and Rosenzweig, 1960).", anims=[FadeIn(mid, scale=1.3)],
                 run_time=1.2, extra=0.5)
        bub = VGroup(cL, cR, tL, tR, mid)
        self.play(bub.animate.scale(0.55).to_corner(UL, buff=0.5).shift(0.45 * DOWN), run_time=1)

        # --- proof for 2x2
        self.chapter(r"2 \,$\cdot$\, Why Gaussian? (the $2\times2$ case)")
        lines = [
            (r"H=\begin{pmatrix} a & b\\ b & d\end{pmatrix}", FG,
             r"Take a $2\times2$ symmetric matrix: three random numbers $a$, $b$, $d$."),
            (r"\text{independent:}\quad P(H)=f(a)\,g(b)\,f(d)", IID,
             r"Independence: the probability is a product of three separate factors."),
            (r"\text{invariant:}\quad P(H)=\Phi\big(\mathrm{Tr}\,H,\ \mathrm{Tr}\,H^2\big)", INV,
             r"Invariance: $P$ can only depend on the eigenvalues, that is, on $\mathrm{Tr}\,H=a+d$ and "
             r"$\mathrm{Tr}\,H^2=a^2+d^2+2b^2$ (they fix both eigenvalues)."),
            (r"\ln f(a)+\ln g(b)+\ln f(d)=\phi\big(a+d,\ a^2+d^2+2b^2\big)", FG,
             r"Take logarithms: a sum of three separate functions must equal a function of the two traces."),
            (r"\Longrightarrow\ \phi = -c\,\mathrm{Tr}\,H^2 + k\,\mathrm{Tr}\,H + \text{const}", SEMI,
             r"Changing $b$ alone only moves $\mathrm{Tr}\,H^2$, so $\phi$ must be linear in it; then $a$ and $d$ "
             r"force linearity in $\mathrm{Tr}\,H$ too."),
            (r"P(H)\ \propto\ e^{-c\,\mathrm{Tr}\,H^2}\quad(\text{Gaussian!})", SEMI,
             r"So $P(H)\propto e^{-c\,\mathrm{Tr}H^2}$ (after shifting $H$ to remove $k$): every entry is Gaussian."),
        ]
        g = VGroup(*[MathTex(t, font_size=34, color=c) for t, c, _ in lines]).arrange(DOWN, buff=0.28,
                                                                                    aligned_edge=LEFT)
        g.move_to([1.6, 0.35, 0])
        if g.width > 8.6:
            g.scale_to_fit_width(8.6).move_to([1.6, 0.35, 0])
        for m, (_, _, cap) in zip(g, lines):
            self.say(cap, anims=[Write(m)], run_time=1.2, extra=0.2)
        self.play(FadeOut(g), run_time=0.6)
        # Maxwell
        mx = Tex(r"Maxwell, 1860: molecules in a gas", font_size=32, color=EIG).move_to([1.4, 1.9, 0])
        rng = np.random.default_rng(1)
        mols = VGroup()
        for i in range(4):
            for j in range(6):
                p = np.array([-0.9 + 0.95 * j, 1.0 - 0.95 * i, 0])
                v = 0.32 * np.r_[rng.standard_normal(2), 0]
                mols.add(VGroup(Dot(p, radius=0.07, color=FG),
                                Arrow(p, p + v, buff=0, color=EIG, stroke_width=3, max_tip_length_to_length_ratio=0.3)))
        arrows = mols
        mxt = Tex(r"independent components\\ $+$ no preferred direction\\ $\Rightarrow$ Gaussian velocities",
                  font_size=28, color=FG).move_to([5.55, -0.4, 0])
        self.say(r"This is exactly James Clerk Maxwell's 1860 argument for the velocities of gas molecules: "
                 r"independent components and no preferred direction force a Gaussian.",
                 anims=[FadeIn(mx), LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.04), FadeIn(mxt)],
                 run_time=2, extra=0.5)
        self.play(FadeOut(VGroup(mx, arrows, mxt, bub)), run_time=0.8)

        # --- beta
        self.chapter(r"2 \,$\cdot$\, Three flavours: $\beta = 1, 2, 4$")
        cols = [(r"\beta=1", r"\text{real}", r"b\in\mathbb R", r"\text{GOE}", r"time-reversal\\ symmetry", GOE),
                (r"\beta=2", r"\text{complex}", r"b\in\mathbb C", r"\text{GUE}", r"no time reversal\\ (magnetic field)", GUE),
                (r"\beta=4", r"\text{quaternion}", r"b\in\mathbb H", r"\text{GSE}", r"time reversal,\\ half-integer spin", GSE)]
        cg = VGroup()
        for i, (bt, kind, ent, name, phys, col) in enumerate(cols):
            box = RoundedRectangle(corner_radius=0.15, width=3.6, height=3.3, stroke_color=col, stroke_width=2.5)
            c = VGroup(MathTex(bt, font_size=44, color=col), MathTex(kind, font_size=30, color=FG),
                       MathTex(ent, font_size=30, color=FG), MathTex(name, font_size=32, color=col),
                       Tex(phys, font_size=24, color=MUTED)).arrange(DOWN, buff=0.16)
            cg.add(VGroup(box, c.move_to(box)))
        cg.arrange(RIGHT, buff=0.45).move_to([0, 0.9, 0])
        self.say(r"Physics allows three kinds of symmetric matrices, depending on the symmetries of the system.",
                 extra=0.2)
        for i, cap in enumerate([
                r"Real symmetric matrices for systems with time-reversal symmetry: the Gaussian Orthogonal Ensemble.",
                r"Complex Hermitian matrices when time reversal is broken, for instance by a magnetic field: GUE.",
                r"Quaternion matrices for time-reversal symmetric systems with half-integer spin: GSE."]):
            self.say(cap, anims=[FadeIn(cg[i], shift=0.2 * UP)], run_time=1, extra=0.2)
        f = MathTex(r"P(H)\;\propto\;\exp\!\Big(-\frac{\beta N}{4}\,\mathrm{Tr}\,H^2\Big)", font_size=46, color=SEMI)
        fb = boxed(f, SEMI).move_to([0, -1.75, 0])
        self.say(r"$\beta$ counts the real numbers in each off-diagonal entry: 1, 2 or 4. One formula covers all "
                 r"three (the factor $N$ keeps the spectrum between $-2$ and $2$).", anims=[FadeIn(fb, shift=0.2 * UP)],
                 run_time=1.2, extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(cg, fb)), run_time=0.8)
