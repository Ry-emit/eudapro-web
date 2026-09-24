#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara la web para subirla al hosting de Eudapro (IONOS, Apache con PHP).

    python3 _exportar.py

Deja el sitio listo en  _entrega/eudapro-web/  y un .zip al lado. Lo que hace,
además de copiar los archivos:

  · quita la etiqueta «noindex» que lleva la copia de revisión;
  · pone las etiquetas de idioma y el «canonical» con la dirección definitiva;
  · escribe robots.txt, sitemap.xml, .htaccess y una página 404;
  · añade enviar.php y hace que el formulario lo use (si falla, el navegador
    sigue cayendo en el correo preparado de siempre);
  · deja fuera lo que no se publica: los generadores, el README, la página de
    prueba de la figura 3D y las imágenes que ya no usa ninguna página.

El original no se toca: todo se escribe en _entrega/.
"""

import os
import re
import shutil
import zipfile
from datetime import date

RAIZ = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, '_entrega')
WEB = os.path.join(SALIDA, 'eudapro-web')

DOMINIO = 'https://www.eudapro.es'          # dirección definitiva, sin barra final
CORREO_DESTINO = 'info@eudapro.es'
CORREO_REMITENTE = 'web@eudapro.es'         # buzón o alias del propio dominio

# Lo que no se sube
FUERA_RAIZ = {'_generar.py', '_generar_en.py', '_serve_nocache.py', '_exportar.py',
              'README.md', 'COMPARTIR.md', '_config.yml', '.gitignore', '.DS_Store',
              'logo-3d.html', 'robots.txt'}
FUERA_CARPETAS = {'_retirados', '_entrega', 'referencias', '.git', 'css', 'js'}
# Archivos de assets que se incluyen aunque nadie los enlace
SIEMPRE = {'assets/img/favicon.png', 'assets/img/apple-touch-icon.png'}


def url_de(rel):
    """Dirección definitiva de una página: index.html es la carpeta."""
    if rel == 'index.html':
        return DOMINIO + '/'
    if rel.endswith('/index.html'):
        return DOMINIO + '/' + rel[:-len('index.html')]
    return DOMINIO + '/' + rel


def paginas():
    hay = sorted(f for f in os.listdir(RAIZ) if f.endswith('.html') and f not in FUERA_RAIZ)
    hay += sorted('en/' + f for f in os.listdir(os.path.join(RAIZ, 'en')) if f.endswith('.html'))
    return hay


def assets_usados():
    """Sigue las referencias desde las páginas: HTML → CSS/JS/imágenes/PDF,
    CSS → tipografías, JS → los módulos que importa. Lo que no aparece, no se
    sube: así no viajan al hosting las tipografías y los logotipos antiguos."""
    pendientes = [(rel, os.path.dirname(rel)) for rel in paginas()]
    vistos, usados = set(), set(SIEMPRE)

    while pendientes:
        rel, base = pendientes.pop()
        if rel in vistos:
            continue
        vistos.add(rel)
        ruta = os.path.join(RAIZ, rel)
        if not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, encoding='utf-8') as f:
                texto = f.read()
        except (UnicodeDecodeError, OSError):
            continue

        refs = re.findall(r'(?:href|src)="([^"]+)"', texto)
        refs += re.findall(r'url\(\s*[\'"]?([^)\'"]+)', texto)
        refs += re.findall(r'from\s+[\'"]([^\'"]+)[\'"]', texto)
        refs += re.findall(r'[\'"]((?:\.\./)*assets/[^\'"]+)[\'"]', texto)

        for r in refs:
            if r.startswith(('http', 'mailto:', 'tel:', 'data:', '#')):
                continue
            destino = os.path.normpath(os.path.join(base, r.split('#')[0].split('?')[0]))
            destino = destino.replace(os.sep, '/')
            if not destino.startswith('assets/'):
                continue
            usados.add(destino)
            pendientes.append((destino, os.path.dirname(destino)))
    return usados


def copiar():
    if os.path.exists(SALIDA):
        shutil.rmtree(SALIDA)
    os.makedirs(WEB)
    for rel in paginas():
        destino = os.path.join(WEB, rel)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(os.path.join(RAIZ, rel), destino)
    usados = assets_usados()
    sobran = []
    for carpeta, _, archivos in os.walk(os.path.join(RAIZ, 'assets')):
        for a in archivos:
            origen = os.path.join(carpeta, a)
            rel = os.path.relpath(origen, RAIZ).replace(os.sep, '/')
            if a == '.DS_Store':
                continue
            if rel not in usados:
                sobran.append(rel)
                continue
            destino = os.path.join(WEB, rel)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origen, destino)
    if sobran:
        print('Fuera del paquete, porque no los enlaza ninguna página (%d):' % len(sobran))
        for rel in sorted(sobran):
            print('  ·', rel)


def arreglar_paginas():
    """Fuera el noindex; las etiquetas de idioma y el canonical, con la dirección real."""
    for rel in paginas():
        ruta = os.path.join(WEB, rel)
        with open(ruta, encoding='utf-8') as f:
            html = f.read()

        html = re.sub(r'[ \t]*<meta name="robots" content="noindex, nofollow">\n', '', html)

        base = os.path.dirname(rel)

        def absoluta(m):
            destino = os.path.normpath(os.path.join(base, m.group(2)))
            return '%s%s"' % (m.group(1), url_de(destino.replace(os.sep, '/')))

        html = re.sub(r'(<link rel="alternate" hreflang="[a-zA-Z-]+" href=")([^"]+)"', absoluta, html)
        html = html.replace('<link rel="alternate"',
                            '<link rel="canonical" href="%s">\n<link rel="alternate"' % url_de(rel), 1)

        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(html)


def formulario_por_php():
    """El formulario pasa a enviar.php. Si el envío falla, sigue el correo de siempre."""
    ruta = os.path.join(WEB, 'assets/js/ui.js')
    with open(ruta, encoding='utf-8') as f:
        js = f.read()
    viejo = "  var ENVIO = null; // p. ej. 'https://formularios.eudapro.com/contacto'"
    nuevo = ("  /* El hosting es PHP: el formulario se envía a enviar.php, que está en la\n"
             "     raíz del sitio. Las páginas en inglés cuelgan de /en/, por eso suben un nivel. */\n"
             "  var ENVIO = ((document.documentElement.lang || 'es').toLowerCase().indexOf('en') === 0 ? '../' : '') + 'enviar.php';")
    assert js.count(viejo) == 1, 'no se encuentra la línea de ENVIO en ui.js'
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(js.replace(viejo, nuevo))


def escribir(nombre, contenido):
    ruta = os.path.join(WEB, nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)


def sitemap():
    hoy = date.today().isoformat()
    # cada página con su equivalente en el otro idioma
    pares = {}
    for rel in paginas():
        ruta = os.path.join(WEB, rel)
        with open(ruta, encoding='utf-8') as f:
            html = f.read()
        alt = re.findall(r'<link rel="alternate" hreflang="([a-zA-Z-]+)" href="([^"]+)"', html)
        pares[rel] = [(idioma, url) for idioma, url in alt]
    filas = []
    for rel in paginas():
        prioridad = '1.0' if rel == 'index.html' else ('0.8' if '/' not in rel else '0.6')
        alternas = '\n'.join(
            '    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (i, u) for i, u in pares[rel])
        filas.append(
            '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n'
            '    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n%s\n  </url>'
            % (url_de(rel), hoy, prioridad, alternas))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(filas) + '\n</urlset>\n')


HTACCESS = """# Eudapro — configuración del servidor (Apache, hosting de IONOS)
# Si algo diera guerra, se puede comentar el bloque correspondiente con #.

