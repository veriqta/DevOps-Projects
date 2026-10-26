# 07. Promote the Same Release With Approval

[← 06. Deploy and Verify Staging](06-deploy-and-verify-staging.md) · [Project home](README.md) · [08. Introduce a Failed Release and Roll Back →](08-introduce-a-failed-release-and-roll-back.md)

## Starting state and working directory

Complete chapter 06 and its checkpoint before continuing. Keep the same lab environment and shell unless instructed otherwise.

**Terminal:** Ubuntu 24.04 lab workstation, using Bash. Commands run inside `01.production-delivery-platform` unless a block explicitly changes directories or names another machine. If you are at the repository root, enter it with:

```bash
cd 01.production-delivery-platform
```

Do not run that `cd` again if you are already in this folder. Uppercase placeholder values must be replaced before execution. Values exported in one terminal are not automatically available in another.

## Why this step exists

An environment name in YAML does not itself create an approval policy. Configure the production environment before running promotion. Its job must wait for staging and for the required reviewer; otherwise you have automated two deployments without a meaningful gate. The same validated input digest is used by both jobs, preventing a tag from moving between test and approval.

## Work through the implementation

Create GitHub environments staging and production. In production add a required reviewer and prevent self-review when another reviewer is available. Restrict deployment branches to main for both environments. The workflow also refuses non-main refs before running a job. Register a dedicated runner: Settings → Actions → Runners → New self-hosted runner → Linux → choose the VM architecture. On the disposable VM, as its normal Docker-capable user, create ~/actions-runner and execute the exact versioned download/extract commands shown by GitHub. Run the displayed ./config.sh command with its short-lived registration token; add the custom label orders-lab when prompted. Use this runner only for this trusted manual promotion workflow, never for untrusted pull-request jobs. Install/start its service with sudo ./svc.sh install and sudo ./svc.sh start from ~/actions-runner. Confirm the runner is Idle in GitHub and the service user can run Docker. The workflow has no pull_request trigger and requires manually selected trusted main. Docker access is host-privileged, so do not share this VM with other workloads. A public lab image needs no registry secret; a private image requires a scoped authenticated pull for the runner user. The approval screenshot and the stored digest files on the same VM are the evidence.

### Commands in execution order

```bash
cp workflows/promote.yml ../.github/workflows/orders-promote.yml
git add ../.github/workflows/orders-promote.yml
git commit -m "Gate Orders promotion"
git push
```

### Read the implementation: `workflows/promote.yml`

This complete file is supplied in the project. Open it in your editor and compare it with the version below before running it. Keep its path unchanged so the later commands can find it.

```yaml
name: Promote Orders release
on:
  workflow_dispatch:
    inputs:
      image:
        description: Full public image@sha256 digest
        required: true
permissions: {contents: read}
concurrency: {group: orders-promotion, cancel-in-progress: false}
jobs:
  staging:
    if: github.ref == 'refs/heads/main'
    runs-on: [self-hosted, linux, orders-lab]
    environment: staging
    steps:
      - uses: actions/checkout@v6
      - name: Deploy staging on the dedicated lab host
        env:
          IMAGE: ${{ inputs.image }}
        run: |
          [[ "$IMAGE" =~ ^ghcr.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$ ]] || exit 2
          cd 01.production-delivery-platform
          bash deploy/release.sh staging "$IMAGE"
  production:
    if: github.ref == 'refs/heads/main'
    needs: staging
    runs-on: [self-hosted, linux, orders-lab]
    environment: production
    steps:
      - uses: actions/checkout@v6
      - name: Promote exactly the same digest
        env:
          IMAGE: ${{ inputs.image }}
        run: |
          [[ "$IMAGE" =~ ^ghcr.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}$ ]] || exit 2
          cd 01.production-delivery-platform
          bash deploy/release.sh production "$IMAGE"
```

## Checkpoint — verify before continuing

Run Promote Orders release using the exact IMAGE digest. Staging completes, production waits for review, and only after approval does port 8082 serve the same digest. Compare $HOME/.local/state/orders-delivery/staging/image and $HOME/.local/state/orders-delivery/production/image on the VM.

Record your actual output, timestamps and resolved versions. Resource IDs, durations and generated names can differ; verify the stated behavior rather than matching incidental values.

## If your result differs

If production starts immediately, inspect Settings → Environments → production and confirm required reviewers are enabled for your repository plan and visibility. A workflow environment declaration alone does not enforce review.

## What to record

Save the command, relevant result and one sentence explaining what it proves. Redact tokens, passwords, private keys and account-specific identifiers before publishing evidence.

## Continue

When this checkpoint passes, continue to [08. Introduce a Failed Release and Roll Back](08-introduce-a-failed-release-and-roll-back.md). The next chapter assumes the state created here.
