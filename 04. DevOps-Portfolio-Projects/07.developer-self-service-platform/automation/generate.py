"""Validated, atomic service generation; no cloud credentials required."""
import argparse,json,re,shutil,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def generate(name,team,destination,dry_run=False,fail=False):
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,30}',name):raise ValueError('name must be 3-31 lowercase letters/digits/hyphens and begin with a letter')
    allowed=json.loads((ROOT/'automation/teams.json').read_text())['teams']
    if team not in allowed:raise ValueError('team is not allowed by platform policy')
    destination=Path(destination).resolve();destination.mkdir(parents=True,exist_ok=True)
    target=destination/name
    if target.exists():raise ValueError('service already exists; refusing replacement')
    files=[p for p in (ROOT/'template').rglob('*') if p.is_file()]
    if dry_run:return {'service':name,'team':team,'files':[str(p.relative_to(ROOT/'template')) for p in files]}
    staging=Path(tempfile.mkdtemp(prefix='.request-',dir=destination))
    try:
        for source in files:
            result=staging/source.relative_to(ROOT/'template');result.parent.mkdir(parents=True,exist_ok=True)
            result.write_text(source.read_text().replace('@@NAME@@',name).replace('@@TEAM@@',team))
        if fail:raise RuntimeError('simulated pre-publication failure')
        # rename to a new directory publishes a complete generated service.
        staging.rename(target)
    finally:
        if staging.exists():shutil.rmtree(staging)
    return {'service':name,'team':team,'path':str(target)}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('name');parser.add_argument('--team',required=True);parser.add_argument('--output',default='.generated');parser.add_argument('--dry-run',action='store_true');parser.add_argument('--fail-after-render',action='store_true');args=parser.parse_args()
    try:print(json.dumps(generate(args.name,args.team,args.output,args.dry_run,args.fail_after_render),indent=2))
    except (ValueError,RuntimeError) as error:parser.exit(1,str(error)+'\n')
