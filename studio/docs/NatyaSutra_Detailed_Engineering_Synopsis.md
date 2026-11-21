# NatyaSutra --- Detailed Engineering Plan Synopsis

## Executive objective

Rebuild NatyaSutra as a secure, reproducible, metadata-driven platform
that can be developed rapidly by multiple engineers and AI coding
agents. Preserve the agreed product and experience architecture while
creating clear boundaries between infrastructure, data, administration,
frontend presentation, journey logic and backend services.

The central engineering principle is to build around **versioned
contracts, metadata and registries**, rather than individually
hard-coded pages, forms and services. Every important artifact should be
inspectable, version-controlled, testable and recoverable.

## 1. Recommended target architecture

  Concern                                Recommended direction
  -------------------------------------- ------------------------------------------
  Edge, DNS, CDN, WAF, DDoS protection   Cloudflare
  Cloud infrastructure                   AWS
  Compute                                ECS Fargate
  Relational database                    AWS RDS MySQL
  Object storage                         AWS S3
  Frontend                               Next.js, React, TypeScript
  UI system                              shadcn/ui, Tailwind
  Backend                                Python, FastAPI
  Secrets                                Infisical
  Infrastructure as code                 Terraform
  Database migrations                    Alembic plus a custom migration registry
  CI/CD                                  GitHub Actions
  Testing                                pytest, Playwright, k6 or Locust
  Source control                         Git monorepo

Start with a **modular monolith**: maintain strict domain boundaries
without the deployment and operational overhead of microservices. Avoid
Kubernetes, Redis, Kafka and additional infrastructure until a
demonstrated requirement justifies them. Retain MySQL as the primary
relational database, consistent with the existing architecture
direction.

## 2. Phase 1 --- Secure, reproducible development environment

**Objective:** Establish a controlled development environment that
mirrors production closely enough to make development, migration and
deployment predictable.

### Environment separation

-   Create separate DEV, STAGING and PROD environments.
-   Prefer separate AWS accounts for production and non-production.
-   Isolate databases, buckets, credentials, secret scopes, network
    policies and deployment permissions.
-   Never expose production databases directly to developers or
    development services.
-   Use sanitized/anonymized production-derived snapshots or synthetic
    data in DEV and STAGING.

### Infrastructure

-   Define all infrastructure in Terraform; avoid undocumented manual
    console changes.
-   Use private VPC subnets for application services and RDS.
-   Restrict database access to authorized application services and
    administrative paths.
-   Enable encryption at rest and in transit, automated backups,
    point-in-time recovery, monitoring and centralized logs.
-   Use S3 encryption, versioning, lifecycle policies and appropriate
    access controls.
-   Put controlled ingress/load balancing behind Cloudflare where
    appropriate.
-   Establish repeatable environment provisioning and teardown
    procedures.

### Identity and access

-   Require managed identity and MFA/2FA for infrastructure and internal
    tools.
-   Use Cloudflare Zero Trust Access for protected internal endpoints.
-   Use least-privilege AWS IAM roles and individual developer
    identities; no shared credentials.
-   Separate infrastructure access from application-level identity and
    authorization.
-   Audit privileged access and administrative operations.

### Infisical and runtime secrets

-   Integrate Infisical using workload identity or another short-lived
    authentication mechanism; avoid permanent bootstrap credentials.
-   Retrieve secrets at runtime into process memory and refresh them
    before expiry.
-   Do not persist secrets in `.env` files, source control, container
    images, build arguments, command-line arguments, frontend bundles,
    logs, traces or exception messages.
-   Build common secrets-provider libraries for Python and TypeScript
    rather than allowing each service to implement its own approach.
-   Define secret scopes per environment, rotation, expiry, access
    policies and retrieval auditing.
-   For local development, use an approved short-lived developer
    authentication flow.
-   Be explicit that a running process necessarily has access to secrets
    it uses; the goal is to prevent persistence and accidental
    disclosure, not to claim that in-memory values are inaccessible.

### Phase 1 deliverables and acceptance

Deliver Terraform-managed DEV infrastructure, access controls, Infisical
integration, RDS and S3, monitoring/logging, CI/CD and developer setup
documentation. A new developer should be able to authenticate, clone,
start the application and run tests without copying secrets into local
configuration files.

## 3. Phase 2 --- Data architecture, cleansing and migration

**Objective:** Restructure the complete data architecture and migrate
legacy relational and object data through a repeatable, auditable and
recoverable process.

The existing architecture document describes a substantial MySQL model
(noted in the prior review as 113 tables across 14 domains), legacy CMS
tables and historical data requiring special treatment. It also
describes the context, intent, experience and page-composition concepts.
Validate exact counts and entity definitions against the authoritative
schema before implementation.