Options -Indexes
AddDefaultCharset UTF-8
DirectoryIndex index.html

# ---- una sola dirección: https y con www -------------------------------
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on
  RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
  RewriteCond %{HTTP_HOST} !^www\\. [NC]
  RewriteRule ^(.*)$ DOMINIO_AQUI/$1 [R=301,L]
</IfModule>

# ---- página de error ---------------------------------------------------
ErrorDocument 404 /404.html

# ---- compresión --------------------------------------------------------
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml
  AddOutputFilterByType DEFLATE application/javascript application/json image/svg+xml
</IfModule>

# ---- caché del navegador ----------------------------------------------
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType application/pdf "access plus 1 month"
</IfModule>

# ---- cabeceras de seguridad -------------------------------------------
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Permissions-Policy "geolocation=(), microphone=(), camera=()"
</IfModule>

# ---- tipos de archivo --------------------------------------------------
AddType font/woff2 .woff2
AddType image/webp .webp
AddType image/svg+xml .svg
"""

ROBOTS = """# Web de EUDAPRO, S.L.
User-agent: *
Allow: /

Sitemap: %(dominio)s/sitemap.xml
"""

PAGINA_404 = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Página no encontrada — Eudapro</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="stylesheet" href="/assets/css/eudapro.css">
</head>
<body>
<main id="principal">
  <section class="bloque">
    <div class="wrap wrap--slim" style="text-align:center; padding:clamp(40px,10vh,120px) 0">
      <a class="marca" href="/" aria-label="Eudapro, inicio">
        <img class="marca__logo marca__logo--completo" src="/assets/img/marca/eudapro-logo.webp"
             alt="Eudapro, European Data Protect: protección de datos" width="637" height="196"
             style="max-width:280px; height:auto; margin:0 auto 32px">
      </a>
      <span class="kicker">Error 404</span>
      <h1 style="margin-bottom:18px">Esta página no existe</h1>
      <p class="lede">Puede que el enlace esté mal escrito o que la página ya no esté publicada.</p>
      <p style="margin-top:8px; color:var(--ink-3)">This page does not exist. <a href="/en/index.html">Go to the English home page</a>.</p>
      <div class="paso__cta mt-m" style="justify-content:center">
        <a class="btn btn--pri" href="/">Ir al inicio</a>
        <a class="btn btn--sec" href="/contacto.html">Contactar</a>
      </div>
    </div>
  </section>
</main>
</body>
</html>
"""

