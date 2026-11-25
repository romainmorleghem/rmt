"""Random matrix samplers and reference curves, shared by compute/ and scenes/.
Normalisation: P(H) ~ exp(-beta N Tr H^2 / 4), so the spectrum fills [-2, 2]."""
import numpy as np


def goe(N, rng, law="gauss"):
    """Real symmetric N x N, off-diagonal variance 1/N. law: gauss | coin (+-1) | uniform."""
    if law == "gauss":
        A = rng.standard_normal((N, N))
    elif law == "coin":
        A = rng.choice([-1.0, 1.0], size=(N, N))
    else:
        A = rng.uniform(-np.sqrt(3), np.sqrt(3), (N, N))
    off = np.triu(A, 1)
    return (off + off.T + np.sqrt(2) * np.diag(np.diag(A))) / np.sqrt(N)   # diagonal variance 2/N (GOE)


def gue(N, rng):
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    return (A + A.conj().T) / np.sqrt(2 * N)


def beta_tridiagonal(N, beta, rng):
    """Dumitriu-Edelman beta-Hermite ensemble, rescaled so the spectrum fills [-2, 2]. Returns eigenvalues."""
    from scipy.linalg import eigvalsh_tridiagonal
    d = rng.standard_normal(N) * np.sqrt(2)
    e = np.sqrt(rng.chisquare(beta * np.arange(N - 1, 0, -1)))
    lam = eigvalsh_tridiagonal(d / np.sqrt(2), e / np.sqrt(2))
    return lam * 2 / np.sqrt(2 * beta * N)


def semicircle(x):
    x = np.asarray(x, float)
    return np.where(np.abs(x) < 2, np.sqrt(np.clip(4 - x * x, 0, None)) / (2 * np.pi), 0.0)


def semicircle_cdf(x):
    x = np.clip(x, -2, 2)
    return 0.5 + (x * np.sqrt(4 - x * x) / 2 + 2 * np.arcsin(x / 2)) / (2 * np.pi)


def unfold_bulk(lam, frac=0.5):
    """Spacings of the central part of a spectrum, unfolded with the semicircle law (mean spacing 1)."""
    lam = np.sort(lam)
    N = len(lam)
    k = int(N * (1 - frac) / 2)
    u = N * semicircle_cdf(lam[k:N - k])
    return np.diff(u)


def surmise(s, beta):
    s = np.asarray(s, float)
    if beta == 0:
        return np.exp(-s)
    if beta == 1:
        return np.pi * s / 2 * np.exp(-np.pi * s * s / 4)
    if beta == 2:
        return 32 / np.pi**2 * s * s * np.exp(-4 * s * s / np.pi)
    return 2**18 / (3**6 * np.pi**3) * s**4 * np.exp(-64 * s * s / (9 * np.pi))


def hermite_gas(N):
    """Zero-temperature Coulomb gas: equilibrium positions = zeros of the Hermite polynomial H_N (Stieltjes),
    rescaled to our normalisation (lambda = sqrt(2/N) x)."""
    from numpy.polynomial.hermite import hermroots
    c = np.zeros(N + 1); c[-1] = 1
    return np.sort(hermroots(c)) * np.sqrt(2 / N)
