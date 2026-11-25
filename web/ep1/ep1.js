import { C, Plot, rng, histogram } from "../assets/plot.js";
import * as R from "../assets/rmt.js";

const $ = id => document.getElementById(id);
const rand = rng(Date.now() % 100000);
const lin = (a, b, n) => Array.from({ length: n + 1 }, (_, i) => a + (b - a) * i / n);
const semiPts = () => lin(-2, 2, 200).map(x => [x, R.semicircle(x)]);
function stepPts(h) {                                    // histogram [[center, density]] -> step outline
  if (!h.length) return [];
  const w = h.length > 1 ? h[1][0] - h[0][0] : 1, p = [];
  for (const [x, y] of h) { p.push([x - w / 2, y], [x + w / 2, y]); }
  return p;
}
function drawHist(P, h, color, alpha = 0.55) { const s = stepPts(h); P.fill(s, color, alpha); P.line(s, color, 1.2); }
function wireSeg(seg, cb) {
  seg.querySelectorAll("button").forEach(b => b.onclick = () => {
    seg.querySelectorAll("button").forEach(x => x.classList.toggle("on", x === b)); cb(); });
}
const segVal = (seg, k) => seg.querySelector("button.on").dataset[k];
const mean = a => a.reduce((s, v) => s + v, 0) / a.length;

// ------------------------------------------------------------------ 1. matrix -> spectrum
const matCv = $("mat"), specP = new Plot($("spec"), { x: [-2.6, 2.6], y: [0, 0.6], aspect: 0.75 });
let cur = null;
function newMatrix() {
  const N = +$("mN").value, law = $("mlaw").value, A = R.wigner(N, law, rand);
  cur = { N, A, lam: R.eigvalsSym(A, N) };
  drawMatrix(); drawSpec();
}
function drawMatrix() {
  const dpr = window.devicePixelRatio || 1, w = matCv.clientWidth || 300;
  matCv.style.height = `${w * 0.75}px`; matCv.width = w * dpr; matCv.height = w * 0.75 * dpr;
  const ctx = matCv.getContext("2d"), { N, A } = cur, side = Math.min(matCv.width, matCv.height) * 0.94;
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, matCv.width, matCv.height);
  const img = ctx.createImageData(N, N), s = Math.sqrt(N);
  const c1 = [242, 181, 68], c2 = [63, 127, 200], bg = [14, 17, 22];
  for (let i = 0; i < N * N; i++) {
    const v = Math.max(-1, Math.min(1, A[i] * s / 2.2)), c = v > 0 ? c1 : c2, t = Math.pow(Math.abs(v), 0.7);
    for (let k = 0; k < 3; k++) img.data[4 * i + k] = bg[k] + (c[k] - bg[k]) * t;
    img.data[4 * i + 3] = 255;
  }
  const tmp = document.createElement("canvas"); tmp.width = N; tmp.height = N; tmp.getContext("2d").putImageData(img, 0, 0);
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(tmp, (matCv.width - side) / 2, (matCv.height - side) / 2, side, side);
}
function drawSpec() {
  const P = specP, { N, lam } = cur; P.clear();
  P.axes({ xl: "eigenvalue", yt: 0, xt: 4 });
  const bins = Math.max(8, Math.min(60, Math.round(Math.sqrt(N) * 2)));
  drawHist(P, histogram(lam, -2.4, 2.4, bins), C.eig);
  if ($("msemi").checked) P.line(semiPts(), C.semi, 2.5);
  P.ctx.fillStyle = C.eig; P.ctx.font = "13px system-ui"; P.ctx.fillText(`N = ${N}`, P.px(1.4), P.py(0.55));
}
["mN", "mlaw"].forEach(id => $(id).onchange = newMatrix);
$("mgo").onclick = newMatrix; $("msemi").onchange = drawSpec;
specP.onresize = () => cur && (drawMatrix(), drawSpec());
newMatrix();