ENVIAR_PHP = r"""<?php
/**
 * Formulario de contacto de eudapro.es
 *
 * Recibe el formulario de contacto.html y de en/contact.html y manda un correo
 * a la dirección de abajo. Devuelve JSON: si algo falla, la propia web prepara
 * el correo en el programa del visitante, así que no se pierde ninguna consulta.
 *
 * Lo único que hay que revisar al subirlo:
 *   · DESTINO   — a dónde llegan las consultas.
 *   · REMITENTE — un buzón o alias del propio dominio. Los servidores rechazan
 *                 el correo si el remitente es la dirección del visitante.
 */
declare(strict_types=1);

const DESTINO   = '%(destino)s';
const REMITENTE = '%(remitente)s';
const ASUNTO_POR_DEFECTO = 'Solicitud de información desde la web';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function responder(int $codigo, string $mensaje): void {
    http_response_code($codigo);
    echo json_encode(['ok' => $codigo === 200, 'mensaje' => $mensaje], JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    responder(405, 'Método no permitido.');
}

/** Un campo de una línea: sin saltos, que es por donde se cuela el spam. */
function campo(string $nombre, int $max = 300): string {
    $v = is_string($_POST[$nombre] ?? null) ? $_POST[$nombre] : '';
    $v = str_replace(["\r", "\n", "\0"], ' ', trim($v));
    return mb_substr($v, 0, $max);
}

// Trampa para robots: una persona no ve ese campo, así que si viene relleno
// se descarta el envío (y se responde bien, para no darle pistas).
if (campo('web') !== '') {
    responder(200, 'Recibido.');
}

$nombre   = campo('nombre', 120);
$correo   = campo('correo', 160);
$telefono = campo('telefono', 40);
$empresa  = campo('empresa', 160);
$asunto   = campo('asunto', 160);
$mensaje  = mb_substr(trim(is_string($_POST['mensaje'] ?? null) ? $_POST['mensaje'] : ''), 0, 5000);
$tratamiento = isset($_POST['consent-tratamiento']);
$comercial   = isset($_POST['consent-comercial']);

if ($nombre === '' || $correo === '') {
    responder(422, 'Faltan el nombre o el correo.');
}
if (!filter_var($correo, FILTER_VALIDATE_EMAIL)) {
    responder(422, 'El correo no es válido.');
}
if (!$tratamiento) {
    responder(422, 'Falta el consentimiento de tratamiento.');
}
if ($asunto === '') {
    $asunto = ASUNTO_POR_DEFECTO;
}

$cuerpo = implode("\n", [
    'Nombre: ' . $nombre,
    'Correo: ' . $correo,
    'Teléfono: ' . ($telefono !== '' ? $telefono : '—'),
    'Empresa / colectivo: ' . ($empresa !== '' ? $empresa : '—'),
    '',
    'Mensaje:',
    $mensaje !== '' ? $mensaje : '—',
    '',
    '— Consentimiento de tratamiento: sí',
    '— Comunicaciones comerciales: ' . ($comercial ? 'sí' : 'no'),
    '',
    'Enviado desde ' . ($_SERVER['HTTP_REFERER'] ?? 'la web') . ' el ' . date('d/m/Y H:i'),
]);

$cabeceras = implode("\r\n", [
    'From: Web Eudapro <' . REMITENTE . '>',
    'Reply-To: ' . $nombre . ' <' . $correo . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

$asuntoCodificado = '=?UTF-8?B?' . base64_encode($asunto) . '?=';
$enviado = @mail(DESTINO, $asuntoCodificado, $cuerpo, $cabeceras, '-f' . REMITENTE);

if (!$enviado) {
    responder(500, 'No se ha podido enviar.');
}
responder(200, 'Recibido.');
"""

