# 04. GitHub Pages Deployment

[← All projects](../../README.md) · **Beginner** · GitHub Actions

Deploy a small static site through an auditable workflow.

## Prerequisites

A GitHub account, Git, and a writable fork or new repository. The linked upstream archive cannot accept pushes.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Prepare a writable repository

If working from the ZIP, create an empty GitHub repository, then run:

```bash
git init -b main
git add .
git commit -m "Add DevOps project labs"
# Replace this URL with YOUR writable repository:
git remote add origin https://github.com/YOUR_USER/YOUR_REPOSITORY.git
git push -u origin main
```

If you already cloned your own fork, skip initialization.

### 2. Add the deployment workflow

```bash
mkdir -p .github/workflows
cp 02.examples/pages.yml .github/workflows/pages.yml
git add .github/workflows/pages.yml 06.site
git commit -m "Deploy lab site to Pages"
git push
```

### 3. Enable deployment

Open your repository → Settings → Pages → Build and deployment → Source → **GitHub Actions**. Open Actions → Deploy Pages → Run workflow if the initial push occurred before Pages was enabled. Open the deployment URL from the completed job.

### 4. Make a change

Change the heading in `06.site/index.html`, commit, push and wait for a successful deployment. Refresh the live site.

## Verify completion

The workflow is green, the site returns HTTP 200, and the heading matches the latest commit. Record the commit SHA and deployment URL.

## Troubleshooting

A 403 often means Pages is disabled or the environment blocks the branch. Confirm `main` is your branch or change the workflow trigger.

## Cleanup

In Settings → Pages unpublish the site. Remove `.github/workflows/pages.yml` and commit the removal.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

---

[← Previous: 03](../03.nginx-log-analyser/README.md) · [All projects](../../README.md) · [Next: 05 →](../05.ssh-remote-server-setup/README.md)
