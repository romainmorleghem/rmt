# Random Matrices — Order from Noise (episode 1)

Same production style as *Routes to Chaos* and *Rare Events*: Manim CE 0.22.1, dark palette
(`common/style.py`), LaTeX, captions via `Narrated.say()`, no voice-over, English. Target ≈ 22 min.
Audience: curious viewers with first-year linear algebra (matrices, eigenvalues) and a little calculus.
Every derivation is shown step by step; every number comes from `compute/` (→ `data/`).

## Scope (validated with the author)
Kept: what RMT is and where it appears; Gaussian ensembles and β (why: the intersection of "independent
entries" and "rotation invariance"); level repulsion vs Poisson and universality; the joint eigenvalue
density; the Coulomb-gas reading; **the physical derivation of the semicircle** (electrostatics + complex
analysis, the only proof shown); numerical convergence to the semicircle; four original computations
(billiards, Anderson, zeta zeros, the "rigged coin" link). Continuous-β slider (tridiagonal model) on the site.
Left out on purpose: moments/Catalan proof, BBP, May's ecosystems, free probability, Tracy–Widom.

## Colour code
gold = eigenvalues / measured histograms, violet = semicircle and theory, light blue = independent
(Poisson) levels, green = GOE (β=1), pink = GUE (β=2), orange = GSE (β=4), sky blue = electric field.

## Sequences
- **s00 Cold open.** A 60×60 matrix shown as an image of noise. Its eigenvalues drop onto a line and pile up
  into a perfect semicircle. "Random matrix theory: a happy marriage between probability and linear
  algebra." Title card.
- **s01 What is a random matrix? Where does it appear?** Matrix → eigenvalues (2×2 then 1000×1000).
  Timeline: Wishart 1928 (statistics), Wigner 1950s (heavy nuclei: replace the unknown Hamiltonian by a
  random one), Dyson 1962 (three ensembles, Coulomb gas), Montgomery–Dyson 1972 (zeta zeros),
  Bohigas–Giannoni–Schmit 1984 (quantum chaos), disordered metals. Questions: where are the eigenvalues,
  how far apart?
- **s02 The Gaussian ensembles.** Two bubbles: *independent entries* (easy to simulate) and *rotation
  invariance* (no preferred basis, P(OHOᵀ)=P(H)). Their intersection is exactly the Gaussian ensembles
  (Porter–Rosenzweig). Proof for 2×2, à la Maxwell (isotropy + independence ⇒ Gaussian velocities).
  β = number of real numbers per entry: real symmetric (β=1, time-reversal symmetric), complex Hermitian
  (β=2, magnetic field), quaternion (β=4, half-integer spin). P(H) ∝ exp(−βN Tr H²/4).
- **s03 Level repulsion.** Two strips: independent points (clumps, gaps exponential) vs eigenvalues
  (evenly spread). 2×2 proof: spacing = distance to the origin in the (a−d, 2b) plane; a small spacing
  needs to hit a point → P(s) ∝ s (ring), GUE: 3D → s² (sphere). Wigner surmise. Large-N numerics and
  universality (±1 entries give the same histogram).
- **s04 The joint density and the Coulomb gas.** H = OΛOᵀ, Tr H² = Σλ², Jacobian |λ₁−λ₂| (same ring as
  s03), in general ∏|λᵢ−λⱼ|^β. Rewrite as e^{−βE}: charges on a wire, harmonic confinement, 2D Coulomb
  (logarithmic) repulsion; β = inverse temperature.
- **s05 The semicircle, step by step (the long one).** Numerics N = 10 → 4000. Zero temperature: charges
  relax to Hermite zeros (Stieltjes 1885). Continuum limit: both energies ∝ N². Force balance x/2 = P∫ρ/(x−y).
  The field lives in the plane: G(z) = ∫ρ/(z−y) is the complex electric field. Crossing the wire
  (Sokhotski–Plemelj = Gauss's law): horizontal part continuous, vertical part jumps by 2πρ. Equation
  G₊+G₋ = x. Trick F = G − z/2 flips sign → F² has no jump → polynomial (Liouville) = z²/4 − 1. Read the
  density: √(4−x²)/2π, edges at ±2 for free. Overlay on numerics.
- **s06 Our own computations.** (a) quantum billiards: circle (Poisson) vs stadium (GOE); (b) Anderson 3D:
  metal (GOE) → insulator (Poisson) across W_c ≈ 16.5; (c) the first 10 000 zeta zeros vs GUE;
  (d) P(all eigenvalues > 0) ~ e^{−θN²}, θ = ln3/4: the rigged coin breaks down at N ≈ 6, a moving wall
  reaches N = 30; why N² (squeezing a whole gas).
- **s07 Recap.** Three ideas (repulsion, Coulomb gas, semicircle) + β as a temperature (tridiagonal model:
  from a Poisson gas to a crystal). Website card.

## Website (web/ep1)
Everything in the video, with each derivation written out, plus: matrix → spectrum sampler (N, entry law),
2×2 rotation explorer (entries change, eigenvalues stay), level-repulsion ring sampler, live Coulomb gas
(Langevin, β slider, "freeze"), complex-field explorer for G(z) with the jump across the wire, continuous-β
tridiagonal sampler (N up to 5000), and the four computations.
