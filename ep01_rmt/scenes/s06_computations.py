"""Seq 6 — Our own computations: quantum billiards, the Anderson transition, zeta zeros, and the probability
that all eigenvalues are positive (the rigged coin, then a moving wall)."""
from _common import *  # noqa
from manim import *
from common.style import FG, MUTED, EIG, SEMI, POI, GOE, GUE, FIELD
from common.narrative import Narrated
from common.rmt import surmise

BI = load("billiards")
AN = load("anderson")
LD = load("ld_positive")
ZE = load("zeta_zeros")


def spacing_axes(pos, w=5.6, h=3.0, ymax=1.05):
    ax = Axes(x_range=[0, 3.5, 1], y_range=[0, ymax, 0.5], x_length=w, y_length=h, axis_config=axis_cfg(),
              x_axis_config={"include_numbers": True, "font_size": 20}).move_to(pos)
    return ax


def refs(ax, betas=(0, 1), widths=(2.5, 2.5)):
    s = np.linspace(0, 3.5, 200)
    cols = {0: POI, 1: GOE, 2: GUE}
    return VGroup(*[curve(ax, s, surmise(s, b), cols[b], w) for b, w in zip(betas, widths)])


def stadium_path(n=26, a=1.0, r=1.0):
    """Billiard ball in a full stadium (straight half-length a, radius r)."""
    p, v = np.array([0.3, 0.1]), np.array([np.cos(0.7), np.sin(0.7)])
    pts = [p.copy()]
    for _ in range(n):
        best, nrm = np.inf, None
        for sgn in (1, -1):                                  # flat walls y = +-r
            if v[1] * sgn > 1e-12:
                t = (sgn * r - p[1]) / v[1]
                q = p + t * v
                if abs(q[0]) <= a and 1e-9 < t < best:
                    best, nrm = t, np.array([0.0, -sgn])
        for cx in (a, -a):                                   # caps
            c = p - np.array([cx, 0])
            B, C = c @ v, c @ c - r * r
            disc = B * B - C
            if disc > 0:
                t = -B + np.sqrt(disc)
                q = p + t * v
                if (q[0] - cx) * np.sign(cx) >= 0 and 1e-9 < t < best:
                    nq = q - np.array([cx, 0])
                    best, nrm = t, -nq / np.linalg.norm(nq)
        p = p + best * v
        v = v - 2 * (v @ nrm) * nrm
        v /= np.linalg.norm(v)
        pts.append(p.copy())
    return np.array(pts)


