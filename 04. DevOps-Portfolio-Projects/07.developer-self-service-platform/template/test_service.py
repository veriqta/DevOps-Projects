import json,threading,unittest
from http.server import HTTPServer
from urllib.request import urlopen
from server import Handler
class ServiceTest(unittest.TestCase):
    def test_health_identifies_service_and_owner(self):
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with urlopen(f'http://127.0.0.1:{server.server_port}/health') as response:
                result=json.load(response);self.assertEqual(result['service'],'@@NAME@@');self.assertEqual(result['team'],'@@TEAM@@')
        finally:server.shutdown();server.server_close();thread.join()
