import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "ep01_rmt" / "data"


def load(name):
    return json.loads((DATA / f"{name}.json").read_text())


from common import style  # noqa: E402
style.setup()
from manim import config as _cfg  # noqa: E402
_cfg.disable_caching = True

import numpy as np  # noqa: E402
from manim import (VGroup, VMobject, Dot, Line, Rectangle, RoundedRectangle, Tex, MathTex, Axes,  # noqa: E402
                   UP, DOWN, LEFT, RIGHT)
from common.style import FG, MUTED, BG, EIG, SEMI  # noqa: E402
from common.rmt import semicircle  # noqa: E402


def axis_cfg(**kw):
    c = {"color": MUTED, "stroke_width": 2, "include_tip": False}
    c.update(kw)
    return c


def steps(ax, edges, heights, color, opacity=0.6, stroke=1.5, base=0.0):
    xs, ys = [edges[0]], [base]
    for i, h in enumerate(heights):
        xs += [edges[i], edges[i + 1]]
        ys += [h, h]
    xs.append(edges[-1]); ys.append(base)
    p = VMobject()
    p.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    return p.set_fill(color, opacity).set_stroke(color, stroke)


def hist(ax, values, bins, lo, hi, color=EIG, opacity=0.6, density=True):
    h, e = np.histogram(values, bins=bins, range=(lo, hi), density=density)
    return steps(ax, e, h, color, opacity)


def curve(ax, xs, ys, color, width=3.0):
    m = VMobject()
    m.set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, ys)])
    return m.set_stroke(color, width).set_fill(opacity=0)


def semi_curve(ax, color=SEMI, width=4):
    x = np.linspace(-2, 2, 300)
    return curve(ax, x, semicircle(x), color, width)


def card(title, body, color, width=5.2, height=2.2, size=46):
    box = RoundedRectangle(corner_radius=0.18, width=width, height=height, stroke_color=color,
                           stroke_width=2.5, fill_color=BG, fill_opacity=0.92)
    t = Tex(title, font_size=28, color=color).next_to(box.get_top(), DOWN, buff=0.25)
    b = MathTex(body, font_size=size, color=FG).move_to(box.get_center() + 0.22 * DOWN)
    return VGroup(box, t, b)


def boxed(mob, color, buff=0.22):
    from manim import SurroundingRectangle
    return VGroup(SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12,
                                       fill_color=BG, fill_opacity=0.92), mob)
