import * as THREE from 'three';

/* Biblioteca de formas del sistema visual: cada figura se construye con
   geometría de Three.js y luego se muestrea a puntos para la nube de partículas.
   Origen: proyecto de diseño "Hero de partículas". */

export function materials() {
  return {
    violet: new THREE.MeshStandardMaterial({ name: 'azul', color: 0x007db3, roughness: 0.34, metalness: 0.3 }),
    graphite: new THREE.MeshStandardMaterial({ name: 'graphite', color: 0x2a2a33, roughness: 0.55, metalness: 0.28 }),
    pearl: new THREE.MeshStandardMaterial({ name: 'pearl', color: 0xffffff, roughness: 0.22, metalness: 0.12 }),
    amber: new THREE.MeshStandardMaterial({ name: 'azul_claro', color: 0x4498e7, roughness: 0.38, metalness: 0.2 })
  };
}

const mesh = (geo, mat, name) => { const m = new THREE.Mesh(geo, mat); m.name = name; return m; };

function tube(a, b, radius, mat, name) {
  const dir = new THREE.Vector3().subVectors(b, a);
  const len = dir.length();
  const g = new THREE.CylinderGeometry(radius, radius, len, 12, 1);
  const m = mesh(g, mat, name);
  m.position.copy(a).addScaledVector(dir, 0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize());
  return m;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---------- formas ---------- */

function shield(M) {
  const g = new THREE.Group(); g.name = 'shield';
  const s = new THREE.Shape();
  s.moveTo(0, 1.3);
  s.bezierCurveTo(0.6, 1.22, 0.98, 0.95, 1.02, 0.6);
  s.lineTo(0.92, -0.28);
  s.bezierCurveTo(0.86, -0.85, 0.5, -1.15, 0, -1.35);
  s.bezierCurveTo(-0.5, -1.15, -0.86, -0.85, -0.92, -0.28);
  s.lineTo(-1.02, 0.6);
  s.bezierCurveTo(-0.98, 0.95, -0.6, 1.22, 0, 1.3);
  const body = new THREE.ExtrudeGeometry(s, { depth: 0.3, bevelEnabled: true, bevelSize: 0.07, bevelThickness: 0.07, bevelSegments: 4, curveSegments: 28 });
  body.translate(0, 0, -0.15);
  g.add(mesh(body, M.violet, 'shield_body'));

  const inner = new THREE.Shape();
  inner.moveTo(0, 0.82);
  inner.bezierCurveTo(0.36, 0.78, 0.6, 0.6, 0.62, 0.38);
  inner.lineTo(0.56, -0.18);
  inner.bezierCurveTo(0.52, -0.55, 0.3, -0.74, 0, -0.86);
  inner.bezierCurveTo(-0.3, -0.74, -0.52, -0.55, -0.56, -0.18);
  inner.lineTo(-0.62, 0.38);
  inner.bezierCurveTo(-0.6, 0.6, -0.36, 0.78, 0, 0.82);
  const crest = new THREE.ExtrudeGeometry(inner, { depth: 0.1, bevelEnabled: true, bevelSize: 0.03, bevelThickness: 0.03, bevelSegments: 3, curveSegments: 24 });
  crest.translate(0, 0, 0.151);
  g.add(mesh(crest, M.pearl, 'shield_crest'));
  return g;
}

function lock(M) {
  const g = new THREE.Group(); g.name = 'lock';
  const body = new THREE.BoxGeometry(1.5, 1.16, 0.66, 4, 4, 4);
  g.add(mesh(body, M.violet, 'lock_body'));
  const bevel = new THREE.BoxGeometry(1.56, 0.1, 0.72);
  bevel.translate(0, 0.53, 0);
  g.add(mesh(bevel, M.pearl, 'lock_lip'));
  const shackle = new THREE.TorusGeometry(0.46, 0.12, 20, 44, Math.PI);
  shackle.translate(0, 0.58, 0);
  g.add(mesh(shackle, M.graphite, 'lock_shackle'));
  for (const x of [-0.46, 0.46]) {
    const leg = new THREE.CylinderGeometry(0.12, 0.12, 0.3, 18);
    leg.translate(x, 0.44, 0);
    g.add(mesh(leg, M.graphite, 'lock_shackle_leg'));
  }
  const key = new THREE.CylinderGeometry(0.19, 0.19, 0.12, 28);
  key.rotateX(Math.PI / 2); key.translate(0, 0.06, 0.32);
  g.add(mesh(key, M.graphite, 'lock_keyhole'));
  const slot = new THREE.BoxGeometry(0.14, 0.34, 0.12);
  slot.translate(0, -0.16, 0.32);
  g.add(mesh(slot, M.graphite, 'lock_keyslot'));
  return g;
}

function globe(M) {
  const g = new THREE.Group(); g.name = 'globe';
  g.add(mesh(new THREE.SphereGeometry(1.12, 56, 36), M.violet, 'globe_core'));
  const ring = (rx, ry, rz, r) => {
    const t = new THREE.TorusGeometry(r, 0.022, 10, 96);
    const m = mesh(t, M.pearl, 'globe_meridian');
    m.rotation.set(rx, ry, rz);
    return m;
  };
  g.add(ring(Math.PI / 2, 0, 0, 1.19));
  for (let i = 0; i < 5; i++) g.add(ring(0, (i / 5) * Math.PI, 0, 1.19));
  for (const y of [-0.62, 0.62]) {
    const lat = new THREE.TorusGeometry(Math.sqrt(Math.max(1.19 * 1.19 - y * y, 0.05)), 0.02, 10, 80);
    lat.rotateX(Math.PI / 2); lat.translate(0, y, 0);
    g.add(mesh(lat, M.pearl, 'globe_parallel'));
  }
  return g;
}

function fingerprint(M) {
  const g = new THREE.Group(); g.name = 'fingerprint';
  const arcs = [
    [0.22, 0.4, 5.4], [0.4, 2.1, 4.4], [0.58, 3.5, 4.8], [0.76, 5.4, 4.2],
    [0.94, 0.9, 4.6], [1.12, 2.6, 4.0], [1.3, 4.4, 4.4]
  ];
  arcs.forEach(([r, start, sweep], i) => {
    const t = new THREE.TorusGeometry(r, 0.055, 12, Math.max(24, Math.round(sweep * 18)), sweep);
    const m = mesh(t, i % 2 ? M.pearl : M.violet, 'ridge_' + i);
    m.rotation.z = start;
    m.position.z = (i % 2 ? 0.02 : -0.02);
    g.add(m);
  });
  const core = new THREE.TorusGeometry(0.08, 0.05, 10, 26, Math.PI * 1.4);
  g.add(mesh(core, M.amber, 'ridge_core'));
  g.scale.set(1, 1.22, 0.34);
  return g;
}

function network(M) {
  const g = new THREE.Group(); g.name = 'network';
  const n = 30, pts = [];
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2;
    const r = Math.sqrt(Math.max(1 - y * y, 0));
    const th = i * 2.3999632;
    pts.push(new THREE.Vector3(Math.cos(th) * r, y, Math.sin(th) * r).multiplyScalar(1.22));
  }
  pts.forEach((p, i) => {
    const s = mesh(new THREE.SphereGeometry(i % 5 === 0 ? 0.1 : 0.068, 20, 14), i % 5 === 0 ? M.amber : M.pearl, 'node_' + i);
    s.position.copy(p);
    g.add(s);
  });
  let k = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    if (pts[i].distanceTo(pts[j]) < 0.78) g.add(tube(pts[i], pts[j], 0.016, M.violet, 'link_' + k++));
  }
  return g;
}

