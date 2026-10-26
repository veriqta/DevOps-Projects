# 04. GitHub Pages Deployment

[← All projects](../README.md) · **Beginner** · GitHub Actions

Deploy a small static site through an auditable workflow.

## Prerequisites

A GitHub account, Git, and a writable fork or new repository. The linked upstream archive cannot accept pushes.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `pages.yml` | Configuration or starter code referenced in the steps below. |
| `site` | Static site published by the Pages workflow. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 04.github-pages-deployment
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Use a writable GitHub repository

Create an empty repository in your GitHub account. From this project folder, move to the parent repository root and initialize it only if you are working from a ZIP:

```bash
cd ..
git init -b main
git add .
git commit -m "Add DevOps project labs"
git remote add origin https://github.com/YOUR_USER/YOUR_REPOSITORY.git
git push -u origin main
cd 04.github-pages-deployment
```

Replace the URL with your own writable repository. If you already cloned a writable repository, skip initialization and stay in this project folder.

### 2. Install the deployment workflow

```bash
mkdir -p ../.github/workflows
cp files/pages.yml ../.github/workflows/pages.yml
git add ../.github/workflows/pages.yml files/site
git commit -m "Deploy lab site to Pages"
git push
```

The workflow lives at the repository root because GitHub requires it there. It publishes this project's `files/site` directory automatically.

### 3. Enable deployment

Open your repository → Settings → Pages → Build and deployment → Source → **GitHub Actions**. Open Actions → Deploy Pages → Run workflow if the initial push occurred before Pages was enabled. Open the deployment URL from the completed job.

### 4. Make a change

Change the heading in `files/site/index.html`, commit, push and wait for a successful deployment. Refresh the live site.

## Verify completion

The workflow is green, the site returns HTTP 200, and the heading matches the latest commit. Record the commit SHA and deployment URL.

## Troubleshooting

A 403 often means Pages is disabled or the environment blocks the branch. Confirm `main` is your branch or change the workflow trigger.

## Cleanup

In Settings → Pages unpublish the site. Remove `../.github/workflows/pages.yml` and commit the removal.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented github pages deployment in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

---

[← Previous: 03](../03.nginx-log-analyser/README.md) · [All projects](../README.md) · [Next: 05 →](../05.ssh-remote-server-setup/README.md)
