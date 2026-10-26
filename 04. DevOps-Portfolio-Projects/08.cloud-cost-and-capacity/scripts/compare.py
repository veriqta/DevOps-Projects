import json,sys
from pathlib import Path

def metric(report,name,field):
    item=report['metrics'][name]
    values=item.get('values',item)
    if field=='value':return values['rate'] if 'rate' in values else values['value']
    return values[field]
def compare(before,after):
    def values(data):return {'p95_ms':metric(data,'http_req_duration','p(95)'), 'failure_rate':metric(data,'http_req_failed','value'), 'requests':metric(data,'http_reqs','count')}
    b,a=values(before),values(after)
    return {'baseline':b,'candidate':a,'candidate_passes_slo':a['p95_ms']<500 and a['failure_rate']<.01}
if __name__=='__main__':
    result=compare(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()))
    print(json.dumps(result,indent=2));raise SystemExit(0 if result['candidate_passes_slo'] else 1)
