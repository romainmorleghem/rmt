"""P(all eigenvalues of a GOE matrix are positive) ~ exp(-theta N^2), theta = ln(3)/4 (Dean & Majumdar 2006).

Two ways to see an event far too rare for brute force:
 1. the 'rigged coin' of Rare Events ep. 1: sample a shifted matrix H + cI, re-weight by the likelihood
    ratio. Works for small N, then the weights explode (we record where it breaks down);
 2. a 'moving wall' (multilevel splitting): simulate the Coulomb gas of eigenvalues directly (Metropolis on
    the joint density), push a hard wall from far left to 0 in small steps, multiply the conditional
    probabilities of each step.
GOE normalisation: density ~ exp(-N Tr H^2 / 4), joint eigenvalue density ~ prod|l_i-l_j| exp(-N sum l^2/4).
-> data/ld_positive.json      python compute/ld_positive.py
"""
import json
from pathlib import Path
import numpy as np
from numba import njit

OUT = Path(__file__).resolve().parents[1] / "data" / "ld_positive.json"
rng = np.random.default_rng(3)


def goe(N, M):
    A = rng.standard_normal((M, N, N))
    return (A + A.transpose(0, 2, 1)) / np.sqrt(2 * N)


def direct(N, M):
    return float(np.log((np.linalg.eigvalsh(goe(N, M))[:, 0] > 0).mean()))


def tilted(N, M, c):
    H = goe(N, M) + c * np.eye(N)
    lmin = np.linalg.eigvalsh(H)[:, 0]
    logw = -(N / 4) * (2 * c * np.trace(H, axis1=1, axis2=2) - N * c * c)
    hit = lmin > 0
    if not hit.any():
        return -np.inf, np.inf
    m = logw[hit].max()
    w = np.where(hit, np.exp(logw - m), 0)
    return float(np.log(w.mean()) + m), float(w.std() / np.sqrt(M) / w.mean())


@njit(cache=True)
def sweep(lam, wall, N, step, nsweep, seed):
    np.random.seed(seed)
    acc = 0
    for _ in range(nsweep):
        for i in range(N):
            new = lam[i] + step * (2 * np.random.random() - 1)
            if new <= wall:
                continue
            dE = N / 4 * (new * new - lam[i] * lam[i])
            for j in range(N):
                if j != i:
                    dE -= np.log(abs(new - lam[j])) - np.log(abs(lam[i] - lam[j]))
            if dE <= 0 or np.random.random() < np.exp(-dE):
                lam[i] = new
                acc += 1
    return acc


def moving_wall(N, nsamp=1500, thin=3, seed=0):
    nlev = max(30, int(0.4 * N * N))          # keep each conditional probability around e^-0.7
    walls = np.concatenate([[-np.inf], np.linspace(-2.6 if N > 6 else -4.0, 0.0, nlev)])
    lam = np.sort(np.linalg.eigvalsh(goe(N, 1)[0]))
    step = 1.2 / np.sqrt(N)
    logp = 0.0
    for k in range(1, len(walls)):
        lo, hi = walls[k - 1], walls[k]
        sweep(lam, lo, N, step, 200, seed + k)               # equilibrate with the previous wall
        cnt = 0
        for s in range(nsamp):
            sweep(lam, lo, N, step, thin, seed * 100000 + k * 1000 + s)
            cnt += lam.min() > hi
        p = max(cnt, 1) / nsamp
        logp += np.log(p)
        lam = np.where(lam <= hi, hi + 1e-3 * (1 + np.arange(N)), lam)   # restart above the new wall
    return float(logp)


if __name__ == "__main__":
    out = {"theta": np.log(3) / 4, "direct": {}, "tilted": {}, "wall": {}}
    for N in (2, 3, 4, 5, 6):
        out["direct"][N] = direct(N, 400000)
        print("direct N=%d lnP=%.3f" % (N, out["direct"][N]), flush=True)
    for N in range(2, 13):
        best = min(((c, *tilted(N, 4000, c)) for c in np.linspace(0.6, 2.4, 19)), key=lambda t: t[2])
        est, rel = tilted(N, 40000, best[0])
        out["tilted"][N] = {"c": float(best[0]), "lnP": est, "rel": rel}
        print("tilted N=%2d lnP=%.2f rel=%.2f" % (N, est, rel), flush=True)
    for N in (2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 21, 25, 30):
        out["wall"][N] = moving_wall(N)
        print("wall   N=%2d lnP=%.2f  -lnP/N^2=%.3f" % (N, out["wall"][N], -out["wall"][N] / N**2), flush=True)
    Ns = np.array([n for n in out["wall"] if n >= 8], float)
    y = np.array([out["wall"][int(n)] for n in Ns])
    A = np.c_[-Ns**2, Ns, np.ones_like(Ns)]
    th, a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    out["fit"] = {"theta": float(th), "a": float(a), "b": float(b), "range": [8, 30]}
    print("fit lnP = -theta N^2 + a N + b : theta=%.4f (ln3/4=%.4f)" % (th, np.log(3) / 4))
    OUT.write_text(json.dumps(out, indent=1))
