// Small helpers shared by the pages: HiDPI canvas with a data frame, colours, exact coin maths.
export const C = {
  bg: "#0E1116", fg: "#E6E6E6", muted: "#7A8291", line: "#262d38",
  eig: "#F2B544", semi: "#C792EA", poi: "#8FA8C8", goe: "#6CCB8B", gue: "#E85D75", gse: "#FF8A4C",
  field: "#5DA9E9", pos: "#F2B544", neg: "#3F7FC8",
};

// A canvas with a data frame [x0,x1]×[y0,y1] and margins for tick labels.
export class Plot {
  constructor(canvas, { x, y, aspect = 0.56, margin = [12, 14, 30, 52] } = {}) {
    this.cv = canvas; this.ctx = canvas.getContext("2d");
    this.x = x; this.y = y; this.aspect = aspect; this.m = margin;   // top right bottom left
    new ResizeObserver(() => this.resize()).observe(canvas);
    this.resize(false);
  }
  resize(redraw = true) {
    const dpr = window.devicePixelRatio || 1, w = this.cv.clientWidth || 600;
    this.cv.style.height = `${Math.round(w * this.aspect)}px`;
    this.cv.width = Math.round(w * dpr); this.cv.height = Math.round(w * this.aspect * dpr);
    this.dpr = dpr; this.W = w; this.H = w * this.aspect;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (redraw && this.onresize) this.onresize();
  }
  get iw() { return this.W - this.m[1] - this.m[3]; }
  get ih() { return this.H - this.m[0] - this.m[2]; }
  px(v) { return this.m[3] + (v - this.x[0]) / (this.x[1] - this.x[0]) * this.iw; }
  py(v) { return this.m[0] + (this.y[1] - v) / (this.y[1] - this.y[0]) * this.ih; }
  clear() { const c = this.ctx; c.fillStyle = C.bg; c.fillRect(0, 0, this.W, this.H); }
  axes({ xt = 4, yt = 4, xl = "", yl = "", yfmt = null, xfmt = null } = {}) {
    const c = this.ctx; c.strokeStyle = C.muted; c.lineWidth = 1; c.fillStyle = C.muted;
    c.font = "11px system-ui, sans-serif";
    c.beginPath(); c.moveTo(this.m[3], this.m[0]); c.lineTo(this.m[3], this.H - this.m[2]);
    c.lineTo(this.W - this.m[1], this.H - this.m[2]); c.stroke();
    const fmt = v => Math.abs(v) < 1e-12 ? "0" : +v.toPrecision(4) + "";
    c.textAlign = "center"; c.textBaseline = "top";
    for (let i = 0; i <= xt; i++) { const v = this.x[0] + i / xt * (this.x[1] - this.x[0]);
      c.fillText((xfmt || fmt)(v), this.px(v), this.H - this.m[2] + 5); }
    c.textAlign = "right"; c.textBaseline = "middle";
    if (yt) for (let i = 0; i <= yt; i++) { const v = this.y[0] + i / yt * (this.y[1] - this.y[0]);
      c.fillText((yfmt || fmt)(v), this.m[3] - 5, this.py(v)); }
    c.font = "italic 13px Georgia, serif"; c.fillStyle = C.fg;
    if (xl) { c.textAlign = "right"; c.textBaseline = "bottom"; c.fillText(xl, this.W - this.m[1], this.H - this.m[2] - 3); }
    if (yl) { c.textAlign = "left"; c.textBaseline = "top"; c.fillText(yl, this.m[3] + 6, this.m[0]); }
    c.textAlign = "left"; c.textBaseline = "alphabetic"; c.font = "12px system-ui, sans-serif";
  }
  clip(draw) { const c = this.ctx; c.save(); c.beginPath(); c.rect(this.m[3], this.m[0], this.iw, this.ih); c.clip(); draw(); c.restore(); }
  line(pts, color, width = 1.5, alpha = 1, dash = null) {
    this.clip(() => { const c = this.ctx; c.strokeStyle = color; c.lineWidth = width; c.globalAlpha = alpha;
      if (dash) c.setLineDash(dash);
      c.beginPath(); pts.forEach(([a, b], i) => i ? c.lineTo(this.px(a), this.py(b)) : c.moveTo(this.px(a), this.py(b)));
      c.stroke(); c.globalAlpha = 1; c.setLineDash([]); });
  }
  fill(pts, color, alpha = 0.5, base = null) {
    base = base ?? this.y[0];
    this.clip(() => { const c = this.ctx; c.fillStyle = color; c.globalAlpha = alpha; c.beginPath();
      c.moveTo(this.px(pts[0][0]), this.py(base));
      pts.forEach(([a, b]) => c.lineTo(this.px(a), this.py(b)));
      c.lineTo(this.px(pts[pts.length - 1][0]), this.py(base)); c.closePath(); c.fill(); c.globalAlpha = 1; });
  }
  bars(xs, ys, w, color, alpha = 0.85) {
    this.clip(() => { const c = this.ctx; c.fillStyle = color; c.globalAlpha = alpha;
      xs.forEach((x, i) => { const y0 = this.py(this.y[0]), y1 = this.py(ys[i]);
        c.fillRect(this.px(x - w / 2), y1, Math.max(1, this.px(x + w / 2) - this.px(x - w / 2) - 0.5), y0 - y1); });
      c.globalAlpha = 1; });
  }
  dot(a, b, color, r = 3) { const c = this.ctx; c.fillStyle = color; c.beginPath(); c.arc(this.px(a), this.py(b), r, 0, 7); c.fill(); }
  vline(x, color, dash = [4, 4], label = "") {
    this.line([[x, this.y[0]], [x, this.y[1]]], color, 1.5, 1, dash);
    if (label) { const c = this.ctx; c.fillStyle = color; c.font = "12px system-ui, sans-serif";
      c.textAlign = "left"; c.textBaseline = "top"; c.fillText(label, this.px(x) + 4, this.m[0] + 2); }
  }
}

// seeded PRNG (mulberry32)
export function rng(seed = 1) {
  let a = seed >>> 0;
  return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
export function histogram(vals, lo, hi, bins) {
  const h = new Array(bins).fill(0), w = (hi - lo) / bins; let n = 0;
  for (const v of vals) { const k = Math.floor((v - lo) / w); if (k >= 0 && k < bins) h[k]++; n++; }
  return h.map((c, k) => [lo + (k + 0.5) * w, c / (n * w)]);
}
