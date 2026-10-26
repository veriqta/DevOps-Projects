"""Run from the repository root. Requires Python; Docker checks are separate."""
import ast,re,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args,**kwargs):subprocess.run(args,check=True,**kwargs)
for p in ROOT.rglob('*.py'):
    if '.generated' not in p.parts:ast.parse(p.read_text(),filename=str(p))
chapters=list(ROOT.glob('[0-9][0-9].*/[0-9][0-9]-*.md'))
assert len(chapters)==80,len(chapters)
for p in ROOT.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' not in link and not link.startswith('#'):
            assert (p.parent/link.split('#')[0]).exists(),(p,link)
    for code in re.findall(r'```bash\n(.*?)```',p.read_text(),re.S):
        result=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True)
        assert result.returncode==0,(p,result.stderr)
for p in ROOT.rglob('*.sh'):run('bash','-n',str(p))
for path in ['01.production-delivery-platform/app','03.kubernetes-application-platform/app','04.sre-observability-and-incidents/app','05.software-supply-chain-security/app','08.cloud-cost-and-capacity/app','05.software-supply-chain-security/policy','07.developer-self-service-platform/automation','08.cloud-cost-and-capacity/scripts']:
    run(sys.executable,'-m','unittest','discover','-s',str(ROOT/path),'-v')
with tempfile.TemporaryDirectory() as temp:
    run(sys.executable,str(ROOT/'07.developer-self-service-platform/automation/generate.py'),'orders-api','--team','payments','--output',temp)
    run(sys.executable,'-m','unittest','discover','-s',str(Path(temp)/'orders-api'),'-v')
print('Passed: Python parsing, Bash scripts/walkthroughs, local links, 80 chapters, behavioral tests and generated-service HTTP test')
