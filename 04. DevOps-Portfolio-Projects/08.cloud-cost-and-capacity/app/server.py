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
