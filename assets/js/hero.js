/* =========================================================================
   Nube de partículas de la portada.
   Lee los pasos del propio HTML (data-forma / data-riel), muestrea cada figura
   y las va transformando una en otra según el avance del scroll dentro de la
   zona .scrolly. Si no hay WebGL, o el usuario pide menos movimiento, se queda
   el respaldo estático y no se carga nada más.
   ========================================================================= */
import * as THREE from 'three';
import { buildShape, materials, sampleGroup } from './cyber-shapes.js';

const escena = document.querySelector('.escena');
const canvas = document.getElementById('nube');
const glow = document.querySelector('.escena__glow');
const pasos = [...document.querySelectorAll('.paso')];

const MENOS_MOVIMIENTO = matchMedia('(prefers-reduced-motion: reduce)').matches;
const MOVIL = innerWidth < 940 || matchMedia('(pointer: coarse)').matches;

/* El texto, el riel y el progreso los lleva ui.js, que no depende de Three.js:
   así el contenido está visible aunque la nube tarde en cargar o falle. */
const estado = window.EUDAPRO || { avance: 0 };

/* ---------- ¿podemos dibujar? ---------- */
function hayWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch (e) { return false; }
}

if (!escena || !canvas || MENOS_MOVIMIENTO || !hayWebGL()) {
  if (escena) escena.classList.add('sin-webgl');
} else {
  arrancar().catch(() => escena.classList.add('sin-webgl'));
}

