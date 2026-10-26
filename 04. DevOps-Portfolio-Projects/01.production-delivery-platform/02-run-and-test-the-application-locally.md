# 02. Run and Test the Application Locally

[← 01. Prepare the Workstation and Repository](01-prepare-the-workstation-and-repository.md) · [Project home](README.md) · [03. Build and Inspect the Container Image →](03-build-and-inspect-the-container-image.md)

## Starting state and working directory

Complete chapter 01 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The API is small enough to understand before automation hides its behavior. A checkout validates a nonempty item, emits a unique order ID and records a metric. The test starts a real ephemeral HTTP server, submits valid and invalid requests, injects a payment failure and confirms only the successful order was stored. This is stronger evidence than checking that a Python file compiles.

## Work through the implementation

Read the GET and POST handlers separately. `/health` is a readiness contract, `/checkout` is the business action, and `/metrics` is an operational interface. A successful health check alone does not prove checkout works, which is why the chapter tests both. The FAULT_FILE and BROKEN_RELEASE switches exist for controlled lab failures; do not expose them as public administrative endpoints.

### Commands in execution order

```bash
python3 -m unittest discover -s app -v
python3 app/server.py
```

### Read the implementation: `app/server.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
"""Orders lab: dependency-free HTTP API with controlled failures and metrics."""
import json, os, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from contextlib import nullcontext
LOCK=threading.Lock(); COUNTS={}; BUCKETS={b:0 for b in [.05,.1,.25,.5,1,2.5,5]}; DURATION_COUNT=0; DURATION_SUM=0.0; ORDERS=[]
TRACER=None
if os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT'):
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    provider=TracerProvider(resource=Resource.create({'service.name':'orders'}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider);TRACER=trace.get_tracer(__name__)
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def response(self,code,body):
        raw=json.dumps(body).encode();self.send_response(code)
        self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/metrics':
            with LOCK:
                lines=['# TYPE orders_requests_total counter']+[f'orders_requests_total{{status="{k}"}} {v}' for k,v in sorted(COUNTS.items())]
                lines+=['# TYPE orders_duration_seconds histogram']
                for b in [.05,.1,.25,.5,1,2.5,5]:lines.append(f'orders_duration_seconds_bucket{{le="{b}"}} {BUCKETS[b]}')
                lines += [f'orders_duration_seconds_bucket{{le="+Inf"}} {DURATION_COUNT}',f'orders_duration_seconds_count {DURATION_COUNT}',f'orders_duration_seconds_sum {DURATION_SUM}']
            raw=('\n'.join(lines)+'\n').encode();self.send_response(200);self.send_header('Content-Type','text/plain; version=0.0.4');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
        if self.path=='/health':return self.response(503 if os.environ.get('BROKEN_RELEASE')=='1' else 200,{'status':'ok','version':os.environ.get('VERSION','local')})
        if self.path=='/orders':
            with LOCK:orders=list(ORDERS)
            return self.response(200,orders)
        self.response(404,{'error':'not found'})
    def do_POST(self):
        global DURATION_COUNT,DURATION_SUM
        if self.path!='/checkout':return self.response(404,{'error':'not found'})
        started=time.monotonic();code=500
        context=TRACER.start_as_current_span('checkout') if TRACER else nullcontext()
        with context:
            trace_id=''
            if TRACER:trace_id=format(trace.get_current_span().get_span_context().trace_id,'032x')
            try:
                size=int(self.headers.get('Content-Length','0'))
                if size<1 or size>4096:raise ValueError('invalid body size')
                payload=json.loads(self.rfile.read(size))
                if not isinstance(payload,dict) or not isinstance(payload.get('item'),str) or not payload['item'].strip():raise ValueError('item is required')
                fault=Path(os.environ.get('FAULT_FILE','/tmp/orders-fault.json'))
                mode=json.loads(fault.read_text()) if fault.exists() else {}
                delay=float(mode.get('delay_ms',os.environ.get('DELAY_MS','0')))/1000
                time.sleep(min(max(delay,0),5))
                if mode.get('fail'):code=503;self.response(code,{'error':'payment provider unavailable'})
                else:
                    order={'id':str(uuid.uuid4()),'item':payload['item'],'version':os.environ.get('VERSION','local')}
                    with LOCK:ORDERS.append(order)
                    code=201;self.response(code,order)
            except (ValueError,TypeError):code=400;self.response(code,{'error':'send JSON with a nonempty item string'})
            finally:
                elapsed=time.monotonic()-started
                with LOCK:
                    COUNTS[str(code)]=COUNTS.get(str(code),0)+1
                    DURATION_COUNT+=1;DURATION_SUM+=elapsed
                    for boundary in BUCKETS:
                        if elapsed<=boundary:BUCKETS[boundary]+=1
                event=json.dumps({'service':'orders','path':'/checkout','status':code,'duration_seconds':elapsed,'trace_id':trace_id,'time':time.time()})
                print(event,flush=True)
                if os.environ.get('LOG_FILE'):
                    with open(os.environ['LOG_FILE'],'a') as stream:stream.write(event+'\n')
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8080'))),Handler).serve_forever()
```

### Read the implementation: `app/test_server.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
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
```

## Checkpoint — verify before continuing

In a second terminal request curl -fsS localhost:8080/health, then curl -fsS -H "Content-Type: application/json" -d '{"item":"book"}' localhost:8080/checkout. Expect status ok and then an order ID with HTTP 201. GET /orders contains that order. Stop the foreground server with Ctrl+C before chapter 03.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

Address already in use means another lab owns port 8080. Use ss -ltnp to identify it; stop only your lab process. An empty item should produce 400, which is a passing negative test.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [03. Build and Inspect the Container Image](03-build-and-inspect-the-container-image.md). The next chapter assumes the state created here.
