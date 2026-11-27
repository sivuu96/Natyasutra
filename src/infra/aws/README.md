# AWS setup

What the deploy workflow expects to exist. Create these once, in a single region (set it as the `AWS_REGION` variable).

## 1. Network and database

- A VPC with two private subnets for the database and two public subnets for the load balancer.
- An RDS PostgreSQL instance (version 16) in the private subnets. Turn on automated backups and deletion protection.
- Store the connection string in AWS Secrets Manager as `natyasutra/database_url`. Format: `postgresql+psycopg://USER:PASSWORD@HOST:5432/DB`.

## 2. Container registry and service

- An ECR repository named `natyasutra-api`.
- An ECS cluster on Fargate, with:
  - a task definition for the API. Image: the ECR image. Port: 8000. Environment: `APP_ENV=production`, `CORS_ORIGINS` set to the Cloudflare Pages domains. Secret: `DATABASE_URL` from Secrets Manager.
  - a service running the task behind an Application Load Balancer, with the health check path `/api/v1/health`.
- A second task definition with the same image and the command overridden to `alembic -c migrations/alembic.ini upgrade head`. The deploy workflow runs this as a one-off task before it updates the service.

## 3. GitHub to AWS access (OIDC, no long-lived keys)

- An IAM OIDC identity provider for `token.actions.githubusercontent.com`.
- An IAM role, for example `natyasutra-github-deploy`, that trusts only this repository and the `main` branch. Give it permission to push to ECR, run and describe ECS tasks, and update the service.
- Put the role ARN in the GitHub secret `AWS_DEPLOY_ROLE_ARN`.

## 4. Cloudflare

- Pages projects for `react/dist` and `html/dist`. Names go in the variables `CF_PAGES_REACT_PROJECT` and `CF_PAGES_HTML_PROJECT`.
- An API token with Pages edit permission, in the secret `CLOUDFLARE_API_TOKEN`. The account ID goes in `CLOUDFLARE_ACCOUNT_ID`.
- A DNS record for the API, for example `api.example.com`, pointing at the load balancer, with the orange-cloud proxy on.

## 5. Variables and secrets

| Name | Kind | Used by |
|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | secret | deploy workflow |
| `AWS_REGION` | variable | deploy workflow |
| `ECR_REPOSITORY` | variable | deploy workflow |
| `ECS_CLUSTER`, `ECS_SERVICE`, `ECS_TASK_FAMILY`, `ECS_MIGRATE_TASK_FAMILY` | variables | deploy workflow |
| `ECS_SUBNETS`, `ECS_SECURITY_GROUPS` | variables | migration task |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | secrets | deploy workflow |
| `CF_PAGES_REACT_PROJECT`, `CF_PAGES_HTML_PROJECT` | variables | deploy workflow |
| `VITE_API_BASE` | variable | React build (the public API origin) |
