"""Seq 5 — The semicircle, step by step: numerics, zero temperature (Hermite zeros), continuum energy, force
balance, the complex electric field, crossing the wire (Plemelj = Gauss), the sign-flip trick, Liouville."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, FIELD, GOE
from common.narrative import Narrated
from common.rmt import semicircle, hermite_gas

SP = load("spectra")
WIRE_Y = -1.0
X = lambda x: 2.6 * x


class Semicircle(Narrated):
    def tool(self, k, text):
        t = Tex(r"\textbf{%d.} %s" % (k, text), font_size=25, color=FIELD)
        if self.tools:
            t.next_to(self.tools[-1], DOWN, buff=0.1, aligned_edge=LEFT)
        else:
            t.next_to(self.tool_title, DOWN, buff=0.12, aligned_edge=LEFT)
        self.tools.add(t)
        self.play(FadeIn(t, shift=0.1 * LEFT), run_time=0.6)

    def construct(self):
        self.tools = VGroup()
        # --- A. numerics
        self.chapter(r"5 \,$\cdot$\, The semicircle: what the computer says")
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 0.5, 0.1], x_length=10, y_length=4.2, axis_config=axis_cfg(),
                  x_axis_config={"include_numbers": True, "font_size": 24}).move_to([0, 0.5, 0])
        ax.y_axis.set_opacity(0)
        xl = Tex(r"eigenvalue", font_size=28, color=FG).next_to(ax.x_axis, DOWN, buff=0.45)
        self.play(Create(ax), FadeIn(xl), run_time=0.8)
        H, lab = None, None
        for N, bins in ((10, 8), (50, 14), (200, 24), (1000, 40), (4000, 80)):
            h = hist(ax, SP["single"][str(N)], bins, -2.2, 2.2, EIG, 0.6)
            L = MathTex(r"N=%d" % N, font_size=36, color=EIG).move_to(ax.c2p(1.9, 0.44))
            cap = {10: r"One random $10\times10$ matrix: a rough histogram of its 10 eigenvalues.",
                   50: r"$N=50$\ldots", 200: r"$N=200$\ldots", 1000: r"$N=1000$\ldots",
                   4000: r"$N=4000$: the histogram settles on a precise shape."}[N]
            anims = [FadeIn(h), FadeIn(L)] if H is None else [Transform(H, h), Transform(lab, L)]
            self.say(cap, anims=anims, run_time=1.2, wait=0.6 if N in (50, 200, 1000) else None)
            if H is None:
                H, lab = h, L
        sc = semi_curve(ax)
        f = MathTex(r"\rho(x)=\frac{1}{2\pi}\sqrt{4-x^2}", font_size=40, color=SEMI).move_to(ax.c2p(-1.75, 0.42))
        self.say(r"This shape is the semicircle law, discovered by Eugene Wigner in 1955. Our goal: "
                 r"derive it, with physics.", anims=[Create(sc), Write(f)], run_time=2, extra=0.4)
        self.unsay()
        self.play(FadeOut(VGroup(ax, xl, H, lab, sc, f)), run_time=0.6)

        # --- B. zero temperature
        self.chapter(r"5 \,$\cdot$\, Step 1: freeze the gas")
        wire = Line([-6.4, WIRE_Y, 0], [6.4, WIRE_Y, 0], color=MUTED, stroke_width=2)
        N = 20
        rng = np.random.default_rng(8)
        x = np.sort(rng.uniform(-2.3, 2.3, N))
        traj = [x.copy()]
        for _ in range(140):
            for _ in range(20):
                d = x[:, None] - x[None, :]
                np.fill_diagonal(d, np.inf)
                x = np.sort(x + 0.004 * (-x / 2 + (1 / d).sum(1) / N))
            traj.append(x.copy())
        k = ValueTracker(0)
        gas = always_redraw(lambda: VGroup(*[Dot([X(v), WIRE_Y, 0], radius=0.1, color=EIG) for v in traj[int(k.get_value())]]))
        self.add(wire, gas)
        self.say(r"Start with the simplest case: zero temperature, no noise at all. The charges just slide to the "
                 r"positions where all forces balance.", anims=[k.animate(rate_func=smooth).set_value(len(traj) - 1)],
                 run_time=6, extra=0.2)
        hz = hermite_gas(N)
        ticks = VGroup(*[Line([X(v), WIRE_Y - 0.25, 0], [X(v), WIRE_Y - 0.12, 0], color=SEMI, stroke_width=3) for v in hz])
        tl = Tex(r"zeros of the Hermite polynomial $H_{20}$ \ (Stieltjes, 1885)", font_size=28, color=SEMI
                 ).next_to(wire, DOWN, buff=0.45)
        self.say(r"In 1885, Thomas Stieltjes found these equilibrium positions exactly: they are the zeros of a "
                 r"famous polynomial, the Hermite polynomial.", anims=[FadeIn(ticks), FadeIn(tl)], run_time=1.2,
                 extra=0.3)
        ax2 = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 0.45, 0.15], x_length=10, y_length=2.6, axis_config=axis_cfg()
                   ).move_to([0, 1.7, 0])
        ax2.y_axis.set_opacity(0)
        hh = hist(ax2, SP["hermite"]["400"], 50, -2.2, 2.2, EIG, 0.6)
        sc2 = semi_curve(ax2)
        self.say(r"Take 400 frozen charges and draw their histogram: already the semicircle. The shape does not come "
                 r"from the randomness; it comes from the balance of forces.", anims=[Create(ax2), FadeIn(hh), Create(sc2)],
                 run_time=1.5, extra=0.5)
        gas.clear_updaters()
        self.play(FadeOut(VGroup(ax2, hh, sc2, ticks, tl, gas)), run_time=0.6)

        # --- C. continuum
        self.chapter(r"5 \,$\cdot$\, Step 2: from charges to a density")
        rho = semicircle(np.linspace(-2.2, 2.2, 200))
        cloud = VGroup(*[Line([X(v), WIRE_Y, 0], [X(v), WIRE_Y + 3.2 * semicircle(v), 0], color=EIG, stroke_width=2,
                              stroke_opacity=0.6) for v in np.linspace(-1.98, 1.98, 90)])
        rl = MathTex(r"\rho(x)", font_size=34, color=EIG).move_to([X(1.2), WIRE_Y + 1.0, 0])
        self.say(r"With many charges, describe them by a density $\rho(x)$: the fraction of charges per unit length "
                 r"(the unknown we want).", anims=[FadeIn(cloud, lag_ratio=0.01), FadeIn(rl)], run_time=1.5, extra=0.2)
        e1 = MathTex(r"E=\frac N4\sum_i\lambda_i^2-\sum_{i<j}\ln|\lambda_i-\lambda_j|", font_size=38, color=FG)
        e2 = MathTex(r"E\simeq N^2\Big[\int\frac{x^2}{4}\rho(x)\,dx-\frac12\iint\ln|x-y|\,\rho(x)\rho(y)\,dx\,dy\Big]",
                     font_size=38, color=FG)
        VGroup(e1, e2).arrange(DOWN, buff=0.35).move_to([0, 2.2, 0])
        self.say(r"The energy: a sum over the $N$ charges becomes $N\int\rho$, and a sum over the $N^2/2$ pairs becomes "
                 r"$\frac{N^2}{2}\iint\rho\rho$.", anims=[Write(e1)], run_time=1.2, extra=0.2)
        self.say(r"Both terms grow like $N^2$. And since the probability is $e^{-\beta E}$, a density that costs even a "
                 r"little extra energy is crushed by a factor $e^{-\beta N^2\times\text{something}}$.",
                 anims=[TransformFromCopy(e1, e2)], run_time=1.5, extra=0.3)
        self.say(r"So for large $N$, at any temperature, the gas sits in the density of \emph{minimum energy}. "
                 r"We need to find it.", extra=0.4)
        self.play(FadeOut(VGroup(e1, e2)), run_time=0.5)

        # --- D. force balance
        self.chapter(r"5 \,$\cdot$\, Step 3: balance of forces")
        self.tool_title = Tex(r"\textbf{toolbox}", font_size=26, color=FIELD).move_to([3.15, 3.35, 0], aligned_edge=LEFT)
        self.add(self.tool_title)
        x0 = 1.1
        probe = Dot([X(x0), WIRE_Y, 0], radius=0.13, color=FG)
        spring = Arrow([X(x0), WIRE_Y - 0.4, 0], [X(x0) - 1.4, WIRE_Y - 0.4, 0], buff=0, color=FIELD, stroke_width=5)
        push = Arrow([X(x0), WIRE_Y - 0.4, 0], [X(x0) + 1.4, WIRE_Y - 0.4, 0], buff=0, color=EIG, stroke_width=5)
        sl = MathTex(r"x/2", font_size=30, color=FIELD).next_to(spring, DOWN, buff=0.08)
        pl_ = MathTex(r"\int\frac{\rho(y)}{x-y}dy", font_size=28, color=EIG).next_to(push, DOWN, buff=0.08)
        self.say(r"Pick a charge at position $x$. The spring pulls it back with force $x/2$\ldots",
                 anims=[FadeOut(rl), FadeIn(probe), GrowArrow(spring), FadeIn(sl)], run_time=1, extra=0.2)
        self.say(r"\ldots and all the other charges push it, each with a force $1/(\text{distance})$.",
                 anims=[GrowArrow(push), FadeIn(pl_)], run_time=1, extra=0.2)
        eq = MathTex(r"\frac{x}{2}\;=\;\mathrm{P}\!\!\int_{-\infty}^{\infty}\frac{\rho(y)}{x-y}\,dy", font_size=46, color=FG)
        eqb = boxed(eq, FG).move_to([-1.5, 2.1, 0])
        self.say(r"Equilibrium: the two must cancel, for every $x$ where there are charges. This is our master "
                 r"equation.", anims=[FadeIn(eqb, shift=0.2 * DOWN)], run_time=1.2, extra=0.3)
        self.tool(1, r"principal value")
        self.say(r"The P means \emph{principal value}: we leave out the tiny neighbourhood of $y=x$ "
                 r"(a charge does not push itself).", extra=0.3)
        self.say(r"The trouble: the unknown $\rho$ sits inside an integral. To solve this, we leave the wire and look "
                 r"at the whole plane.", extra=0.4)
        self.play(FadeOut(VGroup(probe, spring, push, sl, pl_)), eqb.animate.scale(0.75).to_corner(UL, buff=0.45)
                  .shift(0.5 * DOWN), run_time=0.8)

        # --- E. the complex electric field
        self.chapter(r"5 \,$\cdot$\, Step 4: the electric field in the complex plane")
        pts = hermite_gas(16)
        G = lambda z: np.mean(1 / (z - pts))
        arrows = VGroup()
        for gx in np.linspace(-2.3, 2.3, 13):
            for gy in (0.35, 0.75, 1.2, -0.35):
                z = gx + 1j * gy
                v = np.conj(G(z))
                v = v / abs(v) * min(0.55, 0.25 + 0.3 * abs(v))
                start = np.array([X(gx), WIRE_Y + 1.6 * gy, 0])
                arrows.add(Arrow(start, start + np.array([v.real, v.imag, 0]), buff=0, color=FIELD, stroke_width=2.5,
                                 max_tip_length_to_length_ratio=0.3))
        self.play(FadeOut(cloud), run_time=0.3)
        dots = VGroup(*[Dot([X(p), WIRE_Y, 0], radius=0.07, color=EIG) for p in pts])
        self.add(dots)
        gdef = MathTex(r"G(z)=\int\frac{\rho(y)}{z-y}\,dy,\qquad z=x+i\,y", font_size=38, color=FIELD
                       ).move_to([1.7, 2.35, 0])
        self.say(r"Our charges live on a line, but their electric field fills the plane. Use complex numbers "
                 r"$z = x + iy$ for points of the plane.", anims=[LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                              lag_ratio=0.01)], run_time=2.5, extra=0.2)
        self.say(r"In two dimensions, the field of a charge at $y$, seen from $z$, is just $1/(z-y)$ (up to a complex "
                 r"conjugate). Adding all charges gives one function, $G(z)$.", anims=[Write(gdef)], run_time=1.5,
                 extra=0.4)

        # --- F. crossing the wire
        self.chapter(r"5 \,$\cdot$\, Step 5: crossing the wire")
        xc = 0.6
        box = Rectangle(width=1.0, height=1.2, color=FG, stroke_width=2).move_to([X(xc), WIRE_Y, 0])
        up_h = Arrow([X(xc) - 0.9, WIRE_Y + 0.75, 0], [X(xc) - 0.2, WIRE_Y + 0.75, 0], buff=0, color=FIELD, stroke_width=5)
        dn_h = Arrow([X(xc) - 0.9, WIRE_Y - 0.75, 0], [X(xc) - 0.2, WIRE_Y - 0.75, 0], buff=0, color=FIELD, stroke_width=5)
        up_v = Arrow([X(xc) + 0.15, WIRE_Y + 0.6, 0], [X(xc) + 0.15, WIRE_Y + 1.3, 0], buff=0, color=EIG, stroke_width=5)
        dn_v = Arrow([X(xc) + 0.15, WIRE_Y - 0.6, 0], [X(xc) + 0.15, WIRE_Y - 1.3, 0], buff=0, color=EIG, stroke_width=5)
        self.play(FadeOut(arrows), run_time=0.5)
        self.say(r"Now zoom in on the wire, just above and just below a point $x$.", anims=[Create(box)], run_time=1)
        self.say(r"The horizontal part of the field is the same on both sides: it is exactly the push from the other "
                 r"charges, the integral of our master equation.", anims=[GrowArrow(up_h), GrowArrow(dn_h)], run_time=1,
                 extra=0.2)
        self.say(r"The vertical part flips: up above, down below. Gauss's law: the flux leaving the little box equals "
                 r"the charge inside, so the jump is $2\pi\rho(x)$.", anims=[GrowArrow(up_v), GrowArrow(dn_v)],
                 run_time=1, extra=0.3)
        pf = MathTex(r"G(x\pm i0)=\mathrm{P}\!\!\int\frac{\rho(y)}{x-y}\,dy\;\mp\;i\pi\,\rho(x)", font_size=40, color=FG)
        pfb = boxed(pf, FIELD).move_to([1.6, 1.0, 0])
        self.play(FadeOut(gdef), run_time=0.3)
        self.say(r"In complex language: real part = horizontal field, imaginary part = vertical field.",
                 anims=[FadeIn(pfb, shift=0.2 * DOWN)], run_time=1.2, extra=0.2)
        self.tool(2, r"Sokhotski--Plemelj ($=$ Gauss)")
        self.say(r"Mathematicians call this the Sokhotski--Plemelj formula. For a physicist, it is Gauss's law. "
                 r"It gives us two things: the force, and the density we are after.", extra=0.4)
        self.play(FadeOut(VGroup(box, up_h, dn_h, up_v, dn_v, dots)), pfb.animate.scale(0.75).next_to(eqb, DOWN, buff=0.2)
                  .align_to(eqb, LEFT), run_time=0.8)

        # --- G-K. the algebra
        self.chapter(r"5 \,$\cdot$\, Step 6: the trick")
        self.play(FadeOut(VGroup(eqb, pfb, wire)), run_time=0.5)
        steps_ = [
            (r"G(x+i0)+G(x-i0)\;=\;2\,\mathrm{P}\!\!\int\frac{\rho(y)}{x-y}dy\;=\;x", FG,
             r"Add the field just above and just below: the vertical parts cancel, and the master equation turns "
             r"the rest into $x$."),
            (r"F(z)=G(z)-\frac z2\quad\Rightarrow\quad F(x+i0)=-\,F(x-i0)", SEMI,
             r"Now subtract the spring: $F = G - z/2$. Across the wire, $F$ simply changes sign."),
            (r"\Rightarrow\quad F(x+i0)^2 = F(x-i0)^2", SEMI,
             r"So $F^2$ does not jump at all: $F^2$ is perfectly smooth (complex-differentiable) in the whole plane, "
             r"wire included."),
        ]
        col = VGroup()
        for i, (t, c, cap) in enumerate(steps_):
            m = MathTex(t, font_size=36, color=c)
            if col:
                m.next_to(col[-1], DOWN, buff=0.3).align_to(col[0], LEFT)
            else:
                m.move_to([-0.3, 2.3, 0])
            col.add(m)
            self.say(cap, anims=[Write(m)], run_time=1.2, extra=0.3)
        self.play(FadeOut(col[0]), FadeOut(col[1]), col[2].animate.move_to([-0.3, 2.45, 0]), run_time=0.8)
        far = [
            (r"|z|\to\infty:\quad G(z)=\int\frac{\rho(y)}{z-y}dy=\frac{1}{z}\underbrace{\int\rho}_{=1}"
             r"+\frac{1}{z^2}\int y\rho+\dots", FG,
             r"Far away, expand $\frac{1}{z-y}=\frac1z\big(1+\frac yz+\dots\big)$. The leading term is the total "
             r"charge, $\int\rho=1$: seen from afar, the wire is a single unit charge, $G\approx 1/z$."),
            (r"F^2=\Big(-\frac z2+\frac1z+\dots\Big)^2=\frac{z^2}{4}\;\underbrace{-\,2\cdot\frac z2\cdot\frac1z}_{=\,-1}"
             r"\;+\;O\Big(\frac1z\Big)", FG,
             r"Now square $F=-\frac z2+\frac1z+\dots$: the $-1$ is the cross term $2\times(-\frac z2)\times\frac1z$. "
             r"It is the total charge again. Everything else vanishes at infinity."),
        ]
        col2 = VGroup()
        for t, c, cap in far:
            m = MathTex(t, font_size=34, color=c)
            m.next_to(col2[-1] if col2 else col[2], DOWN, buff=0.35).align_to(col[2], LEFT)
            col2.add(m)
            self.say(cap, anims=[Write(m)], run_time=1.4, extra=0.5)
        col = VGroup(col[2], col2)
        self.tool(3, r"Liouville's theorem")
        lv = MathTex(r"F(z)^2=\frac{z^2}{4}-1\ \text{exactly}", font_size=38, color=SEMI).next_to(col, DOWN, buff=0.3
                                                                                                 ).align_to(col, LEFT)
        self.say(r"Liouville's theorem: a function smooth in the whole complex plane that grows like a polynomial "
                 r"\emph{is} a polynomial. The vanishing terms must be exactly zero.", anims=[Write(lv)], run_time=1.2,
                 extra=0.5)
        self.play(FadeOut(VGroup(col, lv)), run_time=0.5)
        r1 = MathTex(r"G(z)=\frac{z}{2}+F(z)=\frac{z-\sqrt{z^2-4}}{2}", font_size=42, color=SEMI).move_to([-0.3, 2.2, 0])
        r2 = MathTex(r"|x|<2:\ \ G(x+i0)=\frac{x-i\sqrt{4-x^2}}{2}", font_size=38, color=FG).next_to(r1, DOWN, buff=0.35)
        r3 = MathTex(r"\rho(x)=-\frac1\pi\,\mathrm{Im}\,G(x+i0)=\frac{1}{2\pi}\sqrt{4-x^2}", font_size=42, color=SEMI)
        r3b = boxed(r3, SEMI).next_to(r2, DOWN, buff=0.4)
        self.say(r"So $F=-\frac12\sqrt{z^2-4}$ (the sign that matches $-z/2$ far away), and the field is known "
                 r"everywhere.", anims=[Write(r1)], run_time=1.5, extra=0.3)
        self.say(r"On the wire, for $|x|<2$, $x^2-4$ is negative: its square root is purely imaginary, "
                 r"$\sqrt{x^2-4}=i\sqrt{4-x^2}$\ldots",
                 anims=[Write(r2)], run_time=1.2, extra=0.2)
        self.say(r"\ldots and the imaginary part, the vertical field, gives the density: the semicircle!",
                 anims=[FadeIn(r3b, shift=0.2 * UP)], run_time=1.2, extra=0.4)
        r4 = MathTex(r"|x|>2:\ \ x^2-4>0\ \Rightarrow\ \sqrt{x^2-4}\in\mathbb R\ \Rightarrow\ \mathrm{Im}\,G=0"
                     r"\ \Rightarrow\ \rho(x)=0", font_size=34, color=FG).next_to(r3b, DOWN, buff=0.35)
        self.say(r"For $|x|>2$, $x^2-4$ is positive: the root is real, $G$ is real, no vertical field, no charge. "
                 r"The edges $\pm2$ were never assumed: they came out of the calculation.", anims=[Write(r4)],
                 run_time=1.2, extra=0.5)
        self.play(FadeOut(VGroup(r1, r2, r4)), r3b.animate.scale(0.8).to_corner(UL, buff=0.45).shift(0.5 * DOWN),
                  run_time=0.8)
        # --- L. back to the data
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 0.5, 0.1], x_length=10, y_length=3.8, axis_config=axis_cfg(),
                  x_axis_config={"include_numbers": True, "font_size": 24}).move_to([0, 0.0, 0])
        ax.y_axis.set_opacity(0)
        h1 = hist(ax, SP["single"]["4000"], 80, -2.2, 2.2, EIG, 0.6)
        sc = semi_curve(ax)
        lab = Tex(r"$N=4000$, Gaussian entries", font_size=28, color=EIG).move_to(ax.c2p(1.6, 0.46))
        self.say(r"Back to the computer: theory and experiment agree perfectly.",
                 anims=[Create(ax), FadeIn(h1), Create(sc), FadeIn(lab)], run_time=2, extra=0.3)
        h2 = hist(ax, SP["laws"]["coin"], 80, -2.2, 2.2, GOE, 0.6)
        lab2 = Tex(r"$N=2000$, entries $\pm1$", font_size=28, color=GOE).move_to(lab)
        self.say(r"And with coin-flip entries, which have no Gaussian in them at all: the same semicircle. "
                 r"Universality again.", anims=[Transform(h1, h2), Transform(lab, lab2)], run_time=1.5, extra=0.5)
        self.unsay()
        self.play(FadeOut(VGroup(ax, h1, sc, lab, r3b, self.tools, self.tool_title)), run_time=0.8)
