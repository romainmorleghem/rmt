// Random-matrix numerics for the browser: samplers, symmetric eigenvalues (Householder + implicit QL),
// the Dumitriu-Edelman tridiagonal beta-ensemble, unfolding, reference curves, complex helpers.
// Normalisation everywhere: P(H) ~ exp(-beta N Tr H^2 / 4), spectrum on [-2, 2].

export function normal(rand) {                     // Box-Muller
  let u = 0; while (u === 0) u = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * rand());
}
export function gamma(a, rand) {                   // Marsaglia-Tsang, shape a > 0, scale 1
  if (a < 1) return gamma(a + 1, rand) * Math.pow(rand(), 1 / a);
  const d = a - 1 / 3, c = 1 / Math.sqrt(9 * d);
  for (;;) {
    let x, v; do { x = normal(rand); v = 1 + c * x; } while (v <= 0);
    v = v * v * v; const u = rand();
    if (u < 1 - 0.0331 * x ** 4 || Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}
const chi = (k, rand) => Math.sqrt(2 * gamma(k / 2, rand));

// Real symmetric Wigner matrix, row-major Float64Array. law: gauss | coin | uniform
export function wigner(N, law, rand) {
  const A = new Float64Array(N * N), s = 1 / Math.sqrt(N);
  const draw = law === "coin" ? () => (rand() < 0.5 ? -1 : 1)
    : law === "uniform" ? () => (2 * rand() - 1) * Math.sqrt(3) : () => normal(rand);
  for (let i = 0; i < N; i++) {
    A[i * N + i] = draw() * Math.SQRT2 * s;
    for (let j = i + 1; j < N; j++) { const v = draw() * s; A[i * N + j] = v; A[j * N + i] = v; }
  }
  return A;
}

// Householder reduction of a symmetric matrix to tridiagonal form (Numerical Recipes tred2, no vectors).
function tred2(a, n, d, e) {
  for (let i = n - 1; i > 0; i--) {
    const l = i - 1; let h = 0, scale = 0;
    if (l > 0) {
      for (let k = 0; k <= l; k++) scale += Math.abs(a[i * n + k]);
      if (scale === 0) e[i] = a[i * n + l];
      else {
        for (let k = 0; k <= l; k++) { a[i * n + k] /= scale; h += a[i * n + k] ** 2; }
        let f = a[i * n + l]; let g = f >= 0 ? -Math.sqrt(h) : Math.sqrt(h);
        e[i] = scale * g; h -= f * g; a[i * n + l] = f - g; f = 0;
        for (let j = 0; j <= l; j++) {
          g = 0;
          for (let k = 0; k <= j; k++) g += a[j * n + k] * a[i * n + k];
          for (let k = j + 1; k <= l; k++) g += a[k * n + j] * a[i * n + k];
          e[j] = g / h; f += e[j] * a[i * n + j];
        }
        const hh = f / (h + h);
        for (let j = 0; j <= l; j++) {
          f = a[i * n + j]; e[j] = g = e[j] - hh * f;
          for (let k = 0; k <= j; k++) a[j * n + k] -= f * e[k] + g * a[i * n + k];
        }
      }
    } else e[i] = a[i * n + l];
    d[i] = h;
  }
  e[0] = 0;
  for (let i = 0; i < n; i++) d[i] = a[i * n + i];
  for (let i = 1; i < n; i++) e[i - 1] = e[i];      // e[i] = off-diagonal (i, i+1)
  e[n - 1] = 0;
}

// Eigenvalues of a symmetric tridiagonal matrix (diag d, off-diag e[i] between i and i+1), implicit QL.
export function tqli(d, e) {
  const n = d.length;
  for (let l = 0; l < n; l++) {
    let iter = 0, m;
    for (;;) {
      for (m = l; m < n - 1; m++) {
        const dd = Math.abs(d[m]) + Math.abs(d[m + 1]);
        if (Math.abs(e[m]) <= 1e-15 * dd) break;
      }
      if (m === l) break;
      if (iter++ > 60) break;
      let g = (d[l + 1] - d[l]) / (2 * e[l]), r = Math.hypot(g, 1);
      g = d[m] - d[l] + e[l] / (g + (g >= 0 ? Math.abs(r) : -Math.abs(r)));
      let s = 1, c = 1, p = 0, i, early = false;
      for (i = m - 1; i >= l; i--) {
        let f = s * e[i]; const b = c * e[i];
        e[i + 1] = r = Math.hypot(f, g);
        if (r === 0) { d[i + 1] -= p; e[m] = 0; early = true; break; }
        s = f / r; c = g / r; g = d[i + 1] - p; r = (d[i] - g) * s + 2 * c * b;
        p = s * r; d[i + 1] = g + p; g = c * r - b;
      }
      if (early) continue;
      d[l] -= p; e[l] = g; e[m] = 0;
    }
  }
  return Array.from(d).sort((x, y) => x - y);
}

export function eigvalsSym(A, N) {
  const a = Float64Array.from(A), d = new Float64Array(N), e = new Float64Array(N);
  tred2(a, N, d, e);
  return tqli(d, e);
}

// Dumitriu-Edelman beta-Hermite ensemble (any beta > 0), rescaled to [-2, 2].
export function betaEnsemble(N, beta, rand) {
  const d = new Float64Array(N), e = new Float64Array(N);
  for (let i = 0; i < N; i++) d[i] = normal(rand);                       // N(0,2)/sqrt2 = N(0,1)
  for (let i = 0; i < N - 1; i++) e[i] = chi(beta * (N - 1 - i), rand) / Math.SQRT2;
  const k = 2 / Math.sqrt(2 * beta * N);
  return tqli(d, e).map(v => v * k);
}

export const semicircle = x => Math.abs(x) < 2 ? Math.sqrt(4 - x * x) / (2 * Math.PI) : 0;
export function semiCdf(x) {
  x = Math.max(-2, Math.min(2, x));
  return 0.5 + (x * Math.sqrt(4 - x * x) / 2 + 2 * Math.asin(x / 2)) / (2 * Math.PI);
}
// spacings of the central part of a spectrum, unfolded with the semicircle law (mean 1)
export function unfold(lam, frac = 0.5) {
  const N = lam.length, k = Math.floor(N * (1 - frac) / 2), u = [];
  for (let i = k; i < N - k; i++) u.push(N * semiCdf(lam[i]));
  const s = []; for (let i = 1; i < u.length; i++) s.push(u[i] - u[i - 1]);
  return s;
}
export function surmise(s, beta) {
  if (beta === 0) return Math.exp(-s);
  if (beta === 1) return Math.PI * s / 2 * Math.exp(-Math.PI * s * s / 4);
  if (beta === 2) return 32 / Math.PI ** 2 * s * s * Math.exp(-4 * s * s / Math.PI);
  return 2 ** 18 / (3 ** 6 * Math.PI ** 3) * s ** 4 * Math.exp(-64 * s * s / (9 * Math.PI));
}

// complex numbers as [re, im]
export const cadd = (a, b) => [a[0] + b[0], a[1] + b[1]];
export const csub = (a, b) => [a[0] - b[0], a[1] - b[1]];
export const cmul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
export function csqrt([x, y]) {                    // principal square root
  const r = Math.hypot(x, y), u = Math.sqrt((r + x) / 2), v = Math.sqrt(Math.max(0, (r - x) / 2));
  return [u, y < 0 ? -v : v];
}
// Stieltjes transform of the semicircle: G(z) = (z - sqrt(z-2) sqrt(z+2)) / 2  (branch ~ 1/z at infinity)
export function Gsemi(z) {
  const s = cmul(csqrt(csub(z, [2, 0])), csqrt(cadd(z, [2, 0])));
  return [(z[0] - s[0]) / 2, (z[1] - s[1]) / 2];
}