function brain(M) {
  const g = new THREE.Group(); g.name = 'brain';
  const lobes = [
    [0.0, 0.42, 0.1, 0.72], [0.46, 0.5, -0.1, 0.5], [-0.46, 0.5, -0.1, 0.5],
    [0.62, 0.06, 0.3, 0.46], [-0.62, 0.06, 0.3, 0.46],
    [0.5, -0.2, -0.36, 0.42], [-0.5, -0.2, -0.36, 0.42],
    [0.0, 0.2, 0.62, 0.44], [0.0, 0.1, -0.66, 0.42],
    [0.3, -0.48, 0.24, 0.36], [-0.3, -0.48, 0.24, 0.36],
    [0.0, -0.6, -0.3, 0.34]
  ];
  lobes.forEach(([x, y, z, r], i) => {
    const s = mesh(new THREE.SphereGeometry(r, 28, 20), M.violet, 'lobe_' + i);
    s.position.set(x, y, z);
    s.scale.set(1, 0.9, 1.05);
    g.add(s);
  });
  const fissure = new THREE.BoxGeometry(0.05, 0.7, 1.1);
  fissure.translate(0, 0.3, 0);
  g.add(mesh(fissure, M.graphite, 'brain_fissure'));
  const stem = new THREE.CylinderGeometry(0.14, 0.2, 0.5, 20);
  stem.translate(0, -0.9, -0.1);
  g.add(mesh(stem, M.pearl, 'brain_stem'));
  g.scale.setScalar(1.05);
  return g;
}