// ------------------------------------------------------------------ 2. rotating a 2x2 matrix
const rotP = new Plot($("rot"), { x: [-3, 3], y: [0, 1], aspect: 0.4, margin: [10, 14, 26, 14] });
function drawRot() {
  const a = +$("ra").value, b = +$("rb").value, d = +$("rd").value, t = +$("rt").value;
  const c = Math.cos(t), s = Math.sin(t);
  const a2 = c * c * a - 2 * c * s * b + s * s * d, b2 = c * s * (a - d) + (c * c - s * s) * b, d2 = s * s * a + 2 * c * s * b + c * c * d;
  const disc = Math.sqrt((a - d) ** 2 + 4 * b * b), l1 = (a + d - disc) / 2, l2 = (a + d + disc) / 2;
  const f = v => (v >= 0 ? " " : "") + v.toFixed(3);
  $("rot-out").innerHTML = `H = [[${f(a)}, ${f(b)}], [${f(b)}, ${f(d)}]]<br>OHOᵀ = [[${f(a2)}, ${f(b2)}], [${f(b2)}, ${f(d2)}]]<br>` +
    `<span style="color:var(--eig)">eigenvalues ${l1.toFixed(3)}, ${l2.toFixed(3)}</span><br>` +
    `Tr = ${(a2 + d2).toFixed(3)} &nbsp; Tr H² = ${(a2 * a2 + d2 * d2 + 2 * b2 * b2).toFixed(3)}`;
  const P = rotP; P.clear(); P.axes({ yt: 0, xt: 6 });
  P.dot(l1, 0.3, C.eig, 6); P.dot(l2, 0.3, C.eig, 6);
  P.dot(a2, 0.7, C.muted, 4); P.dot(d2, 0.7, C.muted, 4);
  const x = P.ctx; x.fillStyle = C.muted; x.font = "12px system-ui"; x.fillText("diagonal entries", P.px(-2.9), P.py(0.85));
  x.fillStyle = C.eig; x.fillText("eigenvalues (fixed)", P.px(-2.9), P.py(0.45));
}
["ra", "rb", "rd", "rt"].forEach(id => $(id).oninput = drawRot);
rotP.onresize = drawRot; drawRot();

// ------------------------------------------------------------------ 3a. strips
const stripP = new Plot($("strips"), { x: [0, 60], y: [0, 1], aspect: 0.22, margin: [8, 10, 10, 10] });
function drawStrips() {
  const P = stripP; P.clear();
  const poi = Array.from({ length: 60 }, () => 60 * rand());
  const lam = R.betaEnsemble(400, 1, rand), N = 400, u = [];
  for (let i = 170; i < 232; i++) u.push(N * R.semiCdf(lam[i]));
  const goe = u.map(v => v - u[0]);
  P.line([[0, 0.72], [60, 0.72]], C.muted, 1); P.line([[0, 0.28], [60, 0.28]], C.muted, 1);
  poi.forEach(v => P.dot(v, 0.72, C.poi, 3.5)); goe.forEach(v => v <= 60 && P.dot(v, 0.28, C.goe, 3.5));
  const x = P.ctx; x.font = "12px system-ui"; x.fillStyle = C.poi; x.fillText("independent points", P.px(0.3), P.py(0.95));
  x.fillStyle = C.goe; x.fillText("eigenvalues", P.px(0.3), P.py(0.5));
}
$("sgo").onclick = drawStrips; stripP.onresize = drawStrips; drawStrips();