### Canonical model and artifacts

Freeze and version: 1. The domain model: entity meaning, ownership and
relationships. 2. The database model: tables, fields, types, indexes,
constraints and foreign keys. 3. The data dictionary: field definitions,
allowed values and semantics. 4. The migration specification:
source-to-target mappings and transformation rules.

Keep these in Git alongside migration code, test fixtures, seeds,
decisions and validation definitions.

### Explicit migration registry

Every source table and record requiring special handling must have an
explicit disposition. Possible actions include map, insert, update,
merge, transform, archive, exclude or delete. Record the reason and
approval for exclusions and destructive actions.

Maintain a migration ledger with at least: - **Migration run:** run ID,
source snapshot ID, target schema version, Git commit hash, operator,
timestamps, status and validation/sign-off state. - **Entity run:**
source/target table, transformation version, expected and actual counts,
status and errors. - **Record mapping/action:** source primary key,
target primary key, action, transformation rule/version, reason and
validation result. - **Exceptions:** source reference, category, issue,
proposed resolution, approval and resolution timestamp.

Keep large before/after snapshots and detailed reports in versioned S3
objects; store hashes and references in the ledger rather than bloating
relational metadata tables.

### Repeatable migration engine

-   Make transformations deterministic and idempotent.
-   Support checkpoints, restart after failure and safe reruns.
-   Use controlled transaction boundaries rather than one enormous
    transaction.
-   Record the exact source snapshot, target schema and code revision
    used.
-   Rebuild a clean target from the approved snapshot and versioned
    artifacts.
-   Define recovery and rollback procedures; retain original source data
    until validation and cutover are complete.

### Data cleansing and human review

Use a four-stage process: 1. **Profile:** discover duplicates, missing
values, invalid references, orphan rows, inconsistent taxonomies,
malformed data and suspicious financial or identity records. 2.
**Propose:** generate suggested merges, corrections, exclusions and
transformations, with reasons and confidence. 3. **Review:** require
human approval for ambiguous, identity-related, financial or destructive
decisions. 4. **Execute and reconcile:** apply approved transformations
and produce before/after reports, exceptions and integrity checks.

AI can accelerate profiling and suggest mappings or anomaly detection,
but must not silently delete, merge or alter important
production-derived records.

### Relational and object storage

Use RDS MySQL for structured entities, relationships, profiles, content
metadata, commerce/financial records and composition configuration. Use
S3 for images, video, audio, documents, originals and derivatives.

Create an asset inventory recording legacy location, destination S3 key,
content type, size, checksum, ownership/reference, migration status and
validation result. Use stable object identifiers in the database, not
temporary URLs or machine-specific filesystem paths.

### Reconciliation

Do not rely on row counts alone. Verify: - Source-to-target row
accounting and dispositions. - Primary key uniqueness and foreign-key
integrity. - Orphans, duplicates and approved exceptions. - Identity and
ownership relationships. - Financial totals and transaction history. -
Media checksums, object existence and references. - Domain-specific
business invariants.

### Controlled migration UX

The future admin console should support: generate plan → preview
differences → review exceptions → approve → execute → reconcile → sign
off. A "single click" should execute an already approved and validated
plan, not make autonomous destructive decisions.

### Phase 2 deliverables and acceptance

Deliver canonical schema and data dictionary, complete source inventory,
versioned mappings and migration registry, transformation runner,
cleansing/exception workflow, S3 asset migration, reconciliation reports
and recovery procedures. An empty target must be reproducible from an
approved snapshot and Git artifacts with the same validated result.

## 4. Phase 3 --- Generated administration and data-management UI

**Objective:** Provide a user-friendly internal application whose
ordinary data-management screens are generated from metadata.

### Technology and generation model

Use Next.js, TypeScript, shadcn/ui and Tailwind---the same frontend
ecosystem as the public application. Prefer this over introducing Lit as
a second frontend stack.

Define declarative metadata for entities, fields, relationships,
validation, display rules and permissions. Generate: - List and detail
views. - Search, filtering and pagination. - Create/edit forms and
validation messages. - Relationship navigation. - Approved bulk
operations. - Change history and audit views.

Allow purpose-built workflows where generic CRUD is insufficient,
especially for financial operations, enrolments, identity resolution and
complex content relationships. Validate metadata against the canonical
schema.

### RBAC and audit

