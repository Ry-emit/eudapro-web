#!/usr/bin/env python3
"""Servidor local sin caché, para ver los cambios al recargar.

    python3 _serve_nocache.py [puerto]
"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class SinCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8232
    print('Sirviendo en http://localhost:%d (sin caché)' % puerto)
    ThreadingHTTPServer(('127.0.0.1', puerto), SinCache).serve_forever()
