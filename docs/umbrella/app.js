import * as THREE from './vendor/three.module.min.js';

/* ------------------------------------------------------------------ constants */
const D2R = Math.PI / 180;
const N = 8;                       // canopy panels (gores)
const W = (2 * Math.PI) / N;       // angular width of one panel
const TW = 256, TH = 384;          // texture tile per panel; row 0 = apex, row TH = rim
const ATW = N * TW;
const AZ = 100 * D2R, UP = 60 * D2R, DN = 75 * D2R;  // human visual field half-extents
const EYE_TO_GROUND = 1.62;
const SHAFT_TO_HAND = 0.78;

const BRANDS = [
  { name: 'RAINBORROW', tag: 'Borrow. Return. Stay dry.', bg: '#FF5A36', fg: '#FFFFFF' },
  { name: 'NOVA TEA', tag: 'Hot tea, two blocks away', bg: '#FFD23F', fg: '#1B1B1B' },
  { name: 'KITE BANK', tag: 'Save for a rainy day', bg: '#1FB6A6', fg: '#FFFFFF' },
  { name: 'MOSS PHONES', tag: 'Waterproof. Finally.', bg: '#FF4F9A', fg: '#FFFFFF' },
];

const S = {
  diam: 1.05, depth: 0.26, height: 0.42, tilt: 0, fwd: 0.10, side: 0.20, spin: 0,
  layout: 'full', panels: 'all', print: 'both', size: 0.8,
  yaw: 0, pitch: 0, fov: 90,
  mode: 'pov', map: 'real',
};

const $ = (id) => document.getElementById(id);
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (v) => { const l = Math.hypot(v[0], v[1], v[2]); return [v[0] / l, v[1] / l, v[2] / l]; };

/* ------------------------------------------------------------------ ad artwork (2D atlas) */
const mk = () => { const c = document.createElement('canvas'); c.width = ATW; c.height = TH; return c; };
const cvIn = mk(), cvOut = mk(), cvMask = mk();
const ctxIn = cvIn.getContext('2d', { willReadFrequently: true });
const ctxOut = cvOut.getContext('2d');
const ctxMask = cvMask.getContext('2d', { willReadFrequently: true });
let inPixels = null;              // Uint8ClampedArray RGBA of the inside atlas
let mask = new Uint8Array(ATW * TH);   // 1 where an ad is printed on the inside

const panelHasAd = (k) => ({
  all: true, alt: k % 2 === 0, front3: k === 0 || k === 1 || k === N - 1, front: k === 0,
}[S.panels]);

function adRect() {
  const s = S.size;
  if (S.layout === 'full') return { x: 0, y: TH * (1 - s), w: TW, h: TH * s };
  if (S.layout === 'band') { const h = TH * 0.5 * s; return { x: 0, y: TH - h, w: TW, h }; }
  const w = TW * 0.92 * s, h = TH * 0.52 * s;       // card
  return { x: (TW - w) / 2, y: TH * 0.64 - h / 2, w, h };
}

function wrap(ctx, text, maxW) {
  const words = text.split(' '), lines = []; let cur = '';
  for (const w of words) {
    const t = cur ? cur + ' ' + w : w;
    if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t;
  }
  if (cur) lines.push(cur);
  return lines;
}

function drawAd(ctx, x0, k, forMask) {
  const r = adRect();
  ctx.save();
  ctx.beginPath(); ctx.rect(x0, 0, TW, TH); ctx.clip();
  const rad = S.layout === 'card' ? 14 : 0;
  ctx.beginPath();
  if (ctx.roundRect && rad) ctx.roundRect(x0 + r.x, r.y, r.w, r.h, rad); else ctx.rect(x0 + r.x, r.y, r.w, r.h);
  const b = BRANDS[k % BRANDS.length];
  ctx.fillStyle = forMask ? '#fff' : b.bg;
  ctx.fill();
  if (!forMask) {
    ctx.clip();
    ctx.fillStyle = b.fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    const cx = x0 + r.x + r.w / 2, pad = r.w * 0.08, maxW = r.w - pad * 2;
    let fs = Math.min(maxW / (b.name.length * 0.68), r.h * 0.26, 46);
    const fam = '"Archivo", "Arial Black", sans-serif';
    ctx.font = `800 ${fs}px ${fam}`;
    const nameY = r.y + r.h * (S.layout === 'band' ? 0.42 : 0.4);
    ctx.fillText(b.name, cx, nameY, maxW);
    const tfs = Math.max(11, Math.min(fs * 0.42, 20));
    ctx.font = `600 ${tfs}px ${fam}`;
    const lines = wrap(ctx, b.tag, maxW);
    lines.forEach((ln, i) => ctx.fillText(ln, cx, nameY + fs * 0.85 + i * tfs * 1.25, maxW));
    // "scan" chip
    const cs = Math.min(r.w * 0.22, r.h * 0.16, 44);
    if (cs > 14) {
      const qy = r.y + r.h - cs - 10;
      ctx.fillStyle = b.fg; ctx.fillRect(cx - cs / 2, qy, cs, cs);
      ctx.fillStyle = b.bg;
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) if ((i * 3 + j * 5 + k) % 3 === 0) ctx.fillRect(cx - cs / 2 + 3 + i * (cs - 6) / 4, qy + 3 + j * (cs - 6) / 4, (cs - 6) / 4 - 1, (cs - 6) / 4 - 1);
    }
  }
  ctx.restore();
}

