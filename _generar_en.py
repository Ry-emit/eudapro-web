#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la versión en inglés de eudapro-site (carpeta en/).

Mismo sistema que _generar.py: la cabecera y el pie se escriben una vez y el
script vuelca las páginas ya montadas. Aquí TODO el texto va en inglés; el
español vive en _generar.py y no se mezclan.

    python3 _generar_en.py

en/index.html y en/data-protection.html están escritas a mano y NO se tocan.
Los ficheros comunes (css, js, imágenes y documentos) se comparten con la web
en español y se enlazan con ../assets/.
"""

import os
import re
import unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, 'en')

MARCA_CABECERA = '<img class="marca__logo" src="../assets/img/marca/eudapro-marca.webp" alt="Eudapro" width="523" height="96">'
MARCA_PIE = '<img class="marca__logo marca__logo--completo" src="../assets/img/marca/eudapro-logo.webp" alt="Eudapro, European Data Protect: data protection" width="637" height="196">'

SERVICIOS = [
    ('data-protection.html', 'Data protection', 'GDPR and LOPDGDD · DPO included'),
    ('video-surveillance.html', 'Video surveillance', 'Cameras compliant with the AEPD'),
]

SUELTAS = [('member-associations.html', 'associations'), ('resources.html', 'resources'), ('about-us.html', 'about us')]

# Cada página en inglés y su equivalente en español (una carpeta más arriba).
IDIOMAS = {
    'index.html': '../index.html',
    'data-protection.html': '../proteccion-de-datos.html',
    'video-surveillance.html': '../videovigilancia.html',
    'member-associations.html': '../colectivos.html',
    'resources.html': '../recursos.html',
    'about-us.html': '../conocenos.html',
    'contact.html': '../contacto.html',
    'legal-notice.html': '../aviso-legal.html',
    'privacy-policy.html': '../politica-de-privacidad.html',
    'cookies-policy.html': '../politica-de-cookies.html',
    'social-media-policy.html': '../politica-redes-sociales.html',
}


def selector_idioma(archivo):
    return '''  <p class="idiomas" role="group" aria-label="Language">
    <a href="%s" hreflang="es" lang="es">ES</a>
    <span class="idiomas__on" aria-current="true">EN</span>
  </p>''' % IDIOMAS[archivo]


def cabecera(archivo):
    servicios = '\n'.join(
        '        <a href="%s"%s>%s <small>%s</small></a>' %
        (h, ' aria-current="page"' if h == archivo else '', t, s)
        for h, t, s in SERVICIOS)
    sueltas = '\n'.join(
        '    <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == archivo else '', t)
        for h, t in SUELTAS)
    return '''<a class="saltar" href="#principal">Skip to content</a>
<div class="progreso" aria-hidden="true"><i id="linea-progreso"></i></div>
<div class="scanline" aria-hidden="true"></div>

<header class="cabecera" id="cabecera">
  <a class="marca" href="index.html" aria-label="Eudapro, home">
    %s
  </a>
  <nav class="nav" id="nav" aria-label="Main navigation">
    <a href="index.html">home</a>
    <div class="desplegable" data-abierto="no">
      <button class="desplegable__btn" type="button" aria-expanded="false">services</button>
      <div class="desplegable__panel">
%s
      </div>
    </div>
%s
  </nav>
%s
  <a class="cabecera__cta" href="contact.html">Get in touch</a>
  <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span></button>
</header>''' % (MARCA_CABECERA, servicios, sueltas, selector_idioma(archivo))


PIE = '''<footer class="pie">
  <div class="wrap">
    <div class="pie__grid">
      <div>
        <a class="marca pie__marca" href="index.html" aria-label="Eudapro, home">
    %s
        </a>
        <p class="pie__nota">Data protection consultancy for small and medium-sized companies, across Spain.</p>
      </div>
      <div>
        <h3>Services</h3>
        <ul>
          <li><a href="data-protection.html">Data protection</a></li>
          <li><a href="video-surveillance.html">Video surveillance</a></li>
        </ul>
      </div>
      <div>
        <h3>Company</h3>
        <ul>
          <li><a href="about-us.html">About us</a></li>
          <li><a href="member-associations.html">Trade associations</a></li>
          <li><a href="resources.html">Resources and downloads</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3>Contact</h3>
        <address>
          <a href="tel:+34900929806">900 929 806</a><br>
          <a href="mailto:info@eudapro.es">info@eudapro.es</a><br><br>
          C/ Irlanda, 7 — 08030 Barcelona
        </address>
      </div>
    </div>
    <div class="pie__legal">
      <span>© <span data-anyo>2026</span> EUDAPRO, S.L. — VAT no. B75390377</span>
      <span>
        <a href="legal-notice.html">Legal notice</a> ·
        <a href="privacy-policy.html">Privacy</a> ·
        <a href="cookies-policy.html">Cookies</a> ·
        <a href="social-media-policy.html">Social media</a> ·
        <a href="#" data-abrir-cookies>Cookie settings</a>
      </span>
      <span>Fonts served from this domain. Analytics cookies only with your consent.</span>
    </div>
  </div>
</footer>''' % MARCA_PIE


def pagina(archivo, titulo, descripcion, cuerpo):
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<link rel="alternate" hreflang="en" href="%s">
<link rel="alternate" hreflang="es" href="%s">
<link rel="alternate" hreflang="x-default" href="%s">
<link rel="icon" href="../assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="../assets/css/eudapro.css">
</head>
<body>

%s

<main id="principal">
%s
</main>

%s

<script src="../assets/js/ui.js"></script>
<script src="../assets/js/cookies.js"></script>
</body>
</html>
''' % (titulo, descripcion, archivo, IDIOMAS[archivo], IDIOMAS[archivo],
       cabecera(archivo), cuerpo, PIE)
    with open(os.path.join(SALIDA, archivo), 'w', encoding='utf-8') as f:
        f.write(html)
    print('  escrito  en/%s' % archivo)


def portada(migas, kicker, h1, lede, icono='', acciones=True):
    botones = ''
    if acciones:
        botones = '''
          <div class="paso__cta mt-m">
            <a class="btn btn--pri" href="contact.html">Get in touch</a>
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
          <span class="kicker kicker--amber">Initial audit</span>
          <h2>%s</h2>
          <p>%s</p>
        </div>
        <div class="cta-banda__acciones">
          <a class="btn btn--pri" href="contact.html">Get in touch</a>
          <a class="btn btn--sec btn--tel" href="tel:+34900929806">900 929 806</a>
        </div>
      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------------------
# Iconos decorativos de portada (los mismos que en la web en español)
# --------------------------------------------------------------------------

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
# VIDEO SURVEILLANCE
# --------------------------------------------------------------------------

video = portada(
    '<a href="index.html">Home</a> / Services / Video surveillance',
    'Service', 'Video surveillance',
    'Having cameras is legal. Having them with no sign, no privacy notice, no retention period and no way of answering someone who asks for their footage is not. We bring your installation in line with the guidance of the Spanish Data Protection Agency.',
    ICO_OJO) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">What the law asks of you</span>
        <h2>Four things an inspector will look at</h2>
      </div>
      <div class="rejilla rejilla--4">
        <div class="tarjeta" data-aparece><h3>Information sign</h3><p>Visible in the monitored area, before anyone enters, with the basic information about the processing and who to contact.</p></div>
        <div class="tarjeta" data-aparece><h3>Full privacy notice</h3><p>The detailed information, available to anyone who asks for it: purpose, legal basis, recipients and rights.</p></div>
        <div class="tarjeta tarjeta--destacada" data-aparece><h3>30 days maximum</h3><p>Footage is kept for a maximum of 30 days, unless it has to be given to the police, courts or tribunals.</p></div>
        <div class="tarjeta" data-aparece><h3>Rights handled</h3><p>Knowing how to answer someone who asks to access their footage, to have it corrected or deleted, or who objects to the processing.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div data-aparece>
          <span class="kicker">Download</span>
          <h2>The video-surveillance sign</h2>
          <p>This is the sign that has to be displayed somewhere visible, before anyone enters the monitored area. Download it, print it and fill in the controller's details.</p>
          <p>If you would rather we did it, we set it up during the adaptation together with the privacy notice and the record of processing activities.</p>
          <div class="paso__cta">
            <a class="btn btn--pri" href="../assets/img/contenido/cartel-videovigilancia.png" download>Download the sign</a>
            <a class="btn btn--sec" href="contact.html">Have us do it</a>
          </div>
        </div>
        <div class="lamina" data-aparece>
          <img src="../assets/img/contenido/cartel-videovigilancia.png" alt="Information sign for a video-monitored area" loading="lazy">
        </div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="encabezado" data-aparece>
        <span class="kicker">Privacy notice</span>
        <h2>Processing of video-surveillance data</h2>
        <p>This is the full text of the processing, as anyone who is filmed must be able to read it.</p>
      </div>
      <div class="acordeon" data-aparece>
        <details open>
          <summary>For what purpose do we process your personal data?</summary>
          <div class="acordeon__cuerpo">
            <p>We process the information provided by data subjects in order to guarantee the safety of people, property and premises through video-surveillance systems. If you do not provide your personal data, we will not be able to fulfil the purposes described.</p>
            <p>No automated decisions will be taken on the basis of the data provided.</p>
          </div>
        </details>
        <details>
          <summary>How long will we keep your data?</summary>
          <div class="acordeon__cuerpo">
            <p>The data will be kept for a maximum of 30 days, unless it has to be disclosed to the State security forces and/or to courts and tribunals.</p>
          </div>
        </details>
        <details>
          <summary>What is the legal basis for processing your data?</summary>
          <div class="acordeon__cuerpo">
            <p>Task carried out in the public interest: processing necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller (GDPR, art. 6.1.e), as set out in the “Guide on the use of video cameras for security and other purposes” published by the Spanish Data Protection Agency.</p>
          </div>
        </details>
        <details>
          <summary>Who will your data be disclosed to?</summary>
          <div class="acordeon__cuerpo">
            <p>Where applicable, to the State security forces and to courts and tribunals, in order to provide the footage if an offence has been committed (legal requirement).</p>
            <p>No international data transfers are envisaged.</p>
          </div>
        </details>
        <details>
          <summary>What are your rights when you give us your data?</summary>
          <div class="acordeon__cuerpo">
            <p>Anyone has the right to obtain confirmation as to whether or not the controller is processing personal data concerning them.</p>
            <p>Data subjects have the right to access their personal data, to ask for inaccurate data to be corrected or, where appropriate, to ask for it to be erased when, among other reasons, the data is no longer necessary for the purposes for which it was collected. They also have the right to data portability.</p>
            <p>In certain circumstances, data subjects may ask for the processing of their data to be restricted, in which case we will only keep it for the exercise or defence of claims.</p>
            <p>In certain circumstances, and on grounds relating to their particular situation, data subjects may object to the processing of their data. In that case the controller will stop processing the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
            <p>You may exercise your rights in practice by going to the premises or offices where the footage is recorded, or by sending a request to the controller's e-mail address.</p>
            <p>Where commercial communications are sent on the basis of the controller's legitimate interest, the data subject may object to their data being processed for that purpose.</p>
            <p>If you believe your data protection rights have been infringed, especially if you have not obtained satisfaction when exercising them, you may lodge a complaint with the competent data protection supervisory authority through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
          </div>
        </details>
        <details>
          <summary>How did we obtain your data?</summary>
          <div class="acordeon__cuerpo">
            <p>The personal data comes from images recorded by security cameras. The categories of data processed are identification data.</p>
          </div>
        </details>
      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------------------
# MEMBER ASSOCIATIONS
# --------------------------------------------------------------------------

colectivos = portada(
    '<a href="index.html">Home</a> / Trade associations',
    'Channel', 'Trade associations',
    'We work with trade guilds, federations and associations. They recommend a provider who already knows their sector; their members get a special offer and someone who speaks their language. These are the agreements we have signed.',
    ICO_RED) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:center">
        <div data-aparece>
          <span class="kicker">Since 2016</span>
          <h2>Gremi de Restauració de Barcelona</h2>
          <p>Since 2016 we have offered, together with the Barcelona restaurant guild, a complete data protection service. With this offer its members are brought into line with the GDPR.</p>
          <p>Eudapro is listed in the guild's Suppliers Guide.</p>
          <div class="paso__cta">
            <a class="btn btn--pri" href="contact.html">I am a member</a>
          </div>
        </div>
        <div data-aparece>
          <div style="border:1px solid var(--line); border-radius:16px; padding:24px; background:var(--card)">
            <img src="../assets/img/gremios/gremi-web.png" alt="Gremi de Restauració de Barcelona" loading="lazy">
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">Other agreements</span>
        <h2>Guilds, federations and networks with an offer for their members</h2>
      </div>
      <div class="rejilla rejilla--3">
        <div class="tarjeta" data-aparece>
          <img src="../assets/img/clientes/gremi-alt-penedes.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1); opacity:.85">
          <h3>Gremi Comarcal d'Hostaleria i Turisme de l'Alt Penedès</h3>
          <p>Agreement signed with the county hospitality guild. On-site adaptation, no maintenance fee, and questions and legal advice all year round.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="../assets/img/clientes/fhirt.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1); opacity:.85">
          <h3>Federació Intercomarcal d'Hostaleria, Restauració i Turisme</h3>
          <p>Agreement with the federation and, by extension, with the guilds that belong to it.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="../assets/img/clientes/cadena-88.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1); opacity:.85">
          <h3>Ehlis / Cadena 88</h3>
          <p>A special offer for the members of this hardware store network: a complete GDPR service that brings the business into line with the European regulation.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <img src="../assets/img/clientes/gremi-bages.png" alt="" style="height:44px; width:auto; object-fit:contain; margin-bottom:18px; filter:grayscale(1); opacity:.85">
          <h3>Gremi d'Hostaleria i Turisme del Bages</h3>
          <p>Work with the county guild of Bages, around Manresa and Sant Fruitós.</p>
        </div>
        <div class="tarjeta" data-aparece>
          <h3>Gremi d'Hostaleria i Turisme de l'Anoia</h3>
          <p>Agreement signed with the guild of the Anoia county.</p>
        </div>
        <div class="tarjeta tarjeta--destacada" data-aparece>
          <h3>Do you represent an association?</h3>
          <p>If you are a guild, federation, association or buying group and you want an offer for your members, let's talk. We prepare the offer and the information material.</p>
          <div class="tarjeta__pie"><a class="enlace-flecha" href="contact.html">Propose an agreement</a></div>
        </div>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ('Are you a member of any of these associations?',
                   'Tell us which one you belong to and we will apply the terms of the agreement.')

# --------------------------------------------------------------------------
# ABOUT US
# --------------------------------------------------------------------------

conocenos = portada(
    '<a href="index.html">Home</a> / About us',
    'Company', 'About us',
    'We are a data protection consultancy based in Barcelona. We work with small and medium-sized companies across Spain: restaurants, hardware stores, clubs, schools, clinics and family businesses.',
    ICO_LLAVE, acciones=False) + '''
  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
        <span class="kicker">In the first person</span>
        <h2>Why we work the way we do</h2>
        <p>At Eudapro we do not believe in off-the-shelf products, just as there are no off-the-shelf people or companies. We only work on a personalised product, made to measure, so that we cover everything our clients need and grow alongside them, keeping up with every new business challenge that comes our way. Welcome: we are here to help you, and your trust is our greatest asset.</p>
        <p>We like working to our clients' measure. As well as providing our services, we do it in a way that makes it easy for you to adapt to the new regulation. That is why we give you every contract and clause personalised for your company: that way we can take care of all the <em>back office</em> this generates and you can keep growing in your sector without worrying about anything else.</p>
        <p>We are also trained to act as your DPO (Data Protection Officer) at no extra cost.</p>
        <p style="margin-top:2em"><strong>Isaac Higueras</strong><br><span style="font-family:var(--mono); font-size:12px; letter-spacing:.1em; color:var(--ink-3)">CEO</span></p>
      </div>
    </div>
  </section>

  <section class="bloque bloque--alt">
    <div class="wrap">
      <div class="encabezado" data-aparece>
        <span class="kicker">In short</span>
        <h2>Four things that define us</h2>
      </div>
      <div class="rejilla rejilla--4">
        <div class="tarjeta" data-aparece><h3>On site</h3><p>We come to your company. The adaptation is not done over the phone or through a form.</p></div>
        <div class="tarjeta" data-aparece><h3>No fees</h3><p>No maintenance fee. Questions and legal advice all year round are included.</p></div>
        <div class="tarjeta" data-aparece><h3>DPO included</h3><p>We act as your Data Protection Officer at no extra cost.</p></div>
        <div class="tarjeta" data-aparece><h3>With associations</h3><p>Agreements with guilds and federations since 2016, mostly in hospitality.</p></div>
      </div>
    </div>
  </section>

  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
        <h2>Company details</h2>
        <dl>
          <dt>Registered name</dt><dd>EUDAPRO, S.L.</dd>
          <dt>Trading name</dt><dd>Eudapro</dd>
          <dt>VAT number</dt><dd>B75390377</dd>
          <dt>Address</dt><dd>C/ Irlanda, 7 — 08030 Barcelona</dd>
          <dt>Phone</dt><dd><a href="tel:+34900929806">900 929 806</a> (freephone)</dd>
          <dt>E-mail</dt><dd><a href="mailto:info@eudapro.es">info@eudapro.es</a></dd>
          <dt>CEO</dt><dd>Isaac Higueras</dd>
        </dl>
      </div>
    </div>
  </section>
''' + CTA_FINAL % ("Let's talk, with no commitment",
                   'Tell us what you do and what you already have in place. The first conversation costs nothing.')

# --------------------------------------------------------------------------
# RESOURCES
# --------------------------------------------------------------------------

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
         'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
MESES_EN = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']


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


def pdfs(carpeta):
    ruta = os.path.join(RAIZ, 'assets', 'doc', carpeta)
    if not os.path.isdir(ruta):
        return []
    return [(unicodedata.normalize('NFC', f), os.path.join(ruta, f))
            for f in sorted(os.listdir(ruta)) if f.lower().endswith('.pdf') and not f.startswith('.')]


def listar_boletines():
    filas = []
    for f, ruta in pdfs('boletines'):
        plano = sin_tildes(f)
        if 'bolet' not in plano:
            continue
        mes = next((m for m in MESES if m in plano), None)
        anyo = re.search(r'20\d{2}', f)
        anyo = anyo.group(0) if anyo else ''
        nombre = MESES_EN[MESES.index(mes)] if mes else ''
        titulo = ('GDPR bulletin — %s %s' % (nombre, anyo)).strip()
        orden = (anyo or '0000', '%02d' % (MESES.index(mes) + 1 if mes else 0))
        filas.append((orden, item('../assets/doc/boletines/' + f, titulo,
                                  'In Spanish · %s' % kb(ruta))))
    filas.sort(key=lambda x: x[0], reverse=True)
    return '\n'.join(f[1] for f in filas)


NOTAS = [
    ('info-derechos-llamadas-comerciales-no-solicitadas.pdf',
     'The right not to receive unsolicited marketing calls',
     'Spanish Data Protection Agency · Law 11/2022 on Telecommunications'),
]


def bloque_descargas(titulo, kicker, intro, filas, alt=False):
    if not filas:
        return ''
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
            out.append(item('../assets/doc/%s/%s' % (carpeta, unicodedata.normalize('NFC', archivo)),
                            titulo, '%s · %s' % (sub, kb(ruta))))
    return '\n'.join(out)


recursos = portada(
    '<a href="index.html">Home</a> / Resources',
    'Library', 'Resources and downloads',
    'Monthly bulletins and briefing notes whenever the rules change. All of it open, with no sign-up and without leaving your e-mail. The documents are published in Spanish.',
    ICO_DOC, acciones=False) + \
    bloque_descargas('GDPR bulletins', 'Monthly bulletin', 'Our round-up of what is new in data protection, issue by issue.',
                     listar_boletines()) + \
    bloque_descargas('Briefing notes', 'Notices', 'When something changes that affects our clients, we publish it here.',
                     filas_fijas('notas', NOTAS), alt=True) + \
    CTA_FINAL % ('Looking for a document that is not here?',
                 'If you need a particular note, or you would like the bulletin when it starts again, write to us.')

# --------------------------------------------------------------------------
# CONTACT
# --------------------------------------------------------------------------

contacto = portada(
    '<a href="index.html">Home</a> / Contact',
    'Contact', "Let's talk",
    'Tell us what you do and what you already have in place. We will reply with what you are missing in order to comply, with no commitment.',
    ICO_LLAVE, acciones=False) + '''
  <section class="bloque">
    <div class="wrap">
      <div class="rejilla rejilla--2" style="gap:clamp(34px,5vw,70px); align-items:start">

        <div data-aparece>
          <span class="kicker">Form</span>
          <h2>Write to us</h2>
          <form class="form mt-m" data-contacto novalidate>
            <div class="form__fila">
              <label class="campo"><span>Your name <em>*</em></span>
                <input type="text" name="nombre" maxlength="400" required autocomplete="name"></label>
              <label class="campo"><span>Your e-mail <em>*</em></span>
                <input type="email" name="correo" required autocomplete="email"></label>
            </div>
            <div class="form__fila">
              <label class="campo"><span>Phone</span>
                <input type="tel" name="telefono" autocomplete="tel"></label>
              <label class="campo"><span>Company or association</span>
                <input type="text" name="empresa" autocomplete="organization"></label>
            </div>
            <label class="campo"><span>Subject</span>
              <input type="text" name="asunto"></label>
            <label class="campo"><span>Your message</span>
              <textarea name="mensaje" placeholder="What you do, what you already have in place and what worries you."></textarea></label>

            <div class="consentimiento">
              <p>EUDAPRO, S.L. is committed to protecting and respecting your privacy, and we will only use your personal information to handle your request and provide the services you ask for. From time to time we would like to contact you about our products and services, as well as other content that may be of interest to you. If you agree to us contacting you for this purpose, please tick the box below:</p>
              <label class="check"><input type="checkbox" name="consent-comercial" value="si">
                <span>I agree to receive other communications from EUDAPRO, S.L.</span></label>

              <p>In order to handle your request, we need to store and process your personal data. If you agree to us storing your personal data for this purpose, please tick the box below.</p>
              <label class="check"><input type="checkbox" name="consent-tratamiento" value="si" required>
                <span>I agree to the processing of data of potential clients and web contacts (<a href="privacy-policy.html">+Info</a>). <em style="color:var(--amber); font-style:normal">*</em></span></label>

              <p class="form__aviso">You can unsubscribe from these communications at any time. For more information on how to unsubscribe, on how we handle personal data and on our commitment to protecting and respecting your privacy, please read our <a href="privacy-policy.html">Privacy Policy</a>.</p>
            </div>

            <div>
              <button class="btn btn--pri" type="submit">Send</button>
              <p class="form__estado" role="status" style="margin-top:14px"></p>
            </div>
          </form>
        </div>

        <div data-aparece>
          <span class="kicker">Direct</span>
          <h2>Or call us</h2>
          <p>The phone number is free of charge. If you prefer e-mail, that works too.</p>

          <div class="rejilla" style="gap:12px; margin-top:26px">
            <a class="tarjeta" href="tel:+34900929806">
              <div class="tarjeta__num">Freephone</div>
              <h3 style="margin:0">900 929 806</h3>
            </a>
            <a class="tarjeta" href="mailto:info@eudapro.es">
              <div class="tarjeta__num">E-mail</div>
              <h3 style="margin:0">info@eudapro.es</h3>
            </a>
          </div>

          <div class="prosa mt-l">
            <h3>Where we are</h3>
            <dl>
              <dt>Address</dt><dd>C/ Irlanda, 7 — 08030 Barcelona</dd>
              <dt>Registered name</dt><dd>EUDAPRO, S.L. — VAT no. B75390377</dd>
            </dl>
          </div>

          <div class="aviso aviso--violeta mt-m">
            <p><strong>We only ask for what we need.</strong> Your name and e-mail so we can reply; everything else is optional. This is what we do for a living: we are not going to do with your data what we tell our clients not to do.</p>
          </div>
        </div>

      </div>
    </div>
  </section>
'''

# --------------------------------------------------------------------------
# LEGAL PAGES
# --------------------------------------------------------------------------


def legal(kicker, h1, lede, prosa):
    return portada('<a href="index.html">Home</a> / %s' % h1, kicker, h1, lede, '', acciones=False) + '''
  <section class="bloque">
    <div class="wrap wrap--slim">
      <div class="prosa" data-aparece>
%s
      </div>
    </div>
  </section>
''' % prosa


# Traducción al inglés de los textos legales oficiales de Eudapro. El texto
# español vive en _generar.py; aquí va solo el inglés.

aviso_legal = legal('Legal', 'Legal notice',
                    'Terms of use of the EUDAPRO, S.L. website.', '''
        <h2>Purpose</h2>
        <p>This legal notice governs the use and utilisation of the website <a href="https://www.eudapro.es" target="_blank" rel="noopener">www.eudapro.es</a>, which is owned by EUDAPRO, S.L. (hereinafter, EUDAPRO).</p>
        <p>Browsing the EUDAPRO website confers upon you the status of USER thereof and entails your full and unreserved acceptance of each and every one of the conditions published in this legal notice, it being noted that those conditions may be amended by EUDAPRO without prior notification, in which case they will be published and notified as far in advance as possible.</p>
        <p>It is therefore advisable to read its content carefully should you wish to access and make use of the information and the services offered through this website.</p>
        <p>The user further undertakes to make correct use of the website in accordance with the law, good faith, public order, generally accepted trade practice and this Legal Notice, and shall be liable to EUDAPRO or to third parties for any damages that may be caused as a result of a breach of that obligation.</p>
        <p>Any use other than that authorised is expressly prohibited, and EUDAPRO may deny or withdraw access and use thereof at any time.</p>
        <h2>Identification</h2>
        <p>EUDAPRO, in compliance with Law 34/2002, of 11 July, on Information Society Services and Electronic Commerce, hereby informs you that:</p>
        <ul>
          <li>Its company name is: EUDAPRO, S.L.</li>
          <li>Its CIF is: B75390377</li>
          <li>Its registered office is at: Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA</li>
          <li>Barcelona Commercial Registry, Folio 1, Sheet B624236, Entry 1.</li>
        </ul>
        <h2>Communications</h2>
        <p>In order to communicate with us, we make available to you various means of contact, which are set out below:</p>
        <ul>
          <li>Tel.: 900929806</li>
          <li>Email: <a href="mailto:info@eudapro.es">info@eudapro.es</a></li>
        </ul>
        <p>All notifications and communications between users and EUDAPRO shall be deemed effective, for all purposes, when made through any of the means set out above.</p>
        <h2>Conditions of access and use</h2>
        <p>The website and its services are freely accessible and free of charge. However, EUDAPRO may make the use of some of the services offered on its website conditional upon the prior completion of the corresponding form.</p>
        <p>The user guarantees the authenticity and currency of all the data communicated to EUDAPRO and shall be solely responsible for any false or inaccurate statements made.</p>
        <p>The user expressly undertakes to make appropriate use of EUDAPRO's contents and services and not to use them, among other things, to:</p>
        <ul>
          <li>Disseminate criminal, violent, pornographic, racist, xenophobic or offensive content, content glorifying terrorism or, in general, content contrary to the law or to public order.</li>
          <li>Introduce computer viruses into the network or carry out acts liable to alter, damage, interrupt or generate errors or damage in the electronic documents, data or physical and logical systems of EUDAPRO or of third parties; as well as to hinder other users' access to the website and to its services through the massive consumption of the computer resources by means of which EUDAPRO provides its services.</li>
          <li>Attempt to access the email accounts of other users or restricted areas of the computer systems of EUDAPRO or of third parties and, where applicable, extract information.</li>
          <li>Infringe intellectual or industrial property rights, as well as breach the confidentiality of EUDAPRO's information or that of third parties.</li>
          <li>Impersonate any other user.</li>
          <li>Reproduce, copy, distribute, make available, or engage in any other form of public communication of, transform or modify the contents, unless the authorisation of the owner of the corresponding rights is held or this is legally permitted.</li>
          <li>Collect data for advertising purposes and send advertising of any kind and communications for sales purposes or others of a commercial nature without a prior request or consent to that effect.</li>
        </ul>
        <p>All the contents of the website, such as texts, photographs, graphics, images, icons, technology, software, as well as its graphic design and source codes, constitute a work the ownership of which belongs to EUDAPRO, and none of the exploitation rights over them may be deemed to be assigned to the user beyond what is strictly necessary for the correct use of the website.</p>
        <p>In short, users who access this website may view the contents and make, where applicable, authorised private copies, provided that the elements reproduced are not subsequently transferred to third parties, nor installed on servers connected to networks, nor subject to any kind of exploitation.</p>
        <p>Likewise, all trademarks, trade names or distinctive signs of any kind that appear on the website are the property of EUDAPRO, and the use of or access to it may not be deemed to grant the user any right over them.</p>
        <p>The distribution, modification, assignment or public communication of the contents and any other act that has not been expressly authorised by the owner of the exploitation rights are prohibited.</p>
        <p>The establishment of a hyperlink in no case implies the existence of a relationship between EUDAPRO and the owner of the website on which it is established, nor the acceptance and approval by EUDAPRO of its contents or services.</p>
        <p>EUDAPRO is not responsible for the use that each user makes of the materials made available on this website, nor for the acts that the user carries out on the basis of them.</p>
        <h2>Exclusion of warranties and of liability in respect of access and use</h2>
        <p>The content of this website is of a general nature and is intended merely for information purposes; full access to all the contents is not guaranteed, nor their completeness, correctness, validity or currency, nor their suitability or usefulness for a specific purpose.</p>
        <p>EUDAPRO excludes, to the extent permitted by law, any liability for damages of any nature arising from:</p>
        <ul>
          <li>The impossibility of accessing the website or the lack of truthfulness, accuracy, completeness and/or currency of the contents, as well as the existence of defects and faults of any kind in the contents transmitted, disseminated, stored or made available, or which have been accessed through the website or through the services offered.</li>
          <li>The presence of viruses or of other elements in the contents which may cause alterations to users' computer systems, electronic documents or data.</li>
          <li>The breach of the law, good faith, public order, generally accepted trade practice and this legal notice as a result of incorrect use of the website. In particular, and by way of example, EUDAPRO is not responsible for the acts of third parties that infringe intellectual and industrial property rights, trade secrets, rights to honour, to personal and family privacy and to one's own image, as well as the rules on unfair competition and unlawful advertising.</li>
        </ul>
        <p>Likewise, EUDAPRO disclaims any liability in respect of information that is located outside this website and is not managed directly by our webmaster. The function of the links that appear on this website is solely to inform the user of the existence of other sources capable of expanding the contents offered by this website. EUDAPRO neither guarantees nor is responsible for the operation or accessibility of the linked sites; nor does it suggest, invite or recommend visiting them, and it shall therefore not be responsible for the result obtained either. EUDAPRO is not responsible for the establishment of hyperlinks by third parties.</p>
        <h2>Procedure in the event of unlawful activities</h2>
        <p>In the event that any user or a third party considers that there are facts or circumstances revealing the unlawful nature of the use of any content and/or of the carrying out of any activity on the web pages included in or accessible through the website, they must send a notification to EUDAPRO, duly identifying themselves and specifying the alleged infringements.</p>
        <h2>Publications</h2>
        <p>The administrative information provided through the website does not replace the legal publication of laws, regulations, plans, general provisions and acts that must be formally published in the official gazettes of the public administrations, which constitute the only instrument attesting to their authenticity and content. The information available on this website must be understood as a guide with no purpose of legal validity.</p>
        <h2>Applicable legislation</h2>
        <p>These conditions shall be governed by the Spanish legislation in force.</p>
        <p>The language used shall be Spanish.</p>
''')

privacidad = legal('Legal', 'Privacy policy',
                   'The personal data processing carried out by EUDAPRO, S.L., section by section.', '''
        <p>At EUDAPRO, S.L. we care about privacy and transparency.</p>
        <p>Below, we set out in detail the processing of personal data that we carry out, together with all the information relating to it.</p>

        <div class="acordeon acordeon--legal">
          <details>
            <summary>Processing of client data</summary>
            <div class="acordeon__cuerpo">
              <h3>Basic information on data protection</h3>
              <dl>
                <dt>Controller</dt><dd>EUDAPRO, S.L.</dd>
                <dt>Purpose</dt><dd>To provide the services requested and to send promotional communications.</dd>
                <dt>Legal basis</dt><dd>Performance of a contract or pre-contractual measures.<br>Legitimate interest of the controller.</dd>
                <dt>Recipients</dt><dd>Data disclosures are envisaged to: Spanish Tax Authority; financial institutions.</dd>
                <dt>Rights</dt><dd>You have the right to access, rectify and erase the data, as well as other rights set out in the additional information, which you may exercise by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</dd>
                <dt>Source</dt><dd>The data subject</dd>
              </dl>
              <h3>Full information on data protection</h3>
              <h4>1. Who is the data controller of your data?</h4>
              <p>EUDAPRO, S.L.<br>B75390377<br>Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA<br>900929806<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>1.1 Contact details of the Data Protection Officer (DPO)</h4>
              <p>JOSEP TREVIÑO<br>C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>2. For what purpose do we process your personal data?</h4>
              <p>At EUDAPRO, S.L. we process the information provided to us by data subjects for the purpose of carrying out the administrative, accounting and tax management of the services requested, as well as sending promotional communications about our products and services. Should you not provide your personal data, we will not be able to fulfil the purposes described.</p>
              <p>No automated decisions will be taken on the basis of the data provided.</p>
              <h4>3. For how long will we keep your data?</h4>
              <p>The data will be kept for as long as the data subject does not request its erasure and, where applicable, for the years necessary to comply with legal obligations.</p>
              <h4>4. What is the legal basis for the processing of your data?</h4>
              <p>We set out below the legal basis for the processing of your data:</p>
              <ul>
                <li>Performance of a contract or pre-contractual measures: Tax, accounting and administrative management of clients. (GDPR, art. 6.1.b).</li>
                <li>Legitimate interest of the controller: Sending promotional communications, including by electronic means. (GDPR, Recital 47, LSSICE, art. 21.2).</li>
              </ul>
              <h4>5. To which recipients will your data be disclosed?</h4>
              <p>The data will be disclosed to the following recipients:</p>
              <ul>
                <li>Spanish Tax Authority, for the purpose of complying with legal obligations (legal requirement).</li>
                <li>Financial institutions, for the purpose of collecting the corresponding payments (contractual requirement).</li>
              </ul>
              <h4>6. International data transfers</h4>
              <p>No international data transfers are envisaged.</p>
              <h4>7. What are your rights when you provide us with your data?</h4>
              <p>Any person has the right to obtain confirmation as to whether or not we at EUDAPRO, S.L. are processing personal data concerning them.</p>
              <p>Data subjects have the right to access their personal data, as well as to request the rectification of inaccurate data or, where appropriate, to request its erasure when, among other reasons, the data is no longer necessary for the purposes for which it was collected. You likewise have the right to the portability of your data.</p>
              <p>In certain circumstances, data subjects may request the restriction of the processing of their data, in which case we will keep it solely for the exercise or defence of claims.</p>
              <p>In certain circumstances and on grounds relating to their particular situation, data subjects may object to the processing of their data. In this case, EUDAPRO, S.L. will cease to process the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
              <p>You may exercise your rights in practice as follows: by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</p>
              <p>Where commercial communications are sent using the legitimate interest of the controller as the legal basis, the data subject may object to the processing of their data for that purpose.</p>
              <p>If you have given your consent for a specific purpose, you have the right to withdraw the consent given at any time, without this affecting the lawfulness of the processing based on the consent prior to its withdrawal.</p>
              <p>Should you consider that your rights regarding the protection of your personal data have been infringed, especially where you have not obtained satisfaction in the exercise of your rights, you may lodge a complaint with the competent data protection supervisory authority through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
              <h4>8. How have we obtained your data?</h4>
              <p>The personal data that we process at EUDAPRO, S.L. comes from: The data subject.<br>The categories of data processed are:</p>
              <ul>
                <li>Identification data.</li>
                <li>Postal and e-mail addresses.</li>
                <li>Commercial information.</li>
                <li>Financial data.</li>
              </ul>
            </div>
          </details>
          <details>
            <summary>Processing of the data of potential clients and contacts</summary>
            <div class="acordeon__cuerpo">
              <h3>Basic information on data protection</h3>
              <dl>
                <dt>Controller</dt><dd>EUDAPRO, S.L.</dd>
                <dt>Purpose</dt><dd>To deal with your request and send you promotional communications</dd>
                <dt>Legal basis</dt><dd>Performance of a contract or pre-contractual measures.<br>Consent of the data subject.<br>Legitimate interest of the controller.</dd>
                <dt>Recipients</dt><dd>No data will be disclosed to third parties, except where required by law.</dd>
                <dt>Rights</dt><dd>You have the right to access, rectify and erase the data, as well as other rights set out in the additional information, which you may exercise by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</dd>
                <dt>Source</dt><dd>The data subject</dd>
              </dl>
              <h3>Full information on data protection</h3>
              <h4>1. Who is the data controller of your data?</h4>
              <p>EUDAPRO, S.L.<br>B75390377<br>Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA<br>900929806<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>1.1 Contact details of the Data Protection Officer (DPO)</h4>
              <p>JOSEP TREVIÑO<br>C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>2. For what purpose do we process your personal data?</h4>
              <p>At EUDAPRO, S.L. we process the information provided to us by data subjects for the purpose of managing potential clients who have shown an interest in our products and/or services, as well as other commercial contacts, and of sending, where applicable, promotional communications, including by electronic means. Should you not provide your personal data, we will not be able to fulfil the purposes described.</p>
              <p>No automated decisions will be taken on the basis of the data provided.</p>
              <h4>3. For how long will we keep your data?</h4>
              <p>The data will be kept for as long as the data subject does not request its erasure.</p>
              <h4>4. What is the legal basis for the processing of your data?</h4>
              <p>We set out below the legal basis for the processing of your data:</p>
              <ul>
                <li>Performance of a contract or pre-contractual measures: Management of potential clients who have shown an interest in our products and/or services. (GDPR, art. 6.1.b).</li>
                <li>Consent of the data subject: To send promotional communications, including by electronic means. (GDPR, art. 6.1.a, LSSICE, art. 21).</li>
                <li>Legitimate interest of the controller: Management of professional contact details (LOPDGDD, art. 19, GDPR, art. 6.1.f).</li>
              </ul>
              <h4>5. To which recipients will your data be disclosed?</h4>
              <p>No data will be disclosed to third parties, except where required by law.</p>
              <h4>6. International data transfers</h4>
              <p>No international data transfers are envisaged.</p>
              <h4>7. What are your rights when you provide us with your data?</h4>
              <p>Any person has the right to obtain confirmation as to whether or not we at EUDAPRO, S.L. are processing personal data concerning them.</p>
              <p>Data subjects have the right to access their personal data, as well as to request the rectification of inaccurate data or, where appropriate, to request its erasure when, among other reasons, the data is no longer necessary for the purposes for which it was collected. You likewise have the right to the portability of your data.</p>
              <p>In certain circumstances, data subjects may request the restriction of the processing of their data, in which case we will keep it solely for the exercise or defence of claims.</p>
              <p>In certain circumstances and on grounds relating to their particular situation, data subjects may object to the processing of their data. In this case, EUDAPRO, S.L. will cease to process the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
              <p>You may exercise your rights in practice as follows: by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</p>
              <p>Where commercial communications are sent using the legitimate interest of the controller as the legal basis, the data subject may object to the processing of their data for that purpose.</p>
              <p>If you have given your consent for a specific purpose, you have the right to withdraw the consent given at any time, without this affecting the lawfulness of the processing based on the consent prior to its withdrawal.</p>
              <p>Should you consider that your rights regarding the protection of your personal data have been infringed, especially where you have not obtained satisfaction in the exercise of your rights, you may lodge a complaint with the competent data protection supervisory authority through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
              <h4>8. How have we obtained your data?</h4>
              <p>The personal data that we process at EUDAPRO, S.L. comes from: The data subject.</p>
            </div>
          </details>
          <details>
            <summary>Processing of supplier data</summary>
            <div class="acordeon__cuerpo">
              <h3>Basic information on data protection</h3>
              <dl>
                <dt>Controller</dt><dd>EUDAPRO, S.L.</dd>
                <dt>Purpose</dt><dd>To manage the provision of the services contracted</dd>
                <dt>Legal basis</dt><dd>Performance of a contract or pre-contractual measures.<br>Legitimate interest of the controller.</dd>
                <dt>Recipients</dt><dd>Data disclosures are envisaged to: Spanish Tax Authority; financial institutions.</dd>
                <dt>Rights</dt><dd>You have the right to access, rectify and erase the data, as well as other rights set out in the additional information, which you may exercise by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</dd>
                <dt>Source</dt><dd>The data subject</dd>
              </dl>
              <h3>Full information on data protection</h3>
              <h4>1. Who is the data controller of your data?</h4>
              <p>EUDAPRO, S.L.<br>B75390377<br>Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA<br>900929806<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>1.1 Contact details of the Data Protection Officer (DPO)</h4>
              <p>JOSEP TREVIÑO<br>C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>2. For what purpose do we process your personal data?</h4>
              <p>At EUDAPRO, S.L. we process the information provided to us by data subjects for the purpose of carrying out the tax, accounting and administrative management of suppliers, as well as of professional contact details. Should you not provide your personal data, we will not be able to fulfil the purposes described.</p>
              <p>No automated decisions will be taken on the basis of the data provided.</p>
              <h4>3. For how long will we keep your data?</h4>
              <p>The data will be kept for as long as the data subject does not request its erasure and, where applicable, for the years necessary to comply with legal obligations.</p>
              <h4>4. What is the legal basis for the processing of your data?</h4>
              <p>We set out below the legal basis for the processing of your data:</p>
              <ul>
                <li>Performance of a contract or pre-contractual measures: Carrying out the administrative, accounting and tax management of the services contracted. (GDPR, art. 6.1.b).</li>
                <li>Legitimate interest of the controller: Management of professional contact details. (LOPDGDD, art. 19, GDPR, art. 6.1.f).</li>
              </ul>
              <h4>5. To which recipients will your data be disclosed?</h4>
              <p>The data will be disclosed to the following recipients:</p>
              <ul>
                <li>Spanish Tax Authority, for the purpose of complying with legal obligations (legal requirement).</li>
                <li>Financial institutions, for the purpose of making the corresponding payments (contractual requirement).</li>
              </ul>
              <h4>6. International data transfers</h4>
              <p>No international data transfers are envisaged.</p>
              <h4>7. What are your rights when you provide us with your data?</h4>
              <p>Any person has the right to obtain confirmation as to whether or not we at EUDAPRO, S.L. are processing personal data concerning them.</p>
              <p>Data subjects have the right to access their personal data, as well as to request the rectification of inaccurate data or, where appropriate, to request its erasure when, among other reasons, the data is no longer necessary for the purposes for which it was collected. You likewise have the right to the portability of your data.</p>
              <p>In certain circumstances, data subjects may request the restriction of the processing of their data, in which case we will keep it solely for the exercise or defence of claims.</p>
              <p>In certain circumstances and on grounds relating to their particular situation, data subjects may object to the processing of their data. In this case, EUDAPRO, S.L. will cease to process the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
              <p>You may exercise your rights in practice as follows: by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</p>
              <p>Where commercial communications are sent using the legitimate interest of the controller as the legal basis, the data subject may object to the processing of their data for that purpose.</p>
              <p>If you have given your consent for a specific purpose, you have the right to withdraw the consent given at any time, without this affecting the lawfulness of the processing based on the consent prior to its withdrawal.</p>
              <p>Should you consider that your rights regarding the protection of your personal data have been infringed, especially where you have not obtained satisfaction in the exercise of your rights, you may lodge a complaint with the competent data protection supervisory authority through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
              <h4>8. How have we obtained your data?</h4>
              <p>The personal data that we process at EUDAPRO, S.L. comes from: The data subject.<br>The categories of data processed are:</p>
              <ul>
                <li>Identification data.</li>
                <li>Postal and e-mail addresses.</li>
                <li>Commercial information.</li>
                <li>Financial data.</li>
              </ul>
            </div>
          </details>          <details>
            <summary>Processing of newsletter subscribers' data</summary>
            <div class="acordeon__cuerpo">
              <h3>Basic information on data protection</h3>
              <dl>
                <dt>Data controller</dt><dd>EUDAPRO, S.L.</dd>
                <dt>Purpose</dt><dd>To send you our newsletter and other promotional communications of interest</dd>
                <dt>Legal basis</dt><dd>Consent of the data subject.</dd>
                <dt>Recipients</dt><dd>No data will be disclosed to third parties, except where required by law.</dd>
                <dt>Rights</dt><dd>You have the right to access, rectify and erase the data, as well as other rights set out in the additional information, which you may exercise by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</dd>
                <dt>Source</dt><dd>The data subject themselves</dd>
              </dl>
              <h3>Full information on data protection</h3>
              <h4>1. Who is the data controller for your data?</h4>
              <p>EUDAPRO, S.L.<br>B75390377<br>Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA<br>900929806<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>1.1 Contact details of the Data Protection Officer (DPO)</h4>
              <p>JOSEP TREVIÑO<br>C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>2. For what purpose do we process your personal data?</h4>
              <p>At EUDAPRO, S.L. we process the information provided to us by data subjects in order to send our newsletter and other promotional communications of interest to its subscribers. If you do not provide your personal data, we will not be able to fulfil the purposes described.</p>
              <p>No automated decisions will be taken on the basis of the data provided.</p>
              <h4>3. How long will we keep your data?</h4>
              <p>The data will be kept for as long as the data subject does not request its erasure.</p>
              <h4>4. What is the legal basis for the processing of your data?</h4>
              <p>The legal basis for the processing of your data is set out below:</p>
              <ul>
                <li>Consent of the data subject: sending our newsletter and other promotional communications of interest to its subscribers (GDPR, art. 6.1.a, and LSSICE art.21)</li>
              </ul>
              <h4>5. To which recipients will your data be disclosed?</h4>
              <p>No data will be disclosed to third parties, except where required by law.</p>
              <h4>6. Transfers of data to third countries</h4>
              <p>No transfers of data to third countries are envisaged.</p>
              <h4>7. What are your rights when you provide us with your data?</h4>
              <p>Any person has the right to obtain confirmation as to whether or not EUDAPRO, S.L. is processing personal data concerning them.</p>
              <p>Data subjects have the right to access their personal data, as well as to request the rectification of inaccurate data or, where appropriate, to request its erasure when, among other reasons, the data is no longer necessary for the purposes for which it was collected. You likewise have the right to the portability of your data.</p>
              <p>In certain circumstances, data subjects may request the restriction of the processing of their data, in which case we will only keep it for the exercise or defence of claims.</p>
              <p>In certain circumstances and on grounds relating to their particular situation, data subjects may object to the processing of their data. In this case, EUDAPRO, S.L. will stop processing the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
              <p>You may exercise your rights in practice as follows: by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</p>
              <p>Where commercial communications are sent using the legitimate interest of the data controller as the legal basis, the data subject may object to the processing of their data for that purpose.</p>
              <p>If you have given your consent for a specific purpose, you have the right to withdraw the consent given at any time, without this affecting the lawfulness of the processing based on the consent prior to its withdrawal.</p>
              <p>If you consider that your rights regarding the protection of your personal data have been infringed, especially where you have not obtained satisfaction in the exercise of your rights, you may lodge a complaint with the competent supervisory authority for data protection through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
              <h4>8. How did we obtain your data?</h4>
              <p>The personal data we process at EUDAPRO, S.L. comes from: The data subject themselves.<br>The categories of data processed are:</p>
              <ul>
                <li>Identification data.</li>
                <li>Postal and e-mail addresses.</li>
                <li>Commercial information.</li>
              </ul>
            </div>
          </details>
          <details>
            <summary>Processing of staff data</summary>
            <div class="acordeon__cuerpo">
              <h3>Basic information on data protection</h3>
              <dl>
                <dt>Data controller</dt><dd>EUDAPRO, S.L.</dd>
                <dt>Purpose</dt><dd>To manage the employment relationship</dd>
                <dt>Legal basis</dt><dd>Performance of a contract or pre-contractual measures.<br>Compliance with a legal obligation.</dd>
                <dt>Recipients</dt><dd>Disclosures of data are envisaged to: the Spanish Tax Authority, Social Security and the mutual insurance company; banks and financial institutions; the Spanish state foundation for workplace training (Fundae).</dd>
                <dt>Rights</dt><dd>You have the right to access, rectify and erase the data, as well as other rights set out in the additional information, which you may exercise by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</dd>
                <dt>Source</dt><dd>The data subject themselves</dd>
              </dl>
              <h3>Full information on data protection</h3>
              <h4>1. Who is the data controller for your data?</h4>
              <p>EUDAPRO, S.L.<br>B75390377<br>Plaça Fius i Palà, n.º 1, Esc. Izq, 3º 2ª - 08241 - Manresa - BARCELONA<br>900929806<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>1.1 Contact details of the Data Protection Officer (DPO)</h4>
              <p>JOSEP TREVIÑO<br>C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA<br><a href="mailto:info@eudapro.es">info@eudapro.es</a></p>
              <h4>2. For what purpose do we process your personal data?</h4>
              <p>At EUDAPRO, S.L. we process the information provided to us by data subjects in order to carry out HR management; training; occupational risk prevention and health surveillance; the preparation of payroll and social security contributions; working time records; workplace accidents, where applicable. If you do not provide your personal data, we will not be able to fulfil the purposes described.</p>
              <p>No automated decisions will be taken on the basis of the data provided.</p>
              <h4>3. How long will we keep your data?</h4>
              <p>For as long as the employment relationship with the entity is maintained and for the years necessary to comply with legal obligations.</p>
              <h4>4. What is the legal basis for the processing of your data?</h4>
              <p>The legal basis for the processing of your data is set out below:</p>
              <ul>
                <li>Performance of a contract or pre-contractual measures: HR management, training and skills development. (GDPR art.6.1.b).</li>
                <li>Compliance with a legal obligation: Occupational risk prevention and health surveillance; the preparation of payroll and social security contributions; working time records; the management of workplace accidents, where applicable. (Law 31/1995, of 8 November, on the Prevention of Occupational Risks; Royal Legislative Decree 2/2015, of 23 October, approving the consolidated text of the Workers' Statute Act; Royal Legislative Decree 8/2015, of 30 October, approving the consolidated text of the General Social Security Act; Royal Decree-Law 8/2019, of 8 March, on urgent social protection measures and measures to combat job insecurity in working hours; GDPR, arts. 6.1.c and 9.2.b). Royal Decree 902/2020, of 13 October, on equal pay for women and men.</li>
              </ul>
              <h4>5. To which recipients will your data be disclosed?</h4>
              <p>The data will be disclosed to the following recipients:</p>
              <ul>
                <li>The Spanish Tax Authority, Social Security and the mutual insurance company, for the purpose of filing taxes and meeting the obligations relating to social security contributions (legal requirement).</li>
                <li>Banks and financial institutions, for the purpose of making payroll payments (contractual requirement).</li>
                <li>The Spanish state foundation for workplace training (Fundae), for the purpose of managing the subsidy for employee training (contractual requirement).</li>
              </ul>
              <h4>6. Transfers of data to third countries</h4>
              <p>No transfers of data to third countries are envisaged.</p>
              <h4>7. What are your rights when you provide us with your data?</h4>
              <p>Any person has the right to obtain confirmation as to whether or not EUDAPRO, S.L. is processing personal data concerning them.</p>
              <p>Data subjects have the right to access their personal data, as well as to request the rectification of inaccurate data or, where appropriate, to request its erasure when, among other reasons, the data is no longer necessary for the purposes for which it was collected. You likewise have the right to the portability of your data.</p>
              <p>In certain circumstances, data subjects may request the restriction of the processing of their data, in which case we will only keep it for the exercise or defence of claims.</p>
              <p>In certain circumstances and on grounds relating to their particular situation, data subjects may object to the processing of their data. In this case, EUDAPRO, S.L. will stop processing the data, except on compelling legitimate grounds, or for the exercise or defence of possible claims.</p>
              <p>You may exercise your rights in practice as follows: by contacting <a href="mailto:info@eudapro.es">info@eudapro.es</a> or C/ IRLANDA, 7, LOCAL 1, BAJOS, 08030, BARCELONA.</p>
              <p>Where commercial communications are sent using the legitimate interest of the data controller as the legal basis, the data subject may object to the processing of their data for that purpose.</p>
              <p>If you have given your consent for a specific purpose, you have the right to withdraw the consent given at any time, without this affecting the lawfulness of the processing based on the consent prior to its withdrawal.</p>
              <p>If you consider that your rights regarding the protection of your personal data have been infringed, especially where you have not obtained satisfaction in the exercise of your rights, you may lodge a complaint with the competent supervisory authority for data protection through its website: <a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>.</p>
              <h4>8. How did we obtain your data?</h4>
              <p>The personal data we process at EUDAPRO, S.L. comes from: The data subject themselves.<br>The categories of data processed are:</p>
              <ul>
                <li>Identification data.</li>
                <li>Postal and e-mail addresses.</li>
                <li>Financial data.</li>
              </ul>
            </div>
          </details>
        </div>
''')

cookies = legal('Legal', 'Cookies policy',
                'Which cookies this site uses, what they are for and how to configure them.', '''
        <h2>What are cookies?</h2>
        <p>This website uses cookies and/or similar technologies that store and retrieve information when you browse. In general, these technologies may serve a wide variety of purposes, such as recognising you as a user, obtaining information about your browsing habits, or personalising the way in which content is displayed. The specific uses we make of these technologies are described below.</p>
        <h2>Why does this website use cookies and which ones are they?</h2>
        <p>The identification of who uses the cookies, the type of cookies used and other details are set out below:</p>
        <p>The cookies used on this website are as follows:</p>
        <div class="tabla-envoltorio">
          <table>
            <thead><tr><th>Cookies</th><th>Name</th><th>Type</th><th>Purpose</th><th>Further information</th></tr></thead>
            <tbody><tr><td>_ga, _ga_&lt;ID&gt;</td><td>Google Analytics</td><td>Third-party</td><td>To collect information about users' browsing of the site in order to ascertain the origin of visits and other similar data at a statistical level. It does not obtain data on users' first names or surnames, nor on the specific postal address from which they connect</td><td>Google Analytics · Google Privacy Centre: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a></td></tr></tbody>
          </table>
        </div>
        <p>Analytics: these are the cookies which, whether processed by us or by third parties, allow us to quantify the number of users and thus carry out the measurement and statistical analysis of the use that users make of the service. Your browsing on our website is therefore analysed in order to improve the user experience.</p>
        <p>Note: 'First-party' cookies are used only by the owner of this website, and 'Third-party' cookies are used by the service provider set out in the table above.</p>
        <h2>How can I disable or delete these cookies?</h2>
        <p>You may allow, block or delete the cookies installed on your device through the settings of the browser installed on your computer:</p>
        <ul class="lista">
          <li><a href="http://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-que-los-sitios-we" target="_blank" rel="noopener">Firefox</a></li>
          <li><a href="http://support.google.com/chrome/bin/answer.py?hl=es&answer=95647" target="_blank" rel="noopener">Chrome</a></li>
          <li><a href="https://support.microsoft.com/es-es/windows/eliminar-y-administrar-cookies-168dab11-0753-043d-7c16-ede5947fc64d" target="_blank" rel="noopener">Explorer</a></li>
          <li><a href="http://support.apple.com/kb/ph5042" target="_blank" rel="noopener">Safari</a></li>
          <li><a href="http://help.opera.com/Windows/11.50/es-ES/cookies.html" target="_blank" rel="noopener">Opera</a></li>
        </ul>
        <h3>Other browsers</h3>
        <p>Please consult the documentation of the browser you have installed.</p>
        <h3>Google Analytics opt-out browser add-on</h3>
        <p>If you wish to refuse Google Analytics analytics cookies in all browsers, so that no information about you is sent to Google Analytics, you may download an add-on that performs this function from this link: <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">https://tools.google.com/dlpage/gaoptout</a>.</p>
        <h2>Configuring the cookies on this website</h2>
        <p>You may change the cookies you accept on this website at any time, without leaving this page.</p>
        <p><button class="btn btn--pri" type="button" data-abrir-cookies>Cookie settings</button></p>
        <h2>Exercising your rights</h2>
        <p>You may find out about and exercise your data protection rights by accessing our Privacy Policy.</p>
        <h2>Further information about cookies</h2>
        <h3>What is a cookie?</h3>
        <p>A cookie is a harmless text file that is stored in your browser when you visit almost any website. The usefulness of the cookie is that the website is able to remember your visit when you browse that page again. Although many people are not aware of it, cookies have been in use for 20 years, since the first browsers for the World Wide Web appeared.</p>
        <h3>What is a cookie NOT?</h3>
        <p>It is not a virus, a Trojan, a worm, spam or spyware, nor does it open pop-up windows.</p>
        <h3>What information does a cookie store?</h3>
        <p>Cookies do not usually store sensitive information about you, such as credit cards or bank details, photographs, your national identity document or personal information, etc. The data they save is of a technical nature: personal preferences, content personalisation, etc.</p>
        <p>The web server does not associate you as a person but rather your web browser. In fact, if you usually browse with Internet Explorer and try to browse the same website with Firefox or Chrome, you will see that the website does not realise that you are the same person, because it is in fact associating the browser, not the person.</p>
        <h3>What types of cookies are there?</h3>
        <ul class="lista">
          <li>Technical (strictly necessary) cookies: These are the most basic and allow, among other things, knowing when a human or an automated application is browsing, and when an anonymous user or a registered user is browsing; basic tasks for the operation of any dynamic website.</li>
          <li>Analytics cookies: They collect information about the type of browsing you are carrying out, the sections you use most, products viewed, time slot of use, language, etc.</li>
          <li>Advertising cookies: They display advertising on the basis of your browsing, your country of origin, language, etc.</li>
        </ul>
        <h3>What are first-party and third-party cookies?</h3>
        <p>First-party cookies are those generated by the page you are visiting, and third-party cookies are those generated by external services or providers such as Facebook, Twitter, Google, etc.</p>
        <h3>What happens if I disable cookies?</h3>
        <p>So that you may understand the effect that disabling cookies can have, we set out some examples below:</p>
        <ul class="lista">
          <li>You will not be able to share content from this website on Facebook, Twitter or any other social network.</li>
          <li>The website will not be able to adapt its content to your personal preferences, as usually happens in online shops.</li>
          <li>You will not be able to access the personal area of this website, such as My account, My profile or My orders.</li>
          <li>Online shops: It will be impossible for you to make online purchases; these will have to be made by telephone or by visiting the physical shop, if there is one.</li>
          <li>It will not be possible to personalise your geographical preferences such as time zone, currency or language.</li>
          <li>The website will not be able to carry out web analytics on visitors and traffic on the site, which will make it more difficult for the website to be competitive.</li>
          <li>You will not be able to write on the blog, upload photos, post comments, or rate or score content. Nor will the website be able to know whether you are a human or an automated application posting spam.</li>
          <li>It will not be possible to display targeted advertising, which will reduce the website's advertising revenue.</li>
          <li>All social networks use cookies; if you disable them you will not be able to use any social network.</li>
        </ul>
        <h3>Can cookies be deleted?</h3>
        <p>Yes. Not only deleted, but also blocked, either generally or specifically for a particular domain.</p>
        <p>To delete the cookies of a website you must go to your browser settings, where you may search for those associated with the domain in question and proceed to delete them.</p>
        <h3>Cookie settings for the most popular browsers</h3>
        <p>Below we indicate how to access a particular cookie in the Chrome browser. Note: these steps may vary depending on the version of the browser:</p>
        <ol>
          <li>Go to Settings or Preferences through the File menu or by clicking the customisation icon that appears at the top right.</li>
          <li>You will see different sections; click the Show advanced settings option.</li>
          <li>Go to Privacy, Content settings.</li>
          <li>Select All cookies and site data.</li>
          <li>A list will appear with all the cookies sorted by domain. To make it easier for you to find the cookies of a particular domain, enter all or part of the address in the Search cookies field.</li>
          <li>After applying this filter, one or more lines will appear on screen with the cookies of the website requested. You now only have to select it and click the X to proceed to delete it.</li>
        </ol>
        <p>To access the cookie settings of the Internet Explorer browser, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Go to Tools, Internet Options</li>
          <li>Click on Privacy.</li>
          <li>Move the slider until you set the level of privacy you want.</li>
        </ol>
        <p>To access the cookie settings of the Firefox browser, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Go to Options or Preferences, depending on your operating system.</li>
          <li>Click on Privacy.</li>
          <li>Under History, choose Use custom settings for history.</li>
          <li>You will now see the Accept cookies option; you may enable or disable it according to your preferences.</li>
        </ol>
        <p>To access the cookie settings of the Safari browser for OSX, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Go to Preferences, then Privacy.</li>
          <li>There you will see the Block cookies option, so that you may set the type of blocking you wish to apply.</li>
        </ol>
        <p>To access the cookie settings of the Safari browser for iOS, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Go to Settings, then Safari.</li>
          <li>Go to Privacy and Security; you will see the Block cookies option, so that you may set the type of blocking you wish to apply.</li>
        </ol>
        <p>To access the cookie settings of the browser for Android devices, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Run the browser and press the Menu key, then Settings.</li>
          <li>Go to Security and Privacy; you will see the Accept cookies option, so that you may tick or untick the box.</li>
        </ol>
        <p>To access the cookie settings of the browser for Windows Phone devices, follow these steps (they may vary depending on the version of the browser):</p>
        <ol>
          <li>Open Internet Explorer, then More, then Settings</li>
          <li>You may now tick or untick the Allow cookies box.</li>
        </ol>
''')

redes = legal('Legal', 'Social media policy',
              'What we do with the public information of the people who follow us on social networks.', '''
        <p>In compliance with REGULATION (EU) 2016/679, of 27 April 2016, of the European Parliament and of the Council on the protection of natural persons with regard to the processing of their personal data, Organic Law 3/2018, of 5 December, on the Protection of Personal Data and guarantee of digital rights, and Law 34/2002, of 11 July, on Information Society Services and Electronic Commerce (LSSI-CE), EUDAPRO, S.L., hereinafter (EUDAPRO), informs users that it has created a profile on social networks for the principal purpose of advertising its products and services.</p>
        <h2>Details of EUDAPRO, S.L.</h2>
        <dl>
          <dt>CIF</dt><dd>B75390377</dd>
          <dt>Registered office</dt><dd>PLAÇA FIUS I PALÀ, N.º 1, ESC. IZQ, 3º 2ª, 08241, MANRESA, BARCELONA</dd>
          <dt>Telephone</dt><dd><a href="tel:+34900929806">900 929 806</a></dd>
          <dt>Email</dt><dd><a href="mailto:info@eudapro.es">info@eudapro.es</a></dd>
          <dt>Website</dt><dd><a href="https://www.eudapro.es" target="_blank" rel="noopener">www.eudapro.es</a></dd>
        </dl>
        <p>The user has a profile on that same social network and has decided to join the page created by EUDAPRO, thereby showing an interest in the information published on the network. By joining our page, you give us your consent to the processing of the personal data published on your profile.</p>
        <p>The user may access the privacy policies of the social network itself at any time, as well as configure their profile in order to safeguard their privacy.</p>
        <p>EUDAPRO accesses and processes the user's public information, in particular their contact name. This data is used only within the social network itself and is under no circumstances incorporated into any file without first requesting the express consent of the data subject.</p>
        <p>With regard to the rights of access, rectification, cancellation and objection, which you have and which may be exercised before EUDAPRO in accordance with REGULATION (EU) 2016/679, of 27 April 2016, of the European Parliament, you must bear in mind that, owing to the very functionality of social networks, you will normally have to exercise your rights before the social network itself.</p>
        <p>EUDAPRO will carry out the following actions:</p>
        <ul class="lista">
          <li>Access to the public information on the profile.</li>
          <li>Publication on the user's profile of all the information already published on EUDAPRO's page.</li>
          <li>Sending personal and individual messages through the social network's channels.</li>
          <li>Updates to the status of the page, which will be published on the user's profile.</li>
        </ul>
        <p>The user may at all times control their connections, delete the contents that no longer interest them and restrict with whom they share their connections; to do so, they must go to their privacy settings.</p>
        <h2>Data of minors</h2>
        <p>Access to and registration on this social network is prohibited for persons under 14 years of age. Access to EUDAPRO's official site is also prohibited for persons under 14 years of age. For their part, if the user does not meet that requirement, EUDAPRO informs them of the need to have the authorisation of their parents, guardians or legal representatives in order to access and use EUDAPRO's official site.</p>
        <p>EUDAPRO is exempt from any liability arising from the use of its official site by minors or by users who do not meet the aforementioned requirements, their legal representatives being, in any event, solely responsible.</p>
        <h2>Posts</h2>
        <p>Once they have joined EUDAPRO's page, the user may post on it comments, links, images or photographs or any other type of multimedia content supported by the social network. In all cases, the user must be the owner thereof, hold the copyright and intellectual property rights or have the consent of the third parties concerned. Any posting on the page, whether of texts, graphics, photographs, videos, etc., that offends or is liable to offend morality, ethics, good taste or decency, and/or that infringes, violates or breaches intellectual or industrial property rights, the right to one's own image or the law, is expressly prohibited. In such cases, EUDAPRO reserves the right to remove the content immediately and may request the permanent blocking of the user.</p>
        <p>EUDAPRO shall not be liable for the contents that a user has freely published.</p>
        <p>The user must bear in mind that their posts will be known to other users, and they are therefore primarily responsible for their own privacy.</p>
        <p>Any images that may be published on the page will not be stored in any file by EUDAPRO, but they will remain on the social network.</p>
        <h2>Competitions and promotions</h2>
        <p>EUDAPRO reserves the right to run competitions and promotions in which the user who has joined its page may take part. The terms and conditions of each of them, where the social network's platform is used for this purpose, will be published on it, always in compliance with the LSSI-CE and with any other rule that may be applicable.</p>
        <p>The social network does not sponsor, endorse or administer, in any way, any of our promotions, nor is it associated with any of them.</p>
        <h2>Advertising</h2>
        <p>EUDAPRO will use the social network to advertise its products and services; in any event, should it decide to process your contact details in order to carry out direct commercial prospecting activities, it will always do so in compliance with the legal requirements of the GDPR, the LOPDGDD and the LSSI-CE.</p>
        <p>Recommending EUDAPRO's page to other users so that they too may enjoy the promotions or be informed of its activity shall not be considered advertising.</p>
''')

# --------------------------------------------------------------------------

PAGINAS = [
    ('video-surveillance.html', 'Video surveillance — Eudapro',
     'Cameras compliant with the Spanish Data Protection Agency guidance: information sign, full privacy notice, 30-day retention and data subject rights.', video),
    ('member-associations.html', 'Trade associations — Eudapro',
     'Agreements with guilds, federations and associations: Gremi de Restauració de Barcelona since 2016, Alt Penedès, FIHRT, Bages, Anoia and Ehlis / Cadena 88.', colectivos),
    ('about-us.html', 'About us — Eudapro',
     'Who we are and why we work to measure, in person and with no maintenance fee. Company details of EUDAPRO, S.L.', conocenos),
    ('resources.html', 'Resources and downloads — Eudapro',
     'GDPR bulletins and AEPD briefing notes in PDF, free to download, with no sign-up and no forms. The documents themselves are in Spanish.', recursos),
    ('contact.html', 'Contact — Eudapro',
     'Freephone 900 929 806, e-mail info@eudapro.es and a contact form with separate consent options.', contacto),
    ('legal-notice.html', 'Legal notice — Eudapro',
     'Terms of use of the EUDAPRO, S.L. website: company identification, contact details, conditions of access, intellectual property and applicable law.', aviso_legal),
    ('privacy-policy.html', 'Privacy policy — Eudapro',
     'The personal data processing carried out by EUDAPRO, S.L.: clients, suppliers, subscribers and staff, with purposes, retention periods and rights.', privacidad),
    ('cookies-policy.html', 'Cookies policy — Eudapro',
     'Which cookies the EUDAPRO, S.L. website uses, what they are for and how to accept, reject or configure them from your browser.', cookies),
    ('social-media-policy.html', 'Social media policy — Eudapro',
     'What data EUDAPRO, S.L. processes on its social media profiles, what actions it takes, data of minors, user posts and advertising.', redes),
]

if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    print('Generating English pages…')
    for archivo, titulo, desc, cuerpo in PAGINAS:
        pagina(archivo, titulo, desc, cuerpo)
    print('Done: %d pages.' % len(PAGINAS))