// ------------------------------------------------------------------ 3b. the ring
const ringP = new Plot($("ring"), { x: [-6, 6], y: [-6, 6], aspect: 1, margin: [10, 10, 24, 30] });
const ringH = new Plot($("ringh"), { x: [0, 3], y: [0, 1.1], aspect: 1 });
let pts = [];
function addRing(n = 2000) {
  const b = +segVal($("ring-seg"), "b");
  for (let i = 0; i < n; i++) {
    const x = Math.SQRT2 * R.normal(rand), y = Math.SQRT2 * R.normal(rand), z = b === 2 ? Math.SQRT2 * R.normal(rand) : 0;
    pts.push([x, y, z]);
  }
  drawRing();
}
function drawRing() {
  const b = +segVal($("ring-seg"), "b"), r0 = +$("rr").value, dr = 0.3;
  $("rr-o").textContent = r0.toFixed(2);
  const P = ringP; P.clear(); P.axes({ xl: "a − d", yl: "2b", xt: 4, yt: 4 });
  let inside = 0;
  const c = P.ctx;
  for (const [x, y, z] of pts) {
    const r = Math.hypot(x, y, z), inR = r >= r0 && r < r0 + dr; if (inR) inside++;
    c.fillStyle = inR ? C.eig : (b === 1 ? C.goe : C.gue); c.globalAlpha = inR ? 1 : 0.45;
    c.fillRect(P.px(x) - 1, P.py(y) - 1, 2, 2);
  }
  c.globalAlpha = 1; c.strokeStyle = C.eig; c.lineWidth = 1.5;
  for (const rr of [r0, r0 + dr]) { c.beginPath(); c.arc(P.px(0), P.py(0), (P.px(rr) - P.px(0)), 0, 7); c.stroke(); }
  c.fillStyle = C.eig; c.font = "12px system-ui"; c.fillText(`${(100 * inside / Math.max(1, pts.length)).toFixed(1)} % of matrices in the ring`, P.px(-5.8), P.py(5.4));
  const rs = pts.map(p => Math.hypot(...p)), m = mean(rs.length ? rs : [1]);
  const H = ringH; H.clear(); H.axes({ xl: "spacing s (mean 1)", xt: 3, yt: 2 });
  if (rs.length) drawHist(H, histogram(rs.map(v => v / m), 0, 3, 30), b === 1 ? C.goe : C.gue);
  H.line(lin(0, 3, 200).map(s => [s, R.surmise(s, b)]), C.semi, 2.5);
  H.vline(r0 / m, C.eig, [3, 3]);
}
wireSeg($("ring-seg"), () => { pts = []; addRing(); });
$("rr").oninput = drawRing; $("radd").onclick = () => addRing();
ringP.onresize = drawRing; ringH.onresize = drawRing; addRing();

// ------------------------------------------------------------------ 3c. large-N spacings
const spP = new Plot($("sp"), { x: [0, 3.5], y: [0, 1.1], aspect: 0.45 });
let spS = [], spLaw = "gauss";
function addSp() {
  const law = $("splaw").value; if (law !== spLaw) { spS = []; spLaw = law; }
  for (let k = 0; k < 5; k++) spS.push(...R.unfold(R.eigvalsSym(R.wigner(400, law, rand), 400)));
  drawSp();
}
function drawSp() {
  const P = spP; P.clear(); P.axes({ xl: "spacing s", xt: 7, yt: 2 });
  if (spS.length) drawHist(P, histogram(spS, 0, 3.5, 35), C.eig);
  P.line(lin(0, 3.5, 200).map(s => [s, R.surmise(s, 1)]), C.goe, 2.5);
  P.line(lin(0, 3.5, 200).map(s => [s, Math.exp(-s)]), C.poi, 1.5, 0.8, [4, 4]);
  $("sp-read").textContent = ` ${spS.length} spacings · green: Wigner surmise (β = 1) · dashed: Poisson`;
}
$("spgo").onclick = addSp; $("splaw").onchange = addSp; spP.onresize = drawSp; addSp();

