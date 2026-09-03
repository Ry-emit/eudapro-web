# Compartir la web con el cliente

## El enlace

    https://ry-emit.github.io/eudapro-web/

Es alojamiento de verdad (GitHub Pages): **no depende de tu Mac**. Funciona
apagado el ordenador, desde móvil, iPad o cualquier ordenador, y no caduca.
Ese es el que le pasas al cliente.

## Cosas que conviene que sepas

- **El repositorio es público.** GitHub Pages gratis solo publica desde repos
  públicos. La web no sale en Google (lleva `noindex` y `robots.txt`), pero
  cualquiera con la dirección puede verla. Es una copia de revisión, no la web
  definitiva del cliente.
- **No se ha subido la carpeta `referencias/`**: dentro hay imágenes de
  inspiración de terceros y no toca republicarlas. Sigue en tu Mac.

## Actualizar la web publicada

Cuando hagas cambios en `~/eudapro-site`:

    cd ~/eudapro-site
    git add -A
    git commit -m "lo que has cambiado"
    git push

Tarda un par de minutos en verse en la dirección de arriba.

## Retirarla

    gh repo delete Ry-emit/eudapro-web --yes

## Para trabajar en local

    cd ~/eudapro-site && python3 _serve_nocache.py 8232

Y abres http://localhost:8232 — sin caché, para ver los cambios al recargar.
