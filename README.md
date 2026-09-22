# Eudapro — web nueva

Web estática de EUDAPRO, S.L. (consultoría de protección de datos), reconstruida
desde cero a partir de dos cosas:

- **El contenido:** la extracción completa de la web anterior en
  `~/Desktop/Eudapro-Web/` (17 páginas, 93 artículos, 533 archivos).
- **El diseño:** el sistema "Hero de partículas" del proyecto de Claude Design
  (`hero-particulas.html`) más las referencias que puso Àlex en `referencias/`:
  Chivo + JetBrains Mono, paleta de **negro #000000, violeta #7D39EB, lima
  #C6FF33 y blanco**, aparato de póster técnico (filetes, marcas de registro,
  etiquetas numeradas) y una nube de partículas en Three.js que se transforma
  con el scroll.

Las reglas del sistema están escritas en `referencias/` (tipografía, colores y
estilo). Eso es lo que manda: si algo de la web contradice esas tres carpetas,
gana la referencia.

---

## Arrancar

```bash
python3 _serve_nocache.py 8232
```

Y abrir `http://localhost:8232`. El servidor sirve sin caché, así que al recargar
se ven los cambios al momento. También está dado de alta en `.claude/launch.json`
con el nombre **eudapro**.

---

## Qué hay

```
index.html                     portada, con la escena de partículas (5 tramos; el primero es la O del logotipo)
logo-3d.html                   prueba aparte de la figura 3D del logotipo (fuera del menú)
proteccion-de-datos.html       el servicio principal — NO existía en la web vieja
videovigilancia.html           requisitos, cartel descargable y cláusula completa
colectivos.html                los 6 convenios con gremios y asociaciones
conocenos.html                 el texto de Isaac Higueras + datos de la empresa
recursos.html                  boletines y notas en PDF (solo los que no llevan la marca antigua)
contacto.html                  formulario con doble consentimiento diferenciado
aviso-legal.html · politica-de-privacidad.html (desplegable por tratamiento)
politica-de-cookies.html · politica-redes-sociales.html

assets/css/eudapro.css         todo el CSS del sitio
assets/js/ui.js                cabecera, menú, riel, apariciones, formulario
assets/js/hero.js              la escena de partículas
assets/js/cyber-shapes.js      las 9 figuras 3D y el muestreo a puntos
assets/js/three.module.js      Three.js 0.184 autoalojado
assets/fonts/                  Chivo y JetBrains Mono en .woff2
assets/doc/                    los PDF (notas, catálogos, guías, boletines)

referencias/01-Tipografia/     TIPOGRAFIA.md + tipografia.html + las fuentes
referencias/02-Colores/        COLORES.md + colores.html + tokens.css
referencias/03-Estilo/         ESTILO.md + estilo.html

_generar.py                    genera las 11 páginas interiores
_serve_nocache.py              servidor local sin caché
_config.yml                    GitHub Pages: no publica README ni COMPARTIR
_retirados/                    PDF e imágenes retirados de la web (no se suben a git)
```

### Sobre `_generar.py`

La cabecera y el pie son idénticos en todas las páginas, así que están escritos
una sola vez ahí y el script vuelca los `.html` ya montados. **El resultado es
HTML plano**: se puede editar a mano sin problema. Lo único que hay que tener en
cuenta es que volver a ejecutar el script sobrescribe esas 12 páginas
(`index.html` y `proteccion-de-datos.html` están a mano y no las toca). Ahora
son 11 páginas: la de formación se eliminó en septiembre de 2026.

---

## Decisiones que se han tomado

**1. El servicio principal ya tiene página.** Protección de datos era el corazón
del negocio y no tenía más que un párrafo en la portada. Ahora es la primera
entrada del menú y la primera tarjeta.

**2. Los gremios salen a la superficie.** Las cuatro páginas de colectivos
estaban fuera del menú: eran invisibles. Ahora hay una entrada propia,
`colectivos.html`, y un tramo entero de la portada.

**3. Los 53 PDF se convierten en argumento.** `recursos.html` los ordena por tipo
y les pone peso. Es el activo que ninguna consultoría pequeña tiene y estaba
enterrado en artículos de 2020.

