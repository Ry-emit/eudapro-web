/* Comportamientos comunes a todas las páginas: cabecera, menú, formulario.
   Sin dependencias externas. */
(function () {
  'use strict';

  /* ---------- un solo oyente de scroll para toda la página ----------
     Todo lo que reacciona al scroll se calcula junto, una vez por fotograma y
     sin volver a medir el documento: las medidas se guardan y solo se refrescan
     al cambiar el tamaño de la ventana. Medir dentro del scroll (offsetHeight,
     getBoundingClientRect…) es lo que hace que en el móvil vaya a tirones. */
  var cabecera = document.getElementById('cabecera');
  var linea = document.getElementById('linea-progreso');
  var alScroll = [];          // funciones que se ejecutan por fotograma
  var alMedir = [];           // funciones que recalculan medidas
  var pendiente = false;

  function pintar() {
    pendiente = false;
    for (var i = 0; i < alScroll.length; i++) alScroll[i](window.scrollY);
  }
  function pedirPintado() {
    if (!pendiente) { pendiente = true; requestAnimationFrame(pintar); }
  }
  function remedir() {
    for (var i = 0; i < alMedir.length; i++) alMedir[i]();
    pintar();
  }
  addEventListener('scroll', pedirPintado, { passive: true });
  addEventListener('resize', remedir);

  if (cabecera) {
    alScroll.push(function (y) { cabecera.classList.toggle('fija', y > 24); });
  }

  if (linea) {
    var maxDoc = 0;
    alMedir.push(function () { maxDoc = document.documentElement.scrollHeight - innerHeight; });
    alScroll.push(function (y) {
      linea.style.width = (maxDoc > 0 ? Math.min(Math.max(y / maxDoc, 0), 1) * 100 : 0).toFixed(2) + '%';
    });
  }

  /* ---------- menú móvil ---------- */
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var abierto = nav.classList.toggle('abierto');
      btn.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('abierto'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ---------- desplegable de servicios ---------- */
  document.querySelectorAll('.desplegable').forEach(function (d) {
    var b = d.querySelector('.desplegable__btn');
    if (!b) return;
    var fino = matchMedia('(min-width: 941px)');
    var reloj = null;
    function abrir(v) {
      clearTimeout(reloj);
      d.dataset.abierto = v ? 'si' : 'no';
      b.setAttribute('aria-expanded', v ? 'true' : 'false');
    }
    /* al salir no se cierra de golpe: da margen para bajar hasta el panel */
    function cerrarConMargen() {
      clearTimeout(reloj);
      reloj = setTimeout(function () { abrir(false); }, 220);
    }
    b.addEventListener('click', function (e) { e.stopPropagation(); abrir(d.dataset.abierto !== 'si'); });
    d.addEventListener('mouseenter', function () { if (fino.matches) abrir(true); });
    d.addEventListener('mouseleave', function () { if (fino.matches) cerrarConMargen(); });
    d.addEventListener('focusin', function () { if (fino.matches) abrir(true); });
    d.addEventListener('focusout', function (e) { if (fino.matches && !d.contains(e.relatedTarget)) abrir(false); });
    document.addEventListener('click', function (e) { if (!d.contains(e.target)) abrir(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') abrir(false); });
  });

  /* ---------- portada con partículas: texto, riel y avance ----------
     Vive aquí, y no en hero.js, para que el contenido se vea al instante
     aunque Three.js tarde en cargar o el navegador no pueda dibujarlo. */
  var estado = window.EUDAPRO = window.EUDAPRO || { avance: 0 };
  var scrolly = document.querySelector('.scrolly');

  if (scrolly) {
    var escena = document.querySelector('.escena');
    var riel = document.querySelector('.riel');
    var pista = document.querySelector('.pista');
    var pasos = [].slice.call(document.querySelectorAll('.paso'));
    var itemsRiel = [];

    if (riel) {
      pasos.forEach(function (p) {
        var d = document.createElement('div');
        d.innerHTML = '<span>' + (p.dataset.riel || '') + '</span><i></i>';
        riel.appendChild(d);
        itemsRiel.push(d);
      });
    }

    var ioPaneles = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle('dentro', e.isIntersecting); });
    }, { rootMargin: matchMedia('(max-width: 940px)').matches ? '-40% 0px -40% 0px' : '-30% 0px -30% 0px' });
    document.querySelectorAll('.paso__panel').forEach(function (p) { ioPaneles.observe(p); });

    /* medidas de la zona de partículas: se toman una vez y se refrescan solo
       al redimensionar */
    var arriba = 0, recorrido = 1, activoPrevio = -1, pistaPrevia = -1, rielPrevio = -1;
    alMedir.push(function () {
      arriba = scrolly.getBoundingClientRect().top + window.scrollY;
      recorrido = scrolly.offsetHeight - (escena ? escena.offsetHeight : innerHeight);
    });
    alScroll.push(function (y) {
      estado.avance = recorrido > 0 ? Math.min(Math.max((y - arriba) / recorrido, 0), 1) : 0;

      var activo = Math.round(estado.avance * (pasos.length - 1));
      if (activo !== activoPrevio) {
        for (var k = 0; k < itemsRiel.length; k++) itemsRiel[k].classList.toggle('on', k === activo);
        activoPrevio = activo;
      }
      var visible = estado.avance > 0.02 ? 0 : 1;
      if (visible !== pistaPrevia) {
        if (pista) pista.style.opacity = visible;
        pistaPrevia = visible;
      }
      /* el riel se evalúa por separado: si dependiera del cambio de la pista,
         al bajar de la zona de partículas se quedaba encima del resto de la web */
      var conRiel = estado.avance >= 0.999 ? 0 : 1;
      if (riel && conRiel !== rielPrevio) {
        riel.style.opacity = conRiel;
        rielPrevio = conRiel;
      }
    });
  }

  remedir();

  /* ---------- año en el pie ---------- */
  document.querySelectorAll('[data-anyo]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- aparición suave de bloques ---------- */
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'none'; obs.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('[data-aparece]').forEach(function (el, i) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(22px)';
      el.style.transition = 'opacity .7s cubic-bezier(.16,.84,.3,1) ' + (i % 4) * 0.06 + 's, transform .7s cubic-bezier(.16,.84,.3,1) ' + (i % 4) * 0.06 + 's';
      obs.observe(el);
    });
  }

  /* ---------- formulario de contacto ----------
     Mientras no haya backend, el envío se prepara como correo con los datos ya
     escritos. En cuanto exista endpoint, basta con cambiar ENVIO a la URL y
     quitar el bloque del mailto (ver README). */
  var ENVIO = null; // p. ej. 'https://formularios.eudapro.com/contacto'
  var DESTINO = 'info@eudapro.es';

  /* La web está en español y en inglés: los mensajes salen del idioma de la
     página, para que no se mezclen los dos. */
  var EN = (document.documentElement.lang || 'es').toLowerCase().indexOf('en') === 0;
  var T = EN ? {
    falta: 'To handle your request we need you to accept the processing of your data.',
    enviando: 'Sending…',
    enviado: 'Received. We will reply within 24 working hours.',
    error: 'We could not send it. Call us on 900 929 806 or write to ',
    nombre: 'Name: ', correo: 'E-mail: ', telefono: 'Phone: ', empresa: 'Company / association: ',
    consentimiento: '— Consent to processing: yes',
    comerciales: '— Marketing communications: ', si: 'yes', no: 'no',
    asunto: 'Information request from the website',
    mailto: 'Your e-mail program will open with the message already written. If it does not, write to us at '
  } : {
    falta: 'Para poder atender tu solicitud necesitamos que aceptes el tratamiento de tus datos.',
    enviando: 'Enviando…',
    enviado: 'Recibido. Te respondemos en menos de 24 h laborables.',
    error: 'No hemos podido enviarlo. Llámanos al 900 929 806 o escribe a ',
    nombre: 'Nombre: ', correo: 'Correo: ', telefono: 'Teléfono: ', empresa: 'Empresa / colectivo: ',
    consentimiento: '— Consentimiento de tratamiento: sí',
    comerciales: '— Comunicaciones comerciales: ', si: 'sí', no: 'no',
    asunto: 'Solicitud de información desde la web',
    mailto: 'Se abrirá tu programa de correo con el mensaje ya escrito. Si no ocurre, escríbenos a '
  };

  document.querySelectorAll('form[data-contacto]').forEach(function (form) {
    var estado = form.querySelector('.form__estado');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var tratamiento = form.querySelector('[name="consent-tratamiento"]');
      if (tratamiento && !tratamiento.checked) {
        if (estado) estado.textContent = T.falta;
        tratamiento.focus();
        return;
      }
      /* Sin servidor que reciba el formulario, o si ese envío falla, se
         prepara el correo con los datos ya escritos: así la consulta no se
         pierde nunca. */
      function porCorreo() {
        var cuerpo = [
          T.nombre + (d.get('nombre') || ''),
          T.correo + (d.get('correo') || ''),
          T.telefono + (d.get('telefono') || ''),
          T.empresa + (d.get('empresa') || ''),
          '',
          (d.get('mensaje') || ''),
          '',
          T.consentimiento,
          T.comerciales + (d.get('consent-comercial') ? T.si : T.no)
        ].join('\n');
        var asunto = d.get('asunto') || T.asunto;
        window.location.href = 'mailto:' + DESTINO +
          '?subject=' + encodeURIComponent(asunto) +
          '&body=' + encodeURIComponent(cuerpo);
        if (estado) estado.textContent = T.mailto + DESTINO + '.';
      }

      if (ENVIO) {
        if (estado) estado.textContent = T.enviando;
        fetch(ENVIO, { method: 'POST', body: d })
          .then(function (r) {
            if (!r.ok) throw new Error(r.status);
            form.reset();
            if (estado) estado.textContent = T.enviado;
          })
          .catch(porCorreo);
        return;
      }
      porCorreo();
    });
  });
})();
