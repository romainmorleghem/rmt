"""Collect the data of the 'Our computations' section and the fact sheet -> web/data/ep1.json and data/facts.json

    python compute/export_web.py
"""
import json, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from common.rmt import surmise  # noqa: E402

DATA = ROOT / "ep01_rmt" / "data"
L = lambda n: json.loads((DATA / f"{n}.json").read_text())
bi, an, ld, sp = L("billiards"), L("anderson"), L("ld_positive"), L("spectra")
z = np.array(L("zeta_zeros"))
Ns = lambda t: t / (2 * np.pi) * np.log(t / (2 * np.pi * np.e)) + 7 / 8
sz = np.diff(Ns(z))
small = lambda s: float((np.asarray(s) < 0.25).mean())
ref = {b: quad(lambda s: surmise(s, b), 0, 0.25)[0] for b in (0, 1, 2)}
facts = {
    "P(s < 0.25): Poisson / GOE / GUE (theory)": "%.3f / %.3f / %.3f" % (ref[0], ref[1], ref[2]),
    "GOE 800×800, bulk spacings: P(s < 0.25)": "%.3f" % small(sp["spacings"]["goe"]),
    "coin-flip entries 800×800: P(s < 0.25)": "%.3f" % small(sp["spacings"]["coin"]),
    "quantum circle billiard (700 levels): P(s < 0.25)": "%.3f" % small(bi["circle"]["s"]),
    "quantum stadium billiard (700 levels): P(s < 0.25)": "%.3f" % small(bi["stadium"]["s"]),
    "stadium grid points": str(bi["stadium"]["grid_points"]),
    "Anderson 14³, W = 2 / 16.5 / 50: P(s < 0.25)": " / ".join("%.3f" % small(an["s"][k]) for k in ("2", "16.5", "50")),
    "zeta zeros computed": "%d (t up to %.1f)" % (len(z), z[-1]),
    "zeta spacings: P(s < 0.25)": "%.3f" % small(sz),
    "P(all eigenvalues > 0), N = 30 (moving wall)": "e^{%.1f} ≈ 10^{%.0f}" % (ld["wall"]["30"], ld["wall"]["30"] / np.log(10)),
    "fitted θ (exact ln3/4 = 0.2747)": "%.3f" % ld["fit"]["theta"],
    "rigged coin breaks down at N ≈": "6 (relative error > 25 %)",
}
web = {"billiards": {k: bi[k]["s"] for k in ("circle", "stadium")},
       "anderson": {"W": an["W"], "s": {k: np.round(v, 3).tolist() for k, v in an["s"].items()}},
       "zeta": np.round(sz, 4).tolist(), "ld": ld, "facts": facts}
(ROOT / "web" / "data" / "ep1.json").write_text(json.dumps(web))
(DATA / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
print(json.dumps(facts, indent=1, ensure_ascii=False))