function paintAtlas() {
  const inside = S.print === 'both' || S.print === 'in';
  const outside = S.print === 'both' || S.print === 'out';
  for (const [ctx, fabric, ads] of [[ctxIn, '#41537A', inside], [ctxOut, '#1B2742', outside]]) {
    for (let k = 0; k < N; k++) {
      const x0 = k * TW;
      ctx.fillStyle = fabric; ctx.fillRect(x0, 0, TW, TH);
      if (ads && panelHasAd(k)) drawAd(ctx, x0, k, false);
      ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.fillRect(x0, 0, 2, TH); ctx.fillRect(x0 + TW - 2, 0, 2, TH);
    }
  }
  ctxMask.fillStyle = '#000'; ctxMask.fillRect(0, 0, ATW, TH);
  if (inside) for (let k = 0; k < N; k++) if (panelHasAd(k)) drawAd(ctxMask, k * TW, k, true);
  const m = ctxMask.getImageData(0, 0, ATW, TH).data;
  for (let i = 0; i < mask.length; i++) mask[i] = m[i * 4] > 127 ? 1 : 0;
  inPixels = ctxIn.getImageData(0, 0, ATW, TH).data;
}

/* ------------------------------------------------------------------ umbrella geometry + ray tracer */
function geometry() {
  const r = S.diam / 2, h = Math.min(S.depth, r * 0.98);
  const Rs = (r * r + h * h) / (2 * h);
  const thetaMax = Math.asin(r / Rs);
  const al = S.tilt * D2R;
  const a = [0, Math.cos(al), -Math.sin(al)];
  const hand = [S.side, S.height - SHAFT_TO_HAND, -S.fwd];
  const apex = [hand[0] + a[0] * SHAFT_TO_HAND, hand[1] + a[1] * SHAFT_TO_HAND, hand[2] + a[2] * SHAFT_TO_HAND];
  const Cs = [apex[0] - a[0] * Rs, apex[1] - a[1] * Rs, apex[2] - a[2] * Rs];
  const f = [0, 0, -1], fa = f[0] * a[0] + f[1] * a[1] + f[2] * a[2];
  const e1 = norm([f[0] - fa * a[0], f[1] - fa * a[1], f[2] - fa * a[2]]);
  const z3 = cross(e1, a);
  return { r, h, Rs, thetaMax, a, hand, apex, Cs, e1, z3, spin: S.spin * D2R };
}

/** Returns classify(dx,dy,dz) for unit rays from the holder's eye: 0 open, 1 canopy fabric, 2 ad. */
function makeTracer(G) {
  const { Cs, a, e1, z3, Rs, thetaMax, spin } = G;
  const cx = Cs[0], cy = Cs[1], cz = Cs[2];
  const cc = cx * cx + cy * cy + cz * cz - Rs * Rs;
  const minLy = Rs * Math.cos(thetaMax);
  const res = { idx: 0 };
  const TAU = 2 * Math.PI;
  function hit(dx, dy, dz) {
    const b = -(cx * dx + cy * dy + cz * dz);
    const disc = b * b - cc;
    if (disc < 0) return false;
    const sq = Math.sqrt(disc);
    for (let i = 0; i < 2; i++) {
      const t = i === 0 ? -b - sq : -b + sq;
      if (t <= 0) continue;
      const px = t * dx - cx, py = t * dy - cy, pz = t * dz - cz;
      const ly = px * a[0] + py * a[1] + pz * a[2];
      if (ly < minLy) continue;
      const lx = px * e1[0] + py * e1[1] + pz * e1[2];
      const lz = px * z3[0] + py * z3[1] + pz * z3[2];
      const theta = Math.acos(clamp(ly / Rs, -1, 1));
      let ph = (Math.atan2(lz, lx) + spin + W / 2) % TAU; if (ph < 0) ph += TAU;
      let k = Math.floor(ph / W); if (k >= N) k = N - 1;
      const u = ph / W - k;
      const row = Math.min(TH - 1, Math.floor((theta / thetaMax) * TH));
      const col = Math.min(TW - 1, Math.floor(u * TW));
      res.idx = row * ATW + k * TW + col;
      return true;
    }
    return false;
  }
  return {
    classify(dx, dy, dz) { return hit(dx, dy, dz) ? (mask[res.idx] ? 2 : 1) : 0; },
    pixel(dx, dy, dz) { return hit(dx, dy, dz) ? res.idx : -1; },
  };
}

