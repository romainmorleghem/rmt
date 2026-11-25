"""Seq 3 — Level repulsion: independent points vs eigenvalues; the 2x2 proof (ring / sphere); Wigner surmise;
large-N check and universality."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, POI, GOE, GUE, GSE
from common.narrative import Narrated
from common.rmt import surmise

SP = load("spectra")


def strip(points, y, color, label, sub):
    line = Line([-5.6, y, 0], [6.4, y, 0], color=MUTED, stroke_width=1.5)
    dots = VGroup(*[Dot([-5.6 + 12 * p / 60, y, 0], radius=0.06, color=color) for p in points if 0 <= p <= 60])
    lab = VGroup(Tex(label, font_size=28, color=color), Tex(sub, font_size=22, color=MUTED)
                 ).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(line, UP, buff=0.18).align_to(line, LEFT)
    return VGroup(line, dots, lab)


class Repulsion(Narrated):
    def construct(self):
        self.chapter(r"3 \,$\cdot$\, Level repulsion")
        A = strip(SP["strip_poisson"], 1.7, POI, r"independent random points", r"thrown at random, one by one")
        B = strip(SP["strip_goe"], -0.4, GOE, r"eigenvalues of a random matrix", r"same average spacing")
        self.say(r"First, the spacings. Here are 60 points thrown independently at random on a line.",
                 anims=[FadeIn(A, lag_ratio=0.02)], run_time=1.5, extra=0.2)
        self.say(r"And here are 60 consecutive eigenvalues of a large random matrix, with the same average spacing.",
                 anims=[FadeIn(B, lag_ratio=0.02)], run_time=1.5, extra=0.3)
        self.say(r"Independent points form clumps and leave big holes. Eigenvalues are spread almost evenly: "
                 r"as if they \emph{repelled} each other.", extra=0.6)
        self.play(FadeOut(VGroup(A, B)), run_time=0.6)

        ax = Axes(x_range=[0, 3.5, 0.5], y_range=[0, 1.05, 0.25], x_length=8, y_length=4.2, axis_config=axis_cfg(),
                  x_axis_config={"include_numbers": True, "font_size": 22},
                  y_axis_config={"include_numbers": True, "font_size": 22}).move_to([0.2, 0.55, 0])
        xl = MathTex(r"\text{spacing } s \ (\text{mean} = 1)", font_size=30, color=FG).next_to(ax.x_axis, DOWN, buff=0.45)
        s = np.linspace(0, 3.5, 300)
        hp = hist(ax, SP["spacings"]["poisson"], 35, 0, 3.5, POI, 0.45)
        cp = curve(ax, s, np.exp(-s), POI, 3.5)
        lp = MathTex(r"e^{-s}", font_size=36, color=POI).move_to(ax.c2p(0.55, 0.95))
        self.play(Create(ax), FadeIn(xl), run_time=1)
        self.say(r"Histogram of the gaps between neighbours. For independent points, the gaps follow $e^{-s}$: "
                 r"the most likely gap is \emph{zero}.", anims=[FadeIn(hp), Create(cp), FadeIn(lp)], run_time=1.5,
                 extra=0.3)
        hg = hist(ax, SP["spacings"]["goe"], 35, 0, 3.5, GOE, 0.5)
        self.say(r"For eigenvalues, the histogram vanishes at zero: two eigenvalues almost never sit on top of each "
                 r"other. Why?", anims=[FadeIn(hg)], run_time=1.5, extra=0.5)
        self.play(FadeOut(VGroup(ax, xl, hp, cp, lp, hg)), run_time=0.6)

        # --- 2x2 proof
        self.chapter(r"3 \,$\cdot$\, Why? The $2\times2$ case")
        f1 = MathTex(r"H=\begin{pmatrix}a&b\\b&d\end{pmatrix}", font_size=40, color=FG)
        f2 = MathTex(r"\lambda_\pm=\frac{a+d}{2}\pm\frac12\sqrt{(a-d)^2+(2b)^2}", font_size=36, color=FG)
        f3 = MathTex(r"s=\lambda_+-\lambda_-=\sqrt{(a-d)^2+(2b)^2}", font_size=36, color=EIG)
        F = VGroup(f1, f2, f3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([-3.6, 0.6, 0])
        self.say(r"Take a $2\times2$ random matrix. Solving the quadratic equation gives both eigenvalues\ldots",
                 anims=[Write(f1), Write(f2)], run_time=2, extra=0.2)
        self.say(r"\ldots and their spacing $s$. Look closely: it is the distance from the origin to the point "
                 r"$(a-d,\ 2b)$ in a plane.", anims=[Write(f3)], run_time=1.5, extra=0.3)
        pl = Axes(x_range=[-5, 5, 5], y_range=[-5, 5, 5], x_length=5.4, y_length=5.4, axis_config=axis_cfg()
                  ).move_to([3.4, 0.55, 0])
        pxl = MathTex(r"a-d", font_size=28, color=FG).next_to(pl.x_axis.get_right(), DOWN, buff=0.15)
        pyl = MathTex(r"2b", font_size=28, color=FG).next_to(pl.y_axis.get_top(), LEFT, buff=0.15)
        X, Y = np.array(SP["two_by_two"]["x"]), np.array(SP["two_by_two"]["y"])
        cloud = VGroup(*[Dot(pl.c2p(x, y), radius=0.022, color=GOE).set_opacity(0.7)
                         for x, y in zip(X[:1500], Y[:1500]) if abs(x) < 5 and abs(y) < 5])
        self.say(r"Each random matrix is one point of this plane. Since the entries are Gaussian, the points form "
                 r"a round cloud.", anims=[Create(pl), FadeIn(pxl), FadeIn(pyl),
                                          LaggedStart(*[FadeIn(d) for d in cloud], lag_ratio=0.001)], run_time=2.5)
        r0 = ValueTracker(1.6)
        ring = always_redraw(lambda: Annulus(inner_radius=pl.x_axis.unit_size * r0.get_value(),
                                             outer_radius=pl.x_axis.unit_size * (r0.get_value() + 0.35),
                                             color=EIG, fill_opacity=0.35, stroke_width=0).move_to(pl.c2p(0, 0)))
        self.add(ring)
        self.say(r"All matrices with a spacing close to $s$ lie in a thin ring of radius $s$. Its length is $2\pi s$.",
                 anims=[r0.animate.set_value(2.6)], run_time=2, extra=0.2)
        self.say(r"Shrink the ring: for a tiny spacing, the ring has almost no room left. A small spacing requires "
                 r"\emph{two} coincidences at once, $a=d$ and $b=0$.", anims=[r0.animate.set_value(0.05)], run_time=3,
                 extra=0.3)
        self.remove(ring)
        surm = MathTex(r"P(s)\;\propto\;\underbrace{2\pi s}_{\text{ring}}\times\underbrace{e^{-s^2/4}}_{\text{Gaussian}}"
                       r"\quad\Rightarrow\quad P(s)=\frac{\pi s}{2}\,e^{-\pi s^2/4}", font_size=34, color=SEMI)
        sb = boxed(surm, SEMI).move_to([0, -2.1, 0])
        self.play(FadeOut(F), run_time=0.5)
        self.say(r"Probability of a spacing $s$ = length of the ring $\times$ Gaussian weight. Rescaled to mean 1: "
                 r"the \emph{Wigner surmise}, which vanishes linearly at $s=0$.", anims=[FadeIn(sb, shift=0.2 * UP)],
                 run_time=1.2, extra=0.5)
        ax2 = Axes(x_range=[0, 3, 1], y_range=[0, 1.0, 0.5], x_length=4.8, y_length=3.0, axis_config=axis_cfg(),
                   x_axis_config={"include_numbers": True, "font_size": 20}).move_to([-3.6, 0.9, 0])
        rr = np.hypot(X, Y); rr /= rr.mean()
        h2 = hist(ax2, rr, 30, 0, 3, GOE, 0.5)
        c1 = curve(ax2, np.linspace(0, 3, 200), surmise(np.linspace(0, 3, 200), 1), SEMI, 3.5)
        self.say(r"Check: the histogram of the distances in the cloud, against the formula.",
                 anims=[Create(ax2), FadeIn(h2), Create(c1)], run_time=1.5, extra=0.3)
        self.play(FadeOut(VGroup(cloud, pl, pxl, pyl)), run_time=0.6)
        gtxt = VGroup(MathTex(r"\beta=2:\ b\in\mathbb C\ \Rightarrow\ (a-d,\,2\,\mathrm{Re}\,b,\,2\,\mathrm{Im}\,b)",
                              font_size=30, color=GUE),
                      MathTex(r"\text{ring}\to\text{sphere}:\ 4\pi s^2\ \Rightarrow\ P(s)\propto s^2 e^{-c s^2}",
                              font_size=30, color=GUE),
                      MathTex(r"\beta=4:\ P(s)\propto s^4 e^{-cs^2}", font_size=30, color=GSE)
                      ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([3.0, 1.0, 0])
        g = np.array(SP["gue_2x2_radius"]); g /= g.mean()
        h3 = hist(ax2, g, 30, 0, 3, GUE, 0.4)
        c2 = curve(ax2, np.linspace(0, 3, 200), surmise(np.linspace(0, 3, 200), 2), GUE, 3.5)
        self.say(r"For complex matrices ($\beta=2$), $b$ carries two numbers: the point lives in 3D, the ring "
                 r"becomes a sphere of area $4\pi s^2$, and the repulsion is quadratic.",
                 anims=[FadeIn(gtxt[:2]), FadeIn(h3), Create(c2)], run_time=1.5, extra=0.3)
        self.say(r"For $\beta=4$, a 5-dimensional sphere: $s^4$. The power of the repulsion is exactly $\beta$.",
                 anims=[FadeIn(gtxt[2])], run_time=1, extra=0.5)
        self.play(FadeOut(VGroup(ax2, h2, c1, h3, c2, gtxt, sb)), run_time=0.6)

        # --- large N and universality
        self.chapter(r"3 \,$\cdot$\, Large matrices and universality")
        ax3 = Axes(x_range=[0, 3.5, 0.5], y_range=[0, 1.05, 0.25], x_length=8, y_length=4.2, axis_config=axis_cfg(),
                   x_axis_config={"include_numbers": True, "font_size": 22},
                   y_axis_config={"include_numbers": True, "font_size": 22}).move_to([0.2, 0.55, 0])
        xl3 = MathTex(r"\text{spacing } s", font_size=30, color=FG).next_to(ax3.x_axis, DOWN, buff=0.45)
        ss = np.linspace(0, 3.5, 300)
        hg = hist(ax3, SP["spacings"]["goe"], 35, 0, 3.5, GOE, 0.5)
        cg = curve(ax3, ss, surmise(ss, 1), SEMI, 3.5)
        lab = Tex(r"20 matrices $800\times800$, real Gaussian", font_size=28, color=GOE).move_to(ax3.c2p(2.4, 0.95))
        self.play(Create(ax3), FadeIn(xl3), run_time=0.8)
        self.say(r"The surmise came from $2\times2$ matrices. Here are the spacings of $800\times800$ matrices "
                 r"(rescaled so the mean spacing is 1): the same curve, to within a percent.",
                 anims=[FadeIn(hg), Create(cg), FadeIn(lab)], run_time=1.5, extra=0.5)
        hc = hist(ax3, SP["spacings"]["coin"], 35, 0, 3.5, EIG, 0.5)
        lab2 = Tex(r"entries $= \pm1$ (coin flips)", font_size=28, color=EIG).move_to(lab)
        self.say(r"Now replace the Gaussian entries by coin flips, $+1$ or $-1$: not rotation invariant at all\ldots",
                 anims=[Transform(hg, hc), Transform(lab, lab2)], run_time=1.5, extra=0.2)
        self.say(r"\ldots and nothing changes. This is \emph{universality}: the local statistics of eigenvalues do "
                 r"not depend on the details of the entries, only on the symmetry class $\beta$.", extra=0.6)
        self.unsay()
        self.play(FadeOut(VGroup(ax3, xl3, hg, cg, lab)), run_time=0.8)