class Computations(Narrated):
    def construct(self):
        # --- a. billiards
        self.chapter(r"6 \,$\cdot$\, Our computations (1): quantum billiards")
        s0 = 0.85
        circ = Circle(radius=1.3 * s0, color=FG, stroke_width=3).move_to([-4.4, 1.6, 0])
        ang = 0.4 + np.arange(28) * 2.39
        cpath = VMobject().set_points_as_corners([circ.get_center() + 1.3 * s0 * np.array([np.cos(t), np.sin(t), 0])
                                                  for t in ang]).set_stroke(POI, 1.6, opacity=0.8)
        st_o = np.array([2.2, 1.6, 0])
        stad = VGroup(Line(st_o + s0 * np.array([-1, 1.3, 0]) * [1.3, 1, 1], st_o + s0 * np.array([1.3, 1.3, 0])),
                      Line(st_o + s0 * np.array([-1.3, -1.3, 0]), st_o + s0 * np.array([1.3, -1.3, 0])),
                      Arc(radius=1.3 * s0, start_angle=-PI / 2, angle=PI).move_arc_center_to(st_o + [1.3 * s0, 0, 0]),
                      Arc(radius=1.3 * s0, start_angle=PI / 2, angle=PI).move_arc_center_to(st_o - [1.3 * s0, 0, 0])
                      ).set_stroke(FG, 3)
        sp = stadium_path(40) * 1.3 * s0
        spath = VMobject().set_points_as_corners([st_o + [x, y, 0] for x, y in sp]).set_stroke(GOE, 1.6, opacity=0.8)
        lc = Tex(r"circle: regular motion", font_size=26, color=POI).next_to(circ, DOWN, buff=0.15)
        ls = Tex(r"stadium: chaotic motion", font_size=26, color=GOE).next_to(stad, DOWN, buff=0.15)
        self.say(r"Time to compute things ourselves. First, a ball bouncing in a box. In a circle, the motion is "
                 r"regular; in a stadium, it is chaotic.", anims=[Create(circ), Create(stad), FadeIn(lc), FadeIn(ls)],
                 run_time=1.2, extra=0.2)
        self.play(Create(cpath), Create(spath), run_time=4, rate_func=linear)
        self.say(r"Now make it quantum: the allowed energies are given by the vibration modes of a drum of that shape. "
                 r"We computed the first 700 of each (circle: exactly; stadium: on a grid of %d points)."
                 % BI["stadium"]["grid_points"], extra=0.3)
        a1 = spacing_axes([-3.6, -1.3, 0], 5.0, 2.3)
        a2 = spacing_axes([3.0, -1.3, 0], 5.0, 2.3)
        h1 = hist(a1, BI["circle"]["s"], 28, 0, 3.5, POI, 0.5)
        h2 = hist(a2, BI["stadium"]["s"], 28, 0, 3.5, GOE, 0.5)
        self.play(FadeOut(VGroup(cpath, spath)), VGroup(circ, lc).animate.shift(0.3 * UP),
                  VGroup(stad, ls).animate.shift(0.3 * UP), run_time=0.5)
        self.say(r"Spacings: the circle gives independent levels ($e^{-s}$), the stadium gives level "
                 r"repulsion (GOE). Chaos makes a spectrum look random-matrix.",
                 anims=[Create(a1), Create(a2), FadeIn(h1), FadeIn(h2), Create(refs(a1)), Create(refs(a2))],
                 run_time=2, extra=0.5)
        self.say(r"This is the Bohigas--Giannoni--Schmit conjecture, seen on our own data.", extra=0.3)
        self.play(FadeOut(VGroup(circ, stad, lc, ls, a1, a2, h1, h2)), *[FadeOut(m) for m in self.mobjects
                                                                          if m not in (self.chapter_tag, self.caption)],
                  run_time=0.6)

        # --- b. Anderson
        self.chapter(r"6 \,$\cdot$\, Our computations (2): metal or insulator?")
        rng = np.random.default_rng(2)
        latt = VGroup()
        for i in range(6):
            for j in range(6):
                latt.add(Square(side_length=0.42, stroke_width=0.5, stroke_color=MUTED, fill_opacity=0.9,
                                fill_color=interpolate_color(ManimColor("#1d2430"), EIG, rng.random())
                                ).move_to([-4.6 + 0.45 * i, 1.0 - 0.45 * j, 0]))
        lt = Tex(r"an electron hopping on a crystal\\ with random site energies (width $W$)", font_size=24,
                 color=FG).next_to(latt, DOWN, buff=0.2)
        self.say(r"Second: an electron hopping in a disordered crystal (Anderson's model, 3D, $14^3$ sites). "
                 r"Weak disorder: a metal. Strong disorder: the electron gets trapped, an insulator.",
                 anims=[FadeIn(latt, lag_ratio=0.01), FadeIn(lt)], run_time=1.5, extra=0.3)
        ax = spacing_axes([2.4, 0.6, 0], 6.6, 3.8)
        xl = MathTex(r"s", font_size=28, color=FG).next_to(ax.x_axis, RIGHT, buff=0.1)
        W = AN["W"]
        hs = [hist(ax, AN["s"][str(w)], 28, 0, 3.5, EIG, 0.55) for w in W]
        lab = lambda w: MathTex(r"W=%g" % w, font_size=36, color=EIG).move_to(ax.c2p(2.7, 0.9))
        H, L = hs[0], lab(W[0])
        r = refs(ax)
        leg = VGroup(Tex(r"GOE (metal)", font_size=24, color=GOE), Tex(r"Poisson (insulator)", font_size=24, color=POI)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(ax.c2p(2.7, 0.62))
        self.say(r"Spacings near the middle of the band: at weak disorder, the GOE curve.",
                 anims=[Create(ax), FadeIn(xl), Create(r), FadeIn(leg), FadeIn(H), FadeIn(L)], run_time=1.5, extra=0.2)
        for w, h in zip(W[1:], hs[1:]):
            self.play(Transform(H, h), Transform(L, lab(w)), run_time=0.9)
            self.wait(0.25 if w != 16.5 else 1.5)
        self.say(r"Increase $W$: around $W_c\approx16.5$ the histogram slides from GOE to Poisson. The level "
                 r"statistics alone detect the metal--insulator transition.", extra=0.5)
        self.play(FadeOut(VGroup(latt, lt, ax, xl, H, L, r, leg)), run_time=0.6)

        # --- c. zeta zeros
        self.chapter(r"6 \,$\cdot$\, Our computations (3): the zeros of $\zeta$")
        z = np.array(ZE)
        Nsmooth = lambda t: t / (2 * np.pi) * np.log(t / (2 * np.pi * np.e)) + 7 / 8
        sz = np.diff(Nsmooth(z))
        zf = MathTex(r"\zeta\big(\tfrac12+i\,t_n\big)=0,\quad t_1=14.13,\ t_2=21.02,\ \dots,\ t_{%d}=%.1f"
                     % (len(z), z[-1]), font_size=34, color=FG).move_to([0, 2.5, 0])
        strip = VGroup(Line([-6, 1.6, 0], [6, 1.6, 0], color=MUTED, stroke_width=1.5),
                       *[Dot([-6 + 12 * (t - z[4000]) / (z[4060] - z[4000]), 1.6, 0], radius=0.06, color=GUE)
                         for t in z[4000:4061]])
        self.say(r"Third: the zeros of the Riemann zeta function, the heart of the distribution of prime numbers. "
                 r"We computed the first %d of them." % len(z), anims=[Write(zf), FadeIn(strip, lag_ratio=0.02)],
                 run_time=2, extra=0.3)
        ax = spacing_axes([0.3, -0.75, 0], 7.0, 3.0)
        hz = hist(ax, sz, 35, 0, 3.5, GUE, 0.5)
        rz = refs(ax, (0, 1, 2), (2, 2, 3.5))
        leg = VGroup(Tex(r"GUE ($\beta=2$)", font_size=24, color=GUE), Tex(r"GOE", font_size=24, color=GOE),
                     Tex(r"Poisson", font_size=24, color=POI)).arrange(DOWN, aligned_edge=LEFT, buff=0.06
                                                                       ).move_to(ax.c2p(2.9, 0.75))
        self.say(r"Their spacings (rescaled to mean 1) follow the GUE curve, the one of complex Hermitian matrices. "
                 r"Nobody knows why: if a Hermitian operator had the zeros as eigenvalues, the Riemann hypothesis would follow.",
                 anims=[Create(ax), FadeIn(hz), Create(rz), FadeIn(leg)], run_time=2, extra=0.6)
        self.play(FadeOut(VGroup(zf, strip, ax, hz, rz, leg)), run_time=0.6)

        # --- d. large deviations
        self.chapter(r"6 \,$\cdot$\, Our computations (4): a very rare event")
        q = MathTex(r"P\big(\text{all } N \text{ eigenvalues} > 0\big)\;\approx\;e^{-\theta N^2},\qquad "
                    r"\theta=\frac{\ln 3}{4}=0.2747", font_size=38, color=FG).move_to([0, 2.5, 0])
        self.say(r"Last: how likely is it that \emph{all} eigenvalues of a GOE matrix are positive? Theory (Dean "
                 r"and Majumdar, 2006): $e^{-\theta N^2}$. Note the $N^2$.", anims=[Write(q)], run_time=1.5, extra=0.3)
        ax = Axes(x_range=[0, 31, 5], y_range=[0, 0.55, 0.1], x_length=8.4, y_length=3.6, axis_config=axis_cfg(),
                  x_axis_config={"include_numbers": True, "font_size": 20},
                  y_axis_config={"include_numbers": True, "font_size": 20,
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([0.3, -0.5, 0])
        xl = MathTex(r"N", font_size=30, color=FG).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex(r"-\ln P/N^2", font_size=30, color=FG).next_to(ax.y_axis.get_top(), RIGHT, buff=0.2)
        th = DashedLine(ax.c2p(0, LD["theta"]), ax.c2p(31, LD["theta"]), color=SEMI, stroke_width=2.5)
        thl = MathTex(r"\ln3/4", font_size=28, color=SEMI).next_to(ax.c2p(31, LD["theta"]), UP, buff=0.1).shift(0.4 * LEFT)
        tilt = VGroup(*[Dot(ax.c2p(int(n), min(0.55, -v["lnP"] / int(n) ** 2)), radius=0.07, color=EIG)
                        for n, v in LD["tilted"].items()])
        wall = VGroup(*[Dot(ax.c2p(int(n), -v / int(n) ** 2), radius=0.07, color=FIELD) for n, v in LD["wall"].items()])
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(th), FadeIn(thl), run_time=1)
        self.say(r"Brute force is hopeless. Our first idea: the rigged coin of the previous video, here a matrix "
                 r"shifted to the right, then re-weighted. It works\ldots up to $N\approx6$, then the weights explode.",
                 anims=[FadeIn(tilt, lag_ratio=0.1)], run_time=1.5, extra=0.4)
        self.say(r"Second idea: simulate the gas of charges directly, and push a wall from the left towards 0 in small "
                 r"steps, multiplying the probabilities of each step.", anims=[FadeIn(wall, lag_ratio=0.1)], run_time=2,
                 extra=0.3)
        F = LD["fit"]
        self.say(r"This reaches $N=30$, a probability of about $10^{-114}$. Fitting the curve gives "
                 r"$\theta\approx%.3f$, within 4\%% of the exact $0.2747$ (the rest is finite-size corrections)." % F["theta"],
                 extra=0.4)
        self.say(r"Why $N^2$ and not $N$ as for coins? To push every eigenvalue to the right of 0, you must squeeze the "
                 r"whole gas against a wall: every pair of charges pays. A Coulomb gas is far stiffer than coins.",
                 extra=0.6)
        self.unsay()
        self.play(FadeOut(VGroup(q, ax, xl, yl, th, thl, tilt, wall)), run_time=0.8)