/* ------------------------------------------------------------------ gaze + visual field sampling */
function gazeBasis(yaw, pitch) {
  const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
  const f = [-sy * cp, sp, -cy * cp];
  const r = [cy, 0, -sy];
  const u = cross([-f[0], -f[1], -f[2]], r);
  return { f, r, u };
}

const inField = (x, y, z) => {
  const az = Math.atan2(x, z), el = Math.asin(clamp(y, -1, 1));
  const e = el >= 0 ? UP : DN;
  return (az / AZ) ** 2 + (el / e) ** 2 <= 1;
};

// evenly spaced directions over the sphere (gaze frame: x right, y up, z forward), kept inside the field
const samples = (() => {
  const M = 90000, ga = Math.PI * (3 - Math.sqrt(5)), out = [];
  for (let i = 0; i < M; i++) {
    const y = 1 - (2 * (i + 0.5)) / M, rr = Math.sqrt(1 - y * y), t = ga * i;
    const x = Math.cos(t) * rr, z = Math.sin(t) * rr;
    if (inField(x, y, z)) out.push(x, y, z);
  }
  return new Float32Array(out);
})();
const CENTRAL_COS = Math.cos(30 * D2R);

function statsFor(tracer, yaw, pitch, viewport) {
  const { f, r, u } = gazeBasis(yaw, pitch);
  let n = 0, ad = 0, can = 0, cn = 0, cad = 0, ccan = 0;
  for (let i = 0; i < samples.length; i += 3) {
    const x = samples[i], y = samples[i + 1], z = samples[i + 2];
    const c = tracer.classify(x * r[0] + y * u[0] + z * f[0], x * r[1] + y * u[1] + z * f[1], x * r[2] + y * u[2] + z * f[2]);
    n++; if (c === 2) ad++; if (c) can++;
    if (z >= CENTRAL_COS) { cn++; if (c === 2) cad++; if (c) ccan++; }
  }
  const out = { field: ad / n, canopy: can / n, central: cad / cn, centralCanopy: ccan / cn };
  if (viewport) {
    const th = Math.tan(viewport.fov * D2R / 2), tw = th * viewport.aspect;
    let vn = 0, vad = 0;
    for (let j = 0; j < 45; j++) for (let i = 0; i < 80; i++) {
      const x = ((i + 0.5) / 80 * 2 - 1) * tw, y = (1 - (j + 0.5) / 45 * 2) * th;
      const l = Math.hypot(x, y, 1), gx = x / l, gy = y / l, gz = 1 / l;
      const c = tracer.classify(gx * r[0] + gy * u[0] + gz * f[0], gx * r[1] + gy * u[1] + gz * f[1], gx * r[2] + gy * u[2] + gz * f[2]);
      vn++; if (c === 2) vad++;
    }
    out.screen = vad / vn;
  }
  return out;
}

function adAreaM2(G) {
  let sum = 0;
  const dth = G.thetaMax / TH;
  for (let row = 0; row < TH; row++) {
    const s = Math.sin((row + 0.5) * dth);
    let cnt = 0;
    for (let k = 0; k < N; k++) for (let c = 0; c < TW; c++) cnt += mask[row * ATW + k * TW + c];
    sum += cnt * s;
  }
  return G.Rs * G.Rs * dth * (W / TW) * sum;
}

/* ------------------------------------------------------------------ fisheye map of the whole visual field */
const fish = $('fish'), fctx = fish.getContext('2d');
const FW = fish.width, FH = fish.height, RMAX = 100 * D2R;
const fimg = fctx.createImageData(FW, FH);

function skyGround(dy) {
  const el = Math.asin(clamp(dy, -1, 1));
  if (el >= 0) { const t = Math.sqrt(el / (Math.PI / 2)); return [213 + (111 - 213) * t, 230 + (168 - 230) * t, 243 + (220 - 243) * t]; }
  const t = clamp(-el / (Math.PI / 2), 0, 1); return [107 + (61 - 107) * t, 112 + (65 - 112) * t, 117 + (69 - 117) * t];
}

