"""Seq 4 — From matrices to eigenvalues: the Jacobian (the ring again), the joint density, and the Coulomb gas."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, GOE, FIELD
from common.narrative import Narrated

WIRE_Y = -0.9


def langevin(N, beta, frames, sub, dt, rng, x0=None):
    x = np.sort(rng.uniform(-2, 2, N)) if x0 is None else x0.copy()
    out = [x.copy()]
    for _ in range(frames):
        for _ in range(sub):
            d = x[:, None] - x[None, :]
            np.fill_diagonal(d, np.inf)
            f = -x / 2 + (1.0 / d).sum(axis=1) / N
            x = x + f * dt + np.sqrt(2 * dt / (beta * N)) * rng.standard_normal(N)
            x = np.sort(x)
        out.append(x.copy())
    return np.array(out)


class CoulombGas(Narrated):
    def construct(self):
        self.chapter(r"4 \,$\cdot$\, From the matrix to its eigenvalues")
        f1 = MathTex(r"H = O\,\Lambda\,O^{\mathsf T}", font_size=44, color=FG)
        f1b = Tex(r"$\Lambda$: eigenvalues $\lambda_1,\dots,\lambda_N$ \quad $O$: a rotation", font_size=28, color=MUTED)
        f2 = MathTex(r"\mathrm{Tr}\,H^2=\sum_i\lambda_i^2", font_size=40, color=FG)
        G = VGroup(f1, f1b, f2).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        self.say(r"We know the probability of a matrix, $P(H)\propto e^{-\beta N\,\mathrm{Tr}H^2/4}$. "
                 r"What is the probability of its eigenvalues?", extra=0.3)
        self.say(r"Every symmetric matrix is a rotation of a diagonal one: change variables from the entries to the "
                 r"eigenvalues plus a rotation.", anims=[Write(f1), FadeIn(f1b)], run_time=1.5, extra=0.2)
        self.say(r"The Gaussian part is easy: $\mathrm{Tr}\,H^2$ is just the sum of the squared eigenvalues.",
                 anims=[Write(f2)], run_time=1, extra=0.2)
        self.say(r"The subtle part is the change of variables itself (the Jacobian). It is our ring again.", extra=0.2)
        self.play(FadeOut(G), run_time=0.5)
        pl = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4.6, y_length=4.6, axis_config=axis_cfg()
                  ).move_to([-3.4, 0.6, 0])
        pol = VGroup(*[Circle(radius=pl.x_axis.unit_size * r, color=MUTED, stroke_width=1).move_to(pl.c2p(0, 0))
                       for r in (0.5, 1, 1.5, 2, 2.5)],
                     *[Line(pl.c2p(0, 0), pl.c2p(2.8 * np.cos(t), 2.8 * np.sin(t)), color=MUTED, stroke_width=1)
                       for t in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
        cell = AnnularSector(inner_radius=pl.x_axis.unit_size * 1.5, outer_radius=pl.x_axis.unit_size * 2.0,
                             angle=PI / 6, start_angle=PI / 6, color=EIG, fill_opacity=0.6).move_arc_center_to(pl.c2p(0, 0))
        eqs = VGroup(MathTex(r"a-d = s\cos 2\theta,\quad 2b = s\sin 2\theta", font_size=32, color=FG),
                     MathTex(r"s=\lambda_1-\lambda_2,\quad \theta=\text{rotation angle}", font_size=32, color=FG),
                     MathTex(r"da\,db\,dd\;\propto\;|\lambda_1-\lambda_2|\;d\lambda_1\,d\lambda_2\,d\theta",
                             font_size=36, color=EIG)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([2.8, 0.6, 0])
        self.say(r"In the $(a-d,\ 2b)$ plane, the spacing is the radius and the rotation of $H$ is the angle: "
                 r"polar coordinates!", anims=[Create(pl), Create(pol), FadeIn(eqs[:2])], run_time=1.5, extra=0.2)
        self.say(r"And in polar coordinates, a little cell has area $s\,ds\,d\theta$: the farther from the centre, the "
                 r"bigger. Hence the factor $|\lambda_1-\lambda_2|$.", anims=[FadeIn(cell), Write(eqs[2])], run_time=1.5,
                 extra=0.4)
        self.play(FadeOut(VGroup(pl, pol, cell, eqs)), run_time=0.6)
        jp = MathTex(r"P(\lambda_1,\dots,\lambda_N)\;\propto\;\prod_{i<j}|\lambda_i-\lambda_j|^{\beta}\;"
                     r"\exp\!\Big(-\frac{\beta N}{4}\sum_i\lambda_i^2\Big)", font_size=44, color=SEMI)
        jb = boxed(jp, SEMI).move_to([0, 1.2, 0])
        self.say(r"For $N$ eigenvalues, every pair contributes such a factor, raised to the power $\beta$. "
                 r"This is the \emph{joint density} of the eigenvalues, exact for every $N$.",
                 anims=[FadeIn(jb, shift=0.2 * UP)], run_time=1.5, extra=0.6)

        # --- Coulomb gas
        self.chapter(r"4 \,$\cdot$\, A gas of charges")
        e = MathTex(r"=\;e^{-\beta E},\qquad E=\underbrace{\frac N4\sum_i\lambda_i^2}_{\text{spring}}"
                    r"\;\underbrace{-\sum_{i<j}\ln|\lambda_i-\lambda_j|}_{\text{repulsion}}", font_size=40, color=FG)
        e.next_to(jb, DOWN, buff=0.35)
        self.say(r"Now rewrite it as a Boltzmann weight $e^{-\beta E}$, like in statistical physics. "
                 r"Read off the energy $E$:", anims=[Write(e)], run_time=2, extra=0.4)
        self.play(VGroup(jb, e).animate.scale(0.72).to_edge(UP, buff=0.55), run_time=0.8)
        wire = Line([-6.2, WIRE_Y, 0], [6.2, WIRE_Y, 0], color=MUTED, stroke_width=2)
        X = lambda x: x * 2.6
        well = FunctionGraph(lambda x: WIRE_Y + 0.05 * x * x, x_range=[-6, 6], color=FIELD, stroke_width=2.5)
        rng = np.random.default_rng(5)
        x0 = np.sort(rng.uniform(-2, 2, 14))
        charges = VGroup(*[Dot([X(x), WIRE_Y, 0], radius=0.11, color=EIG) for x in x0])
        self.say(r"This is the energy of $N$ electric charges on a wire, held by a spring towards the centre\ldots",
                 anims=[Create(wire), Create(well), FadeIn(charges)], run_time=1.5, extra=0.2)
        lines = VGroup(*[Line(charges[6].get_center(), charges[6].get_center() + 0.9 * np.array([np.cos(t), np.sin(t), 0]),
                              color=FIELD, stroke_width=1.5) for t in np.linspace(0, 2 * np.pi, 16, endpoint=False)])
        lab = Tex(r"in a flat (2D) world: force $\propto 1/r$, energy $=-\ln r$", font_size=28, color=FIELD
                  ).move_to([0, 0.6, 0])
        self.say(r"\ldots repelling each other through $-\ln$ of their distance: exactly the electric energy of charges "
                 r"in a two-dimensional world, where field lines spread on circles and forces decay like $1/r$.",
                 anims=[Create(lines), FadeIn(lab)], run_time=1.5, extra=0.4)
        self.play(FadeOut(VGroup(lines, lab)), run_time=0.5)
        T = Tex(r"$\beta = 1/\text{temperature}$", font_size=34, color=SEMI).move_to([0, 0.5, 0])
        self.say(r"And $\beta$ is an inverse temperature: GOE, GUE and GSE are the same gas at three temperatures. "
                 r"Freeman Dyson called it the \emph{Coulomb gas}.", anims=[FadeIn(T)], run_time=1, extra=0.3)
        # dynamics: hot, then cold
        N = 30
        for beta, txt in ((0.4, r"hot ($\beta = 0.4$): a jittery, loose gas"),
                          (12, r"cold ($\beta = 12$): almost a crystal")):
            traj = langevin(N, beta, 150, 25, 6e-4, rng, x0=None)
            k = ValueTracker(0)
            gas = always_redraw(lambda: VGroup(*[Dot([X(v), WIRE_Y, 0], radius=0.09, color=EIG)
                                                 for v in traj[int(k.get_value())]]))
            self.remove(charges)
            self.add(gas)
            tt = Tex(txt, font_size=30, color=SEMI).move_to([0, -0.1, 0])
            self.say(r"Watch it at a high temperature\ldots" if beta < 1 else r"\ldots and at a low temperature.",
                     anims=[FadeIn(tt), k.animate(rate_func=linear).set_value(len(traj) - 1)], run_time=6, wait=0.3)
            gas.clear_updaters()
            self.play(FadeOut(tt), run_time=0.3)
            charges = gas
        self.say(r"Either way, the charges never cross, and their crowd has the same overall shape. "
                 r"Which shape? Let us compute it.", extra=0.4)
        self.unsay()
        self.play(FadeOut(VGroup(jb, e, wire, well, charges, T)), run_time=0.8)
