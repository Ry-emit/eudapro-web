#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de las páginas interiores de eudapro-site.

La cabecera y el pie son idénticos en todas las páginas, así que se escriben
una sola vez aquí y el script vuelca los .html ya montados. Los archivos que
produce son HTML plano y estático: se pueden editar a mano sin problema, pero
si vuelves a ejecutar este script se sobrescriben.

    python3 _generar.py

index.html y proteccion-de-datos.html están escritas a mano y NO se tocan.
"""

import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Estructura común
# --------------------------------------------------------------------------

# Logotipo de Eudapro (septiembre de 2026). En la cabecera solo va la franja
# EUDAPRO con el escudo, porque el lema no se leería a ese tamaño; en el pie va
# el logotipo completo.
MARCA_CABECERA = '<img class="marca__logo" src="assets/img/marca/eudapro-marca.webp" alt="Eudapro" width="523" height="96">'
MARCA_PIE = '<img class="marca__logo marca__logo--completo" src="assets/img/marca/eudapro-logo.webp" alt="Eudapro, European Data Protect: protección de datos" width="637" height="196">'

SERVICIOS = [
    ('proteccion-de-datos.html', 'Protección de datos', 'RGPD y LOPDGDD · DPD incluido'),
    ('formacion.html', 'Formación bonificada', 'Cursos financiados con FUNDAE'),
    ('ciberseguridad.html', 'Ciberseguridad', 'Normativa NIS y sanciones'),
    ('videovigilancia.html', 'Videovigilancia', 'Cámaras conformes a la AEPD'),
    ('blanqueo-de-capitales.html', 'Prevención del blanqueo', 'LPBC · Ley 10/2010'),
]

SUELTAS = [('colectivos.html', 'colectivos'), ('recursos.html', 'recursos'), ('conocenos.html', 'conócenos')]


def cabecera(archivo):
    servicios = '\n'.join(
        '        <a href="%s"%s>%s <small>%s</small></a>' %
        (h, ' aria-current="page"' if h == archivo else '', t, s)
        for h, t, s in SERVICIOS)
    sueltas = '\n'.join(
        '    <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == archivo else '', t)
        for h, t in SUELTAS)
    return '''<a class="saltar" href="#principal">Saltar al contenido</a>
<div class="progreso" aria-hidden="true"><i id="linea-progreso"></i></div>
<div class="scanline" aria-hidden="true"></div>

<header class="cabecera" id="cabecera">
  <a class="marca" href="index.html" aria-label="Eudapro, inicio">
    %s
  </a>
  <nav class="nav" id="nav" aria-label="Navegación principal">
    <a href="index.html">inicio</a>
    <div class="desplegable" data-abierto="no">
      <button class="desplegable__btn" type="button" aria-expanded="false">servicios</button>
      <div class="desplegable__panel">
%s
      </div>
    </div>
%s
  </nav>
  <a class="cabecera__cta" href="contacto.html">Solicitar auditoría</a>
  <button class="menu-btn" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span></button>
</header>''' % (MARCA_CABECERA, servicios, sueltas)


PIE = '''<footer class="pie">
  <div class="wrap">
    <div class="pie__grid">
      <div>
        <a class="marca pie__marca" href="index.html" aria-label="Eudapro, inicio">
    %s
        </a>
        <p class="pie__nota">EUDAPRO, S.L. es la marca actual de All in Solutions for Business, S.L. Consultoría de protección de datos para pymes desde Barcelona y Sant Fruitós de Bages.</p>
      </div>
      <div>
        <h4>Servicios</h4>
        <ul>
          <li><a href="proteccion-de-datos.html">Protección de datos</a></li>
          <li><a href="formacion.html">Formación bonificada</a></li>
          <li><a href="ciberseguridad.html">Ciberseguridad</a></li>
          <li><a href="videovigilancia.html">Videovigilancia</a></li>
          <li><a href="blanqueo-de-capitales.html">Prevención del blanqueo</a></li>
        </ul>
      </div>
      <div>
        <h4>Empresa</h4>
        <ul>
          <li><a href="conocenos.html">Conócenos</a></li>
          <li><a href="colectivos.html">Colectivos con convenio</a></li>
          <li><a href="recursos.html">Recursos y descargas</a></li>
          <li><a href="contacto.html">Contacto</a></li>
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <address>
          <a href="tel:+34900929806">900 929 806</a><br>
          <a href="mailto:info@allins4b.com">info@allins4b.com</a><br><br>
          Oficina de atención<br>
          C/ Irlanda, 7 — 08030 Barcelona<br><br>
          Domicilio social<br>
          Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages
        </address>
      </div>
    </div>
    <div class="pie__legal">
      <span>© <span data-anyo>2026</span> EUDAPRO, S.L. — CIF B75390377</span>
      <span>
        <a href="aviso-legal.html">Aviso legal</a> ·
        <a href="politica-de-privacidad.html">Privacidad</a> ·
        <a href="politica-de-cookies.html">Cookies</a> ·
        <a href="politica-redes-sociales.html">Redes sociales</a>
      </span>
      <span>Sin cookies de terceros. Fuentes servidas desde este dominio.</span>
    </div>
  </div>
</footer>''' % MARCA_PIE


def pagina(archivo, titulo, descripcion, cuerpo):
    html = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="assets/css/eudapro.css">
</head>
<body>

%s

<main id="principal">
%s
</main>

%s

<script src="assets/js/ui.js"></script>
</body>
</html>
''' % (titulo, descripcion, cabecera(archivo), cuerpo, PIE)
    with open(os.path.join(RAIZ, archivo), 'w', encoding='utf-8') as f:
        f.write(html)
    print('  escrito  %s' % archivo)


def portada(migas, kicker, h1, lede, icono='', acciones=True):
    botones = ''
    if acciones:
        botones = '''
          <div class="paso__cta mt-m">
            <a class="btn btn--pri" href="contacto.html">Solicitar auditoría</a>
            <a class="btn btn--sec btn--tel" href="tel:+34900929806">900 929 806</a>
          </div>'''
    return '''  <section class="portada">
    <div class="wrap">
      <div class="portada__grid">
        <div class="portada__txt">
          <p class="migas">%s</p>
          <span class="kicker">%s</span>
          <h1>%s</h1>
          <p class="lede">%s</p>%s
        </div>
        %s
      </div>
    </div>
  </section>
''' % (migas, kicker, h1, lede, botones, icono)


CTA_FINAL = '''  <section class="bloque">
    <div class="wrap">
      <div class="cta-banda" data-aparece>
        <div>
          <span class="kicker kicker--amber">Auditoría inicial</span>
          <h2>%s</h2>
          <p>%s</p>
        </div>
        <div class="cta-banda__acciones">
          <a class="btn btn--pri" href="contacto.html">Solicitar auditoría</a>
          <a class="btn btn--sec btn--tel" href="tel:+34900929806">900 929 806</a>
        </div>
      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------------------
# Iconos decorativos de portada
# --------------------------------------------------------------------------

ICO_CIBER = '''<svg class="portada__icono" viewBox="0 0 120 140" fill="none" aria-hidden="true">
          <circle cx="60" cy="70" r="46" stroke="#007db3" stroke-width="2" fill="rgba(0,125,179,.08)"/>
          <circle cx="60" cy="70" r="30" stroke="rgba(255,255,255,.45)" stroke-width="1.4"/>
          <circle cx="60" cy="70" r="7" fill="#4498e7"/>
          <path d="M60 24v-14M60 130v-14M14 70H0M120 70h-14M27 37 17 27M93 103l10 10M93 37l10-10M27 103 17 113" stroke="#007db3" stroke-width="2" stroke-linecap="round"/>
        </svg>'''

ICO_OJO = '''<svg class="portada__icono" viewBox="0 0 140 120" fill="none" aria-hidden="true">
          <path d="M6 60s26-38 64-38 64 38 64 38-26 38-64 38S6 60 6 60z" stroke="#007db3" stroke-width="2" fill="rgba(0,125,179,.08)"/>
          <circle cx="70" cy="60" r="22" fill="rgba(255,255,255,.18)" stroke="rgba(255,255,255,.5)" stroke-width="1.4"/>
          <circle cx="70" cy="60" r="10" fill="#007db3"/>
          <circle cx="76" cy="53" r="3.4" fill="#4498e7"/>
        </svg>'''

ICO_RED = '''<svg class="portada__icono" viewBox="0 0 130 130" fill="none" aria-hidden="true">
          <path d="M65 22 24 48v34l41 26 41-26V48L65 22z" stroke="rgba(255,255,255,.35)" stroke-width="1.4"/>
          <path d="M65 22v86M24 48l82 34M106 48 24 82" stroke="#007db3" stroke-width="1.2" opacity=".7"/>
          <circle cx="65" cy="22" r="7" fill="#4498e7"/>
          <circle cx="24" cy="48" r="6" fill="#007db3"/>
          <circle cx="106" cy="48" r="6" fill="#007db3"/>
          <circle cx="24" cy="82" r="6" fill="#007db3"/>
          <circle cx="106" cy="82" r="6" fill="#007db3"/>
          <circle cx="65" cy="108" r="7" fill="#ffffff"/>
        </svg>'''

ICO_LIBRO = '''<svg class="portada__icono" viewBox="0 0 130 120" fill="none" aria-hidden="true">
          <path d="M65 34 12 52l53 18 53-18-53-18z" fill="rgba(0,125,179,.16)" stroke="#007db3" stroke-width="2" stroke-linejoin="round"/>
          <path d="M30 62v26c0 8 16 14 35 14s35-6 35-14V62" stroke="rgba(255,255,255,.5)" stroke-width="1.6"/>
          <path d="M112 56v26" stroke="#4498e7" stroke-width="2.4" stroke-linecap="round"/>
        </svg>'''

ICO_LLAVE = '''<svg class="portada__icono" viewBox="0 0 120 130" fill="none" aria-hidden="true">
          <circle cx="60" cy="36" r="24" stroke="#007db3" stroke-width="3" fill="rgba(0,125,179,.1)"/>
          <path d="M60 60v58" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
          <path d="M60 86h20M60 102h16" stroke="#007db3" stroke-width="3" stroke-linecap="round"/>
          <circle cx="60" cy="36" r="7" fill="#4498e7"/>
        </svg>'''

ICO_DOC = '''<svg class="portada__icono" viewBox="0 0 110 130" fill="none" aria-hidden="true">
          <path d="M18 10h48l26 26v84H18V10z" fill="rgba(0,125,179,.1)" stroke="#007db3" stroke-width="2" stroke-linejoin="round"/>
          <path d="M66 10v26h26" stroke="#007db3" stroke-width="2" stroke-linejoin="round"/>
          <path d="M34 62h42M34 78h42M34 94h26" stroke="rgba(255,255,255,.55)" stroke-width="2.4" stroke-linecap="round"/>
          <circle cx="84" cy="98" r="9" fill="#4498e7"/>
        </svg>'''

# --------------------------------------------------------------------------
# CIBERSEGURIDAD
# --------------------------------------------------------------------------

ciber = portada(
    '<a href="index.html">Inicio</a> / Servicios / Ciberseguridad',
    'Servicio', 'Ciberseguridad',
    'Millones de datos sensibles viajan cada día por correo o se guardan en bases de datos alojadas en la red. La ciberseguridad es el conjunto de sistemas, protocolos y reglas que evitan que eso acabe mal, y desde 2018 también es una obligación con sanciones detrás.',
    ICO_CIBER) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Qué es</span>
        <h2>Una capa de seguridad que actúa en cuatro momentos</h2>
        <p>El término ciberseguridad hace referencia a los sistemas, herramientas, protocolos, medidas y reglas relacionados con la protección de los servidores y los equipos informáticos.</p>
      </div>
      <div class="rejilla rejilla--4">
        <div class="tarjeta" data-aparece><div class="tarjeta__num">01</div><h3>Prevenir</h3><p>Acciones encaminadas a evitar que el ataque llegue a producirse.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">02</div><h3>Neutralizar</h3><p>Acciones para cortar un ataque una vez que ya está ocurriendo.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">03</div><h3>Reducir el daño</h3><p>Si el ataque tiene éxito: restablecer sistemas y recuperar la información.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">04</div><h3>Mejorar</h3><p>Revisar las tres anteriores y dejarlas mejor de lo que estaban.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,80px); align-items:start">
        <div data-aparece>
          <span class="kicker">Objetivos</span>
          <h2>Dos peligros que hay que evitar</h2>
          <p>Estamos cada vez más conectados y los riesgos se han multiplicado. La disciplina trabaja, sobre todo, para evitar dos cosas.</p>
        </div>
        <div data-aparece>
          <ul class="lista">
            <li><strong>Daños en las infraestructuras informáticas</strong> y, con ellos, la caída de los servicios que ofreces a tus clientes: que no puedas seguir trabajando.</li>
            <li><strong>Robo de datos.</strong> De clientes, de patentes o información del propio negocio: beneficios, inversiones, planes de expansión y demás información sensible.</li>
          </ul>
          <p class="mt-m">Se trabaja en dos frentes: el nacional e internacional, creando estándares y políticas comunes en la Unión Europea, y el empresarial, adaptando esos estándares a las necesidades concretas de cada organización.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="encabezado" data-aparece>
        <span class="kicker">Normativa</span>
        <h2>Qué normas te aplican</h2>
        <p>La seguridad en el ciberespacio ya forma parte de las agendas de los estados, que cooperan para crear una base normativa de derechos, obligaciones y sanciones.</p>
      </div>
      <div class="acordeon" data-aparece>
        <details open>
          <summary>Normativa europea</summary>
          <div class="acordeon__cuerpo">
            <ul class="lista">
              <li>Estrategia de Ciberseguridad de la Unión Europea (<em>Cybersecurity Strategy of the European Union: an Open, Safe and Secure Cyberspace</em>).</li>
              <li>Directiva 2016/1148, conocida como <strong>Directiva NIS</strong>, aprobada por el Consejo de la Unión Europea para garantizar un nivel común de seguridad de las redes y los sistemas de información en la Unión.</li>
            </ul>
          </div>
        </details>
        <details>
          <summary>Normativa nacional</summary>
          <div class="acordeon__cuerpo">
            <ul class="lista">
              <li><strong>Código Penal.</strong> Tipifica los delitos informáticos: intrusión, interceptación de transmisiones de datos, fraudes informáticos, sabotajes, posesión de software para delinquir o vulneración de la propiedad intelectual e industrial.</li>
              <li><strong>Real Decreto-ley 12/2018.</strong> Regula la seguridad de las redes y los sistemas de información para servicios esenciales y digitales, y establece un sistema de notificación de incidentes.</li>
              <li><strong>Código de Derecho de la Ciberseguridad.</strong> Desarrolla y aplica la política nacional de ciberseguridad.</li>
              <li><strong>LOPDGDD.</strong> Regula el tratamiento de datos personales como derecho fundamental y las sanciones por un uso incorrecto.</li>
            </ul>
          </div>
        </details>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker kicker--amber">Infracciones y sanciones</span>
        <h2>Lo que cuesta no adoptar las medidas</h2>
        <p>El artículo 36 del Real Decreto-ley 12/2018 recoge las infracciones por no adoptar las medidas necesarias de protección.</p>
      </div>
      <div class="rejilla rejilla--3">
        <div class="tarjeta tarjeta--destacada" data-aparece>
          <div class="tarjeta__num">Muy graves</div>
          <h3>500.001 € – 1.000.000 €</h3>
          <p>No adoptar medidas para subsanar incumplimientos ya detectados, no notificar los incidentes o no tomar medidas para incidentes futuros en la prestación de servicios digitales, en España o en otros Estados miembros.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <div class="tarjeta__num">Graves</div>
          <h3>100.000 € – 500.000 €</h3>
          <p>No adoptar medidas mínimas tras el tercer requerimiento en cinco años, no notificar incidentes, desinterés en resolverlos, dar información falsa o engañosa sobre los estándares que se tienen y poner obstáculos a las auditorías.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <div class="tarjeta__num">Leves</div>
          <h3>Amonestación – 100.000 €</h3>
          <p>Las que no encajan en las anteriores, además de impedir la recogida de información por parte del CSIRT o de la autoridad competente.</p>
        </div>
      </div>
      <div class="aviso mt-l" data-aparece>
        <p>Las cuantías varían según el grado de culpabilidad o intencionalidad, el perjuicio causado, la reincidencia, el número de usuarios afectados y el grado de implicación en la infracción.</p>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('¿Quién responde si mañana te entran?',
                   'Revisamos qué medidas tienes, qué te pide la norma según tu actividad y qué hay que notificar si pasa algo.')

# --------------------------------------------------------------------------
# VIDEOVIGILANCIA
# --------------------------------------------------------------------------

video = portada(
    '<a href="index.html">Inicio</a> / Servicios / Videovigilancia',
    'Servicio', 'Videovigilancia',
    'Tener cámaras es legal. Tenerlas sin cartel, sin cláusula, sin plazo de conservación y sin saber atender a quien pide sus imágenes, no. Dejamos tu instalación conforme a la guía de la Agencia Española de Protección de Datos.',
    ICO_OJO) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Lo que la ley te pide</span>
        <h2>Cuatro cosas que un inspector va a mirar</h2>
      </div>
      <div class="rejilla rejilla--4">
        <div class="tarjeta" data-aparece><h3>Cartel informativo</h3><p>Visible en la zona videovigilada, antes de entrar, con la información básica del tratamiento y a quién dirigirse.</p></div>
        <div class="tarjeta" data-aparece><h3>Cláusula completa</h3><p>La información detallada, disponible para quien la pida: finalidad, base legal, destinatarios y derechos.</p></div>
        <div class="tarjeta tarjeta--destacada" data-aparece><h3>30 días máximo</h3><p>Las imágenes se conservan un máximo de 30 días, salvo comunicación a Fuerzas y Cuerpos de Seguridad, juzgados y tribunales.</p></div>
        <div class="tarjeta" data-aparece><h3>Derechos atendidos</h3><p>Saber responder a quien pide acceder a sus imágenes, rectificarlas, suprimirlas u oponerse al tratamiento.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div data-aparece>
          <span class="kicker">Descargable</span>
          <h2>El cartel de zona videovigilada</h2>
          <p>Este es el cartel que tiene que estar colocado en un sitio visible, antes de acceder a la zona vigilada. Descárgalo, imprímelo y complétalo con los datos del responsable.</p>
          <p>Si prefieres que lo hagamos nosotros, lo dejamos montado junto con la cláusula y el registro de actividades durante la adaptación.</p>
          <div class="paso__cta">
            <a class="btn btn--pri" href="assets/img/contenido/cartel-videovigilancia.png" download>Descargar el cartel</a>
            <a class="btn btn--sec" href="contacto.html">Que lo hagáis vosotros</a>
          </div>
        </div>
        <div class="lamina" data-aparece>
          <img src="assets/img/contenido/cartel-videovigilancia.png" alt="Cartel informativo de zona videovigilada" loading="lazy">
        </div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="encabezado" data-aparece>
        <span class="kicker">Cláusula informativa</span>
        <h2>Tratamiento de los datos de videovigilancia</h2>
        <p>Este es el texto completo del tratamiento, tal y como debe poder consultarlo cualquier persona grabada.</p>
      </div>
      <div class="acordeon" data-aparece>
        <details open>
          <summary>¿Con qué finalidad tratamos sus datos personales?</summary>
          <div class="acordeon__cuerpo">
            <p>Tratamos la información que nos facilitan las personas interesadas con el fin de garantizar la seguridad de las personas, bienes e instalaciones usando los sistemas de videovigilancia. En el caso de que no facilite sus datos personales, no podremos cumplir con las finalidades descritas.</p>
            <p>No se van a tomar decisiones automatizadas en base a los datos proporcionados.</p>
          </div>
        </details>
        <details>
          <summary>¿Por cuánto tiempo conservaremos sus datos?</summary>
          <div class="acordeon__cuerpo">
            <p>Los datos se conservarán un máximo de 30 días, salvo comunicación a Fuerzas y Cuerpos de Seguridad, y/o Juzgados y Tribunales.</p>
          </div>
        </details>
        <details>
          <summary>¿Cuál es la legitimación para el tratamiento de sus datos?</summary>
          <div class="acordeon__cuerpo">
            <p>Misión en interés público: tratamiento necesario para el cumplimiento de una misión realizada en interés público o en el ejercicio de poderes públicos conferidos al responsable del tratamiento (RGPD art. 6.1.e), según consta en la «Guía sobre el uso de videocámaras para seguridad y otras finalidades», publicada por la Agencia Española de Protección de Datos.</p>
          </div>
        </details>
        <details>
          <summary>¿A qué destinatarios se comunicarán sus datos?</summary>
          <div class="acordeon__cuerpo">
            <p>En su caso, a las fuerzas y cuerpos de seguridad del Estado, así como a juzgados y tribunales, con la finalidad de aportar las imágenes si se ha cometido un delito (requisito legal).</p>
            <p>No están previstas transferencias de datos a terceros países.</p>
          </div>
        </details>
        <details>
          <summary>¿Cuáles son sus derechos cuando nos facilita sus datos?</summary>
          <div class="acordeon__cuerpo">
            <p>Cualquier persona tiene derecho a obtener confirmación sobre si el responsable está tratando, o no, datos personales que le conciernan.</p>
            <p>Las personas interesadas tienen derecho a acceder a sus datos personales, así como a solicitar la rectificación de los datos inexactos o, en su caso, solicitar su supresión cuando, entre otros motivos, los datos ya no sean necesarios para los fines para los que fueron recogidos. Igualmente tienen derecho a la portabilidad de sus datos.</p>
            <p>En determinadas circunstancias, los interesados podrán solicitar la limitación del tratamiento de sus datos, en cuyo caso únicamente los conservaremos para el ejercicio o la defensa de reclamaciones.</p>
            <p>En determinadas circunstancias y por motivos relacionados con su situación particular, los interesados podrán oponerse al tratamiento de sus datos. En este caso, el responsable dejará de tratar los datos, salvo por motivos legítimos imperiosos, o el ejercicio o la defensa de posibles reclamaciones.</p>
            <p>Podrá ejercitar materialmente sus derechos dirigiéndose a las instalaciones u oficinas donde las imágenes sean recabadas, o enviando una solicitud al correo del responsable.</p>
            <p>Cuando se realice el envío de comunicaciones comerciales utilizando como base jurídica el interés legítimo del responsable, el interesado podrá oponerse al tratamiento de sus datos con ese fin.</p>
            <p>En caso de que sienta vulnerados sus derechos en lo concerniente a la protección de sus datos personales, especialmente cuando no haya obtenido satisfacción en el ejercicio de sus derechos, puede presentar una reclamación ante la Autoridad de Control en materia de Protección de Datos competente a través de su sitio web: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
          </div>
        </details>
        <details>
          <summary>¿Cómo hemos obtenido sus datos?</summary>
          <div class="acordeon__cuerpo">
            <p>Los datos personales proceden de la grabación de imágenes por cámaras de seguridad. Las categorías de datos que se tratan son datos identificativos.</p>
          </div>
        </details>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('¿Tus cámaras están en regla?',
                   'Revisamos la instalación, los carteles, los plazos y quién tiene acceso a las grabaciones.')

# --------------------------------------------------------------------------
# BLANQUEO DE CAPITALES
# --------------------------------------------------------------------------

blanqueo = portada(
    '<a href="index.html">Inicio</a> / Servicios / Prevención del blanqueo',
    'Servicio', 'Prevención del blanqueo de capitales',
    'Servicio de adaptación a la Ley 10/2010 de Prevención del Blanqueo de Capitales y de la Financiación del Terrorismo, en dos modalidades según el tamaño del sujeto obligado.',
    ICO_DOC) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Dos modalidades</span>
        <h2>Según cuántos sois y cuánto facturáis</h2>
        <p>Hemos desarrollado dos modalidades de asesoramiento para adecuar las actuaciones a lo que debe cumplir cada tipo de sujeto obligado no financiero.</p>
      </div>

      <div class="rejilla rejilla--2">
        <div class="tarjeta" data-aparece>
          <div class="tarjeta__num">LPBC Diligence</div>
          <h3>Menos de 10 empleados y menos de 2 M€ de facturación</h3>
          <ul class="lista mt-m">
            <li>Análisis previo de la situación del cliente.</li>
            <li>Nombramiento de la persona representante ante el SEPBLAC.</li>
            <li>Confección de la política interna de prevención del blanqueo.</li>
            <li>Auditoría anual.</li>
            <li>Respuesta ante requerimientos e inspecciones del SEPBLAC.</li>
            <li>Asesoramiento permanente en prevención del blanqueo y financiación del terrorismo.</li>
          </ul>
        </div>

        <div class="tarjeta tarjeta--destacada" data-aparece>
          <div class="tarjeta__num">LPBC Integral</div>
          <h3>Más de 10 empleados y más de 2 M€ de facturación</h3>
          <ul class="lista mt-m">
            <li>Todo lo del servicio Diligence.</li>
            <li>Creación del Órgano de Control Interno (OCIC), en caso necesario.</li>
            <li>Confección del Manual de Procedimientos.</li>
            <li>Elaboración del Plan Anual de Formación.</li>
            <li>Examen anual por experto externo.</li>
            <li>Asesoramiento jurídico, defensa jurídica y seguro de responsabilidad civil.</li>
          </ul>
        </div>
      </div>

      <div class="aviso mt-l" data-aparece>
        <p><strong>Un buen motivo para estar bien asesorado.</strong> El incumplimiento de la Ley de Prevención del Blanqueo de Capitales y de la Financiación del Terrorismo comporta sanciones que pueden oscilar entre los 60.000 € y los 1.500.000 €, o cuantías mayores en función de la infracción.</p>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div data-aparece>
          <span class="kicker">Sujetos obligados</span>
          <h2>¿Te aplica a ti?</h2>
          <p>La ley enumera quién está sujeto a estas obligaciones. También quedan sujetas las personas o entidades no residentes que, a través de sucursales, agentes o prestando servicios sin establecimiento permanente, desarrollen en España actividades de la misma naturaleza.</p>
          <p>Si no tienes claro si entras en la lista, dínoslo y lo miramos: es la primera pregunta que hay que responder.</p>
          <div class="paso__cta"><a class="btn btn--pri" href="contacto.html">Consultar mi caso</a></div>
        </div>
        <div class="lamina" data-aparece>
          <img src="assets/img/contenido/sujetos-obligados.png" alt="Listado de sujetos obligados de la Ley 10/2010" loading="lazy">
        </div>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('¿Eres sujeto obligado y aún no tienes representante ante el SEPBLAC?',
                   'Empezamos por el análisis previo y te decimos qué modalidad te corresponde.')

# --------------------------------------------------------------------------
# FORMACIÓN
# --------------------------------------------------------------------------

formacion = portada(
    '<a href="index.html">Inicio</a> / Servicios / Formación bonificada',
    'Servicio', 'Formación bonificada',
    'Cursos online financiados con los créditos de FUNDAE que tu empresa ya tiene asignados. Con materiales propios, guías didácticas y catálogo abierto y también <em>in company</em>.',
    ICO_LIBRO) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="aviso aviso--violeta" data-aparece>
        <p><strong>La formación en protección de datos es una obligación legal, no un extra.</strong> Si tu equipo trata datos personales, tiene que estar formado para hacerlo. Y si la formación es bonificada, el coste efectivo para la empresa suele ser cero.</p>
      </div>
    </div>
  </section>

  <section class="bloque" style="padding-top:0">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Catálogo</span>
        <h2>Cursos que impartimos</h2>
      </div>
      <div class="rejilla rejilla--3">
        <div class="tarjeta" data-aparece><div class="tarjeta__num">40 horas · online</div><h3>RGPD</h3><p>El reglamento aplicado al día a día de la empresa: qué son datos personales, qué se puede hacer con ellos y qué no.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">60 horas · online</div><h3>RGPD ampliado</h3><p>La versión larga, para quien lleva la responsabilidad del cumplimiento dentro de la organización.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">Online</div><h3>Ciberseguridad laboral y personal</h3><p>Contraseñas, correo, dispositivos, teletrabajo y las estafas que llegan por email a cualquier empresa.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">60 horas · online</div><h3>Prevención del blanqueo de capitales</h3><p>Obligaciones de los sujetos obligados, señales de alerta y procedimientos internos.</p></div>
        <div class="tarjeta" data-aparece><div class="tarjeta__num">Restauración</div><h3>Manipulación de alimentos y alérgenos</h3><p>El curso que piden los gremios de restauración y hostelería, junto con la adaptación al RGPD.</p></div>
        <div class="tarjeta tarjeta--destacada" data-aparece><div class="tarjeta__num">A medida</div><h3><em>In company</em></h3><p>El mismo contenido adaptado a tu sector, con los ejemplos y los procedimientos de tu empresa.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Descargables</span>
        <h2>Los catálogos, en PDF</h2>
      </div>
      <div class="rejilla rejilla--2" style="align-items:center; gap:clamp(28px,4vw,60px)">
        <a class="tarjeta" href="assets/doc/catalogos/Catalogoeuda2025-1.pdf" data-aparece style="flex-direction:row; gap:24px; align-items:center">
          <img src="assets/img/contenido/catalogo-eudapro-2025.jpg" alt="Portada del catálogo de formación Eudapro 2025" loading="lazy" style="width:120px; border-radius:8px; flex:none">
          <span>
            <h3>Catálogo de formación 2025</h3>
            <p>El catálogo actual, con la relación de cursos, horas y modalidades.</p>
            <span class="enlace-flecha" style="margin-top:12px; display:inline-flex">Descargar PDF</span>
          </span>
        </a>
        <a class="tarjeta" href="assets/doc/catalogos/CATALOGO-CURSOS.pdf" data-aparece style="flex-direction:row; gap:24px; align-items:center">
          <img src="assets/img/contenido/catalogo-cursos.png" alt="Portada del catálogo de cursos" loading="lazy" style="width:120px; border-radius:8px; flex:none">
          <span>
            <h3>Catálogo de cursos</h3>
            <p>Fichas por curso: objetivos, contenidos y a quién va dirigido.</p>
            <span class="enlace-flecha" style="margin-top:12px; display:inline-flex">Descargar PDF</span>
          </span>
        </a>
      </div>
      <p class="mt-l" data-aparece><a class="enlace-flecha" href="recursos.html">Ver también las guías didácticas de cada curso</a></p>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="encabezado" data-aparece>
        <span class="kicker">Cómo funciona la bonificación</span>
        <h2>De dónde sale el dinero</h2>
      </div>
      <div class="acordeon" data-aparece>
        <details open>
          <summary>¿Qué significa que la formación es bonificada?</summary>
          <div class="acordeon__cuerpo"><p>Que se financia a través del crédito de formación que tu empresa ya tiene asignado en FUNDAE por cotizar. No es una subvención que haya que pedir: es un crédito que se pierde si no se usa.</p></div>
        </details>
        <details>
          <summary>¿Qué tengo que hacer yo?</summary>
          <div class="acordeon__cuerpo"><p>Decidir qué curso y quién lo hace. Del resto (alta del grupo, documentación y justificación) nos ocupamos nosotros, como del back office de la adaptación.</p></div>
        </details>
        <details>
          <summary>¿Vale también para una empresa pequeña?</summary>
          <div class="acordeon__cuerpo"><p>Sí. El crédito existe desde el primer trabajador; lo que cambia es la cuantía. Consúltanos y lo miramos antes de que empieces.</p></div>
        </details>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('¿Formamos a tu equipo este trimestre?',
                   'Dinos cuántas personas sois y a qué os dedicáis, y te decimos qué curso encaja y qué crédito tienes.')

# --------------------------------------------------------------------------
# COLECTIVOS
# --------------------------------------------------------------------------

colectivos = portada(
    '<a href="index.html">Inicio</a> / Colectivos con convenio',
    'Canal', 'Colectivos con convenio',
    'Trabajamos con gremios, federaciones y asociaciones. Ellos recomiendan un proveedor que ya conoce su sector; sus agremiados tienen promoción especial. Estos son los acuerdos que tenemos firmados.',
    ICO_RED) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div data-aparece>
          <span class="kicker">Desde 2016</span>
          <h2>Gremi de Restauració de Barcelona</h2>
          <p>Desde 2016 ofrecemos, junto al Gremi de Restauració de Barcelona, un servicio integral en protección de datos. Con esta oferta los agremiados quedan adecuados al RGPD y, a la vez, reciben formación en protección de datos y en manipulación de alimentos y alérgenos.</p>
          <p>Eudapro figura en la Guía de Proveedores del Gremi.</p>
          <div class="paso__cta">
            <a class="btn btn--pri" href="contacto.html">Soy agremiado</a>
            <a class="btn btn--sec" href="assets/img/gremios/Flyer-Promo-Gremi.jpg" target="_blank" rel="noopener">Ver la promoción</a>
          </div>
        </div>
        <div data-aparece style="display:grid; gap:16px">
          <div style="border:1px solid var(--line); border-radius:16px; padding:24px; background:var(--card)">
            <img src="assets/img/gremios/gremi-web.png" alt="Gremi de Restauració de Barcelona" loading="lazy">
          </div>
          <div style="border:1px solid var(--line); border-radius:16px; padding:20px; background:var(--card)">
            <img src="assets/img/gremios/signatura-gremi.png" alt="Firma del convenio de colaboración con el Gremi de Restauració de Barcelona" loading="lazy">
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Resto de acuerdos</span>
        <h2>Gremios, federaciones y redes con promoción para sus asociados</h2>
      </div>
      <div class="rejilla rejilla--3">
        <div class="tarjeta" data-aparece>
          <img src="assets/img/clientes/gremi-alt-penedes.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1) brightness(1.9); opacity:.75">
          <h3>Gremi Comarcal d'Hostaleria i Turisme de l'Alt Penedès</h3>
          <p>Convenio firmado con el gremio comarcal. Adaptación presencial, sin cuota de mantenimiento y con consultas y asesoría jurídica durante todo el año.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="assets/img/clientes/fhirt.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1) brightness(1.9); opacity:.75">
          <h3>Federació Intercomarcal d'Hostaleria, Restauració i Turisme</h3>
          <p>Convenio con la federación y, por extensión, con los gremios que la integran.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="assets/img/clientes/cadena-88.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1) brightness(1.9); opacity:.75">
          <h3>Ehlis / Cadena 88</h3>
          <p>Promoción especial para los asociados de la red de ferreterías: servicio integral de RGPD con el que la empresa queda adecuada a la reglamentación europea.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="assets/img/clientes/gremi-bages.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1) brightness(1.9); opacity:.75">
          <h3>Gremi d'Hostaleria i Turisme del Bages</h3>
          <p>Colaboración con el gremio comarcal del Bages, en la zona de Manresa y Sant Fruitós.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <h3>Gremi d'Hostaleria i Turisme de l'Anoia</h3>
          <p>Convenio firmado con el gremio de la comarca de l'Anoia.</p>
        </div>
        <div class="tarjeta tarjeta--destacada" data-aparece>
          <h3>¿Representas a un colectivo?</h3>
          <p>Si eres gremio, federación, asociación o central de compras y quieres una promoción para tus asociados, hablemos. Preparamos la oferta y el material informativo.</p>
          <div class="tarjeta__pie"><a class="enlace-flecha" href="contacto.html">Proponer un convenio</a></div>
        </div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div class="lamina" data-aparece>
          <img src="assets/img/contenido/guia-proveedores-gremi.png" alt="Guía de Proveedores del Gremi de Restauració de Barcelona" loading="lazy">
        </div>
        <div data-aparece>
          <span class="kicker">Qué incluye la promoción</span>
          <h2>Lo mismo que cualquier cliente, con condiciones de agremiado</h2>
          <ul class="lista">
            <li>Adaptación completa al RGPD y a la LOPDGDD, presencial.</li>
            <li>Contratos y cláusulas personalizados para el negocio.</li>
            <li>DPD incluido, sin coste extra.</li>
            <li>Formación en protección de datos y, en restauración, en manipulación de alimentos y alérgenos.</li>
            <li>Sin cuota de mantenimiento: consultas y asesoría jurídica todo el año.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('¿Eres agremiado de alguno de estos colectivos?',
                   'Dinos a cuál perteneces y te aplicamos las condiciones del convenio.')

# --------------------------------------------------------------------------
# CONÓCENOS
# --------------------------------------------------------------------------

conocenos = portada(
    '<a href="index.html">Inicio</a> / Conócenos',
    'Empresa', 'Conócenos',
    'Somos una consultoría de protección de datos con base en Barcelona y en Sant Fruitós de Bages. Trabajamos sobre todo con pymes catalanas: restaurantes, ferreterías, clubes, colegios, clínicas y empresas familiares.',
    ICO_LLAVE, acciones=False) + '''
  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
        <span class="kicker">En primera persona</span>
        <h2>Por qué trabajamos así</h2>
        <p>En All in Solutions for Business no creemos en los productos estándar, así como no hay personas estándar ni empresas que así lo sean. Nosotros solo trabajamos en un producto personalizado, a medida, para cubrir así todas las necesidades de nuestros clientes y crecer juntos, estando al día en todos los nuevos retos empresariales que se nos irán presentando. Bienvenidos: estamos aquí para ayudaros, vuestra confianza es nuestro mayor activo.</p>
        <p>Nos gusta trabajar a medida de nuestros clientes. Además de ofreceros nuestros servicios, lo haremos de modo que os resulte sencillo adaptaros a las novedades del nuevo reglamento. Por eso os daremos todos los contratos y cláusulas personalizados para vuestra empresa: de este modo podremos ocuparnos de todo el <em>back office</em> que esto genera y vosotros podréis seguir creciendo en vuestro sector sin preocuparos de nada más.</p>
        <p>Además, estamos formados para ofreceros el servicio de DPD (Delegado en Protección de Datos) sin que esto genere ningún gasto extra, evitando así cualquier sanción.</p>
        <p style="margin-top:2em"><strong>Isaac Higueras</strong><br><span style="font-family:var(--mono); font-size:12px; letter-spacing:.1em; color:var(--ink-3)">DIRECTOR</span></p>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">En resumen</span>
        <h2>Cuatro cosas que nos definen</h2>
      </div>
      <div class="rejilla rejilla--4">
        <div class="tarjeta" data-aparece><h3>Presenciales</h3><p>Vamos a la empresa. La adaptación no se hace por teléfono ni por formulario.</p></div>
        <div class="tarjeta" data-aparece><h3>Sin cuota</h3><p>Ninguna cuota de mantenimiento. Consultas y asesoría jurídica todo el año.</p></div>
        <div class="tarjeta" data-aparece><h3>Con DPD</h3><p>Ejercemos como Delegado de Protección de Datos sin coste añadido.</p></div>
        <div class="tarjeta" data-aparece><h3>Con gremios</h3><p>Convenios con gremios y federaciones desde 2016, sobre todo en hostelería.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
        <h2>Datos de la empresa</h2>
        <dl>
          <dt>Razón social</dt><dd>EUDAPRO, S.L.</dd>
          <dt>Nombre comercial</dt><dd>Eudapro</dd>
          <dt>CIF</dt><dd>B75390377</dd>
          <dt>Domicilio social</dt><dd>Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages (Barcelona)</dd>
          <dt>Oficina de atención</dt><dd>C/ Irlanda, 7 — 08030 Barcelona</dd>
          <dt>Registro Mercantil</dt><dd>Santa Cruz de Tenerife, tomo 3396, folio 212, hoja TF-55772, inscripción primera</dd>
          <dt>Teléfono</dt><dd><a href="tel:+34900929806">900 929 806</a> (gratuito)</dd>
          <dt>Correo</dt><dd><a href="mailto:info@allins4b.com">info@allins4b.com</a></dd>
          <dt>Dirección</dt><dd>Isaac Higueras, director</dd>
        </dl>
        <div class="aviso" style="margin-top:2em">
          <p><strong>Sobre el nombre.</strong> La empresa nació como All in Solutions for Business, S.L. — de ahí el dominio allins4b.com — y hoy es EUDAPRO, S.L. Los convenios firmados con los gremios y parte de los materiales antiguos llevan todavía el nombre anterior: es la misma empresa y el mismo equipo.</p>
        </div>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('Hablemos sin compromiso',
                   'Cuéntanos a qué te dedicas y qué tienes montado. La primera conversación no cuesta nada.')

# --------------------------------------------------------------------------
# RECURSOS (índice de PDFs generado desde assets/doc)
# --------------------------------------------------------------------------

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
         'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']


def sin_tildes(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn').lower()


def kb(ruta):
    n = os.path.getsize(ruta) / 1024.0
    return '%.1f MB' % (n / 1024.0) if n > 1024 else '%d KB' % round(n)


def item(ruta_rel, titulo, sub):
    return '''        <a class="descarga" href="%s" data-aparece>
          <span class="descarga__tipo">PDF</span>
          <span class="descarga__txt"><b>%s</b><span>%s</span></span>
          <span class="descarga__flecha" aria-hidden="true">↓</span>
        </a>''' % (ruta_rel, titulo, sub)


def listar_boletines():
    carpeta = os.path.join(RAIZ, 'assets', 'doc', 'boletines')
    filas = []
    for f in sorted(os.listdir(carpeta)):
        if not f.lower().endswith('.pdf'):
            continue
        plano = sin_tildes(f)
        mes = next((m for m in MESES if m in plano), None)
        anyo = re.search(r'20\d{2}', f)
        anyo = anyo.group(0) if anyo else ''
        if mes and anyo:
            titulo = 'Boletín RGPD — %s %s' % (mes.capitalize(), anyo)
        elif mes:
            titulo = 'Boletín RGPD — %s' % mes.capitalize()
        else:
            titulo = 'Boletín RGPD'
        orden = (anyo or '0000', '%02d' % (MESES.index(mes) + 1 if mes else 0))
        filas.append((orden, item('assets/doc/boletines/' + f, titulo, kb(os.path.join(carpeta, f)))))
    filas.sort(key=lambda x: x[0], reverse=True)
    return '\n'.join(f[1] for f in filas)


NOTAS = [
    ('Nota-Infomativa-diciembre-2023.pdf', 'Control laboral mediante huella dactilar',
     'Diciembre 2023 · qué dijo la AEPD sobre fichar con huella o reconocimiento facial'),
    ('Nota-Infomativa-Uso-DNI.pdf', 'El criterio de la AEPD respecto al DNI',
     'Septiembre 2024 · cuándo se puede pedir y fotocopiar el documento de identidad'),
    ('Nota-Infomativa-cookies.pdf', 'La normativa de cookies',
     'Abril 2024 · qué exige el banner y qué se considera consentimiento válido'),
    ('Nota-Infomativa-registro-alojamientos-turisticos.pdf', 'Registro de datos en alojamientos turísticos',
     'Mayo 2024 · el registro de viajeros y los datos que hay que comunicar'),
    ('NOTA-INFOMATIVA-FORMACION-EN-PROTECCION-DE-DATOS-COMO-OBLICACION-LEGAL.pdf',
     'La formación en protección de datos es una obligación legal',
     'Enero 2024 · por qué formar al equipo no es opcional'),
]

GUIAS = [
    ('GUIA-DIDACTICA-ALUMNO-ONLINE-RGPD-40-HORAS-2023.pdf', 'Guía didáctica — RGPD 40 horas', 'Curso online'),
    ('GUIA-DIDACTICA-ALUMNO-ONLINE-RGPD-60-2023.pdf', 'Guía didáctica — RGPD 60 horas', 'Curso online'),
    ('GUÍA-DIDÁCTICA-ALUMNO-ONLINE-UNIÓN-FORMATIVA-GESIDEA-RGPD-60..pdf', 'Guía didáctica — RGPD 60 horas (unión formativa)', 'Curso online'),
    ('GUIA-DIDACTICA-ALUMNO-ONLINE-UNION-FORMATIVA-GESIDEA-BLANQUEO-60-2023.pdf', 'Guía didáctica — Blanqueo de capitales 60 horas', 'Curso online'),
    ('GUIA-DIDACTICA-CURSO-CIBERSEGURIDAD-LABORAL-Y-PERSONAL-2023.pdf', 'Guía didáctica — Ciberseguridad laboral y personal', 'Curso online'),
    ('GUIA-2024.pdf', 'Guía didáctica 2024', 'Curso online'),
    ('GUIA-2024-IMPL.pdf', 'Guía didáctica 2024 — implantación', 'Curso online'),
]

CATALOGOS = [
    ('Catalogoeuda2025-1.pdf', 'Catálogo de formación 2025', 'El catálogo vigente'),
    ('CATALOGO-CURSOS.pdf', 'Catálogo de cursos', 'Fichas por curso'),
    ('Catalogoallin2023.pdf', 'Catálogo de formación 2023', 'Archivo'),
]


def bloque_descargas(titulo, kicker, intro, filas, alt=False):
    return '''  <section class="bloque%s">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">%s</span>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <div class="rejilla rejilla--2" style="gap:12px">
%s
      </div>
    </div>
  </section>
''' % (' bloque--alt' if alt else '', kicker, titulo, intro, filas)


def filas_fijas(carpeta, lista):
    base = os.path.join(RAIZ, 'assets', 'doc', carpeta)
    out = []
    for archivo, titulo, sub in lista:
        ruta = os.path.join(base, archivo)
        if os.path.exists(ruta):
            out.append(item('assets/doc/%s/%s' % (carpeta, archivo), titulo, '%s · %s' % (sub, kb(ruta))))
    return '\n'.join(out)


recursos = portada(
    '<a href="index.html">Inicio</a> / Recursos',
    'Biblioteca', 'Recursos y descargas',
    'Boletines mensuales, notas informativas cuando cambia la norma, guías de los cursos y catálogos de formación. Todo en abierto, sin registro y sin dejar tu correo.',
    ICO_DOC, acciones=False) + \
    bloque_descargas('Notas informativas', 'Avisos', 'Cuando cambia algo que afecta a nuestros clientes, lo escribimos y lo publicamos.',
                     filas_fijas('notas', NOTAS)) + \
    bloque_descargas('Catálogos de formación', 'Formación', 'Los cursos bonificables, sus horas y sus modalidades.',
                     filas_fijas('catalogos', CATALOGOS), alt=True) + \
    bloque_descargas('Guías didácticas de los cursos', 'Formación', 'Objetivos, contenidos y metodología de cada curso online.',
                     filas_fijas('guias', GUIAS)) + \
    bloque_descargas('Boletines RGPD', 'Boletín mensual', 'El resumen de novedades en protección de datos, número a número.',
                     listar_boletines(), alt=True) + \
    CTA_FINAL % ('¿Te falta algún documento?',
                 'Si buscas una nota concreta o quieres recibir el boletín cuando se retome, escríbenos.')

# --------------------------------------------------------------------------
# CONTACTO
# --------------------------------------------------------------------------

contacto = portada(
    '<a href="index.html">Inicio</a> / Contacto',
    'Contacto', 'Hablemos',
    'Cuéntanos a qué te dedicas y qué tienes montado. Te respondemos con lo que te falta para cumplir, sin compromiso.',
    ICO_LLAVE, acciones=False) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:start">

        <div data-aparece>
          <span class="kicker">Formulario</span>
          <h2>Escríbenos</h2>
          <form class="form mt-m" data-contacto novalidate>
            <div class="form__fila">
              <label class="campo"><span>Tu nombre <em>*</em></span>
                <input type="text" name="nombre" maxlength="400" required autocomplete="name"></label>
              <label class="campo"><span>Tu correo electrónico <em>*</em></span>
                <input type="email" name="correo" required autocomplete="email"></label>
            </div>
            <div class="form__fila">
              <label class="campo"><span>Teléfono</span>
                <input type="tel" name="telefono" autocomplete="tel"></label>
              <label class="campo"><span>Empresa o colectivo</span>
                <input type="text" name="empresa" autocomplete="organization"></label>
            </div>
            <label class="campo"><span>Asunto</span>
              <input type="text" name="asunto"></label>
            <label class="campo"><span>Tu mensaje</span>
              <textarea name="mensaje" placeholder="A qué te dedicas, qué tienes montado y qué te preocupa."></textarea></label>

            <div class="consentimiento">
              <p>EUDAPRO, S.L. se compromete a proteger y respetar tu privacidad, y solo usaremos tu información personal para gestionar tu solicitud y proporcionarte los servicios solicitados. De vez en cuando, nos gustaría ponernos en contacto contigo acerca de nuestros productos y servicios, así como sobre otros contenidos que puedan interesarte. Si aceptas que nos comuniquemos contigo para este fin, marca la casilla siguiente:</p>
              <label class="check"><input type="checkbox" name="consent-comercial" value="si">
                <span>Acepto recibir otras comunicaciones de EUDAPRO, S.L.</span></label>

              <p>Para poder atender tu solicitud, debemos almacenar y gestionar tus datos personales. Si aceptas que almacenemos tus datos personales para este fin, marca la casilla de abajo.</p>
              <label class="check"><input type="checkbox" name="consent-tratamiento" value="si" required>
                <span>Acepto el tratamiento de datos de potenciales clientes y contactos web (<a href="politica-de-privacidad.html">+Info</a>). <em style="color:var(--amber); font-style:normal">*</em></span></label>

              <p class="form__aviso">Puedes darte de baja de estas comunicaciones en cualquier momento. Para obtener más información sobre cómo darte de baja, el tratamiento que hacemos de los datos personales y cómo nos comprometemos a proteger y respetar tu privacidad, consulta nuestra <a href="politica-de-privacidad.html">Política de Privacidad</a>.</p>
            </div>

            <div>
              <button class="btn btn--pri" type="submit">Enviar</button>
              <p class="form__estado" role="status" style="margin-top:14px"></p>
            </div>
          </form>
        </div>

        <div data-aparece>
          <span class="kicker">Directo</span>
          <h2>O llámanos</h2>
          <p>El teléfono es gratuito. Si prefieres el correo, también va bien.</p>

          <div class="rejilla" style="gap:12px; margin-top:26px">
            <a class="tarjeta" href="tel:+34900929806">
              <div class="tarjeta__num">Teléfono gratuito</div>
              <h3 style="margin:0">900 929 806</h3>
            </a>
            <a class="tarjeta" href="mailto:info@allins4b.com">
              <div class="tarjeta__num">Correo</div>
              <h3 style="margin:0">info@allins4b.com</h3>
            </a>
          </div>

          <div class="prosa mt-l">
            <h3>Dónde estamos</h3>
            <dl>
              <dt>Oficina de atención</dt><dd>C/ Irlanda, 7 — 08030 Barcelona</dd>
              <dt>Domicilio social</dt><dd>Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages (Barcelona)</dd>
              <dt>Razón social</dt><dd>EUDAPRO, S.L. — CIF B75390377</dd>
            </dl>
          </div>

          <div class="aviso aviso--violeta mt-m">
            <p><strong>Solo te pedimos lo que necesitamos.</strong> Nombre y correo para poder responderte; el resto es opcional. Nos dedicamos a esto: no vamos a hacer con tus datos lo que le decimos a nuestros clientes que no hagan.</p>
          </div>
        </div>

      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------------------
# LEGALES
# --------------------------------------------------------------------------


def legal(kicker, h1, lede, prosa):
    return portada('<a href="index.html">Inicio</a> / %s' % h1, kicker, h1, lede, '', acciones=False) + '''
  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
%s
      </div>
    </div>
  </section>
''' % prosa


aviso_legal = legal('Legal', 'Aviso legal',
                    'Condiciones de uso del sitio web de EUDAPRO, S.L.', '''
        <h2>1. Objeto</h2>
        <p>El presente aviso legal regula el uso y utilización del sitio web del que es titular <strong>EUDAPRO, S.L.</strong> (en adelante, EL PROPIETARIO DE LA WEB).</p>
        <p>La navegación por el sitio web de EL PROPIETARIO DE LA WEB le atribuye la condición de USUARIO del mismo y conlleva su aceptación plena y sin reservas de todas y cada una de las condiciones publicadas en este aviso legal, advirtiendo de que dichas condiciones podrán ser modificadas sin notificación previa por parte de EL PROPIETARIO DE LA WEB, en cuyo caso se procederá a su publicación y aviso con la máxima antelación posible.</p>
        <p>Por ello es recomendable leer atentamente su contenido en caso de desear acceder y hacer uso de la información y de los servicios ofrecidos desde este sitio web.</p>
        <p>El usuario, además, se obliga a hacer un uso correcto del sitio web de conformidad con las leyes, la buena fe, el orden público, los usos del tráfico y el presente aviso legal, y responderá frente a EL PROPIETARIO DE LA WEB o frente a terceros de cualesquiera daños y perjuicios que pudieran causarse como consecuencia del incumplimiento de dicha obligación.</p>
        <p>Cualquier utilización distinta a la autorizada está expresamente prohibida, pudiendo EL PROPIETARIO DE LA WEB denegar o retirar el acceso y su uso en cualquier momento.</p>

        <h2>2. Identificación</h2>
        <p>EL PROPIETARIO DE LA WEB, en cumplimiento de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico, le informa de que:</p>
        <dl>
          <dt>Denominación social</dt><dd>EUDAPRO, S.L.</dd>
          <dt>CIF</dt><dd>B75390377</dd>
          <dt>Domicilio social</dt><dd>Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages, Barcelona</dd>
          <dt>Registro Mercantil</dt><dd>Santa Cruz de Tenerife, tomo 3396, folio 212, hoja TF-55772, inscripción primera</dd>
        </dl>

        <h2>3. Comunicaciones</h2>
        <p>Para comunicarse con nosotros ponemos a su disposición los siguientes medios de contacto:</p>
        <ul>
          <li>Teléfono: <a href="tel:+34900929806">900 929 806</a></li>
          <li>Correo electrónico: <a href="mailto:info@allins4b.com">info@allins4b.com</a></li>
        </ul>
        <p>Todas las notificaciones y comunicaciones entre los usuarios y EL PROPIETARIO DE LA WEB se considerarán eficaces, a todos los efectos, cuando se realicen a través de cualquiera de los medios detallados anteriormente.</p>

        <h2>4. Condiciones de acceso y utilización</h2>
        <p>El sitio web y sus servicios son de acceso libre y gratuito. No obstante, EL PROPIETARIO DE LA WEB puede condicionar la utilización de algunos de los servicios ofrecidos en su web a la previa cumplimentación del correspondiente formulario.</p>
        <p>El usuario garantiza la autenticidad y actualidad de todos aquellos datos que comunique a EL PROPIETARIO DE LA WEB y será el único responsable de las manifestaciones falsas o inexactas que realice.</p>
        <p>El usuario se compromete expresamente a hacer un uso adecuado de los contenidos y servicios de EL PROPIETARIO DE LA WEB y a no emplearlos para, entre otros:</p>
        <ol>
          <li>Difundir contenidos delictivos, violentos, pornográficos, racistas, xenófobos, ofensivos, de apología del terrorismo o, en general, contrarios a la ley o al orden público.</li>
          <li>Introducir en la red virus informáticos o realizar actuaciones susceptibles de alterar, estropear, interrumpir o generar errores o daños en los documentos electrónicos, datos o sistemas físicos y lógicos de EL PROPIETARIO DE LA WEB o de terceras personas; así como obstaculizar el acceso de otros usuarios al sitio web y a sus servicios mediante el consumo masivo de los recursos informáticos a través de los cuales EL PROPIETARIO DE LA WEB presta sus servicios.</li>
          <li>Intentar acceder a las cuentas de correo electrónico de otros usuarios o a áreas restringidas de los sistemas informáticos de EL PROPIETARIO DE LA WEB o de terceros y, en su caso, extraer información.</li>
          <li>Vulnerar los derechos de propiedad intelectual o industrial, así como violar la confidencialidad de la información de EL PROPIETARIO DE LA WEB o de terceros.</li>
          <li>Suplantar la identidad de cualquier otro usuario.</li>
          <li>Reproducir, copiar, distribuir, poner a disposición de, o cualquier otra forma de comunicación pública, transformar o modificar los contenidos, a menos que se cuente con la autorización del titular de los correspondientes derechos o ello resulte legalmente permitido.</li>
          <li>Recabar datos con finalidad publicitaria y remitir publicidad de cualquier clase y comunicaciones con fines de venta u otras de naturaleza comercial sin que medie su previa solicitud o consentimiento.</li>
        </ol>
        <p>Todos los contenidos del sitio web, como textos, fotografías, gráficos, imágenes, iconos, tecnología, software, así como su diseño gráfico y códigos fuente, constituyen una obra cuya propiedad pertenece a EL PROPIETARIO DE LA WEB, sin que puedan entenderse cedidos al usuario ninguno de los derechos de explotación sobre los mismos más allá de lo estrictamente necesario para el correcto uso de la web.</p>
        <p>En definitiva, los usuarios que accedan a este sitio web pueden visualizar los contenidos y efectuar, en su caso, copias privadas autorizadas siempre que los elementos reproducidos no sean cedidos posteriormente a terceros, ni se instalen en servidores conectados a redes, ni sean objeto de ningún tipo de explotación.</p>
        <p>Asimismo, todas las marcas, nombres comerciales o signos distintivos de cualquier clase que aparecen en el sitio web son propiedad de EL PROPIETARIO DE LA WEB, sin que pueda entenderse que el uso o acceso al mismo atribuya al usuario derecho alguno sobre los mismos.</p>
        <p>La distribución, modificación, cesión o comunicación pública de los contenidos y cualquier otro acto que no haya sido expresamente autorizado por el titular de los derechos de explotación quedan prohibidos.</p>
        <p>El establecimiento de un hiperenlace no implica en ningún caso la existencia de relaciones entre EL PROPIETARIO DE LA WEB y el propietario del sitio web en la que se establezca, ni la aceptación y aprobación por parte de EL PROPIETARIO DE LA WEB de sus contenidos o servicios.</p>
        <p>EL PROPIETARIO DE LA WEB no se responsabiliza del uso que cada usuario dé a los materiales puestos a disposición en este sitio web ni de las actuaciones que realice en base a los mismos.</p>

        <h3>4.1. Exclusión de garantías y de responsabilidad en el acceso y la utilización</h3>
        <p>El contenido del presente sitio web es de carácter general y tiene una finalidad meramente informativa, sin que se garantice plenamente el acceso a todos los contenidos, ni su exhaustividad, corrección, vigencia o actualidad, ni su idoneidad o utilidad para un objetivo específico.</p>
        <p>EL PROPIETARIO DE LA WEB excluye, hasta donde permite el ordenamiento jurídico, cualquier responsabilidad por los daños y perjuicios de toda naturaleza derivados de:</p>
        <ol>
          <li>La imposibilidad de acceso al sitio web o la falta de veracidad, exactitud, exhaustividad y/o actualidad de los contenidos, así como la existencia de vicios y defectos de toda clase de los contenidos transmitidos, difundidos, almacenados, puestos a disposición, a los que se haya accedido a través del sitio web o de los servicios que se ofrecen.</li>
          <li>La presencia de virus o de otros elementos en los contenidos que puedan producir alteraciones en los sistemas informáticos, documentos electrónicos o datos de los usuarios.</li>
          <li>El incumplimiento de las leyes, la buena fe, el orden público, los usos del tráfico y el presente aviso legal como consecuencia del uso incorrecto del sitio web. En particular, y a modo ejemplificativo, EL PROPIETARIO DE LA WEB no se hace responsable de las actuaciones de terceros que vulneren derechos de propiedad intelectual e industrial, secretos empresariales, derechos al honor, a la intimidad personal y familiar y a la propia imagen, así como la normativa en materia de competencia desleal y publicidad ilícita.</li>
        </ol>
        <p>Asimismo, EL PROPIETARIO DE LA WEB declina cualquier responsabilidad respecto a la información que se halle fuera de esta web y no sea gestionada directamente por nuestro webmaster. La función de los enlaces que aparecen en esta web es exclusivamente la de informar al usuario sobre la existencia de otras fuentes susceptibles de ampliar los contenidos que ofrece este sitio web. EL PROPIETARIO DE LA WEB no garantiza ni se responsabiliza del funcionamiento o accesibilidad de los sitios enlazados; ni sugiere, invita o recomienda la visita a los mismos, por lo que tampoco será responsable del resultado obtenido. EL PROPIETARIO DE LA WEB no se responsabiliza del establecimiento de hipervínculos por parte de terceros.</p>

        <h3>4.2. Procedimiento en caso de realización de actividades de carácter ilícito</h3>
        <p>En el caso de que cualquier usuario o un tercero consideren que existen hechos o circunstancias que revelen el carácter ilícito de la utilización de cualquier contenido y/o de la realización de cualquier actividad en las páginas web incluidas o accesibles a través del sitio web, deberá enviar una notificación a EL PROPIETARIO DE LA WEB identificándose debidamente y especificando las supuestas infracciones.</p>

        <h3>4.3. Publicaciones</h3>
        <p>La información administrativa facilitada a través del sitio web no sustituye la publicidad legal de las leyes, normativas, planes, disposiciones generales y actos que tengan que ser publicados formalmente en los diarios oficiales de las administraciones públicas, que constituyen el único instrumento que da fe de su autenticidad y contenido. La información disponible en este sitio web debe entenderse como una guía sin propósito de validez legal.</p>

        <h2>5. Propiedad intelectual e industrial</h2>
        <p>EL PROPIETARIO DE LA WEB, por sí mismo o como cesionario, es titular de todos los derechos de propiedad intelectual e industrial de su página web, así como de los elementos contenidos en la misma (a título enunciativo: imágenes, sonido, audio, vídeo, software o textos; marcas o logotipos, combinaciones de colores, estructura y diseño, selección de materiales usados, programas de ordenador necesarios para su funcionamiento, acceso y uso, etc.). Serán, por consiguiente, obras protegidas como propiedad intelectual por el ordenamiento jurídico español, siéndoles aplicables tanto la normativa española y comunitaria en este campo como los tratados internacionales relativos a la materia y suscritos por España.</p>
        <p>Todos los derechos reservados. En virtud de lo dispuesto en los artículos 8 y 32.1, párrafo segundo, de la Ley de Propiedad Intelectual, quedan expresamente prohibidas la reproducción, la distribución y la comunicación pública, incluida su modalidad de puesta a disposición, de la totalidad o parte de los contenidos de esta página web, con fines comerciales, en cualquier soporte y por cualquier medio técnico, sin la autorización de EL PROPIETARIO DE LA WEB.</p>
        <p>El usuario se compromete a respetar los derechos de propiedad intelectual e industrial titularidad de EL PROPIETARIO DE LA WEB. Podrá visualizar los elementos del portal e incluso imprimirlos, copiarlos y almacenarlos en el disco duro de su ordenador o en cualquier otro soporte físico siempre y cuando sea, única y exclusivamente, para su uso personal y privado. El usuario deberá abstenerse de suprimir, alterar, eludir o manipular cualquier dispositivo de protección o sistema de seguridad que estuviera instalado en las páginas de EL PROPIETARIO DE LA WEB.</p>

        <h2>6. Acciones legales, legislación aplicable y jurisdicción</h2>
        <p>EL PROPIETARIO DE LA WEB se reserva la facultad de presentar las acciones civiles o penales que considere oportunas por la utilización indebida de su sitio web y contenidos, o por el incumplimiento de las presentes condiciones.</p>
        <p>La relación entre el usuario y el prestador se regirá por la normativa vigente y de aplicación en el territorio español. De surgir cualquier controversia, las partes podrán someter sus conflictos a arbitraje o acudir a la jurisdicción ordinaria cumpliendo con las normas sobre jurisdicción y competencia al respecto. EL PROPIETARIO DE LA WEB tiene su domicilio en Barcelona, España.</p>
        <p>La lengua utilizada será el castellano.</p>
''')

privacidad = legal('Legal', 'Política de privacidad',
                   'Cómo tratamos los datos personales que llegan a través de esta web.', '''
        <p>En EUDAPRO, S.L. nos preocupamos por la privacidad y la transparencia.</p>
        <p>A continuación le indicamos en detalle los tratamientos de datos personales que realizamos, así como toda la información relativa a los mismos, de acuerdo con lo establecido por el REGLAMENTO (UE) 2016/679, de 27 de abril de 2016, del Parlamento Europeo y del Consejo, relativo a la protección de las personas físicas en lo que respecta al tratamiento de sus datos personales, y por la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales.</p>

        <h2>Responsable del tratamiento</h2>
        <dl>
          <dt>Identidad</dt><dd>EUDAPRO, S.L. — CIF B75390377</dd>
          <dt>Domicilio social</dt><dd>Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages, Barcelona</dd>
          <dt>Oficina de atención</dt><dd>C/ Irlanda, 7 — 08030 Barcelona</dd>
          <dt>Teléfono</dt><dd><a href="tel:+34900929806">900 929 806</a></dd>
          <dt>Correo electrónico</dt><dd><a href="mailto:info@allins4b.com">info@allins4b.com</a></dd>
        </dl>

        <h2>Tratamiento: contactos y potenciales clientes de la web</h2>
        <h3>¿Con qué finalidad tratamos sus datos personales?</h3>
        <p>Para gestionar la solicitud que nos hace llegar a través del formulario de contacto o del correo electrónico, y proporcionarle los servicios solicitados. Si nos da su consentimiento expreso, también para enviarle comunicaciones sobre nuestros productos y servicios, así como sobre otros contenidos que puedan interesarle.</p>
        <h3>¿Cuál es la legitimación para el tratamiento de sus datos?</h3>
        <p>El consentimiento del interesado, que se recoge de forma diferenciada: uno para poder atender la solicitud y otro, independiente y opcional, para recibir comunicaciones comerciales.</p>
        <h3>¿Por cuánto tiempo conservaremos sus datos?</h3>
        <p>Durante el tiempo necesario para atender su solicitud y, después, durante los plazos legalmente previstos para atender posibles responsabilidades. Si consintió recibir comunicaciones comerciales, hasta que solicite la baja.</p>
        <h3>¿A qué destinatarios se comunicarán sus datos?</h3>
        <p>No se comunican datos a terceros, salvo obligación legal. No están previstas transferencias de datos a terceros países.</p>

        <h2>Tratamiento: videovigilancia</h2>
        <p>El tratamiento de las imágenes captadas por los sistemas de videovigilancia se detalla en la <a href="videovigilancia.html">cláusula informativa de videovigilancia</a>: finalidad, plazo de conservación de 30 días, base legal, destinatarios y ejercicio de derechos.</p>

        <h2>¿Cuáles son sus derechos cuando nos facilita sus datos?</h2>
        <p>Cualquier persona tiene derecho a obtener confirmación sobre si estamos tratando, o no, datos personales que le conciernan.</p>
        <p>Las personas interesadas tienen derecho a acceder a sus datos personales, así como a solicitar la rectificación de los datos inexactos o, en su caso, solicitar su supresión cuando, entre otros motivos, los datos ya no sean necesarios para los fines para los que fueron recogidos. Igualmente tienen derecho a la portabilidad de sus datos.</p>
        <p>En determinadas circunstancias, los interesados podrán solicitar la limitación del tratamiento de sus datos, en cuyo caso únicamente los conservaremos para el ejercicio o la defensa de reclamaciones.</p>
        <p>En determinadas circunstancias y por motivos relacionados con su situación particular, los interesados podrán oponerse al tratamiento de sus datos. En este caso dejaremos de tratarlos, salvo por motivos legítimos imperiosos o el ejercicio o la defensa de posibles reclamaciones.</p>
        <p>Puede ejercer sus derechos escribiendo a <a href="mailto:info@allins4b.com">info@allins4b.com</a> o por correo postal a la dirección del responsable, acreditando su identidad.</p>
        <p>Si considera vulnerados sus derechos, especialmente cuando no haya obtenido satisfacción en su ejercicio, puede presentar una reclamación ante la Agencia Española de Protección de Datos a través de <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>

        <h2>Cookies</h2>
        <p>El uso de cookies de este sitio se detalla en la <a href="politica-de-cookies.html">Política de Cookies</a>.</p>
''')

cookies = legal('Legal', 'Política de cookies',
                'Qué son las cookies, cuáles usa este sitio y cómo desactivarlas.', '''
        <h2>¿Qué son las cookies?</h2>
        <p>Una cookie es un fichero que se descarga en su ordenador al acceder a determinadas páginas web. Las cookies permiten a una página web, entre otras cosas, almacenar y recuperar información sobre los hábitos de navegación de un usuario o de su equipo y, dependiendo de la información que contengan y de la forma en que utilice su equipo, pueden utilizarse para reconocer al usuario.</p>

        <h2>¿Qué cookies utiliza esta página web?</h2>
        <p>Esta web se sirve sin cookies de terceros: las tipografías y los scripts se cargan desde este mismo dominio y no se incrusta contenido externo que instale cookies. Si en el futuro se incorporan herramientas de análisis, se detallarán en esta tabla y se solicitará el consentimiento previo.</p>
        <div class="tabla-envoltorio">
          <table>
            <thead><tr><th>Cookie</th><th>Tipo</th><th>Propósito</th></tr></thead>
            <tbody><tr><td colspan="3">Actualmente no se instalan cookies de análisis, de personalización ni publicitarias.</td></tr></tbody>
          </table>
        </div>

        <h2>¿Cómo puedo desactivar o eliminar las cookies?</h2>
        <p>Puede permitir, bloquear o eliminar las cookies instaladas en su equipo mediante la configuración de las opciones del navegador:</p>
        <ul>
          <li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener">Firefox</a></li>
          <li><a href="https://support.google.com/chrome/answer/95647?hl=es" target="_blank" rel="noopener">Chrome</a></li>
          <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Safari</a></li>
          <li><a href="https://support.microsoft.com/es-es/microsoft-edge" target="_blank" rel="noopener">Edge</a></li>
          <li><a href="https://help.opera.com/en/latest/web-preferences/" target="_blank" rel="noopener">Opera</a></li>
        </ul>
        <p>Para el resto de navegadores, consulte su documentación.</p>

        <h2>Más información sobre las cookies</h2>
        <h3>¿Qué NO es una cookie?</h3>
        <p>No es un virus, ni un troyano, ni un gusano, ni spam, ni spyware, ni abre ventanas emergentes.</p>
        <h3>¿Qué información almacena una cookie?</h3>
        <p>Las cookies no suelen almacenar información sensible sobre usted, como tarjetas de crédito o datos bancarios, fotografías, su DNI o información personal. Los datos que guardan son de carácter técnico, preferencias personales, personalización de contenidos, etc.</p>
        <p>El servidor web no le asocia a usted como persona, sino a su navegador. De hecho, si navega habitualmente con un navegador y prueba a visitar la misma web con otro, verá que el sitio no reconoce que es la misma persona, porque en realidad está asociando al navegador y no a usted.</p>
        <h3>¿Qué tipos de cookies existen?</h3>
        <ul>
          <li><strong>Técnicas:</strong> las más elementales; permiten tareas básicas para el funcionamiento de cualquier web dinámica.</li>
          <li><strong>De análisis:</strong> recogen información sobre el tipo de navegación, las secciones más utilizadas, la franja horaria de uso o el idioma.</li>
          <li><strong>Publicitarias:</strong> muestran publicidad en función de la navegación, el país de procedencia o el idioma.</li>
        </ul>
        <h3>¿Qué son las cookies propias y las de terceros?</h3>
        <p>Las propias son las generadas por la página que está visitando; las de terceros son las generadas por servicios o proveedores externos.</p>
        <h3>¿Se pueden eliminar las cookies?</h3>
        <p>Sí. No solo eliminar, también bloquear, de forma general o particular para un dominio específico. Para eliminar las cookies de un sitio web debe ir a la configuración de su navegador, buscar las asociadas al dominio en cuestión y proceder a su eliminación.</p>
''')

redes = legal('Legal', 'Política de redes sociales',
              'Qué hacemos con la información pública de quienes nos siguen en redes.', '''
        <p>En cumplimiento del REGLAMENTO (UE) 2016/679, de 27 de abril de 2016, del Parlamento Europeo y del Consejo, relativo a la protección de las personas físicas en lo que respecta al tratamiento de sus datos personales; de la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales; y de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), EUDAPRO, S.L., en adelante EL PROPIETARIO DE LA WEB, informa a los usuarios de que ha procedido a crear un perfil en las redes sociales con la finalidad principal de publicitar sus productos y servicios.</p>

        <dl>
          <dt>Datos de EUDAPRO, S.L.</dt>
          <dd>CIF B75390377<br>Ctra. de Vic, 105 — 08272 Sant Fruitós de Bages, Barcelona<br><a href="mailto:info@allins4b.com">info@allins4b.com</a></dd>
        </dl>

        <p>El usuario dispone de un perfil en la misma red social y ha decidido unirse a la página creada por EL PROPIETARIO DE LA WEB, mostrando así interés en la información que se publicite en la red. Al unirse a nuestra página, nos facilita su consentimiento para el tratamiento de aquellos datos personales publicados en su perfil.</p>
        <p>El usuario puede acceder en todo momento a las políticas de privacidad de la propia red social, así como configurar su perfil para garantizar su privacidad.</p>
        <p>EL PROPIETARIO DE LA WEB tiene acceso y trata aquella información pública del usuario, en especial su nombre de contacto. Estos datos solo son utilizados dentro de la propia red social y en ningún caso son incorporados a ningún fichero sin solicitar previamente el consentimiento expreso del interesado.</p>
        <p>En relación con los derechos de acceso, rectificación, cancelación y oposición de los que usted dispone y que pueden ser ejercitados ante EL PROPIETARIO DE LA WEB, debe tener en cuenta que, por la propia funcionalidad de las redes sociales, normalmente deberá ejercer sus derechos ante la propia red social.</p>

        <h2>Actuaciones</h2>
        <ul>
          <li>Acceso a la información pública del perfil.</li>
          <li>Publicación en el perfil del usuario de aquella información ya publicada en la página de EL PROPIETARIO DE LA WEB.</li>
          <li>Envío de mensajes personales e individuales a través de los canales de la red social.</li>
          <li>Actualizaciones del estado de la página que se publicarán en el perfil del usuario.</li>
        </ul>
        <p>El usuario siempre puede controlar sus conexiones, eliminar los contenidos que dejen de interesarle y restringir con quién comparte sus conexiones; para ello deberá acceder a su configuración de privacidad.</p>

        <h2>Datos de menores</h2>
        <p>El acceso y registro en esta red social está prohibido para menores de 14 años. El acceso al sitio oficial de EL PROPIETARIO DE LA WEB está también prohibido para menores de 14 años. Si el usuario no cumple dicho requisito, EL PROPIETARIO DE LA WEB le informa de la necesidad de tener la autorización de sus padres, tutores o responsables legales para acceder y utilizar el sitio oficial.</p>
        <p>EL PROPIETARIO DE LA WEB queda eximido de cualquier responsabilidad derivada del uso de su sitio oficial por menores o usuarios que no cumplan los requisitos mencionados, siendo en cualquier caso sus representantes legales los únicos responsables.</p>

        <h2>Publicaciones</h2>
        <p>El usuario, una vez unido a la página de EL PROPIETARIO DE LA WEB, podrá publicar en ella comentarios, enlaces, imágenes o fotografías o cualquier otro tipo de contenido multimedia soportado por la red social. El usuario, en todos los casos, debe ser el titular de los mismos, gozar de los derechos de autor y de propiedad intelectual o contar con el consentimiento de los terceros afectados.</p>
        <p>Se prohíbe expresamente cualquier publicación en la página, ya sean textos, gráficos, fotografías o vídeos, que atente o sea susceptible de atentar contra la moral, la ética, el buen gusto o el decoro, y/o que infrinja, viole o quebrante los derechos de propiedad intelectual o industrial, el derecho a la imagen o la ley. En estos casos, EL PROPIETARIO DE LA WEB se reserva el derecho a retirar de inmediato el contenido, pudiendo solicitar el bloqueo permanente del usuario.</p>
        <p>EL PROPIETARIO DE LA WEB no se hará responsable de los contenidos que libremente haya publicado un usuario. El usuario debe tener presente que sus publicaciones serán conocidas por los otros usuarios, por lo que él mismo es el principal responsable de su privacidad.</p>
        <p>Las imágenes que puedan publicarse en la página no serán almacenadas en ningún fichero por parte de EL PROPIETARIO DE LA WEB, pero sí permanecerán en la red social.</p>

        <h2>Concursos y promociones</h2>
        <p>EL PROPIETARIO DE LA WEB se reserva el derecho a realizar concursos y promociones en los que podrá participar el usuario unido a su página. Las bases de cada uno de ellos, cuando se utilice para ello la plataforma de la red social, serán publicadas en la misma, cumpliendo siempre con la LSSI-CE y con cualquier otra norma que le sea de aplicación. La red social no patrocina, avala ni administra de modo alguno ninguna de nuestras promociones, ni está asociada a ninguna de ellas.</p>

        <h2>Publicidad</h2>
        <p>EL PROPIETARIO DE LA WEB utilizará la red social para publicitar sus productos y servicios. En todo caso, si decide tratar sus datos de contacto para realizar acciones directas de prospección comercial, será siempre cumpliendo con las exigencias legales del RGPD, de la LOPDGDD y de la LSSI-CE.</p>
        <p>No se considerará publicidad el hecho de recomendar a otros usuarios la página de EL PROPIETARIO DE LA WEB para que también ellos puedan disfrutar de las promociones o estar informados de su actividad.</p>
''')

# --------------------------------------------------------------------------

PAGINAS = [
    ('ciberseguridad.html', 'Ciberseguridad — Eudapro',
     'Qué exige la normativa de ciberseguridad (Directiva NIS, Real Decreto-ley 12/2018, Código de Derecho de la Ciberseguridad) y qué sanciones acarrea no adoptar las medidas necesarias.', ciber),
    ('videovigilancia.html', 'Videovigilancia — Eudapro',
     'Cámaras de seguridad conformes a la guía de la AEPD: cartel informativo, cláusula completa, conservación máxima de 30 días y atención de los derechos de las personas grabadas.', video),
    ('blanqueo-de-capitales.html', 'Prevención del blanqueo de capitales — Eudapro',
     'Adaptación a la Ley 10/2010 de Prevención del Blanqueo de Capitales: servicios LPBC Diligence y LPBC Integral, representante ante el SEPBLAC, política interna y auditoría anual.', blanqueo),
    ('formacion.html', 'Formación bonificada — Eudapro',
     'Cursos online de RGPD, ciberseguridad, blanqueo de capitales y manipulación de alimentos, bonificables con el crédito de FUNDAE. Catálogo y guías didácticas descargables.', formacion),
    ('colectivos.html', 'Colectivos con convenio — Eudapro',
     'Convenios con gremios, federaciones y asociaciones: Gremi de Restauració de Barcelona desde 2016, Alt Penedès, FIHRT, Bages, Anoia y Ehlis / Cadena 88.', colectivos),
    ('conocenos.html', 'Conócenos — Eudapro',
     'Quiénes somos y por qué trabajamos a medida, en persona y sin cuota de mantenimiento. Datos de la empresa EUDAPRO, S.L.', conocenos),
    ('recursos.html', 'Recursos y descargas — Eudapro',
     'Boletines RGPD, notas informativas, guías didácticas y catálogos de formación en PDF, en abierto y sin registro.', recursos),
    ('contacto.html', 'Contacto — Eudapro',
     'Teléfono gratuito 900 929 806, correo info@allins4b.com y formulario de contacto con doble consentimiento diferenciado.', contacto),
    ('aviso-legal.html', 'Aviso legal — Eudapro', 'Aviso legal del sitio web de EUDAPRO, S.L.', aviso_legal),
    ('politica-de-privacidad.html', 'Política de privacidad — Eudapro', 'Política de privacidad de EUDAPRO, S.L.', privacidad),
    ('politica-de-cookies.html', 'Política de cookies — Eudapro', 'Política de cookies de EUDAPRO, S.L.', cookies),
    ('politica-redes-sociales.html', 'Política de redes sociales — Eudapro', 'Política de redes sociales de EUDAPRO, S.L.', redes),
]

if __name__ == '__main__':
    print('Generando páginas…')
    for archivo, titulo, desc, cuerpo in PAGINAS:
        pagina(archivo, titulo, desc, cuerpo)
    print('Listo: %d páginas.' % len(PAGINAS))