/* ---------- escena ---------- */
async function arrancar() {
  /* En móvil todo baja: menos partículas, sin líneas de conexión y sin brillo.
     El cuello de botella del scroll en un teléfono no es la GPU, es todo lo que
     se recalcula por fotograma. */
  const COUNT = MOVIL ? 12000 : 42000;
  const LINEAS = !MOVIL;
  const NODOS = LINEAS ? 180 : 0;

  const formas = pasos.map(p => p.dataset.forma).filter(Boolean);
  if (formas.length < 2) { escena.classList.add('sin-webgl'); return; }

  const M = materials();
  const objetivos = [], objetivosNodo = [];
  for (let i = 0; i < formas.length; i++) {
    const g = buildShape(formas[i], M);
    objetivos.push(sampleGroup(g, COUNT, 100 + i * 7));
    if (LINEAS) objetivosNodo.push(sampleGroup(g, NODOS, 900 + i * 13));
    await new Promise(r => requestAnimationFrame(r));
  }

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  const dpr = Math.min(devicePixelRatio, 2);
  renderer.setPixelRatio(dpr);
  renderer.setSize(escena.clientWidth, escena.clientHeight, false);
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(42, escena.clientWidth / escena.clientHeight, 0.1, 100);
  const DIST = MOVIL ? 9.0 : 6.3;
  camera.position.set(0, 0, DIST);

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(objetivos[0].slice(), 3));
  geo.setAttribute('aPosB', new THREE.BufferAttribute(objetivos[1].slice(), 3));
  const rnd = new Float32Array(COUNT * 3);
  for (let i = 0; i < COUNT * 3; i++) rnd[i] = Math.random();
  geo.setAttribute('aRnd', new THREE.BufferAttribute(rnd, 3));

  const uniforms = {
    uMix: { value: 0 }, uTime: { value: 0 },
    uSize: { value: (MOVIL ? 7.8 : 5.5) * dpr },
    uOpacidad: { value: MOVIL ? 1.3 : 1 },
    /* el desvanecido por profundidad va referido a la distancia de la cámara:
       si no, al alejarla en móvil los puntos salían al 40 % de opacidad */
    uProfA: { value: DIST + 1.9 },
    uProfB: { value: DIST - 2.1 },
    uRayO: { value: new THREE.Vector3(0, 0, 5) }, uRayD: { value: new THREE.Vector3(0, 0, -1) },
    uMouseOn: { value: 0 }
  };

  const mat = new THREE.ShaderMaterial({
    uniforms, transparent: true, depthWrite: false, blending: THREE.NormalBlending,
    vertexShader: `
      attribute vec3 aPosB; attribute vec3 aRnd;
      uniform float uMix, uTime, uSize, uMouseOn, uProfA, uProfB;
      uniform vec3 uRayO, uRayD;
      varying float vRnd; varying float vDisp; varying float vDepth;
      void main() {
        vec3 p = mix(position, aPosB, uMix);
        float burst = sin(uMix * 3.14159265);
        vec3 dir = normalize(aRnd - 0.5 + 0.0001);
        p += dir * burst * (0.34 + aRnd.x * 0.9);
        p += dir * sin(uTime * 0.7 + aRnd.y * 12.0) * 0.018;
        vec3 d = p - uRayO;
        vec3 perp = d - dot(d, uRayD) * uRayD;
        float dist = length(perp);
        float f = clamp(1.0 - dist / 1.05, 0.0, 1.0) * uMouseOn;
        p += normalize(perp + 0.0001) * f * f * 0.85;
        vDisp = max(burst, f);
        vRnd = aRnd.z;
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_PointSize = uSize * (1.0 / -mv.z) * (0.6 + aRnd.x * 0.7);
        vDepth = smoothstep(uProfA, uProfB, -mv.z);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform float uOpacidad;
      varying float vRnd; varying float vDisp; varying float vDepth;
      void main() {
        vec2 c = gl_PointCoord - 0.5;
        float a = smoothstep(0.5, 0.2, length(c));
        if (a < 0.02) discard;
        vec3 azul   = vec3(0.0, 0.49, 0.70);     /* #007DB3 — azul del logotipo */
        vec3 blanco = vec3(1.0, 1.0, 1.0);
        vec3 claro  = vec3(0.27, 0.60, 0.91);    /* #4498E7 — azul claro suyo */
        vec3 col = mix(azul, blanco, smoothstep(0.55, 1.0, vRnd));
        col = mix(col, claro, step(0.986, vRnd));
        col += vDisp * 0.18;
        gl_FragColor = vec4(col, min(a * (0.32 + vRnd * 0.45) * (0.4 + vDepth * 0.8) * uOpacidad, 1.0));
      }`
  });

  const nube = new THREE.Group();
  scene.add(nube);
  nube.add(new THREE.Points(geo, mat));

  /* líneas de conexión sobre un conjunto reducido de nodos (solo escritorio:
     es un bucle de 180×180 por fotograma y en móvil no compensa) */
  const MAXPAR = 900;
  let lineGeo = null, lineas = null, posNodo = null;
  if (LINEAS) {
    lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXPAR * 6), 3));
    lineas = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({
      color: 0x007db3, transparent: true, opacity: 0.18, blending: THREE.AdditiveBlending, depthWrite: false
    }));
    nube.add(lineas);
    posNodo = new Float32Array(NODOS * 3);
  }

  /* Una pose por figura: dónde se coloca, cuánto gira y su tamaño.
     Las posiciones se mantienen dentro de la banda central de la pantalla y
     alternan lado (la figura siempre cruza el medio, nunca se va al borde).
     En pantalla la cámara desplaza todo +0.9, así que x = −1.75 queda a la
     izquierda del centro y x = 0.30 a la derecha. */
  const POSES = [
    { x: 0.30, y: 0.00, z: 0.0, rx: -0.06, ry: 0.10, rz: 0.02, s: 1.06 },
    { x: -1.75, y: -0.26, z: 0.6, rx: 0.08, ry: -0.22, rz: -0.03, s: 0.98 },
    { x: 0.35, y: 0.26, z: -0.6, rx: -0.05, ry: 0.26, rz: 0.04, s: 1.16 },
    { x: -1.70, y: 0.30, z: 0.8, rx: 0.12, ry: -0.14, rz: -0.02, s: 1.02 },
    { x: 0.30, y: -0.30, z: -0.9, rx: -0.12, ry: 0.30, rz: 0.03, s: 1.22 },
    { x: -1.78, y: 0.16, z: 0.4, rx: 0.10, ry: -0.28, rz: -0.04, s: 1.08 },
    { x: 0.34, y: -0.20, z: -0.7, rx: -0.08, ry: 0.20, rz: 0.02, s: 1.12 },
    { x: -1.66, y: 0.32, z: 0.7, rx: 0.14, ry: -0.24, rz: -0.03, s: 1.00 },
    { x: 0.28, y: -0.08, z: -0.4, rx: -0.10, ry: 0.16, rz: 0.02, s: 1.18 }
  ];
  /* En móvil la figura se queda casi centrada y sube a la mitad de arriba de la
     pantalla, para que el texto (que va abajo) se lea sin nada por encima. */
  const AMP = MOVIL ? 0.16 : 1;
  const DESVIO_Y = MOVIL ? 1.25 : 0;
  const lerp = (a, b, k) => a + (b - a) * k;
  const invMat = new THREE.Matrix4();

  let idxA = 0;
  function fijarPar(i) {
    idxA = i;
    geo.attributes.position.array.set(objetivos[i]);
    geo.attributes.aPosB.array.set(objetivos[Math.min(i + 1, objetivos.length - 1)]);
    geo.attributes.position.needsUpdate = true;
    geo.attributes.aPosB.needsUpdate = true;
  }

  /* puntero → rayo en el mundo (el ratón repele las partículas) */
  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2(0, 0);
  let raton = 0;
  if (!MOVIL) {
    addEventListener('pointermove', e => {
      const r = escena.getBoundingClientRect();
      ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      raton = 1;
    }, { passive: true });
    addEventListener('pointerleave', () => { raton = 0; });
  }

  /* En el móvil, al esconderse la barra del navegador cambia el alto y se
     dispara un resize: redimensionar el lienzo ahí provoca un tirón en pleno
     scroll. Solo se hace caso si cambia el ancho (giro de pantalla). */
  let anchoPrevio = escena.clientWidth;
  addEventListener('resize', () => {
    if (MOVIL && escena.clientWidth === anchoPrevio) return;
    anchoPrevio = escena.clientWidth;
    renderer.setSize(escena.clientWidth, escena.clientHeight, false);
    camera.aspect = escena.clientWidth / escena.clientHeight;
    camera.updateProjectionMatrix();
  });

  let framesLineas = 99;
  function rehacerLineas() {
    if (!LINEAS) return;
    const A = objetivosNodo[idxA], B = objetivosNodo[Math.min(idxA + 1, objetivosNodo.length - 1)];
    for (let i = 0; i < NODOS * 3; i++) posNodo[i] = A[i] + (B[i] - A[i]) * uniforms.uMix.value;
    const arr = lineGeo.attributes.position.array;
    let n = 0;
    const umbral = 0.62;
    for (let i = 0; i < NODOS && n < MAXPAR; i++) {
      for (let j = i + 1; j < NODOS && n < MAXPAR; j++) {
        const dx = posNodo[i * 3] - posNodo[j * 3];
        const dy = posNodo[i * 3 + 1] - posNodo[j * 3 + 1];
        const dz = posNodo[i * 3 + 2] - posNodo[j * 3 + 2];
        if (dx * dx + dy * dy + dz * dz < umbral * umbral) {
          arr[n * 6] = posNodo[i * 3]; arr[n * 6 + 1] = posNodo[i * 3 + 1]; arr[n * 6 + 2] = posNodo[i * 3 + 2];
          arr[n * 6 + 3] = posNodo[j * 3]; arr[n * 6 + 4] = posNodo[j * 3 + 1]; arr[n * 6 + 5] = posNodo[j * 3 + 2];
          n++;
        }
      }
    }
    for (let k = n; k < MAXPAR; k++) for (let q = 0; q < 6; q++) arr[k * 6 + q] = 0;
    lineGeo.attributes.position.needsUpdate = true;
    lineGeo.setDrawRange(0, n * 2);
  }

  /* solo dibujamos mientras la escena está en pantalla */
  let visible = true, corriendo = false;
  new IntersectionObserver(es => {
    visible = es[0].isIntersecting;
    if (visible && !corriendo) { corriendo = true; requestAnimationFrame(tick); }
  }, { rootMargin: '120px' }).observe(escena);

  const reloj = new THREE.Clock();
  const proy = new THREE.Vector3();
  let mostrado = 0, ratonSuave = 0;
  /* En móvil no hay movimiento de fondo: la figura solo se mueve con el dedo.
     Si nada ha cambiado, no se dibuja. Eso deja la CPU libre para el scroll. */
  let ultimoDibujo = NaN;

  function tick() {
    if (!visible) { corriendo = false; return; }
    const t = reloj.getElapsedTime();
    /* Cada tramo de texto tiene su figura: cuando el panel k está centrado en
       pantalla, la figura k ya está hecha y quieta a su lado. Por eso el índice
       se calcula contra el número de tramos y con medio tramo de desfase, no
       repartiendo el scroll a partes iguales. */
    const N = objetivos.length;
    const objetivo = Math.min(Math.max(estado.avance * N - 0.5, 0), N - 1);
    mostrado += (objetivo - mostrado) * 0.032;   /* inercia lenta: pesa */

    const i = Math.min(Math.floor(mostrado), objetivos.length - 2);
    if (i !== idxA) fijarPar(Math.max(i, 0));
    const local = Math.min(Math.max(mostrado - i, 0), 1);

    /* Dos tiempos distintos, y esta es la clave del movimiento:

       — MEZCLA (el cambio de forma) ocurre pronto y rápido: empieza nada más
         arrancar el tramo y está terminada al 30 % del recorrido, cuando la
         figura todavía está saliendo de un lado. Así llega al centro de la
         pantalla ya acabada.
       — RECORRIDO (el viaje de un lado a otro) es lento y continuo durante
         todo el tramo. El 70 % restante se ve la forma entera cruzando el
         medio. La figura no gira: se desplaza. */
    const e = Math.min(Math.max((local - 0.02) / 0.28, 0), 1);
    const mezcla = e * e * e * (e * (e * 6 - 15) + 10);
    const estallido = Math.sin(Math.PI * mezcla);
    const kPos = local * local * local * (local * (local * 6 - 15) + 10);

    ratonSuave += (raton - ratonSuave) * 0.06;
    uniforms.uMix.value = mezcla;
    uniforms.uTime.value = t;
    uniforms.uMouseOn.value = ratonSuave;

    const A = POSES[idxA % POSES.length];
    const B = POSES[Math.min(idxA + 1, POSES.length - 1)];
    const k = kPos;

    /* La figura tiene peso: no da vueltas. Se desplaza de un lado a otro, se
       hunde un poco al cruzar (como algo pesado que se transporta) y solo
       cabecea muy despacio. Nada de giro continuo.
       En móvil el cabeceo se apaga: sin él no hace falta repintar cuando el
       dedo está quieto. */
    const balanceo = MOVIL ? 0 : Math.sin(t * 0.16) * 0.035;
    const respira = MOVIL ? 0 : Math.sin(t * 0.22) * 0.05;
    const peso = Math.sin(Math.PI * k);            /* el hundimiento del cruce */

    nube.position.set(
      lerp(A.x, B.x, k) * AMP,
      lerp(A.y, B.y, k) + respira - peso * 0.12 + DESVIO_Y,
      lerp(A.z, B.z, k) - peso * 0.25
    );
    nube.rotation.set(
      lerp(A.rx, B.rx, k) + balanceo * 0.5,
      lerp(A.ry, B.ry, k),
      lerp(A.rz || 0, B.rz || 0, k) + balanceo
    );
    /* al cruzar pesa más: se encoge un pelo en vez de crecer */
    nube.scale.setScalar(lerp(A.s, B.s, k) * (1 - peso * 0.04));
    if (lineas) lineas.material.opacity = 0.14 + estallido * 0.22;

    /* cámara fija: mirar siempre de frente es lo que hace que la figura
       parezca un objeto y no un planeta girando */
    camera.position.set(0, 0, DIST);
    camera.lookAt(0, 0, 0);
    camera.translateX(MOVIL ? 0 : -0.9);

    if (!MOVIL) {
      ray.setFromCamera(ndc, camera);
      nube.updateMatrixWorld();
      invMat.copy(nube.matrixWorld).invert();
      uniforms.uRayO.value.copy(ray.ray.origin).applyMatrix4(invMat);
      uniforms.uRayD.value.copy(ray.ray.direction).transformDirection(invMat).normalize();
    }

    if (glow && !MOVIL) {
      proy.set(0, 0, 0).applyMatrix4(nube.matrixWorld).project(camera);
      const w = escena.clientWidth, h = escena.clientHeight;
      glow.style.transform = 'translate(' + ((proy.x * 0.5 + 0.5) * w) + 'px,' +
        ((-proy.y * 0.5 + 0.5) * h) + 'px) translate(-50%,-50%) scale(' + (1 + estallido * 0.45) + ')';
      glow.style.opacity = String(0.3 + estallido * 0.4);
    }

    if (LINEAS && ++framesLineas > 5) { rehacerLineas(); framesLineas = 0; }

    /* en móvil: si el dedo no ha movido nada, no se repinta */
    if (!MOVIL || !(Math.abs(mostrado - ultimoDibujo) < 0.0004)) {
      ultimoDibujo = mostrado;
      renderer.render(scene, camera);
    }
    requestAnimationFrame(tick);
  }

  fijarPar(0);
  corriendo = true;
  requestAnimationFrame(tick);
  canvas.style.transition = 'opacity .8s ease';
  canvas.style.opacity = '1';
}