Begin with roles such as Super Admin, Data Admin, Content Editor,
Finance Admin and Read Only. Enforce permissions at the API/service
layer---not merely by hiding controls in the UI. Audit who changed what,
capture before/after values where appropriate, require confirmation for
destructive actions and add approval workflows for sensitive financial
or identity changes.

### Migration console

Include a dedicated migration area to select snapshots and versions, run
profiling, review proposed changes, resolve exceptions, approve
execution, monitor progress and inspect reconciliation reports.

### Phase 3 deliverables and acceptance

Deliver metadata-driven CRUD, search and relationship management, RBAC,
audit history and migration console. Adding an entity through metadata
should generate its standard interface while sensitive operations remain
controlled and auditable.

## 5. Phase 4 --- Frontend restructuring

**Objective:** Rebuild the public experience as a clean, reusable,
configurable Next.js application that can render dynamically according
to visitor journey and characteristics.

### Technology and migration approach

Use Next.js App Router, React, TypeScript, Tailwind, shadcn/ui and Zod
for runtime schema validation. Migrate incrementally rather than
rewriting everything at once. Begin with the homepage, guru page and
class page as reference experiences.

### Separation of concerns

Keep distinct boundaries for: - Design tokens, themes and styling. -
Primitives and reusable components. - Configurable visual blocks and
layouts. - Domain-specific frontend features. - Journey/step/intent
logic. - Page composition and registries. - API services and mock
implementations. - Types and runtime schemas.

### Component and composer architecture

Keep the component vocabulary small, highly configurable and addressable
through stable identifiers. The existing architecture describes 12
reusable blocks, approximately 8 layouts and a seven-zone page canvas;
preserve these concepts and verify their exact names and specifications
against the architecture source.

The page composer selects and orders blocks and supplies configuration;
it must not contain presentation code. Individual blocks render their
content and slots; they must not decide journey-selection logic. Resolve
block identifiers through a registry and validate structured page
specifications from the backend. Unknown or invalid block types should
fail gracefully with safe fallbacks.

### Mock services and contracts

Define API contracts before backend implementation. Build mock services
against those contracts so frontend development does not wait for the
real services. Mock and production implementations must be
interchangeable and return realistic data for visitor states such as
anonymous, curious, explorer, beginner student, returning learner and
high purchase intent.

### Architecture verification

Enforce boundaries through ESLint restrictions, strict TypeScript,
import/dependency checks, component contract tests and automated
architectural checks that developers and Claude Code can run.

### Phase 4 deliverables and acceptance

Deliver the Next.js application, design system, reusable components,
block/layout registries, page composer integration, journey definitions,
API contracts and mock services. A new experience should be assembled by
changing content and composition configuration rather than writing
page-specific presentation code.

## 6. Phase 5 --- Backend services and testing

**Objective:** Implement domain services and establish thorough
automated quality controls.

### Backend structure

Use Python/FastAPI and begin with a modular monolith. Organize clear
domains around the agreed model, including users, profiles, content,
programmes, music, commerce, revenue, engagement, context, intent,
composer and media. Keep shared infrastructure concerns---database,
security, secrets, storage, logging and events---separate from domain
rules. Domains should own their business logic and data access; avoid
arbitrary cross-domain SQL.

Use background workers for asynchronous/non-critical processing such as
media processing, analytics and profile updates. Do not split into
independently deployed microservices until there is a clear scaling or
operational reason.

### Suggested implementation order

1.  Authentication and authorization.
2.  Content API.
3.  Media service.
4.  Visit identity and tracking.
5.  Signal pipeline.
6.  Intent engine.
7.  Page composer.
8.  Profile service.
9.  Recommendation engine.
10. Conversation agent/RAG.

Start with deterministic content, visit and composition APIs, using mock
intent where needed. This gets the first end-to-end experience working
before the full intelligence engine exists.

### Testing

  ------------------------------------------------------------------------
  Layer                   Tool                     Purpose
  ----------------------- ------------------------ -----------------------
  Unit                    pytest                   Domain and business
                                                   logic

  API integration         pytest + HTTPX           Endpoint behaviour

  Database                pytest + test MySQL      Queries, constraints
                                                   and transactions

  Contract                OpenAPI/schema           Frontend/backend
                          validation               compatibility

  End-to-end              Playwright               Critical visitor
                                                   journeys

  Performance             k6 or Locust             Load, latency and
                                                   concurrency

  Security                Automated                Vulnerabilities and
                          dependency/application   unsafe configuration
                          scans                    
  ------------------------------------------------------------------------

Test referential integrity, transaction rollback, concurrent writes and
migration repeatability. Test blocks with complete, partial and missing
optional content; verify responsive layouts, unknown-block handling and
neutral fallbacks. Test a full visitor journey: anonymous arrival →
exploration → signal capture → intent update → updated composition →
guru discovery → class viewing.