// ------------------------------------------------------------------ 4. live Coulomb gas
const gasP = new Plot($("gas"), { x: [-3, 3], y: [-1, 1], aspect: 0.16, margin: [6, 10, 20, 10] });
const gasH = new Plot($("gash"), { x: [-2.6, 2.6], y: [0, 0.6], aspect: 0.32 });
let gx = [], gacc = [], frozen = false;
const gN = () => +$("gN").value, gBeta = () => frozen ? Infinity : 10 ** +$("gb").value;
function scatter() { const N = gN(); gx = Array.from({ length: N }, () => 4 * rand() - 2).sort((a, b) => a - b); gacc = []; frozen = false; }
function gasStep() {
  const N = gx.length, beta = gBeta(), dt = 0.002 / Math.max(1, N / 40);
  for (let it = 0; it < 12; it++) {
    const f = new Array(N).fill(0);
    for (let i = 0; i < N; i++) { let s = 0; for (let j = 0; j < N; j++) if (j !== i) s += 1 / (gx[i] - gx[j]); f[i] = -gx[i] / 2 + s / N; }
    const amp = isFinite(beta) ? Math.sqrt(2 * dt / (beta * N)) : 0;
    for (let i = 0; i < N; i++) gx[i] += f[i] * dt + amp * R.normal(rand);
    gx.sort((a, b) => a - b);
  }
  gacc.push(...gx); if (gacc.length > 200000) gacc.splice(0, gacc.length - 200000);
}
function drawGas() {
  const P = gasP; P.clear(); P.line([[-3, 0], [3, 0]], C.muted, 1);
  P.axes({ yt: 0, xt: 6 }); gx.forEach(v => P.dot(v, 0, C.eig, 3.5));
  const H = gasH; H.clear(); H.axes({ xl: "position", yt: 0, xt: 4 });
  if (gacc.length) drawHist(H, histogram(gacc, -2.6, 2.6, 52), C.eig);
  H.line(semiPts(), C.semi, 2.5);
  $("gN-o").textContent = gN(); $("gb-o").textContent = frozen ? "∞" : (10 ** +$("gb").value).toPrecision(2);
}
let gasVisible = false;
new IntersectionObserver(e => { gasVisible = e[0].isIntersecting; }).observe($("gas"));
function loop() { if (gasVisible) { gasStep(); drawGas(); } requestAnimationFrame(loop); }
$("gN").oninput = scatter; $("gb").oninput = () => { frozen = false; gacc = []; };
$("gfreeze").onclick = () => { frozen = true; gacc = []; }; $("greset").onclick = scatter;
scatter(); drawGas(); requestAnimationFrame(loop);

