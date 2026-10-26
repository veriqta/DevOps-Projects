import importlib.util, json, os, shutil, socket, subprocess, tempfile, time, unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parents[1]
NODE=os.environ.get('NODE_BIN') or shutil.which('node')
def port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0)); return sock.getsockname()[1]
def wait(url,process):
    for _ in range(100):
        if process.poll() is not None: raise RuntimeError('server exited before becoming ready')
        try:
            with urlopen(url,timeout=0.3) as response: return response.read()
        except (OSError,HTTPError): time.sleep(0.05)
    raise RuntimeError('server never became ready')
@unittest.skipUnless(NODE,'Node executable required; set NODE_BIN')
class DemoHTTPTest(unittest.TestCase):
    def test_health_404_metrics_and_shutdown(self):
        selected=port(); base=f'http://127.0.0.1:{selected}'
        proc=subprocess.Popen([NODE,str(ROOT/'02.examples/app/server.js')],env={**os.environ,'PORT':str(selected),'HOST':'127.0.0.1','VERSION':'test-release'},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            self.assertEqual(json.loads(wait(base+'/health',proc)),{'version':'test-release','status':'ok'})
            with self.assertRaises(HTTPError) as error: urlopen(base+'/missing')
            self.assertEqual(error.exception.code,404)
            with urlopen(base+'/metrics') as response:
                self.assertIn(b'demo_requests_total 2',response.read())
            proc.terminate(); self.assertEqual(proc.wait(timeout=5),0)
        finally:
            if proc.poll() is None: proc.kill(); proc.wait()
class JobsHTTPTest(unittest.TestCase):
    def test_queued_job_survives_api_restart_then_completes(self):
        with tempfile.TemporaryDirectory() as temp:
            selected=port(); base=f'http://127.0.0.1:{selected}'
            env={**os.environ,'PORT':str(selected),'DB_PATH':str(Path(temp)/'jobs.db')}
            def start():
                process=subprocess.Popen([os.sys.executable,str(ROOT/'02.examples/multiservice/app.py')],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                wait(base+'/health',process); return process
            api=start(); worker=None
            try:
                request=Request(base+'/jobs',data=b'{"value":"recover me"}',headers={'Content-Type':'application/json'})
                with urlopen(request) as response:
                    self.assertEqual(response.status,202); job=json.load(response)['id']
                api.terminate(); api.wait(timeout=5); api=start()
                with urlopen(base+f'/jobs/{job}') as response: self.assertEqual(json.load(response)['status'],'queued')
                worker=subprocess.Popen([os.sys.executable,str(ROOT/'02.examples/multiservice/app.py'),'worker'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                for _ in range(100):
                    with urlopen(base+f'/jobs/{job}') as response: result=json.load(response)
                    if result['status']=='done': break
                    time.sleep(.05)
                self.assertEqual(result['result'],'RECOVER ME')
                with self.assertRaises(HTTPError) as error: urlopen(base+'/jobs/99999')
                self.assertEqual(error.exception.code,404)
                with self.assertRaises(HTTPError) as error: urlopen(Request(base+'/jobs',data=b'not JSON'))
                self.assertEqual(error.exception.code,400)
                with self.assertRaises(HTTPError) as error: urlopen(Request(base+'/jobs',data=b'[]'))
                self.assertEqual(error.exception.code,400)
            finally:
                for process in [api,worker]:
                    if process and process.poll() is None: process.terminate(); process.wait(timeout=5)