function drawFisheye(tracer) {
  const { f, r, u } = gazeBasis(S.yaw * D2R, S.pitch * D2R);
  const d = fimg.data, cov = S.map === 'cov';
  for (let py = 0; py < FH; py++) for (let px = 0; px < FW; px++) {
    const o = (py * FW + px) * 4;
    const x = ((px + 0.5) / FW) * 2 - 1, y = 1 - ((py + 0.5) / FH) * 2, rr = Math.hypot(x, y);
    let R = 10, G = 13, B = 18;
    if (rr <= 1) {
      const rho = rr * RMAX, psi = Math.atan2(y, x), s = Math.sin(rho);
      const gx = s * Math.cos(psi), gy = s * Math.sin(psi), gz = Math.cos(rho);
      if (inField(gx, gy, gz)) {
        const wx = gx * r[0] + gy * u[0] + gz * f[0], wy = gx * r[1] + gy * u[1] + gz * f[1], wz = gx * r[2] + gy * u[2] + gz * f[2];
        const idx = tracer.pixel(wx, wy, wz);
        if (idx < 0) { [R, G, B] = cov ? [22, 32, 44] : skyGround(wy); }
        else if (cov) { [R, G, B] = mask[idx] ? [255, 79, 139] : [91, 107, 138]; }
        else { R = inPixels[idx * 4]; G = inPixels[idx * 4 + 1]; B = inPixels[idx * 4 + 2]; }
      } else { R = 20; G = 26; B = 34; }
    }
    d[o] = R; d[o + 1] = G; d[o + 2] = B; d[o + 3] = 255;
  }
  fctx.putImageData(fimg, 0, 0);
  const cx = FW / 2, cy = FH / 2, rad = FW / 2;
  fctx.lineWidth = 1; fctx.strokeStyle = 'rgba(255,255,255,.28)'; fctx.fillStyle = 'rgba(255,255,255,.7)';
  fctx.font = '11px "IBM Plex Mono", monospace';
  for (const deg of [30, 60, 90]) {
    fctx.beginPath(); fctx.arc(cx, cy, (deg / 100) * rad, 0, 7); fctx.stroke();
    fctx.fillText(deg + '°', cx + 4, cy - (deg / 100) * rad + 12);
  }
  fctx.beginPath(); fctx.moveTo(cx - 6, cy); fctx.lineTo(cx + 6, cy); fctx.moveTo(cx, cy - 6); fctx.lineTo(cx, cy + 6); fctx.stroke();
  fctx.strokeStyle = '#FFD23F'; fctx.lineWidth = 1.6; fctx.beginPath();
  for (let i = 0; i <= 120; i++) {
    const t = (i / 120) * 2 * Math.PI, az = AZ * Math.cos(t), el = (Math.sin(t) >= 0 ? UP : DN) * Math.sin(t);
    const gx = Math.cos(el) * Math.sin(az), gy = Math.sin(el), gz = Math.cos(el) * Math.cos(az);
    const rho = Math.acos(clamp(gz, -1, 1)), psi = Math.atan2(gy, gx);
    const px = cx + (rho / RMAX) * rad * Math.cos(psi), py = cy - (rho / RMAX) * rad * Math.sin(psi);
    i ? fctx.lineTo(px, py) : fctx.moveTo(px, py);
  }
  fctx.stroke();
  fctx.fillStyle = 'rgba(255,255,255,.8)'; fctx.textAlign = 'center';
  fctx.fillText('up', cx, 12); fctx.fillText('down', cx, FH - 5);
  fctx.textAlign = 'left'; fctx.fillText('left', 4, cy + 4); fctx.textAlign = 'right'; fctx.fillText('right', FW - 4, cy + 4); fctx.textAlign = 'left';
}

/* ------------------------------------------------------------------ Three.js scene */
const viewer = $('viewer'), glcanvas = $('gl');
let renderer = null;
try { renderer = new THREE.WebGLRenderer({ canvas: glcanvas, antialias: true, preserveDrawingBuffer: true }); }
catch (e) { $('nogl').style.display = 'block'; glcanvas.style.display = 'none'; }

const scene = new THREE.Scene();
const povCam = new THREE.PerspectiveCamera(S.fov, 16 / 10, 0.02, 500);
povCam.rotation.order = 'YXZ';
const outCam = new THREE.PerspectiveCamera(40, 16 / 10, 0.05, 600);
const orbit = { az: 38 * D2R, el: 12 * D2R, dist: 4.1, target: new THREE.Vector3(0.1, -0.6, 0) };
let needsRender = true;