function eye(M) {
  const g = new THREE.Group(); g.name = 'eye';
  g.add(mesh(new THREE.SphereGeometry(0.95, 48, 32), M.pearl, 'sclera'));
  const iris = new THREE.SphereGeometry(0.965, 48, 24, 0, Math.PI * 2, 0, 0.46);
  const im = mesh(iris, M.violet, 'iris');
  im.rotation.x = Math.PI / 2;
  im.position.z = 0.0;
  g.add(im);
  const pupil = new THREE.SphereGeometry(0.985, 40, 20, 0, Math.PI * 2, 0, 0.2);
  const pm = mesh(pupil, M.graphite, 'pupil');
  pm.rotation.x = Math.PI / 2;
  g.add(pm);
  const rim = new THREE.TorusGeometry(0.44, 0.035, 14, 90);
  rim.translate(0, 0, 0.86);
  g.add(mesh(rim, M.amber, 'iris_rim'));
  const halo = new THREE.TorusGeometry(1.14, 0.05, 16, 120);
  const hm = mesh(halo, M.violet, 'eye_ring');
  hm.scale.set(1, 0.58, 1);
  g.add(hm);
  return g;
}

function dataCube(M) {
  const g = new THREE.Group(); g.name = 'data_cube';
  const a = 1.02, t = 0.07;
  let e = 0;
  for (const ax of ['x', 'y', 'z']) for (const s1 of [-1, 1]) for (const s2 of [-1, 1]) {
    const geo = ax === 'x' ? new THREE.BoxGeometry(a * 2, t, t)
      : ax === 'y' ? new THREE.BoxGeometry(t, a * 2, t)
        : new THREE.BoxGeometry(t, t, a * 2);
    const m = mesh(geo, M.violet, 'edge_' + e++);
    if (ax === 'x') m.position.set(0, a * s1, a * s2);
    if (ax === 'y') m.position.set(a * s1, 0, a * s2);
    if (ax === 'z') m.position.set(a * s1, a * s2, 0);
    g.add(m);
  }
  for (const x of [-a, a]) for (const y of [-a, a]) for (const z of [-a, a]) {
    const c = mesh(new THREE.BoxGeometry(0.16, 0.16, 0.16), M.pearl, 'corner');
    c.position.set(x, y, z);
    g.add(c);
  }
  const rnd = mulberry32(7);
  for (let i = 0; i < 14; i++) {
    const s = 0.1 + rnd() * 0.16;
    const b = mesh(new THREE.BoxGeometry(s, s, s), i % 4 === 0 ? M.amber : M.graphite, 'datum_' + i);
    b.position.set((rnd() - 0.5) * 1.4, (rnd() - 0.5) * 1.4, (rnd() - 0.5) * 1.4);
    b.rotation.set(rnd() * 3, rnd() * 3, rnd() * 3);
    g.add(b);
  }
  return g;
}

function key(M) {
  const g = new THREE.Group(); g.name = 'key';
  const bow = new THREE.TorusGeometry(0.42, 0.12, 18, 56);
  bow.translate(0, 0.86, 0);
  g.add(mesh(bow, M.violet, 'key_bow'));
  const shaft = new THREE.CylinderGeometry(0.095, 0.095, 1.5, 24);
  shaft.translate(0, -0.32, 0);
  g.add(mesh(shaft, M.pearl, 'key_shaft'));
  const teeth = [[0.24, -0.72, 0.3], [0.2, -0.9, 0.22], [0.26, -1.03, 0.34]];
  teeth.forEach(([w, y, h], i) => {
    const b = new THREE.BoxGeometry(w, h, 0.11);
    b.translate(0.1 + w / 2, y, 0);
    g.add(mesh(b, M.violet, 'tooth_' + i));
  });
  const collar = new THREE.CylinderGeometry(0.15, 0.15, 0.12, 24);
  collar.translate(0, 0.34, 0);
  g.add(mesh(collar, M.amber, 'key_collar'));
  return g;
}

