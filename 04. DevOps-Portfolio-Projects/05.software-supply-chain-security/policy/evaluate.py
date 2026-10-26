import json,sys
from pathlib import Path

def violations(report):
    if not isinstance(report,dict) or not isinstance(report.get('Results'),list):
        raise ValueError('Scan report must contain a Results array; missing data is not a clean scan')
    failures=[]
    for result in report.get('Results',[]):
        for item in result.get('Vulnerabilities') or []:
            if item.get('Severity') in ['HIGH','CRITICAL'] and item.get('FixedVersion'):
                failures.append(item['VulnerabilityID'])
    return sorted(set(failures))
if __name__=='__main__':
    found=violations(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps({'blocked_vulnerabilities':found}))
    raise SystemExit(1 if found else 0)
