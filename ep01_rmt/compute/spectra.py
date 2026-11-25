"""Spectra used by the scenes and the web page -> data/spectra.json

    python compute/spectra.py
"""
import json, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from common.rmt import goe, gue, unfold_bulk, hermite_gas  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "spectra.json"
rng = np.random.default_rng(2026)
r = lambda a, d=4: np.round(np.asarray(a, float), d).tolist()
D = {}

# one matrix per size: how the histogram approaches the semicircle
D["single"] = {str(N): r(np.linalg.eigvalsh(goe(N, rng))) for N in (10, 50, 200, 1000, 4000)}
# universality of the semicircle: other laws for the entries
D["laws"] = {law: r(np.linalg.eigvalsh(goe(2000, rng, law))) for law in ("coin", "uniform")}
# the matrix shown as an image in the cold open (60 x 60) and its spectrum
M = goe(60, rng)
D["pixels"] = {"M": r(M * np.sqrt(60), 3), "eig": r(np.linalg.eigvalsh(M))}
# two strips: independent points vs eigenvalues (same mean spacing)
D["strip_poisson"] = r(np.sort(rng.uniform(0, 60, 60)))
lam = np.linalg.eigvalsh(goe(400, rng))
u = np.cumsum(np.r_[0, unfold_bulk(lam, 0.3)])
D["strip_goe"] = r(u[:61] - u[0])
# 2 x 2 matrices: (a - d, 2b) plane for GOE, radius for GUE
a = rng.standard_normal((4000, 3))
D["two_by_two"] = {"x": r(np.sqrt(2) * (a[:, 0] - a[:, 2]) / np.sqrt(2), 3), "y": r(2 * a[:, 1] / np.sqrt(2), 3)}
g = rng.standard_normal((20000, 3))
D["gue_2x2_radius"] = r(np.linalg.norm(g, axis=1), 3)
# bulk spacings of large matrices (unfolded)
D["spacings"] = {
    "goe": r(np.concatenate([unfold_bulk(np.linalg.eigvalsh(goe(800, rng))) for _ in range(20)]), 3),
    "gue": r(np.concatenate([unfold_bulk(np.linalg.eigvalsh(gue(800, rng))) for _ in range(20)]), 3),
    "coin": r(np.concatenate([unfold_bulk(np.linalg.eigvalsh(goe(800, rng, "coin"))) for _ in range(20)]), 3),
    "poisson": r(rng.exponential(1, 8000), 3),
}
# zero temperature: Hermite zeros
D["hermite"] = {str(N): r(hermite_gas(N)) for N in (8, 30, 100, 400)}
OUT.write_text(json.dumps(D))
print({k: (len(v) if isinstance(v, list) else list(v)) for k, v in D.items()})
