"""Unfolding helpers: rescale a spectrum so that the mean level spacing is 1."""
import numpy as np


def unfold_weyl(E, skip=20):
    """Unfold with a smooth Weyl-type counting function N(E) = a E + b sqrt(E) + c (billiards)."""
    E = np.sort(E)[skip:]
    n = np.arange(skip, skip + len(E)) + 0.5
    A = np.c_[E, np.sqrt(E), np.ones_like(E)]
    coef, *_ = np.linalg.lstsq(A, n, rcond=None)
    return np.diff(A @ coef)


def unfold_poly(E, deg=5):
    """Unfold a window of a spectrum with a low-degree polynomial fit of the counting function."""
    E = np.sort(E)
    n = np.arange(len(E)) + 0.5
    x = (E - E.mean()) / (E.std() + 1e-300)
    p = np.polyfit(x, n, deg)
    return np.diff(np.polyval(p, x))