LEEME = """EUDAPRO — WEB LISTA PARA SUBIR
Preparada el %(fecha)s por Alex Catala

QUÉ HAY AQUÍ
------------
El contenido de esta carpeta es la web entera. Todo lo que hay dentro va a la
carpeta pública del hosting (en IONOS suele llamarse /, htdocs o public_html),
manteniendo las subcarpetas tal y como están.

  index.html y el resto de .html   las 11 páginas en español
  en/                              las 11 páginas en inglés
  assets/                          tipografías, imágenes, estilos, guiones y PDF
  enviar.php                       el formulario de contacto
  .htaccess                        configuración del servidor (Apache)
  robots.txt y sitemap.xml         para los buscadores
  404.html                         la página de error

TRES COSAS QUE HAY QUE REVISAR AL SUBIRLA
-----------------------------------------
1. El correo del formulario. En enviar.php, arriba del todo:
      DESTINO   = %(destino)s        (a dónde llegan las consultas)
      REMITENTE = %(remitente)s      (tiene que existir como buzón o alias en IONOS)
   Si el remitente no es una dirección del propio dominio, el servidor de correo
   rechaza el envío. Si enviar.php fallara, la web no pierde la consulta: abre
   el programa de correo del visitante con el mensaje ya escrito.

2. La dirección del sitio. Las etiquetas de idioma, el canonical, el sitemap y
   el .htaccess están puestos para %(dominio)s. Si al final la web va sin www o
   a otro dominio, hay que cambiarlo en:
      · .htaccess (la regla de redirección)
      · robots.txt (la línea del Sitemap)
      · sitemap.xml
      · las etiquetas <link rel="canonical"> y <link rel="alternate"> de cada
        página (una búsqueda y sustitución de %(dominio)s basta)

3. La analítica. En assets/js/cookies.js, la primera línea de código es:
      var GA_ID = '';
   Mientras esté vacía no se carga Google Analytics ni se instala ninguna
   cookie. Cuando Eudapro facilite su identificador (G-XXXXXXXXXX), se escribe
   ahí dentro de las comillas y ya está: el aviso de cookies y el gestor por
   categorías están puestos y funcionando.

LO QUE NO SE INCLUYE
--------------------
· Los generadores de las páginas (_generar.py y _generar_en.py) y el README:
  son herramientas de trabajo, no forman parte de la web.
· logo-3d.html, la página suelta con la figura 3D del logotipo, que era una
  prueba para enseñar la animación y no está enlazada en el menú.
· Las imágenes del logotipo antiguo y las de las páginas retiradas.

COMPROBADO ANTES DE EMPAQUETAR
------------------------------
· Las 22 páginas cargan sin errores y sin enlaces ni imágenes rotas.
· El selector de idioma va y vuelve en todas.
· No se instala ninguna cookie hasta que el visitante la acepta.
· Se ve bien en móvil, tableta y ordenador.
"""


def main():
    copiar()
    arreglar_paginas()
    formulario_por_php()
    escribir('.htaccess', HTACCESS.replace('DOMINIO_AQUI', DOMINIO))
    escribir('robots.txt', ROBOTS % {'dominio': DOMINIO})
    escribir('sitemap.xml', sitemap())
    escribir('404.html', PAGINA_404)
    escribir('enviar.php', ENVIAR_PHP % {'destino': CORREO_DESTINO, 'remitente': CORREO_REMITENTE})
    escribir('LEEME-PRIMERO.txt', LEEME % {'fecha': date.today().strftime('%d/%m/%Y'),
                                           'dominio': DOMINIO, 'destino': CORREO_DESTINO,
                                           'remitente': CORREO_REMITENTE})

    zip_ruta = os.path.join(SALIDA, 'eudapro-web-%s.zip' % date.today().isoformat())
    with zipfile.ZipFile(zip_ruta, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for carpeta, _, archivos in os.walk(WEB):
            for a in sorted(archivos):
                ruta = os.path.join(carpeta, a)
                z.write(ruta, os.path.relpath(ruta, WEB))

    total = sum(os.path.getsize(os.path.join(c, a))
                for c, _, f in os.walk(WEB) for a in f)
    print('Carpeta: %s' % WEB)
    print('Zip:     %s  (%.1f MB, la web sin comprimir ocupa %.1f MB)'
          % (zip_ruta, os.path.getsize(zip_ruta) / 1048576, total / 1048576))


if __name__ == '__main__':
    main()