function buildWorld() {
  // sky dome with the same gradient the fisheye map uses
  const sky = new THREE.SphereGeometry(300, 40, 20);
  const cols = [], p = sky.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const [r, g, b] = skyGround(p.getY(i) / 300);
    cols.push(r / 255, g / 255, b / 255);
  }
  sky.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
  scene.add(new THREE.Mesh(sky, new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.BackSide, fog: false })));

  // pavement
  const gc = document.createElement('canvas'); gc.width = gc.height = 256;
  const g2 = gc.getContext('2d'); g2.fillStyle = '#5c6167'; g2.fillRect(0, 0, 256, 256);
  g2.strokeStyle = '#575c62'; g2.lineWidth = 2; g2.strokeRect(0, 0, 256, 256); g2.beginPath(); g2.moveTo(128, 0); g2.lineTo(128, 256); g2.moveTo(0, 128); g2.lineTo(256, 128); g2.stroke();
  const gt = new THREE.CanvasTexture(gc); gt.wrapS = gt.wrapT = THREE.RepeatWrapping; gt.repeat.set(120, 120); gt.colorSpace = THREE.SRGBColorSpace; gt.anisotropy = 8;
  const ground = new THREE.Mesh(new THREE.CircleGeometry(280, 48), new THREE.MeshStandardMaterial({ map: gt, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -EYE_TO_GROUND; scene.add(ground);

  // a street of buildings
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const wc = document.createElement('canvas'); wc.width = 64; wc.height = 128;
  const w2 = wc.getContext('2d'); w2.fillStyle = '#fff'; w2.fillRect(0, 0, 64, 128); w2.fillStyle = '#9fb4c7';
  for (let y = 8; y < 120; y += 16) for (let x = 6; x < 60; x += 18) w2.fillRect(x, y, 10, 9);
  const wt = new THREE.CanvasTexture(wc); wt.wrapS = wt.wrapT = THREE.RepeatWrapping; wt.colorSpace = THREE.SRGBColorSpace;
  const tints = ['#c9b8a6', '#b7c2cc', '#d8c9b0', '#a9b5a3', '#c7a99b', '#bdbdc9'];
  for (let side = -1; side <= 1; side += 2) {
    for (let z = -170; z < 90; z += 16 + rnd() * 6) {
      const w = 12 + rnd() * 6, h = 14 + rnd() * 34, d = 12 + rnd() * 6;
      const t = wt.clone(); t.needsUpdate = true; t.repeat.set(Math.max(1, Math.round(w / 4)), Math.max(1, Math.round(h / 8)));
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshStandardMaterial({ color: tints[Math.floor(rnd() * tints.length)], map: t, roughness: 0.9 }));
      m.position.set(side * (9 + w / 2 + rnd() * 2), h / 2 - EYE_TO_GROUND, z); scene.add(m);
    }
  }
  scene.add(new THREE.HemisphereLight(0xdfeeff, 0x55575a, 1.5));
  const sun = new THREE.DirectionalLight(0xffffff, 2.0); sun.position.set(-8, 14, 6); scene.add(sun);

  // the holder (only shown in outside view)
  person.name = 'person';
  const coat = new THREE.MeshStandardMaterial({ color: '#39404a', roughness: 0.9 });
  const skin = new THREE.MeshStandardMaterial({ color: '#d9a982', roughness: 0.8 });
  const add = (geo, mat, x, y, z) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); person.add(m); return m; };
  add(new THREE.SphereGeometry(0.1, 24, 16), skin, 0, 0.02, 0.08);
  const hair = add(new THREE.SphereGeometry(0.104, 24, 12, 0, Math.PI * 2, 0, Math.PI * 0.55), new THREE.MeshStandardMaterial({ color: '#2a211c' }), 0, 0.03, 0.09); hair.rotation.x = -0.25;
  add(new THREE.CylinderGeometry(0.045, 0.05, 0.12, 12), skin, 0, -0.1, 0.08);
  add(new THREE.CapsuleGeometry(0.17, 0.42, 6, 16), coat, 0, -0.5, 0.08).scale.set(1.15, 1, 0.75);
  add(new THREE.CylinderGeometry(0.075, 0.065, 0.78, 14), new THREE.MeshStandardMaterial({ color: '#232a36' }), -0.09, -1.22, 0.08);
  add(new THREE.CylinderGeometry(0.075, 0.065, 0.78, 14), new THREE.MeshStandardMaterial({ color: '#232a36' }), 0.09, -1.22, 0.08);
  add(new THREE.BoxGeometry(0.1, 0.06, 0.24), new THREE.MeshStandardMaterial({ color: '#15181d' }), -0.09, -1.59, 0.03);
  add(new THREE.BoxGeometry(0.1, 0.06, 0.24), new THREE.MeshStandardMaterial({ color: '#15181d' }), 0.09, -1.59, 0.03);
  add(new THREE.CylinderGeometry(0.04, 0.035, 0.34, 10), coat, -0.27, -0.42, 0.08).rotation.z = 0.15;
  scene.add(person);
  scene.add(umbrellaRoot); scene.add(fieldRoot);
}

const person = new THREE.Group();
const umbrellaRoot = new THREE.Group();
const fieldRoot = new THREE.Group();
let armMesh = null, handMesh = null;
const skinMat = new THREE.MeshStandardMaterial({ color: '#d9a982', roughness: 0.8 });
const coatMat = new THREE.MeshStandardMaterial({ color: '#39404a', roughness: 0.9 });

