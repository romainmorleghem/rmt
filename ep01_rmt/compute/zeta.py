"""Imaginary parts of the first N_ZEROS non-trivial zeros of the Riemann zeta function -> data/zeta_zeros.json.
Uses mpmath.zetazero (exact to 15 digits). Slow (~1 h on one core): run once, the result is committed.

    python compute/zeta.py
"""
import json, sys
from multiprocessing import Pool
from pathlib import Path
import mpmath

N_ZEROS = 10000
OUT = Path(__file__).resolve().parents[1] / "data" / "zeta_zeros.json"


def zero(n):
    mpmath.mp.dps = 20
    return float(mpmath.zetazero(n).imag)


if __name__ == "__main__":
    with Pool() as p:
        t = p.map(zero, range(1, N_ZEROS + 1), chunksize=50)
    OUT.write_text(json.dumps([round(v, 9) for v in t]))
    print("zeros:", len(t), "last:", t[-1])
