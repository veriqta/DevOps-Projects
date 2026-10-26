# 01. Run the Platform Locally

[← 00. Developer Request and Platform Contract](00-developer-request-and-platform-contract.md) · [Project home](README.md) · [02. Define the Service Template and Inputs →](02-define-the-service-template-and-inputs.md)

## Starting state and working directory

Complete chapter 00 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `07.developer-self-service-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 07.developer-self-service-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

The developer-facing CLI calls the same generator used by automated tests. Input policy is not implemented separately in each interface. The generator stages output in a temporary directory and renames it into place only after all files are rendered. This reduces the chance that a failed request leaves a misleading partly complete service.

## Work through the implementation

The primary path uses the noninteractive command for reproducibility. To try the portal run `python3 portal/request.py` and enter a new valid name plus payments or platform; do not reuse orders-api before the next chapter if you want its deterministic example. Both entry points enforce the same policy.

### Commands in execution order

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git jq unzip python3 python3-venv openssl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'deb [arch=%s signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu %s stable\n' "$(dpkg --print-architecture)" "$VERSION_CODENAME" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"

```

Log out of the Ubuntu session and reconnect before continuing so Docker group membership is active. Verify `docker version` shows the server. Then run:

```bash
python3 -m unittest discover -s automation -v
python3 automation/generate.py orders-api --team payments --dry-run
```

### Read the implementation: `portal/request.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
"""Interactive developer entry point using the same validated generator."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from generate import generate
if __name__=='__main__':
    name=input('Service name (for example orders-api): ').strip()
    team=input('Owning team (payments or platform): ').strip()
    try:print(generate(name,team,'.generated'))
    except ValueError as error:raise SystemExit(str(error))
```

### Read the implementation: `automation/generate.py`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```python
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
```

## Checkpoint — verify before continuing

All four generator tests pass. Dry-run lists the service files without creating .generated/orders-api. The output includes the generated CI workflow.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If imports fail, run unittest discovery from this project with -s automation as shown. Do not run the template tests directly before replacing their tokens.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [02. Define the Service Template and Inputs](02-define-the-service-template-and-inputs.md). The next chapter assumes the state created here.