/* La «O» del logotipo de Eudapro (septiembre de 2026): un aro en media luna,
   más grueso abajo a la izquierda, con un filo fino por fuera arriba a la
   derecha, y dentro un escudo con la cerradura. La cerradura es un hueco de
   verdad en la placa del escudo: en la nube se lee como espacio vacío.
   Los nombres de las mallas empiezan por la pieza (aro_, filo_, marco_,
   placa_) para poder colorear cada parte por separado. */
function logo(M) {
  const g = new THREE.Group(); g.name = 'logo';

  const aro = new THREE.Shape();
  aro.absarc(0, 0, 1.32, 0, Math.PI * 2, false);
  const hueco = new THREE.Path();
  hueco.absarc(0.13, 0.11, 1.05, 0, Math.PI * 2, true);
  aro.holes.push(hueco);
  const aroGeo = new THREE.ExtrudeGeometry(aro, { depth: 0.26, bevelEnabled: true, bevelSize: 0.04, bevelThickness: 0.05, bevelSegments: 3, curveSegments: 96 });
  aroGeo.translate(0, 0, -0.13);
  g.add(mesh(aroGeo, M.violet, 'aro'));

  /* el filo claro que abraza el aro por arriba a la derecha */
  const filo = new THREE.TorusGeometry(1.43, 0.034, 10, 120, 2.35);
  filo.rotateZ(-0.95);
  g.add(mesh(filo, M.amber, 'filo'));

  const contorno = (k) => {
    const s = new THREE.Shape();
    s.moveTo(0, 0.70 * k);
    s.quadraticCurveTo(0.30 * k, 0.55 * k, 0.62 * k, 0.56 * k);
    s.lineTo(0.60 * k, 0.05 * k);
    s.bezierCurveTo(0.58 * k, -0.40 * k, 0.30 * k, -0.66 * k, 0, -0.84 * k);
    s.bezierCurveTo(-0.30 * k, -0.66 * k, -0.58 * k, -0.40 * k, -0.60 * k, 0.05 * k);
    s.lineTo(-0.62 * k, 0.56 * k);
    s.quadraticCurveTo(-0.30 * k, 0.55 * k, 0, 0.70 * k);
    return s;
  };
  /* el escudo va centrado en el hueco, no en el aro, y ocupa lo mismo que en
     el logotipo: algo más de la mitad del ancho de la O */
  const DX = 0.07, DY = 0.08, ESC = 1.12;

  const marco = contorno(1);
  const dentro = new THREE.Path(contorno(0.84).getPoints(48));
  marco.holes.push(dentro);
  const marcoGeo = new THREE.ExtrudeGeometry(marco, { depth: 0.22, bevelEnabled: true, bevelSize: 0.025, bevelThickness: 0.03, bevelSegments: 2, curveSegments: 32 });
  marcoGeo.scale(ESC, ESC, 1); marcoGeo.translate(DX, DY, -0.11);
  g.add(mesh(marcoGeo, M.violet, 'marco'));

  const placa = contorno(0.85);
  const r = 0.155, cy = 0.13, ancho = 0.06;
  const corte = Math.sqrt(r * r - ancho * ancho);
  const cerradura = new THREE.Path();
  cerradura.moveTo(-0.13, -0.38);
  cerradura.lineTo(-ancho, cy - corte);
  cerradura.absarc(0, cy, r, Math.atan2(-corte, -ancho) + Math.PI * 2, Math.atan2(-corte, ancho), true);
  cerradura.lineTo(0.13, -0.38);
  cerradura.lineTo(-0.13, -0.38);
  placa.holes.push(cerradura);
  const placaGeo = new THREE.ExtrudeGeometry(placa, { depth: 0.1, bevelEnabled: false, curveSegments: 40 });
  placaGeo.scale(ESC, ESC, 1); placaGeo.translate(DX, DY, -0.05);
  g.add(mesh(placaGeo, M.pearl, 'placa'));

  /* y la cerradura, maciza y por delante de la placa, como en el logotipo */
  const llave = new THREE.ExtrudeGeometry(new THREE.Shape(cerradura.getPoints(40)), { depth: 0.07, bevelEnabled: false });
  llave.scale(ESC, ESC, 1); llave.translate(DX, DY, 0.05);
  g.add(mesh(llave, M.graphite, 'cerradura'));

  return g;
}