Initial performance targets to validate against real traffic
requirements: - Ordinary read API p95 below 300 ms. - Page composer p95
below 500 ms, excluding external AI inference. - No material degradation
under an agreed concurrent-user load.

### CI/CD gates

Every pull request runs formatting, linting, type checking,
unit/integration tests, schema compatibility checks, frontend build,
security/dependency scans and migration checks. Merge to the integration
branch deploys DEV. STAGING requires explicit promotion. PROD requires
authorized approval and a verified release artifact.

## 7. Cross-cutting workstream --- Parallel engineering and AI collaboration

This must be designed from the beginning because multiple developers and
Claude Code agents will work concurrently.

### Git as the source of truth

Keep all application-defining artifacts in Git: source code,
domain/database models, migrations and registry definitions,
infrastructure, API contracts, schemas, component/entity metadata,
journey/composition definitions, tests, ADRs, standards and runbooks.

Use the collaboration platform/database for operational
coordination---tasks, assignments, discussions, review status, progress
and approvals---but not as the only home of canonical technical
definitions.

### Monorepo proposal

``` text
natyasutra/
  apps/
    web/
    admin/
    api/
  packages/
    ui/
    contracts/
    schemas/
    domain/
    test-utils/
  data/
    architecture/
    migrations/
    seeds/
  infrastructure/
    terraform/
  docs/
    architecture/
    decisions/
    standards/
    runbooks/
  tests/
    e2e/
    performance/
    security/
  .github/
    workflows/
    pull_request_template.md
    CODEOWNERS
```

### Developer/AI operating contract

Every task must define objective, scope, dependencies, acceptance
criteria, required tests and deliverables. Developers/agents work in
separate branches or worktrees. No direct commits to `main`; no
unreviewed schema migrations; shared contract changes require review;
every task includes tests; every PR includes an architectural impact
statement. AI-generated code passes the same quality and review gates as
human-written code.

Create a root `CLAUDE.md` explaining architecture, repository structure,
technology choices, boundaries, naming, security, testing and setup. Add
domain-specific instructions for data, frontend, backend and
infrastructure. Maintain Architecture Decision Records (ADRs) for
material choices so agents do not make contradictory assumptions.

## 8. Cross-cutting security and operations

-   **Data protection:** Classify data before production-derived
    snapshots are copied. Mask/anonymize personal, payment, bank,
    authentication and other sensitive data; prefer synthetic data when
    practical.
-   **Schema governance:** All schema changes are reviewed and
    represented by versioned migrations.
-   **Secrets:** Never place secrets in Git, `.env`, images, build
    arguments, browser bundles, logs, traces or command-line arguments.
-   **Least privilege:** Isolate environments and use individual
    identities, short-lived credentials and scoped permissions.
-   **Audit:** Record privileged actions, data changes, migration
    decisions and approvals.
-   **Observability:** Add centralized logs, metrics, monitoring and
    actionable alerts early; avoid sensitive payloads in logs.
-   **Feature flags:** Introduce early, especially for page composition,
    personalization and the conversation agent.
-   **Recovery:** Test database restore, object recovery, migration
    recovery, deployment rollback and incident procedures.
-   **Release governance:** Promote verified artifacts DEV → STAGING →
    PROD with explicit production approval.

## 9. Indicative delivery schedule

An approximately eight-week initial foundation programme is possible
with a small team working in parallel; it is an estimate, not a
commitment. Full legacy migration and production readiness may take
longer.

  -----------------------------------------------------------------------
  Timing                  Focus                   Outcomes
  ----------------------- ----------------------- -----------------------
  Weeks 1--2              Secure foundation       AWS DEV, Cloudflare,
                                                  Infisical, Terraform,
                                                  CI/CD and repository
                                                  standards

  Weeks 2--3              Data architecture       Schema freeze, source
                                                  inventory, migration
                                                  registry,
                                                  transformation
                                                  framework and S3 design

  Weeks 3--4              Migration/admin         Profiling, cleansing
                          foundation              proposals, migration
                                                  runner, generated CRUD
                                                  and RBAC

  Weeks 3--5              Frontend foundation     Next.js, design tokens,
                                                  component registry,
                                                  layouts, blocks and
                                                  mock APIs

  Weeks 5--6              First vertical slice    Content API, media,
                                                  homepage, guru page,
                                                  class page and
                                                  integration tests

  Weeks 6--7              Intelligence foundation Visit service, signals,
                                                  initial intent logic
                                                  and composer
                                                  integration

  Weeks 7--8              Integration/hardening   Playwright journeys,
                                                  reconciliation,
                                                  performance tests and
                                                  STAGING deployment
  -----------------------------------------------------------------------

