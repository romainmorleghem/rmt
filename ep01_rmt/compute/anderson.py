"""Anderson model in 3D: level spacings near the band centre, from metal (GOE) to insulator (Poisson).
L^3 sites, periodic, hopping 1, on-site energies uniform in [-W/2, W/2]. -> data/anderson.json

    python compute/anderson.py
"""
import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_unfold import unfold_poly

OUT = Path(__file__).resolve().parents[1] / "data" / "anderson.json"
L, REAL = 14, 8
WS = [2, 6, 10, 14, 16.5, 20, 26, 35, 50]


def hamiltonian(W, rng):
    n = L ** 3
    H = np.zeros((n, n))
    i = np.arange(n)
    x, y, z = i // (L * L), (i // L) % L, i % L
    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        j = ((x + dx) % L) * L * L + ((y + dy) % L) * L + (z + dz) % L
        H[i, j] = H[j, i] = -1.0
    H[i, i] = rng.uniform(-W / 2, W / 2, n)
    return H


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    t, out = time.time(), {"L": L, "realisations": REAL, "W": WS, "s": {}}
    for W in WS:
        ss = []
        for _ in range(REAL):
            E = np.linalg.eigvalsh(hamiltonian(W, rng))
            n = len(E)
            win = E[int(0.4 * n):int(0.6 * n)]           # band centre
            ss.append(unfold_poly(win, 3))
        s = np.concatenate(ss)
        s /= s.mean()
        out["s"][str(W)] = s.round(4).tolist()
        print("W=%5.1f  spacings %d  P(s<0.25)=%.3f  <s^2>=%.3f" % (W, len(s), (s < 0.25).mean(), (s**2).mean()), flush=True)
    OUT.write_text(json.dumps(out))
    print("time %.0fs" % (time.time() - t))
