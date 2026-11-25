"""Quantum billiards: circle (integrable, exact Bessel zeros) vs stadium (chaotic, finite differences).
Desymmetrised quarter domains, Dirichlet everywhere -> one symmetry class. -> data/billiards.json

    python compute/billiards.py
"""
import json, sys, time
from pathlib import Path
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from scipy.special import jn_zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_unfold import unfold_weyl

OUT = Path(__file__).resolve().parents[1] / "data" / "billiards.json"
NLEV = 700


def circle_levels(nlev=NLEV):
    """Quarter disk, Dirichlet on the axes: J_m(k r) sin(m theta), m even >= 2. k^2 = j_{m,n}^2."""
    ks = []
    for m in range(2, 400, 2):
        z = jn_zeros(m, 60)
        ks.extend(z)
    E = np.sort(np.array(ks) ** 2)
    return E[:nlev]


def stadium_levels(nlev=NLEV, h=0.0065, a=1.0, r=1.0):
    """Quarter stadium {0<y<r, 0<x, x<a or (x-a)^2+y^2<r^2}, 5-point Laplacian, Dirichlet boundary."""
    xs = np.arange(1, int((a + r) / h) + 2) * h
    ys = np.arange(1, int(r / h) + 2) * h
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    inside = (Y < r) & ((X <= a) | ((X - a) ** 2 + Y ** 2 < r ** 2))
    idx = -np.ones(X.shape, int)
    idx[inside] = np.arange(inside.sum())
    n = inside.sum()
    rows, cols = [], []
    I, J = np.nonzero(inside)
    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ii, jj = I + di, J + dj
        ok = (ii >= 0) & (jj >= 0) & (ii < X.shape[0]) & (jj < X.shape[1])
        ok[ok] &= inside[ii[ok], jj[ok]]
        rows.append(idx[I[ok], J[ok]]); cols.append(idx[ii[ok], jj[ok]])
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    L = sp.csr_matrix((-np.ones(len(rows)), (rows, cols)), shape=(n, n)) + 4 * sp.identity(n)
    vals = eigsh(L, k=nlev, sigma=0, which="LM", return_eigenvectors=False)
    return np.sort(vals) / h ** 2, n


if __name__ == "__main__":
    t = time.time()
    Ec = circle_levels()
    Es, npts = stadium_levels()
    out = {"circle": {"E": Ec.round(6).tolist(), "s": unfold_weyl(Ec).round(5).tolist()},
           "stadium": {"E": Es.round(6).tolist(), "s": unfold_weyl(Es).round(5).tolist(), "grid_points": int(npts)}}
    OUT.write_text(json.dumps(out))
    for k in ("circle", "stadium"):
        s = np.array(out[k]["s"])
        print(k, "levels", len(out[k]["E"]), "mean s %.3f" % s.mean(), "P(s<0.25) %.3f" % (s < 0.25).mean())
    print("time %.0fs" % (time.time() - t))
