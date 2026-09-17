/* =========================================================================
   Página de prueba: la «O» del logotipo como figura de partículas.
   Usa la misma biblioteca de formas que la portada (cyber-shapes.js) y el
   mismo tipo de nube, pero coloreada por piezas con los azules del logotipo.
   ========================================================================= */
import * as THREE from 'three';
import { buildShape, coloresLogo, materials, sampleGroup, sampleGroupTagged } from './cyber-shapes.js';

const escenario = document.querySelector('.escenario');
const brillo = document.querySelector('.brillo');
const canvas = document.getElementById('nube');
const btnTransformar = document.getElementById('transformar');
const btnRearmar = document.getElementById('rearmar');

const MENOS_MOVIMIENTO = matchMedia('(prefers-reduced-motion: reduce)').matches;
const MOVIL = innerWidth < 820 || matchMedia('(pointer: coarse)').matches;

function hayWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}

if (!canvas || !hayWebGL()) {
  document.body.classList.add('sin-webgl');
} else {
  arrancar().catch(() => document.body.classList.add('sin-webgl'));
}

async function arrancar() {
  const COUNT = MOVIL ? 16000 : 44000;
  const NODOS = MOVIL ? 0 : 170;

  const M = materials();
  const logo = sampleGroupTagged(buildShape('logo', M), COUNT, 311);
  /* la figura siguiente de la portada: el candado de «Qué incluye» */
  const candado = sampleGroup(buildShape('lock', M), COUNT, 107);
  const nodosLogo = NODOS ? sampleGroup(buildShape('logo', M), NODOS, 907) : null;
  const nodosCandado = NODOS ? sampleGroup(buildShape('lock', M), NODOS, 913) : null;

  /* punto de partida: una nube suelta alrededor, para verla formarse */
  const suelta = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT; i++) {
    const u = Math.random() * 2 - 1, th = Math.random() * Math.PI * 2;
    const r = 1.9 + Math.random() * 1.3, s = Math.sqrt(1 - u * u);
    suelta[i * 3] = Math.cos(th) * s * r;
    suelta[i * 3 + 1] = u * r;
    suelta[i * 3 + 2] = Math.sin(th) * s * r * 0.6;
  }

  /* color por pieza: la misma paleta que usa la portada */
  const tono = coloresLogo(logo);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  const dpr = Math.min(devicePixelRatio, 2);
  renderer.setPixelRatio(dpr);
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  let DIST = 6.4;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(suelta.slice(), 3));
  geo.setAttribute('aPosB', new THREE.BufferAttribute(logo.pos.slice(), 3));
  const rnd = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT * 3; i++) rnd[i] = Math.random();
  geo.setAttribute('aRnd', new THREE.BufferAttribute(rnd, 3));
  geo.setAttribute('aTono', new THREE.BufferAttribute(tono, 4));

  const uniforms = {
    uMix: { value: 0 }, uTime: { value: 0 }, uEstallido: { value: 1 },
    uSize: { value: (MOVIL ? 10 : 8.4) * dpr },
    uProfA: { value: DIST + 1.9 }, uProfB: { value: DIST - 2.1 },
    uRayO: { value: new THREE.Vector3(0, 0, 5) }, uRayD: { value: new THREE.Vector3(0, 0, -1) },
    uMouseOn: { value: 0 }
  };

  const mat = new THREE.ShaderMaterial({
    uniforms, transparent: true, depthWrite: false, blending: THREE.NormalBlending,
    vertexShader: `
      attribute vec3 aPosB; attribute vec3 aRnd; attribute vec4 aTono;
      uniform float uMix, uTime, uSize, uMouseOn, uProfA, uProfB, uEstallido;
      uniform vec3 uRayO, uRayD;
      varying float vRnd; varying float vDepth; varying vec4 vTono;
      void main() {
        vec3 p = mix(position, aPosB, uMix);
        float burst = sin(uMix * 3.14159265) * uEstallido;
        vec3 dir = normalize(aRnd - 0.5 + 0.0001);
        p += dir * burst * (0.3 + aRnd.x * 0.8);
        p += dir * sin(uTime * 0.7 + aRnd.y * 12.0) * 0.014;
        vec3 d = p - uRayO;
        vec3 perp = d - dot(d, uRayD) * uRayD;
        float f = clamp(1.0 - length(perp) / 0.6, 0.0, 1.0) * uMouseOn;
        p += normalize(perp + 0.0001) * f * f * 0.45;
        vRnd = aRnd.z;
        vTono = aTono;
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_PointSize = uSize * (1.0 / -mv.z) * (0.6 + aRnd.x * 0.7);
        vDepth = smoothstep(uProfA, uProfB, -mv.z);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      varying float vRnd; varying float vDepth; varying vec4 vTono;
      void main() {
        vec2 c = gl_PointCoord - 0.5;
        float a = smoothstep(0.5, 0.2, length(c));
        if (a < 0.02) discard;
        vec3 col = vTono.rgb * (0.9 + vRnd * 0.18);
        gl_FragColor = vec4(col, min(a * (0.55 + vRnd * 0.45) * (0.55 + vDepth * 0.6) * vTono.a * 1.35, 1.0));
      }`
  });

  const nube = new THREE.Group();
  scene.add(nube);
  nube.add(new THREE.Points(geo, mat));

  /* líneas entre nodos cercanos, como en la portada (solo escritorio) */
  const MAXPAR = 800;
  let lineGeo = null, lineas = null;
  const posNodo = NODOS ? new Float32Array(NODOS * 3) : null;
  if (NODOS) {
    lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXPAR * 6), 3));
    lineas = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({ color: 0x007db3, transparent: true, opacity: 0.08, depthWrite: false }));
    nube.add(lineas);
  }
  let nodosA = nodosLogo, nodosB = nodosLogo;
  function rehacerLineas() {
    if (!NODOS) return;
    const k = uniforms.uMix.value;
    for (let i = 0; i < NODOS * 3; i++) posNodo[i] = nodosA[i] + (nodosB[i] - nodosA[i]) * k;
    const arr = lineGeo.attributes.position.array;
    let n = 0;
    for (let i = 0; i < NODOS && n < MAXPAR; i++) {
      for (let j = i + 1; j < NODOS && n < MAXPAR; j++) {
        const dx = posNodo[i * 3] - posNodo[j * 3], dy = posNodo[i * 3 + 1] - posNodo[j * 3 + 1], dz = posNodo[i * 3 + 2] - posNodo[j * 3 + 2];
        if (dx * dx + dy * dy + dz * dz < 0.2) {
          arr.set([posNodo[i * 3], posNodo[i * 3 + 1], posNodo[i * 3 + 2], posNodo[j * 3], posNodo[j * 3 + 1], posNodo[j * 3 + 2]], n * 6);
          n++;
        }
      }
    }
    lineGeo.attributes.position.needsUpdate = true;
    lineGeo.setDrawRange(0, n * 2);
  }

  /* ---------- transiciones ---------- */
  const suave = (e) => e * e * e * (e * (e * 6 - 15) + 10);
  let tramos = [];              /* cola de { desde, hacia, nodos, dur, pausa } */
  let tramo = null, inicioTramo = 0;

  function fijar(desde, hacia) {
    geo.attributes.position.array.set(desde);
    geo.attributes.aPosB.array.set(hacia);
    geo.attributes.position.needsUpdate = true;
    geo.attributes.aPosB.needsUpdate = true;
  }
  function lanzar(lista) {
    tramos = lista.slice();
    tramo = null;
  }
  function formar() {
    if (MENOS_MOVIMIENTO) { fijar(logo.pos, logo.pos); uniforms.uMix.value = 1; nodosA = nodosB = nodosLogo; return; }
    lanzar([{ desde: suelta, hacia: logo.pos, nA: nodosLogo, nB: nodosLogo, dur: 2.8, estallido: 0.35 }]);
  }
  function transformar() {
    const ida = { desde: logo.pos, hacia: candado, nA: nodosLogo, nB: nodosCandado, dur: MENOS_MOVIMIENTO ? 0.01 : 1.7, estallido: 1, pausa: 1.1 };
    const vuelta = { desde: candado, hacia: logo.pos, nA: nodosCandado, nB: nodosLogo, dur: MENOS_MOVIMIENTO ? 0.01 : 1.7, estallido: 1 };
    lanzar([ida, vuelta]);
  }
  btnTransformar?.addEventListener('click', transformar);
  btnRearmar?.addEventListener('click', formar);

  /* ---------- tamaño ---------- */
  function medir() {
    const w = escenario.clientWidth, h = escenario.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    /* que la figura entera quepa también en vertical */
    DIST = Math.max(6.4, 1.35 * 1.45 / (Math.tan(THREE.MathUtils.degToRad(21)) * camera.aspect));
    uniforms.uProfA.value = DIST + 1.9;
    uniforms.uProfB.value = DIST - 2.1;
    camera.updateProjectionMatrix();
  }
  medir();
  addEventListener('resize', medir);

  /* ---------- ratón: aparta partículas y, arrastrando, gira la figura ---------- */
  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  let raton = 0, arrastrando = false, px = 0, py = 0;
  const giro = { x: 0, y: 0 }, giroObj = { x: 0, y: 0 };
  canvas.addEventListener('pointermove', e => {
    const r = canvas.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    if (e.pointerType === 'mouse') raton = 1;
    if (arrastrando) {
      giroObj.y += (e.clientX - px) * 0.007;
      giroObj.x = Math.max(-0.7, Math.min(0.7, giroObj.x + (e.clientY - py) * 0.005));
      px = e.clientX; py = e.clientY;
    }
  });
  canvas.addEventListener('pointerdown', e => { arrastrando = true; px = e.clientX; py = e.clientY; canvas.setPointerCapture(e.pointerId); canvas.classList.add('agarrando'); });
  const soltar = () => { arrastrando = false; canvas.classList.remove('agarrando'); };
  canvas.addEventListener('pointerup', soltar);
  canvas.addEventListener('pointercancel', soltar);
  canvas.addEventListener('pointerleave', () => { raton = 0; });

  const inicio = performance.now();
  const proy = new THREE.Vector3();
  const invMat = new THREE.Matrix4();
  let ratonSuave = 0, cuentaLineas = 99;

  function tick() {
    const t = (performance.now() - inicio) / 1000;

    /* avanzar la cola de transiciones */
    if (!tramo && tramos.length) {
      tramo = tramos.shift();
      inicioTramo = t;
      fijar(tramo.desde, tramo.hacia);
      nodosA = tramo.nA; nodosB = tramo.nB;
      uniforms.uEstallido.value = tramo.estallido;
    }
    if (tramo) {
      const e = Math.min((t - inicioTramo) / tramo.dur, 1);
      uniforms.uMix.value = suave(e);
      if (t - inicioTramo >= tramo.dur + (tramo.pausa || 0)) tramo = null;
    }

    /* sin arrastrar, vuelve despacio a mirar de frente */
    if (!arrastrando) { giroObj.x *= 0.965; giroObj.y *= 0.965; }
    giro.x += (giroObj.x - giro.x) * 0.12;
    giro.y += (giroObj.y - giro.y) * 0.12;
    const vaiven = MENOS_MOVIMIENTO ? 0 : Math.sin(t * 0.32) * 0.3;
    const cabeceo = MENOS_MOVIMIENTO ? 0 : Math.sin(t * 0.21) * 0.06;
    nube.rotation.set(cabeceo + giro.x, vaiven + giro.y, 0);
    nube.position.y = MENOS_MOVIMIENTO ? 0 : Math.sin(t * 0.4) * 0.04;

    ratonSuave += (raton - ratonSuave) * 0.08;
    uniforms.uMouseOn.value = ratonSuave;
    uniforms.uTime.value = t;

    camera.position.set(0, 0, DIST);
    camera.lookAt(0, 0, 0);
    /* en escritorio el texto va a la izquierda: la figura se corre a la derecha */
    if (!MOVIL && camera.aspect > 1.2) camera.translateX(-1.15);
    camera.updateMatrixWorld(true);
    ray.setFromCamera(ndc, camera);
    nube.updateMatrixWorld();
    invMat.copy(nube.matrixWorld).invert();
    uniforms.uRayO.value.copy(ray.ray.origin).applyMatrix4(invMat);
    uniforms.uRayD.value.copy(ray.ray.direction).transformDirection(invMat).normalize();

    if (NODOS && ++cuentaLineas > 4) { rehacerLineas(); cuentaLineas = 0; }
    /* mientras se forma desde la nube suelta, las líneas aparecen con ella */
    /* las líneas, discretas: que no tapen la cerradura */
    if (lineas) lineas.material.opacity = 0.08 * (tramo && tramo.desde === suelta ? uniforms.uMix.value : 1);

    /* el halo de fondo sigue a la figura */
    if (brillo) {
      proy.set(0, 0, 0).applyMatrix4(nube.matrixWorld).project(camera);
      brillo.style.transform = 'translate(' + ((proy.x * 0.5 + 0.5) * escenario.clientWidth) + 'px,' +
        ((-proy.y * 0.5 + 0.5) * escenario.clientHeight) + 'px) translate(-50%,-50%)';
    }

    renderer.render(scene, camera);
    requestAnimationFrame(tick);
  }

  formar();
  document.body.classList.add('lista');
  requestAnimationFrame(tick);
}
