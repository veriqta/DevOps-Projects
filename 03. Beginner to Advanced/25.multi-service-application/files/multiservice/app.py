"""Durable SQLite job API and worker for a single-host lab."""
import json, os, sqlite3, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
DB = os.environ.get('DB_PATH', '/data/jobs.db')
def connect():
    db = sqlite3.connect(DB, timeout=30)
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, value TEXT NOT NULL, result TEXT, status TEXT NOT NULL DEFAULT "queued")')
    db.commit()
    return db
class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body):
        data=json.dumps(body).encode(); self.send_response(status)
        self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health': return self.reply(200,{'status':'ok'})
        if self.path.startswith('/jobs/'):
            try: job_id=int(self.path.rsplit('/',1)[1])
            except ValueError: return self.reply(400,{'error':'invalid id'})
            with connect() as db:
                row=db.execute('SELECT id,value,result,status FROM jobs WHERE id=?',(job_id,)).fetchone()
            return self.reply(200,dict(zip(['id','value','result','status'],row))) if row else self.reply(404,{'error':'not found'})
        self.reply(404,{'error':'not found'})
    def do_POST(self):
        if self.path!='/jobs': return self.reply(404,{'error':'not found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>4096: return self.reply(400,{'error':'body must be 1..4096 bytes'})
            value=json.loads(self.rfile.read(size))['value']
            if not isinstance(value,str): raise ValueError('value must be a string')
        except (ValueError,KeyError,TypeError): return self.reply(400,{'error':'send JSON with string value'})
        with connect() as db:
            cursor=db.execute('INSERT INTO jobs(value) VALUES (?)',(value,)); job_id=cursor.lastrowid
        self.reply(202,{'id':job_id})
def work_once():
    # Transaction encompasses selection/update: a killed worker leaves the job queued.
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row=db.execute('SELECT id,value FROM jobs WHERE status="queued" ORDER BY id LIMIT 1').fetchone()
        if row:
            db.execute('UPDATE jobs SET result=?,status="done" WHERE id=?',(row[1].upper(),row[0]))
        return bool(row)
if __name__=='__main__':
    connect().close()
    if len(sys.argv)>1 and sys.argv[1]=='worker':
        while True:
            if not work_once(): time.sleep(0.2)
    else: ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
