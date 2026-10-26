import json,os
from http.server import BaseHTTPRequestHandler,HTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        code=200 if self.path=='/health' else 404
        body=json.dumps({'service':'@@NAME@@','team':'@@TEAM@@','healthy':code==200}).encode()
        self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__=='__main__':HTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