**4. El blog no se ha migrado.** Está parado desde septiembre de 2024 y una
sección visiblemente abandonada resta credibilidad justo aquí. En su lugar está
"Recursos", que no caduca. Si se decide reactivar el blog, los 93 artículos están
en Markdown listos para importar.

**5. Nada de terceros.** Las tipografías se sirven desde el propio dominio y no
hay Google Fonts, ni Analytics, ni iframes. En una web de protección de datos,
pedirle la fuente a un servidor de Google es exactamente lo que le decimos al
cliente que no haga. Por eso la política de cookies dice hoy que no se instalan
cookies: **si se añade analítica, hay que actualizar esa tabla y poner banner**.

**6. LSSI-CE no tiene página.** En la web vieja existía publicada y vacía. O se
escribe el contenido o se redirige; mientras tanto, no se publica.

**7. Las dos direcciones se explican en vez de esconderse.** La página de
contacto y el aviso legal decían cosas distintas. Ahora aparecen etiquetadas:
*oficina de atención* (C/ Irlanda 7, Barcelona) y *domicilio social* (Ctra. de
Vic 105, Sant Fruitós). **Hay que confirmarlo con el cliente.**

**8. La marca.** Solo Eudapro. Por petición del cliente (briefing del 17/09/2026)
no queda ninguna mención a la marca anterior ni a su dominio, tampoco dentro de
PDF o imágenes, y todos los correos se unifican en `info@eudapro.es`.

**9. Cambios del briefing del 17/09/2026.** Fuera la formación bonificada entera
(página, menú, tarjeta, catálogos y guías); "Solicitar auditoría" pasa a
"Contáctanos"; la política de privacidad recupera el texto literal de la web
antigua en desplegables. Los PDF con la marca anterior (casi todos los boletines,
todas las notas, catálogos y guías), el folleto y el artículo del Gremi y la franja
de marca del cartel de videovigilancia se han retirado a `_retirados/`: cuando
Eudapro pase las versiones con su marca, se vuelven a dejar en `assets/doc/`.

---

## Lo que falta y hay que decidir con el cliente

| Tema | Estado |
|---|---|
| **Conócenos** | Eudapro enviará el texto nuevo. De momento solo se han quitado las menciones a la marca anterior. |
| **Colectivos** | Oscar confirmará qué gremios se mantienen (afecta también a la tarjeta 05 de la portada). |
| **Confían en nosotros** | Texto y logos nuevos pendientes de Oscar. |
| **PDF con la marca nueva** | Boletines y notas informativas: en la web solo quedan 3 documentos limpios. |
| **Web en inglés** | Pregunta abierta del cliente: hay que pasar valoración. |
| **Backend del formulario** | No hay. Hoy el formulario abre el correo del usuario con los datos ya escritos. Para conectarlo: en `assets/js/ui.js`, poner la URL en `var ENVIO` y quitar el bloque del `mailto`. |
| **Las dos direcciones** | Publicadas como oficina y domicilio social. Confirmar. |
| **Logos de clientes** | Son marcas de terceros: confirmar el permiso de cada empresa antes de publicar. |

---

## Detalles técnicos

- **Sin dependencias ni build.** HTML, CSS y JavaScript planos. Lo único externo
  es Three.js, y está descargado dentro del proyecto.
- **La escena 3D es opcional.** El texto lo pinta `ui.js`, que no depende de
  Three.js. Si el navegador no tiene WebGL, si el usuario pide menos movimiento
  (`prefers-reduced-motion`) o si `hero.js` falla, queda un escudo estático y la
  web funciona igual.
- **Rendimiento.** 42.000 partículas en escritorio, 18.000 en móvil. El bucle de
  dibujo se para en cuanto la escena sale de pantalla.
- **El tiempo de la escena.** El cambio de forma ocurre en el primer 30 % de cada
  tramo, cuando la figura todavía está en un lado; el 70 % restante la figura ya
  está hecha y cruza el centro de la pantalla entera. Cada figura está quieta y
  acabada junto a su texto (índice = `avance × nº de tramos − 0.5`).
- **Accesibilidad.** Enlace de salto al contenido, foco visible, `aria-current`
  en el menú, contraste AA en todo el texto, la escena marcada como decorativa.
- **Peso.** ~37 MB son los PDF de `assets/doc/`. La página en sí carga unos 2 MB
  la primera vez (Three.js incluido) y luego tira de caché.