// ------------------------------------------------------------------ 5. complex field explorer
const fP = new Plot($("field"), { x: [-3.2, 3.2], y: [-2, 2], aspect: 0.62, margin: [10, 10, 24, 30] });
let probe = null;
function drawField() {
  const P = fP; P.clear(); P.axes({ xl: "Re z", yl: "Im z", xt: 8, yt: 4 });
  const c = P.ctx;
  for (let gx_ = -3; gx_ <= 3.001; gx_ += 0.4) for (let gy = -1.8; gy <= 1.81; gy += 0.4) {
    if (Math.abs(gy) < 0.15) continue;
    const g = R.Gsemi([gx_, gy]), vx = g[0], vy = -g[1], L = Math.hypot(vx, vy), l = 0.16 + 0.2 * Math.min(1, L);
    const x0 = P.px(gx_), y0 = P.py(gy), x1 = P.px(gx_ + vx / L * l), y1 = P.py(gy + vy / L * l);
    c.strokeStyle = C.field; c.fillStyle = C.field; c.lineWidth = 1.4;
    c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
    const a = Math.atan2(y1 - y0, x1 - x0); c.beginPath(); c.moveTo(x1, y1);
    c.lineTo(x1 - 6 * Math.cos(a - 0.4), y1 - 6 * Math.sin(a - 0.4)); c.lineTo(x1 - 6 * Math.cos(a + 0.4), y1 - 6 * Math.sin(a + 0.4)); c.fill();
  }
  P.line([[-3.2, 0], [3.2, 0]], C.muted, 1);
  P.fill(lin(-2, 2, 200).map(x => [x, 0.9 * R.semicircle(x)]), C.eig, 0.6, 0);
  if (probe) {
    P.dot(probe[0], probe[1], C.fg, 4);
    const g = R.Gsemi(probe), side = probe[1] > 0 ? "above" : "below";
    let txt = `z = ${probe[0].toFixed(2)} ${probe[1] >= 0 ? "+" : "−"} ${Math.abs(probe[1]).toFixed(2)} i &nbsp;·&nbsp; G(z) = ${g[0].toFixed(3)} ${g[1] >= 0 ? "+" : "−"} ${Math.abs(g[1]).toFixed(3)} i`;
    if (Math.abs(probe[1]) < 0.12 && Math.abs(probe[0]) < 2) {
      txt += `<br>just ${side} the wire: Re G ≈ x/2 = ${(probe[0] / 2).toFixed(3)}, Im G ≈ ${probe[1] > 0 ? "−" : "+"}πρ(x) = ${probe[1] > 0 ? "−" : "+"}${(Math.PI * R.semicircle(probe[0])).toFixed(3)}`;
    }
    $("field-read").innerHTML = txt;
  }
}
$("field").addEventListener("pointermove", ev => {
  const r = $("field").getBoundingClientRect(), X = ev.clientX - r.left, Y = ev.clientY - r.top;
  const x = fP.x[0] + (X - fP.m[3]) / fP.iw * (fP.x[1] - fP.x[0]), y = fP.y[1] - (Y - fP.m[0]) / fP.ih * (fP.y[1] - fP.y[0]);
  probe = [x, Math.abs(y) < 1e-3 ? 1e-3 : y]; drawField();
});
fP.onresize = drawField; drawField();

// ------------------------------------------------------------------ 6. any beta
const bH = new Plot($("bh"), { x: [-2.6, 2.6], y: [0, 0.6], aspect: 0.7 });
const bS = new Plot($("bs"), { x: [0, 3.5], y: [0, 1.6], aspect: 0.7 });
const bStrip = new Plot($("bstrip"), { x: [0, 50], y: [0, 1], aspect: 0.08, margin: [4, 10, 4, 10] });
function drawBeta() {
  const beta = 10 ** +$("bb").value, N = +$("bN").value; $("bb-o").textContent = beta.toPrecision(3);
  const lam = R.betaEnsemble(N, beta, rand), s = R.unfold(lam);
  bH.clear(); bH.axes({ xl: "eigenvalue", yt: 0, xt: 4 }); drawHist(bH, histogram(lam, -2.4, 2.4, 48), C.eig); bH.line(semiPts(), C.semi, 2.5);
  bS.clear(); bS.axes({ xl: "spacing s", xt: 7, yt: 2 }); drawHist(bS, histogram(s, 0, 3.5, 35), C.eig);
  [[0, C.poi], [1, C.goe], [2, C.gue], [4, C.gse]].forEach(([b, c]) => bS.line(lin(0, 3.5, 200).map(x => [x, R.surmise(x, b)]), c, 1.6, 0.9));
  bStrip.clear(); const k = Math.floor(N / 2), u0 = N * R.semiCdf(lam[k]);
  bStrip.line([[0, 0.5], [50, 0.5]], C.muted, 1);
  for (let i = k; i < N; i++) { const u = N * R.semiCdf(lam[i]) - u0; if (u > 50) break; bStrip.dot(u, 0.5, C.eig, 3.5); }
}
["bb", "bN"].forEach(id => $(id).oninput = drawBeta); $("bgo").onclick = drawBeta;
bH.onresize = drawBeta; drawBeta();