### Five accountable workstreams

-   **A --- Infrastructure:** AWS, Cloudflare, Terraform, Infisical.
-   **B --- Data:** Schema, migration, cleansing and storage.
-   **C --- Admin:** Generated UI, RBAC and migration console.
-   **D --- Frontend:** Next.js, design system, components, journeys and
    composer.
-   **E --- Backend:** FastAPI, domain services, APIs and testing.

A person may own multiple workstreams, but each workstream needs one
accountable owner. Define dependencies and contracts so work can proceed
in parallel without conflicting changes.

## 10. First 10 working days

  Day   Outcome
  ----- -----------------------------------------------------
  1     Freeze technology choices and repository structure
  2     Establish AWS DEV and Cloudflare access
  3     Integrate Infisical and common secret provider
  4     Set up Terraform, CI/CD and developer workflow
  5     Import source schema and produce schema inventory
  6     Finalize target schema and data dictionary
  7     Build migration registry and profiling framework
  8     Define API contracts and frontend architecture
  9     Start admin generator and Next.js application shell
  10    Run the first integrated build in DEV

By day 10, aim to have a working secure environment, formal migration
plan, running application shell and first generated admin interface.
This creates a shared foundation before broad parallel coding begins.

## 11. Definition of done

### Foundation

-   New developers can set up without manually provisioning static
    secrets.
-   DEV is isolated and MFA-protected.
-   Infrastructure can be recreated from Git.
-   Runtime secrets are not persisted in application configuration
    files.

### Data

-   Every source table and asset has an explicit disposition.
-   Every transformed/excluded record has an auditable reason.
-   Migrations are repeatable and recoverable.
-   Data passes row-level and business-level reconciliation.
-   Media assets are migrated and verified.

### Administration

-   New entities can be configured through metadata.
-   Standard CRUD interfaces are generated.
-   API-level permissions are enforced.
-   Changes and migration approvals are auditable.

### Frontend

-   Homepage, guru and class experiences work.
-   Components are reusable, configurable and addressable.
-   Mock and production services implement identical contracts.
-   Composition logic is separate from presentation.

### Backend

-   Core domain services work.
-   API contracts are validated.
-   Critical end-to-end journeys pass.
-   Performance and security tests pass.
-   Deployment and recovery procedures are tested.

## 12. Decisions to approve and freeze

  Decision                   Proposed direction
  -------------------------- -------------------------------------
  Cloud provider             AWS
  Edge/security              Cloudflare
  Primary database           MySQL on RDS
  Object storage             S3
  Compute                    ECS Fargate
  Secrets                    Infisical
  Infrastructure as code     Terraform
  Frontend                   Next.js, React, TypeScript
  Admin                      Next.js + shadcn/ui
  Backend                    FastAPI
  Application architecture   Modular monolith initially
  Migrations                 Alembic + custom migration registry
  Repository                 Monorepo
  CI/CD                      GitHub Actions
  Testing                    pytest + Playwright + k6/Locust
  Caching                    Defer until justified
  AI integration             Separate domain/service boundary

These are recommendations for formal approval, not assumptions that
every decision has already been finalized.

## 13. Guiding principle and immediate next artifacts

Build the platform around **contracts, metadata and registries**: -
Infrastructure is defined by Terraform. - Secrets are managed through
Infisical. - Data transformations are defined by versioned migration
metadata. - Admin interfaces are generated from entity metadata. -
Frontend components are selected through stable registries. -
Experiences are assembled through the page composer. - APIs are governed
by versioned contracts. - Tests verify contracts and architectural
boundaries.

Do not build the complete intelligent personalization engine before the
platform foundation works. First deliver secure infrastructure,
validated data, content APIs, the three core experiences and
deterministic page composition with mock intent. Then progressively
introduce real behavioural signals, intent scoring, recommendations and
AI.

Turn this synopsis into four implementation-ready artifacts:

1.  **Architecture Decision Record (ADR):** technology choices,
    deployment topology, security model and architectural boundaries.
2.  **Engineering backlog:** epics, tasks, dependencies, owners and
    acceptance criteria across all five phases.
3.  **Repository specification:** directory structure, coding standards,
    Claude instructions, Git workflow and CI/CD requirements.
4.  **Data migration specification:** migration registry schema,
    transformation framework, cleansing/approval workflow and
    reconciliation design.

These artifacts should become the shared engineering contract for the
team and its AI coding agents.