export const SHAPES = [
  { id: 'shield', label: 'Escudo', build: shield },
  { id: 'lock', label: 'Candado', build: lock },
  { id: 'globe', label: 'Globo', build: globe },
  { id: 'fingerprint', label: 'Huella', build: fingerprint },
  { id: 'network', label: 'Red', build: network },
  { id: 'brain', label: 'Cerebro', build: brain },
  { id: 'eye', label: 'Ojo', build: eye },
  { id: 'data_cube', label: 'Cubo de datos', build: dataCube },
  { id: 'key', label: 'Llave', build: key },
  { id: 'logo', label: 'Logotipo', build: logo }
];

export function buildShape(id, M = materials()) {
  const def = SHAPES.find(s => s.id === id) || SHAPES[0];
  return def.build(M);
}

/* Muestreo uniforme sobre la superficie de todas las mallas del grupo,
   normalizado a una esfera de radio `fit` y centrado: así todas las formas
   se transforman unas en otras de manera comparable. */
export function sampleGroup(group, count, seed = 1, fit = 1.35) {
  return sampleGroupTagged(group, count, seed, fit).pos;
}

/* Igual que sampleGroup, pero además dice de qué malla sale cada punto
   (`tag` = índice en `names`), para poder colorear por piezas. */
export function sampleGroupTagged(group, count, seed = 1, fit = 1.35) {
  group.updateMatrixWorld(true);
  const tri = [], cum = [], triMesh = [], names = [];
  let total = 0;
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  const ab = new THREE.Vector3(), ac = new THREE.Vector3(), cr = new THREE.Vector3();
  group.traverse(o => {
    if (!o.isMesh) return;
    names.push(o.name);
    const meshIdx = names.length - 1;
    const pos = o.geometry.attributes.position, idx = o.geometry.index, m = o.matrixWorld;
    const n = idx ? idx.count : pos.count;
    for (let i = 0; i + 2 < n; i += 3) {
      const i0 = idx ? idx.getX(i) : i, i1 = idx ? idx.getX(i + 1) : i + 1, i2 = idx ? idx.getX(i + 2) : i + 2;
      a.fromBufferAttribute(pos, i0).applyMatrix4(m);
      b.fromBufferAttribute(pos, i1).applyMatrix4(m);
      c.fromBufferAttribute(pos, i2).applyMatrix4(m);
      ab.subVectors(b, a); ac.subVectors(c, a);
      const area = cr.crossVectors(ab, ac).length() * 0.5;
      if (area < 1e-9) continue;
      total += area;
      tri.push(a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z);
      cum.push(total);
      triMesh.push(meshIdx);
    }
  });
  const rnd = mulberry32(seed);
  const out = new Float32Array(count * 3);
  const tag = new Uint8Array(count);
  let minX = Infinity, minY = Infinity, minZ = Infinity, maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
  for (let i = 0; i < count; i++) {
    const r = rnd() * total;
    let lo = 0, hi = cum.length - 1;
    while (lo < hi) { const mid = (lo + hi) >> 1; if (cum[mid] < r) lo = mid + 1; else hi = mid; }
    const o = lo * 9;
    let u = rnd(), v = rnd();
    if (u + v > 1) { u = 1 - u; v = 1 - v; }
    const w = 1 - u - v;
    const x = tri[o] * w + tri[o + 3] * u + tri[o + 6] * v;
    const y = tri[o + 1] * w + tri[o + 4] * u + tri[o + 7] * v;
    const z = tri[o + 2] * w + tri[o + 5] * u + tri[o + 8] * v;
    out[i * 3] = x; out[i * 3 + 1] = y; out[i * 3 + 2] = z;
    tag[i] = triMesh[lo];
    if (x < minX) minX = x; if (x > maxX) maxX = x;
    if (y < minY) minY = y; if (y > maxY) maxY = y;
    if (z < minZ) minZ = z; if (z > maxZ) maxZ = z;
  }
  const cx = (minX + maxX) / 2, cy = (minY + maxY) / 2, cz = (minZ + maxZ) / 2;
  const span = Math.max(maxX - minX, maxY - minY, maxZ - minZ) || 1;
  const k = (fit * 2) / span;
  for (let i = 0; i < count; i++) {
    out[i * 3] = (out[i * 3] - cx) * k;
    out[i * 3 + 1] = (out[i * 3 + 1] - cy) * k;
    out[i * 3 + 2] = (out[i * 3 + 2] - cz) * k;
  }
  return { pos: out, tag, names };
}