// ------------------------------------------------------------------ 7. our computations
fetch("../data/ep1.json").then(r => r.json()).then(D => {
  const ref = (P, betas) => betas.forEach(([b, c]) => P.line(lin(0, 3.5, 200).map(x => [x, R.surmise(x, b)]), c, 2.2));
  const mk = (id, s, col, betas, title) => {
    const P = new Plot($(id), { x: [0, 3.5], y: [0, 1.1], aspect: 0.62 });
    const draw = () => { P.clear(); P.axes({ xl: "spacing s", xt: 7, yt: 2 }); drawHist(P, histogram(s, 0, 3.5, 28), col); ref(P, betas);
      P.ctx.fillStyle = col; P.ctx.font = "13px system-ui"; P.ctx.fillText(title, P.px(1.6), P.py(1.0)); };
    P.onresize = draw; draw();
  };
  mk("bc", D.billiards.circle, C.poi, [[0, C.poi], [1, C.goe]], "circle (regular)");
  mk("bst", D.billiards.stadium, C.goe, [[0, C.poi], [1, C.goe]], "stadium (chaotic)");
  const aP = new Plot($("and"), { x: [0, 3.5], y: [0, 1.1], aspect: 0.45 });
  const drawA = () => { const i = +$("aW").value, W = D.anderson.W[i]; $("aW-o").textContent = W;
    aP.clear(); aP.axes({ xl: "spacing s", xt: 7, yt: 2 }); drawHist(aP, histogram(D.anderson.s[String(W)], 0, 3.5, 28), C.eig);
    ref(aP, [[0, C.poi], [1, C.goe]]); };
  $("aW").max = D.anderson.W.length - 1; $("aW").oninput = drawA; aP.onresize = drawA; drawA();
  const zP = new Plot($("zeta"), { x: [0, 3.5], y: [0, 1.1], aspect: 0.45 });
  const drawZ = () => { zP.clear(); zP.axes({ xl: "spacing s", xt: 7, yt: 2 }); drawHist(zP, histogram(D.zeta, 0, 3.5, 35), C.gue);
    ref(zP, [[0, C.poi], [1, C.goe], [2, C.gue]]); };
  zP.onresize = drawZ; drawZ();
  $("zeta-read").textContent = `${D.zeta.length} spacings · curves: Poisson, GOE, GUE (pink)`;
  const L = D.ld, lP = new Plot($("ld"), { x: [0, 31], y: [0, 0.55], aspect: 0.45 });
  const drawL = () => { lP.clear(); lP.axes({ xl: "N", yl: "−ln P / N²", xt: 6, yt: 5 });
    lP.line([[0, L.theta], [31, L.theta]], C.semi, 1.5, 1, [5, 4]);
    Object.entries(L.tilted).forEach(([n, v]) => lP.dot(+n, Math.min(0.55, -v.lnP / n / n), C.eig, 4));
    Object.entries(L.wall).forEach(([n, v]) => lP.dot(+n, -v / n / n, C.field, 4));
    Object.entries(L.direct).forEach(([n, v]) => lP.dot(+n, -v / n / n, C.fg, 2.5));
    const c = lP.ctx; c.font = "12px system-ui"; c.fillStyle = C.eig; c.fillText("rigged coin (shifted matrix)", lP.px(14), lP.py(0.52));
    c.fillStyle = C.field; c.fillText("moving wall", lP.px(14), lP.py(0.47)); c.fillStyle = C.semi; c.fillText("ln 3 / 4", lP.px(26), lP.py(L.theta) - 6); };
  lP.onresize = drawL; drawL();
  $("ld-read").textContent = `Fit ln P = −θN² + aN + b on N = ${L.fit.range[0]}…${L.fit.range[1]}: θ = ${L.fit.theta.toFixed(3)} (exact 0.2747).`;
  const F = D.facts, rows = Object.entries(F).map(([k, v]) => `<tr><td style="text-align:left">${k}</td><td>${v}</td></tr>`).join("");
  $("facts").innerHTML = `<tr><th style="text-align:left">quantity</th><th>value</th></tr>${rows}`;
});
