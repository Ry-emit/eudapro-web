/* =========================================================================
   Faldón informativo y gestor de cookies de Eudapro.

   Sigue el documento «Faldón informativo de cookies» que facilitó Eudapro:

   — Primera capa: texto, enlace a la Política de Cookies y tres botones,
     Aceptar / Rechazar / Ajustes, con el mismo peso visual (el botón Aceptar
     no va resaltado con otro color ni otro formato).
   — Segunda capa: gestor de cookies por categorías, accesible después desde
     «Ajustes», desde el pie y desde la propia Política de Cookies.
   — Las cookies de análisis solo se instalan cuando la persona las acepta.
     Ni la inactividad ni la navegación cuentan como consentimiento.

   La decisión se guarda en el propio navegador (localStorage), no en una
   cookie, para no escribir nada antes de tener permiso.
   ========================================================================= */
(function () {
  'use strict';

  /* Identificador de medición de Google Analytics 4 (formato G-XXXXXXXXXX).
     Mientras esté vacío no se carga Analytics ni se instala ninguna cookie:
     en cuanto Eudapro lo facilite, basta con escribirlo aquí. */
  var GA_ID = '';

  var CLAVE = 'eudapro:cookies';
  var VERSION = 1;

  function leer() {
    try {
      var d = JSON.parse(localStorage.getItem(CLAVE));
      return d && d.version === VERSION ? d : null;
    } catch (e) { return null; }
  }

  function guardar(analitica) {
    try {
      localStorage.setItem(CLAVE, JSON.stringify({
        version: VERSION, analitica: !!analitica, fecha: new Date().toISOString()
      }));
    } catch (e) { /* navegación privada: se preguntará de nuevo */ }
  }

  /* ---------- Google Analytics, solo con consentimiento ---------- */
  var analyticsCargado = false;
  function cargarAnalytics() {
    if (analyticsCargado || !GA_ID) return;
    analyticsCargado = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID, { anonymize_ip: true });
  }

  /* Si ya las había rechazado (o las rechaza ahora), se borran las cookies de
     Analytics que pudieran quedar de una visita anterior. */
  function borrarAnalytics() {
    var dominios = [location.hostname, '.' + location.hostname];
    var punto = location.hostname.split('.');
    if (punto.length > 2) dominios.push('.' + punto.slice(-2).join('.'));
    document.cookie.split(';').forEach(function (par) {
      var nombre = par.split('=')[0].trim();
      if (!/^_ga/.test(nombre) && !/^_gid$/.test(nombre) && !/^_gat/.test(nombre)) return;
      dominios.forEach(function (d) {
        document.cookie = nombre + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/; domain=' + d;
      });
      document.cookie = nombre + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';
    });
  }

  function aplicar(analitica) {
    if (analitica) cargarAnalytics(); else borrarAnalytics();
  }

  /* ---------- piezas de la interfaz ---------- */
  var faldon = null, panel = null, focoPrevio = null;

  function crearFaldon() {
    faldon = document.createElement('div');
    faldon.className = 'cookies';
    faldon.setAttribute('role', 'region');
    faldon.setAttribute('aria-label', 'Información sobre cookies');
    faldon.innerHTML =
      '<div class="cookies__caja">' +
        '<p class="cookies__txt">Utilizamos cookies propias y de terceros con fines analíticos, para saber cómo se usa la web. ' +
        'Puede aceptarlas, rechazarlas o elegir cuáles acepta. Más información en nuestra ' +
        '<a href="politica-de-cookies.html">Política de Cookies</a>.</p>' +
        '<div class="cookies__acciones">' +
          '<button type="button" class="cookies__btn" data-cookies="aceptar">Aceptar</button>' +
          '<button type="button" class="cookies__btn" data-cookies="rechazar">Rechazar</button>' +
          '<button type="button" class="cookies__btn" data-cookies="ajustes">Ajustes</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(faldon);
  }

  function cerrarFaldon() {
    if (faldon) { faldon.remove(); faldon = null; }
  }

  function crearPanel(analiticaActual) {
    focoPrevio = document.activeElement;
    panel = document.createElement('div');
    panel.className = 'cookies-panel';
    panel.innerHTML =
      '<div class="cookies-panel__fondo" data-cookies="cerrar"></div>' +
      '<div class="cookies-panel__caja" role="dialog" aria-modal="true" aria-labelledby="cookies-titulo">' +
        '<h2 id="cookies-titulo">Configuración de cookies</h2>' +
        '<p>Elija qué cookies acepta en esta web. Puede cambiarlo cuando quiera desde el pie de página o desde la Política de Cookies.</p>' +
        '<div class="cookies-grupo">' +
          '<div class="cookies-grupo__cab"><b>Cookies técnicas</b><span class="cookies-fijo">Siempre activas</span></div>' +
          '<p>Son las necesarias para que la web funcione y se recuerde su decisión sobre las cookies. No se pueden desactivar.</p>' +
        '</div>' +
        '<div class="cookies-grupo">' +
          '<div class="cookies-grupo__cab"><b>Cookies de análisis</b>' +
            '<label class="cookies-interruptor"><input type="checkbox" id="cookies-analitica"' + (analiticaActual ? ' checked' : '') + '>' +
            '<span class="cookies-interruptor__pista" aria-hidden="true"></span><span class="cookies-interruptor__txt">Activar</span></label>' +
          '</div>' +
          '<p>Google Analytics. Nos dicen cuántas personas visitan la web y qué páginas leen, de forma estadística. Si las rechaza, la web funciona igual.</p>' +
        '</div>' +
        '<div class="cookies-panel__acciones">' +
          '<button type="button" class="cookies__btn" data-cookies="guardar">Guardar mi elección</button>' +
          '<button type="button" class="cookies__btn" data-cookies="aceptar">Aceptar todas</button>' +
          '<button type="button" class="cookies__btn" data-cookies="rechazar">Rechazar todas</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(panel);
    var primero = panel.querySelector('#cookies-analitica');
    if (primero) primero.focus();
    document.addEventListener('keydown', alPulsarTecla);
  }

  function cerrarPanel() {
    if (!panel) return;
    panel.remove(); panel = null;
    document.removeEventListener('keydown', alPulsarTecla);
    if (focoPrevio && focoPrevio.focus) focoPrevio.focus();
  }

  function alPulsarTecla(e) {
    if (e.key === 'Escape') cerrarPanel();
  }

  function decidir(analitica) {
    guardar(analitica);
    aplicar(analitica);
    cerrarPanel();
    cerrarFaldon();
  }

  /* ---------- arranque ---------- */
  function abrirAjustes() {
    var d = leer();
    crearPanel(d ? d.analitica : false);
  }

  document.addEventListener('click', function (e) {
    var abrir = e.target.closest('[data-abrir-cookies]');
    if (abrir) { e.preventDefault(); abrirAjustes(); return; }
    var b = e.target.closest('[data-cookies]');
    if (!b) return;
    var accion = b.getAttribute('data-cookies');
    if (accion === 'aceptar') decidir(true);
    else if (accion === 'rechazar') decidir(false);
    else if (accion === 'ajustes') abrirAjustes();
    else if (accion === 'cerrar') cerrarPanel();
    else if (accion === 'guardar') {
      var casilla = document.getElementById('cookies-analitica');
      decidir(!!(casilla && casilla.checked));
    }
  });

  var decision = leer();
  if (decision) {
    aplicar(decision.analitica);
  } else {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', crearFaldon);
    } else {
      crearFaldon();
    }
  }

  window.EUDAPRO_COOKIES = { abrir: abrirAjustes, estado: leer };
})();
