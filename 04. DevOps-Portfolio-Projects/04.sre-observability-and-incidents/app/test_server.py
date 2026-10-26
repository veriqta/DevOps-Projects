import json, os, subprocess, sys, tempfile, time, unittest
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from pathlib import Path
import socket
class OrdersTest(unittest.TestCase):
    def test_checkout_validation_metrics_and_fault(self):
        with tempfile.TemporaryDirectory() as temp:
            with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            fault=Path(temp)/'fault.json';base=f'http://127.0.0.1:{port}'
            proc=subprocess.Popen([sys.executable,str(Path(__file__).with_name('server.py'))],env={**os.environ,'PORT':str(port),'FAULT_FILE':str(fault)},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            try:
                for _ in range(100):
                    try:
                        with urlopen(base+'/health',timeout=.2):break
                    except OSError:time.sleep(.05)
                with urlopen(Request(base+'/checkout',data=b'{"item":"book"}')) as response:self.assertEqual(response.status,201);self.assertTrue(json.load(response)['id'])
                with self.assertRaises(HTTPError) as error:urlopen(Request(base+'/checkout',data=b'{}'))
                self.assertEqual(error.exception.code,400)
                fault.write_text('{"fail":true}')
                with self.assertRaises(HTTPError) as error:urlopen(Request(base+'/checkout',data=b'{"item":"book"}'))
                self.assertEqual(error.exception.code,503)
                with urlopen(base+'/metrics') as response:self.assertIn(b'orders_requests_total{status="201"} 1',response.read())
                with urlopen(base+'/orders') as response:self.assertEqual(len(json.load(response)),1)
            finally:proc.terminate();proc.wait(timeout=5)
if __name__=='__main__':unittest.main()