function canopyGeometry(G, mirror, shaded) {
  const SEG = 12, RING = 20, pos = [], nor = [], uv = [], idx = [], col = [];
  for (let k = 0; k < N; k++) {
    const base = pos.length / 3;
    for (let j = 0; j <= RING; j++) {
      const th = (G.thetaMax * j) / RING, st = Math.sin(th), ct = Math.cos(th);
      for (let i = 0; i <= SEG; i++) {
        const ph = k * W - W / 2 + (W * i) / SEG, cp = Math.cos(ph), sp = Math.sin(ph);
        pos.push(G.Rs * st * cp, G.Rs * ct, G.Rs * st * sp); nor.push(st * cp, ct, st * sp);
        const uu = i / SEG; uv.push((k + (mirror ? 1 - uu : uu)) / N, 1 - j / RING);
        const sh = shaded ? 0.72 + 0.28 * Math.pow(1 - j / RING, 0.7) : 1; col.push(sh, sh, sh);
      }
    }
    for (let j = 0; j < RING; j++) for (let i = 0; i < SEG; i++) {
      const a = base + j * (SEG + 1) + i, b = a + SEG + 1, c = a + 1, d = b + 1;
      idx.push(a, c, b, b, c, d);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  g.setIndex(idx);
  return g;
}

let texIn = null, texOut = null;
function makeTex(canvas) {
  const t = new THREE.CanvasTexture(canvas); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

function disposeGroup(g) {
  g.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material && !o.material.userData.keep) o.material.dispose(); });
  g.clear();
}

let G = geometry();
function rebuildUmbrella() {
  G = geometry();
  disposeGroup(umbrellaRoot);
  if (!texIn) { texIn = makeTex(cvIn); texOut = makeTex(cvOut); }
  const canopy = new THREE.Group();
  canopy.position.set(...G.Cs);
  canopy.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(new THREE.Vector3(...G.e1), new THREE.Vector3(...G.a), new THREE.Vector3(...G.z3)));
  const spin = new THREE.Group(); spin.rotation.y = G.spin; canopy.add(spin);

  const inner = new THREE.Mesh(canopyGeometry(G, false, true), new THREE.MeshBasicMaterial({ map: texIn, vertexColors: true, side: THREE.BackSide }));
  const outer = new THREE.Mesh(canopyGeometry(G, true, false), new THREE.MeshStandardMaterial({ map: texOut, roughness: 0.65, side: THREE.FrontSide }));
  spin.add(inner, outer);

  const metal = new THREE.MeshStandardMaterial({ color: '#2b2f36', metalness: 0.6, roughness: 0.4 });
  for (let k = 0; k < N; k++) {
    const ph = k * W - W / 2, pts = [];
    for (let j = 0; j <= 24; j++) { const th = (G.thetaMax * j) / 24; pts.push(new THREE.Vector3(G.Rs * Math.sin(th) * Math.cos(ph), G.Rs * Math.cos(th), G.Rs * Math.sin(th) * Math.sin(ph))); }
    spin.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, 0.004, 5), metal));
    const tip = new THREE.Mesh(new THREE.SphereGeometry(0.008, 8, 6), metal);
    tip.position.copy(pts[24]); spin.add(tip);
  }
  const ferrule = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.008, 0.07, 8), metal); ferrule.position.set(0, G.Rs + 0.03, 0); spin.add(ferrule);
  umbrellaRoot.add(canopy);

  // shaft + grip
  const A = new THREE.Vector3(...G.apex), av = new THREE.Vector3(...G.a), q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), av);
  const shaftLen = SHAFT_TO_HAND + 0.1;
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.007, 0.007, shaftLen, 8), metal);
  shaft.quaternion.copy(q); shaft.position.copy(A).addScaledVector(av, -shaftLen / 2); umbrellaRoot.add(shaft);
  const grip = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.15, 10), new THREE.MeshStandardMaterial({ color: '#4b2f1c', roughness: 0.6 }));
  grip.quaternion.copy(q); grip.position.copy(A).addScaledVector(av, -(SHAFT_TO_HAND + 0.02)); umbrellaRoot.add(grip);

  // arm from shoulder to the hand on the grip
  const S0 = new THREE.Vector3(0.22, -0.25, 0.08), H = new THREE.Vector3(...G.hand);
  const dir = H.clone().sub(S0), len = dir.length();
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.035, len, 10), coatMat);
  arm.position.copy(S0).addScaledVector(dir, 0.5); arm.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
  const hand = new THREE.Mesh(new THREE.SphereGeometry(0.04, 12, 8), skinMat); hand.position.copy(H);
  umbrellaRoot.add(arm, hand);
  needsRender = true;
}

/* gaze cone drawn in the outside view */
function rebuildField() {
  disposeGroup(fieldRoot);
  const { f, r, u } = gazeBasis(S.yaw * D2R, S.pitch * D2R), R = 1.9, pts = [], spokes = [];
  for (let i = 0; i < 96; i++) {
    const t = (i / 96) * 2 * Math.PI, az = AZ * Math.cos(t), el = (Math.sin(t) >= 0 ? UP : DN) * Math.sin(t);
    const gx = Math.cos(el) * Math.sin(az), gy = Math.sin(el), gz = Math.cos(el) * Math.cos(az);
    const v = new THREE.Vector3((gx * r[0] + gy * u[0] + gz * f[0]) * R, (gx * r[1] + gy * u[1] + gz * f[1]) * R, (gx * r[2] + gy * u[2] + gz * f[2]) * R);
    pts.push(v); if (i % 8 === 0) spokes.push(new THREE.Vector3(0, 0, 0), v);
  }
  fieldRoot.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xffd23f })));
  fieldRoot.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(spokes), new THREE.LineBasicMaterial({ color: 0xffd23f, transparent: true, opacity: 0.3 })));
  fieldRoot.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(f[0] * R, f[1] * R, f[2] * R)]), new THREE.LineBasicMaterial({ color: 0x5cc8ff })));
  needsRender = true;
}

