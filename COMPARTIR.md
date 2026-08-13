# Compartir la web con el cliente

## Enlace público (el que le pasas al cliente)

    https://radio-compiler-measurements-buy.trycloudflare.com

Funciona desde cualquier sitio: móvil, ordenador o iPad, con datos o con otra WiFi.
Es HTTPS y no hace falta instalar nada.

**Ojo: el enlace vive mientras tu Mac esté encendido y el túnel abierto.**
Si apagas el Mac o cierras el túnel, deja de funcionar y hay que crear otro
(la dirección cambia cada vez).

## Enlace de red local (solo para tus dispositivos en la misma WiFi)

    http://192.168.1.83:8232

## Volver a levantarlo si se cae

Dos comandos, en dos terminales (o con `&` al final):

    cd ~/eudapro-site && python3 _serve_nocache.py 8232
    cloudflared tunnel --url http://localhost:8232

La segunda línea imprime la nueva dirección `https://….trycloudflare.com`.

## Cerrarlo

    pkill -f cloudflared
    pkill -f _serve_nocache

## Nota

La web lleva `noindex` y un `robots.txt` que bloquea a los buscadores: es una
copia de trabajo y no debe salir en Google mientras la web real del cliente
siga publicada.

Para algo permanente (que no dependa de tu Mac) hay que subirla a un hosting
estático — GitHub Pages, Netlify o Cloudflare Pages. Eso necesita tu cuenta.
