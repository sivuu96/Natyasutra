# NatyaSutra app skeleton

A starting point for the Tailwind + React + FastAPI + PostgreSQL stack, deployed to Cloudflare (frontends) and AWS (API and RDS).

## Layout

| Folder | What it is | Deploys to |
|---|---|---|
| `html/` | Static HTML pages built with Tailwind CSS | Cloudflare Pages |
| `react/` | Single-page app built with Vite, React and Tailwind CSS | Cloudflare Pages |
| `python/` | FastAPI service (`app/`) and its tests | AWS (container on ECS, behind a load balancer) |
| `migrations/` | Alembic migration scripts for PostgreSQL | Run once per deploy, against RDS |
| `infra/` | Cloudflare and AWS configuration notes | Read by the people setting up the accounts |

The GitHub Actions workflows live in `.github/workflows/` at the repository root, because that is the only place GitHub reads them from. They are `ci.yml` (tests and builds on every push and pull request) and `deploy.yml` (deploys from `main`).

## Run locally

```bash
cp .env.example .env            # set DATABASE_URL to a local Postgres

# Database
cd migrations && alembic -c alembic.ini upgrade head && cd ..

# API
cd python && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (second terminal)
cd react && npm install && npm run dev     # proxies /api to :8000

# Static HTML (optional)
cd html && npm install && npm run build
```

## Deploy

1. Cloudflare: create two Pages projects, one for `html/dist` and one for `react/dist`. See `infra/cloudflare/wrangler.toml`.
2. AWS: create the RDS PostgreSQL instance, an ECR repository, an ECS cluster and service, and an IAM role for GitHub OIDC. See `infra/aws/README.md`.
3. GitHub: add the secrets and variables listed in `.github/workflows/deploy.yml`.
4. Push to `main`. The deploy workflow builds the API image, runs migrations, rolls the ECS service and deploys both frontends.

## Notes

- This is a skeleton. Routes, models and styling are examples to replace.
- The first migration creates two tables from the content data model (`dim_language` and `cnt_item`). The full model is in `studio/docs/content-model.md`.
- Keep secrets out of the repository. Use `.env` locally, and GitHub secrets or AWS Secrets Manager in CI and production.