function updateCameras() {
  povCam.fov = S.fov; povCam.rotation.set(S.pitch * D2R, S.yaw * D2R, 0); povCam.position.set(0, 0, 0); povCam.updateProjectionMatrix();
  const c = Math.cos(orbit.el);
  outCam.position.set(orbit.target.x + orbit.dist * c * Math.sin(orbit.az), orbit.target.y + orbit.dist * Math.sin(orbit.el), orbit.target.z + orbit.dist * c * Math.cos(orbit.az));
  outCam.lookAt(orbit.target);
  const pov = S.mode === 'pov';
  person.visible = !pov; fieldRoot.visible = !pov;
  needsRender = true;
}

function resize() {
  const w = viewer.clientWidth, h = viewer.clientHeight;
  if (!renderer || !w || !h) return;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(w, h, false);
  povCam.aspect = outCam.aspect = w / h; povCam.updateProjectionMatrix(); outCam.updateProjectionMatrix();
  needsRender = true; analysisDirty = true;
}

/* ------------------------------------------------------------------ analysis + UI */
const pct = (x) => (x * 100).toFixed(x < 0.1 ? 1 : 0) + '%';
let tracer = null, analysisDirty = true, tableDirty = true, lastRun = 0, tableTimer = 0;

function tableRows() {
  const rows = [['Down at phone (−30°)', -30], ['Straight ahead (0°)', 0], ['Up 30°', 30], ['Up at canopy (60°)', 60]];
  $('gaze-table').innerHTML = rows.map(([label, p]) => {
    const s = statsFor(tracer, S.yaw * D2R, p * D2R);
    const cur = Math.abs(S.pitch - p) < 1.5 ? ' class="cur"' : '';
    return `<tr${cur}><td>${label}</td><td>${pct(s.field)}</td><td>${pct(s.canopy)}</td></tr>`;
  }).join('');
}

function analyse() {
  tracer = makeTracer(G);
  const aspect = viewer.clientWidth / Math.max(1, viewer.clientHeight);
  const s = statsFor(tracer, S.yaw * D2R, S.pitch * D2R, { fov: S.fov, aspect });
  $('h-num').textContent = pct(s.field);
  $('bar-ad').style.width = (s.field * 100) + '%';
  $('bar-can').style.width = ((s.canopy - s.field) * 100) + '%';
  $('r-canopy').textContent = pct(s.canopy);
  $('r-central').textContent = pct(s.central);
  $('r-screen').textContent = pct(s.screen);
  $('badge-num').textContent = pct(s.screen);
  $('r-area').textContent = adAreaM2(G).toFixed(2) + ' m² of ' + (2 * Math.PI * G.Rs * G.Rs * (1 - Math.cos(G.thetaMax))).toFixed(2) + ' m²';
  drawFisheye(tracer);
  latest = s;
  clearTimeout(tableTimer); tableTimer = setTimeout(tableRows, 120);
}
let latest = null;

let dirtyGeo = true, dirtyAds = true;
function frame(now) {
  if (dirtyAds) { paintAtlas(); if (texIn) { texIn.needsUpdate = true; texOut.needsUpdate = true; } dirtyAds = false; analysisDirty = true; needsRender = true; }
  if (dirtyGeo) { rebuildUmbrella(); dirtyGeo = false; analysisDirty = true; }
  if (analysisDirty && now - lastRun > 40) { analysisDirty = false; lastRun = now; analyse(); }
  if (renderer && needsRender) { renderer.render(scene, S.mode === 'pov' ? povCam : outCam); needsRender = false; }
  requestAnimationFrame(frame);
}

/* ------------------------------------------------------------------ inputs */
const sliders = {
  yaw: [1, (v) => v + '°', (v) => { S.yaw = v; gaze(); }], pitch: [1, (v) => v + '°', (v) => { S.pitch = v; gaze(); }], fov: [1, (v) => v + '°', (v) => { S.fov = v; gaze(); }],
  size: [0.01, (v) => Math.round(v * 100) + '%', (v) => { S.size = v; dirtyAds = true; }],
  diam: [0.01, (v) => Math.round(v * 100) + ' cm', (v) => { S.diam = v; dirtyGeo = true; }],
  depth: [0.01, (v) => Math.round(v * 100) + ' cm', (v) => { S.depth = v; dirtyGeo = true; }],
  height: [0.01, (v) => Math.round(v * 100) + ' cm', (v) => { S.height = v; dirtyGeo = true; }],
  tilt: [1, (v) => v + '°', (v) => { S.tilt = v; dirtyGeo = true; }],
  fwd: [0.01, (v) => Math.round(v * 100) + ' cm', (v) => { S.fwd = v; dirtyGeo = true; }],
  side: [0.01, (v) => Math.round(v * 100) + ' cm', (v) => { S.side = v; dirtyGeo = true; }],
  spin: [1, (v) => v + '°', (v) => { S.spin = v; dirtyGeo = true; }],
};

