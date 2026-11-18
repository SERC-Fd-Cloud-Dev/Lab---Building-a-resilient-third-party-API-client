"""Actual localhost socket check, separate from deterministic MockTransport tests."""
import threading,time
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
import httpx

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(0.5)
        try:
            self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
        except BrokenPipeError: pass
    def log_message(self,*args): pass

server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
try:
    try:
        httpx.get(f'http://127.0.0.1:{server.server_port}',timeout=0.1,trust_env=False)
    except httpx.ReadTimeout:
        print('PASS: real socket raised ReadTimeout before the delayed response')
    else:
        raise SystemExit('FAIL: expected a read timeout')
finally:
    server.shutdown(); server.server_close()
