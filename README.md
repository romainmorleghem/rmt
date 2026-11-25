# Random Matrices

A video series (YouTube, no voice-over, captions only) and an interactive companion website on
**random matrix theory: a happy marriage between probability and linear algebra**.

Website: <https://romainmorleghem.github.io/rmt/> (each episode: the video + every derivation written out + live simulations).

| Ep | Title | Video | Web page |
|----|-------|-------|----------|
| 1 | Order from Noise: level repulsion, Coulomb gases and the semicircle | `web/ep1/ep01_1080p.mp4` | [ep1](https://romainmorleghem.github.io/rmt/ep1/) |

---

## Episode 1 in a nutshell
- **What and where.** A random symmetric matrix has random real eigenvalues, with strong correlations. The same
  statistics appear for heavy nuclei (Wigner), zeta zeros (Montgomery–Dyson), chaotic quantum systems
  (Bohigas–Giannoni–Schmit), disordered metals…
- **Gaussian ensembles.** Independent entries ∩ rotation invariance = Gaussian (Porter–Rosenzweig; Maxwell's argument,
  shown for 2×2). β = 1, 2, 4 (real, complex, quaternion): P(H) ∝ exp(−βN Tr H²/4).
- **Level repulsion.** 2×2: the spacing is the distance to the origin in the (a−d, 2b) plane → P(s) ∝ s (ring),
  s² for β = 2 (sphere); Wigner surmise; checked on 800×800 matrices and on ±1 entries (universality).
- **Joint density and Coulomb gas.** ∏|λᵢ−λⱼ|^β exp(−βN Σλ²/4) = e^{−βE}: charges on a wire, harmonic spring,
  2D (logarithmic) repulsion, temperature 1/β.
- **The semicircle, step by step (physics proof).** Zero temperature → Hermite zeros (Stieltjes); continuum limit
  (both energies ∝ N²); force balance x/2 = P∫ρ(y)/(x−y)dy; the complex field G(z); crossing the wire
  (Sokhotski–Plemelj = Gauss); F = G − z/2 flips sign → F² entire → Liouville → G = (z − √(z²−4))/2 →
  ρ = √(4−x²)/2π.
- **Our computations.** Quantum billiards (circle: Poisson; stadium: GOE), Anderson 3D (GOE → Poisson across
  W_c ≈ 16.5), the first 10 000 zeta zeros (GUE), and P(all eigenvalues > 0) ≈ e^{−θN²} (rigged coin up to N ≈ 6,
  moving wall up to N = 30, fitted θ = 0.285 vs ln3/4 = 0.2747).

## Repository layout
```
common/                 style (palette, LaTeX), narration helper, random-matrix samplers (rmt.py)
ep01_rmt/compute/       spectra.py, billiards.py, anderson.py, zeta.py, ld_positive.py, export_web.py -> data/*.json
ep01_rmt/scenes/        Manim Community scenes, one file per sequence (sNN_*.py)
ep01_rmt/render.py      renders all sequences and concatenates them
ep01_rmt/storyboard.md  plan of the episode
web/                    static website (canvas + ES modules + KaTeX); web/assets/rmt.js = browser numerics
```

## Setup and render
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # Manim needs LaTeX + pango/cairo system libraries
cd ep01_rmt
python compute/spectra.py                # ~5 min
python compute/billiards.py              # ~3 min
python compute/anderson.py               # ~10 min
python compute/ld_positive.py            # ~10 min (numba)
python compute/zeta.py                   # ~20 min on 4 cores
python compute/export_web.py
python render.py                         # 480p preview -> media/ep01/ep01_480p15.mp4
python render.py -q f                    # 1080p30
python render.py --only s05              # re-render one sequence and re-assemble
```
All data files are committed, so the render works without re-running the computations.

## Website
```bash
cd web && python -m http.server 8000     # open http://localhost:8000
```
GitHub Pages: `.github/workflows/pages.yml` deploys `web/` on every push to `main`
(enable once: Settings → Pages → Source: GitHub Actions).