function gaze() { updateCameras(); rebuildField(); analysisDirty = true; }
function syncSlider(id) {
  const [scale, fmt] = sliders[id], el = $(id);
  el.value = Math.round(S[id] / scale); $('o-' + id).textContent = fmt(S[id]);
}
for (const id of Object.keys(sliders)) {
  syncSlider(id);
  $(id).addEventListener('input', (e) => { const v = +e.target.value * sliders[id][0]; sliders[id][2](v); $('o-' + id).textContent = sliders[id][1](v); });
}
for (const id of ['layout', 'panels', 'print']) {
  $(id).value = S[id];
  $(id).addEventListener('change', (e) => { S[id] = e.target.value; dirtyAds = true; });
}
document.querySelectorAll('[data-gaze]').forEach((b) => b.addEventListener('click', () => { S.pitch = +b.dataset.gaze; syncSlider('pitch'); gaze(); }));

function setMode(m) {
  S.mode = m;
  $('mode-pov').setAttribute('aria-pressed', m === 'pov'); $('mode-out').setAttribute('aria-pressed', m === 'out');
  $('hint').textContent = m === 'pov' ? 'Drag to look around like the holder would · scroll to zoom the field of view.'
    : 'Drag to orbit · scroll to zoom. Yellow outline = the holder\'s visual field, blue line = gaze direction.';
  updateCameras();
}
$('mode-pov').addEventListener('click', () => setMode('pov'));
$('mode-out').addEventListener('click', () => setMode('out'));
function setMap(m) { S.map = m; $('map-real').setAttribute('aria-pressed', m === 'real'); $('map-cov').setAttribute('aria-pressed', m === 'cov'); analysisDirty = true; }
$('map-real').addEventListener('click', () => setMap('real'));
$('map-cov').addEventListener('click', () => setMap('cov'));

let drag = null;
viewer.addEventListener('pointerdown', (e) => { if (e.target.closest('.hud')) return; drag = { x: e.clientX, y: e.clientY }; viewer.setPointerCapture(e.pointerId); });
viewer.addEventListener('pointerup', () => { drag = null; });
viewer.addEventListener('pointercancel', () => { drag = null; });
viewer.addEventListener('pointermove', (e) => {
  if (!drag) return;
  const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag = { x: e.clientX, y: e.clientY };
  if (S.mode === 'pov') {
    const k = S.fov / viewer.clientHeight;             // pixels -> degrees, so the scene follows the finger
    S.yaw = clamp(S.yaw - dx * k, -120, 120); S.pitch = clamp(S.pitch + dy * k, -70, 85);
    syncSlider('yaw'); syncSlider('pitch'); gaze();
  } else {
    orbit.az -= dx * 0.008; orbit.el = clamp(orbit.el + dy * 0.006, -0.2, 1.4); updateCameras();
  }
});
viewer.addEventListener('wheel', (e) => {
  e.preventDefault();
  if (S.mode === 'pov') { S.fov = clamp(S.fov + Math.sign(e.deltaY) * 3, 50, 120); syncSlider('fov'); gaze(); }
  else { orbit.dist = clamp(orbit.dist * (1 + Math.sign(e.deltaY) * 0.08), 1.6, 12); updateCameras(); }
}, { passive: false });
addEventListener('keydown', (e) => {
  if (e.target.matches('input,select')) return;
  const step = 3, m = { ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, step], ArrowDown: [0, -step] }[e.key];
  if (!m) return; e.preventDefault();
  S.yaw = clamp(S.yaw + m[0], -120, 120); S.pitch = clamp(S.pitch + m[1], -70, 85); syncSlider('yaw'); syncSlider('pitch'); gaze();
});
new ResizeObserver(resize).observe(viewer);

/* ------------------------------------------------------------------ start */
buildWorld();
paintAtlas();
setMode('pov'); rebuildField(); resize();
requestAnimationFrame(frame);
if (document.fonts) document.fonts.load('800 20px Archivo').then(() => { dirtyAds = true; }).catch(() => {});

// handy for automated checks
window.__sim = { S, orbit, stats: () => latest, setState: (o) => { Object.assign(S, o); dirtyAds = dirtyGeo = true; gaze(); Object.keys(sliders).forEach(syncSlider); } };
