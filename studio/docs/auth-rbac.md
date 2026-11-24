# Auth and RBAC data model (first cut)

Status: **draft for discussion.** Covers identity, MFA, tokens, visitor tracking, roles, permissions, policies, assignments and audit logs. Target: MySQL 8, InnoDB, utf8mb4. Table prefixes follow the target model in the architecture PDF (section 12): `usr_`, `ctx_`, `eng_`, `log_`.

Items marked **[reconstructed]** were not in the final version of the earlier RBAC reply (it was cut off). Check them before migrating.

---

## 1. Actors

| Actor | Who | Login | 2FA |
|---|---|---|---|
| Visitor | Anonymous browser | No | No |
| Customer | Account holder who browses, buys and learns (replaces "student") | Yes | Opt-in |
| Contributor | Guru, artist or producer. Sees how their work does, answers questions | Yes | **Mandatory at every login** |
| Admin | Manages content and site structure. Permissions come from policies | Yes | **Mandatory** |
| Superadmin | Full access, separate role | Yes | **Mandatory**, every action audited |

**Why:** the legacy model treats people as two groups (admin and student). Contributors and admins need different capabilities, and visitors have no account at all. Four actors plus superadmin matches how the business works.

A single account can hold several roles through `usr_account_roles`, so a guru who also buys classes is one person with one login.

---

## 2. Design principles

- **Role says who you are. Policy says what you may do.** Roles are a short fixed set. Policies are data, so finance and content rights can change without a deploy.
- **Permissions are granular, `resource.action`.** Examples: `programme.view`, `programme.update`, `payout.approve`, `bank_details.reveal`. They are defined in code and seeded. Admins cannot create new ones.
- **Deny by default.** No grant means no access.
- **One authorization check on the server.** Hiding buttons in the UI is not enforcement.
- **No privilege escalation.** An admin can only grant a policy whose permissions they already hold.
- **Separation of duties for money.** Creating and approving a payout or refund are different permissions. The requester cannot approve their own.
- **Filtered scope for contributors.** A contributor policy can only be assigned as `filtered`, so a contributor never gets unrestricted access.
- **Time-bound grants.** Assignments have an optional `expires_at`.
- **Every grant and revoke is logged.**
- **No raw SQL from input.** Filters only use fields in a code registry.

---

## 3. Identity tables

```sql
CREATE TABLE usr_accounts (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email             VARCHAR(255) NOT NULL,
  phone             VARCHAR(20) NULL,
  password_hash     VARCHAR(255) NULL,            -- argon2id or bcrypt; NULL until set
  status            ENUM('pending','active','suspended','closed') NOT NULL DEFAULT 'pending',
  email_verified_at DATETIME NULL,
  last_login_at     DATETIME NULL,
  password_changed_at DATETIME NULL,
  legacy_source     VARCHAR(40) NULL,             -- e.g. 'tb_student', 'tb_admin'; for migration tracing
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_accounts_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** one row per login for all actors. Absorbs the login columns of `tb_student` and `tb_admin`. Profile fields (names, bio, addresses) stay out. They move to the Learners and Gurus groups.

```sql
CREATE TABLE usr_account_roles (
  account_id BIGINT UNSIGNED NOT NULL,
  role       ENUM('customer','contributor','admin','superadmin') NOT NULL,
  granted_by BIGINT UNSIGNED NULL,
  granted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revoked_at DATETIME NULL,
  PRIMARY KEY (account_id, role),
  CONSTRAINT fk_roles_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id),
  CONSTRAINT fk_roles_granted_by FOREIGN KEY (granted_by) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** roles are rows, not a column, so one person can hold several and revocation keeps history. `revoked_at` replaces deletion.

```sql
CREATE TABLE usr_contributor_links (
  account_id       BIGINT UNSIGNED NOT NULL,
  contributor_type ENUM('guru','artist','producer') NOT NULL,
  contributor_id   BIGINT UNSIGNED NOT NULL,
  verified_at      DATETIME NULL,
  PRIMARY KEY (account_id, contributor_type, contributor_id),
  KEY ix_links_contributor (contributor_type, contributor_id),
  CONSTRAINT fk_links_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** links an account to its guru, artist or producer record. `own` scope checks use this table: `$self.guru_ids` resolves from here at evaluation time. `contributor_id` has no foreign key because it points at one of three tables. The Gurus group settles those targets.

---

## 4. MFA and tokens

```sql
CREATE TABLE usr_mfa_factors (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  account_id    BIGINT UNSIGNED NOT NULL,
  factor_type   ENUM('totp','webauthn') NOT NULL,
  secret_enc    VARBINARY(512) NULL,              -- TOTP secret, encrypted at rest (app-level key)
  credential_id VARBINARY(255) NULL,              -- WebAuthn credential
  label         VARCHAR(80) NULL,
  verified_at   DATETIME NULL,
  last_used_at  DATETIME NULL,
  revoked_at    DATETIME NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY ix_mfa_account (account_id, revoked_at),
  CONSTRAINT fk_mfa_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usr_mfa_recovery_codes (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  account_id  BIGINT UNSIGNED NOT NULL,
  code_hash   CHAR(64) NOT NULL,                  -- SHA-256 of the code; codes are never stored in clear
  used_at     DATETIME NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY ix_recovery_account (account_id, used_at),
  CONSTRAINT fk_recovery_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usr_tokens (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  account_id  BIGINT UNSIGNED NOT NULL,
  purpose     ENUM('activation','password_reset','email_verify','api','mfa_challenge') NOT NULL,
  token_hash  CHAR(64) NOT NULL,                  -- SHA-256; the raw token is sent once, never stored
  expires_at  DATETIME NOT NULL,
  used_at     DATETIME NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_tokens_hash (token_hash),
  KEY ix_tokens_account (account_id, purpose, used_at),
  CONSTRAINT fk_tokens_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** activation, reset and API tokens need a home, and the legacy `tb_student` columns (`activation_key`, `verification_code`, `api_token`) cannot hold several live tokens with expiry. Storing hashes means a database leak does not expose live tokens. The PDF's 113 tables do not include these, so the total goes past 113. We accept that rather than hide it in a wide table.

---

## 5. Visitor tracking

```sql
CREATE TABLE ctx_visitors (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  cookie_id       CHAR(36) NOT NULL,              -- random UUID set in a first-party cookie
  account_id      BIGINT UNSIGNED NULL,           -- set on sign-in
  first_seen_at   DATETIME NOT NULL,
  last_seen_at    DATETIME NOT NULL,
  first_referrer  VARCHAR(500) NULL,
  utm_source      VARCHAR(100) NULL,
  utm_medium      VARCHAR(100) NULL,
  utm_campaign    VARCHAR(100) NULL,
  device_class    ENUM('desktop','tablet','mobile','unknown') NOT NULL DEFAULT 'unknown',
  country_code    CHAR(2) NULL,                   -- coarse only; no raw IP stored
  consent_status  ENUM('unknown','granted','denied','withdrawn') NOT NULL DEFAULT 'unknown',
  consent_at      DATETIME NULL,
  UNIQUE KEY uq_visitors_cookie (cookie_id),
  KEY ix_visitors_account (account_id),
  CONSTRAINT fk_visitors_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ctx_visits (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  visitor_id   BIGINT UNSIGNED NOT NULL,
  started_at   DATETIME NOT NULL,
  ended_at     DATETIME NULL,
  entry_page   VARCHAR(500) NOT NULL,
  exit_page    VARCHAR(500) NULL,
  source       VARCHAR(100) NULL,
  KEY ix_visits_visitor (visitor_id, started_at),
  CONSTRAINT fk_visits_visitor FOREIGN KEY (visitor_id) REFERENCES ctx_visitors(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE eng_events (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  visit_id    BIGINT UNSIGNED NOT NULL,
  visitor_id  BIGINT UNSIGNED NOT NULL,
  account_id  BIGINT UNSIGNED NULL,
  event_type  VARCHAR(40) NOT NULL,              -- page_view, class_viewed, search, add_to_cart, ...
  subject_type VARCHAR(40) NULL,                  -- programme, music, product, ...
  subject_id  BIGINT UNSIGNED NULL,
  occurred_at DATETIME(3) NOT NULL,
  payload     JSON NULL,
  KEY ix_events_visit (visit_id, occurred_at),
  KEY ix_events_visitor (visitor_id, occurred_at),
  KEY ix_events_type (event_type, occurred_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** the journey is `ctx_visits` plus ordered `eng_events`. `account_id` on the visitor links the anonymous journey to the account on sign-in, and that link is kept.

**Privacy:** visitor data needs a consent record, and raw IP addresses are not stored. Proposed retention is 12 months, to be confirmed. A purge job deletes visits and events older than the window and keeps aggregates.

---

## 6. Logs

```sql
CREATE TABLE log_login_attempts (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  account_id        BIGINT UNSIGNED NULL,         -- NULL when no account matched
  identifier_tried  VARCHAR(255) NULL,            -- what was typed; truncated
  outcome           ENUM('success','bad_password','unknown_account','mfa_failed','locked','suspended') NOT NULL,
  ip_hash           CHAR(64) NULL,                -- salted hash, not raw IP
  user_agent        VARCHAR(255) NULL,
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY ix_login_account (account_id, created_at),
  KEY ix_login_created (created_at),
  CONSTRAINT fk_login_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE log_admin_actions (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  actor_id     BIGINT UNSIGNED NOT NULL,
  action       VARCHAR(80) NOT NULL,              -- permission code or policy.grant / policy.revoke
  target_type  VARCHAR(40) NULL,
  target_id    VARCHAR(64) NULL,
  before_json  JSON NULL,
  after_json   JSON NULL,
  ip_hash      CHAR(64) NULL,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY ix_admin_actor (actor_id, created_at),
  KEY ix_admin_target (target_type, target_id),
  CONSTRAINT fk_admin_actor FOREIGN KEY (actor_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Why:** `log_login_attempts` replaces `tb_student_login_log` and `student_login_attempt_failed`. It records successes and failures, and covers admins and contributors, which were never logged before. `log_admin_actions` is the audit trail for sensitive reads and every grant or revoke.

---

## 7. Permissions, policies and assignments (RBAC)

```sql
CREATE TABLE usr_permissions (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(80) NOT NULL,              -- e.g. payout.approve
  resource     VARCHAR(40) NOT NULL,
  action       VARCHAR(30) NOT NULL,
  is_sensitive TINYINT(1) NOT NULL DEFAULT 0,     -- requires fresh step-up 2FA
  description  VARCHAR(255) NULL,
  UNIQUE KEY uq_permissions_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usr_policies (
  id          SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code        VARCHAR(60) NOT NULL,
  name        VARCHAR(120) NOT NULL,
  actor_role  ENUM('admin','contributor') NOT NULL,  -- who may hold it
  max_scope   ENUM('all','filtered') NOT NULL,       -- contributor policies: 'filtered'
  is_system   TINYINT(1) NOT NULL DEFAULT 1,
  description VARCHAR(500) NULL,
  UNIQUE KEY uq_policies_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usr_policy_permissions (
  policy_id     SMALLINT UNSIGNED NOT NULL,
  permission_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (policy_id, permission_id),
  CONSTRAINT fk_pp_policy FOREIGN KEY (policy_id) REFERENCES usr_policies(id),
  CONSTRAINT fk_pp_permission FOREIGN KEY (permission_id) REFERENCES usr_permissions(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE usr_policy_assignments (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  account_id   BIGINT UNSIGNED NOT NULL,
  policy_id    SMALLINT UNSIGNED NOT NULL,
  scope        ENUM('all','filtered') NOT NULL DEFAULT 'filtered',
  granted_by   BIGINT UNSIGNED NOT NULL,
  granted_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at   DATETIME NULL,
  revoked_at   DATETIME NULL,
  revoked_by   BIGINT UNSIGNED NULL,
  reason       VARCHAR(255) NULL,
  KEY ix_assign_account (account_id, revoked_at, expires_at),
  CONSTRAINT fk_assign_account FOREIGN KEY (account_id) REFERENCES usr_accounts(id),
  CONSTRAINT fk_assign_policy FOREIGN KEY (policy_id) REFERENCES usr_policies(id),
  CONSTRAINT fk_assign_granted_by FOREIGN KEY (granted_by) REFERENCES usr_accounts(id),   -- [reconstructed]
  CONSTRAINT fk_assign_revoked_by FOREIGN KEY (revoked_by) REFERENCES usr_accounts(id)    -- [reconstructed]
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- [reconstructed] Filters restrict an assignment to matching rows.
-- Example rows: programme.id IN (12,15); payout.payee_guru_id IN $self.guru_ids; payout.amount <= 50000
CREATE TABLE usr_policy_assignment_filters (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  assignment_id BIGINT UNSIGNED NOT NULL,
  field_code    VARCHAR(80) NOT NULL,             -- must exist in the code registry, e.g. payout.payee_guru_id
  operator      ENUM('eq','in','lte','gte','between') NOT NULL,
  value_json    JSON NULL,                        -- literal values, or a reference such as {"ref":"$self.guru_ids"}
  KEY ix_filters_assignment (assignment_id),
  CONSTRAINT fk_filters_assignment FOREIGN KEY (assignment_id) REFERENCES usr_policy_assignments(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### How a check works

1. Load the account's active roles (`revoked_at IS NULL`).
2. Load active assignments (`revoked_at IS NULL` and `expires_at` null or in the future).
3. For each assignment, take the policy's permissions. If the assignment is `filtered`, keep only rows that match its filters.
4. A request is allowed when some assignment grants the permission and, for row-level checks, the row passes that assignment's filters.
5. Sensitive permissions (`is_sensitive = 1`) additionally require a step-up 2FA within a short window.
6. Effective permissions are the union across policies.

Superadmin passes every check implicitly, and is still audited.

### Worked example

Finance policy on `usr_policies` with permissions `payout.view`, `payout.approve`, `refund.create`, `transaction.view`, `report.export`. Assigned to account 42 with scope `filtered` and filters:

- `payout.amount <= 50000`
- `payout.currency IN ('INR')`

Account 42 can view and approve payouts up to 50,000 INR. Approving a payout they requested is refused by the separation-of-duties rule. A payout of 80,000 is invisible to them, so the check returns not-found rather than forbidden, to avoid leaking existence.

A contributor (guru 7) holds "Contributor (own)" with `programme.update` and `payout.view`, scope `filtered`, filter `payout.payee_guru_id IN $self.guru_ids`. Their own payouts show. Another guru's do not.

---

## 8. Policies (first cut)

| Policy | Actor | Max scope | Covers | Deliberately excluded |
|---|---|---|---|---|
| Catalogue manager | admin | all | programme, music, product CRUD and publish; pricing | payouts, refunds |
| Content editor | admin | all | pages, banners, menus, homepage placement | pricing, money |
| Finance | admin | filtered | payout view and approve, refund create, transaction and revenue reports, export | catalogue edits, account deletion |
| Support | admin | filtered | customer view, purchase view, password-reset initiation | bank reveal, refunds |
| Moderator | admin | all | feedback and review view, hide, respond | pricing, money |
| Contributor (own) | contributor | filtered | own programmes and music view and update, own feedback respond, own earnings view, own bank update with step-up 2FA | any other contributor's data |

These are proposals. The list of permissions per policy is to be finalised with the team.

---

## 9. Legacy migration map

| Legacy | Target | Notes |
|---|---|---|
| `tb_admin` | `usr_accounts` + `usr_account_roles` (admin) + policy assignments | Map `user_type` 1 to superadmin, 2 to admin with Catalogue or Content policy, 3 to admin with Finance policy. Map `accessible_menus` to real grants. Archive the table as `cms_archive_admin` once the rows exist. |
| `tb_student` (login columns) | `usr_accounts` + `usr_account_roles` (customer) | Profile columns move to the Learners group. |
| `tb_student_login_log` | `log_login_attempts` (outcome = success) | |
| `student_login_attempt_failed` | `log_login_attempts` (outcome = bad_password / unknown_account) | Only 20 rows in the dump. Not yet decided whether to migrate. |
| `ci_sessions` | unchanged | Kept while the CI backend is live. |
| `tb_guru_basics`, `tb_producer` | `usr_contributor_links` | Confirm these are the four legacy tables the PDF means. |

**Password migration:** legacy hashes look like unsalted MD5. Recommended: do not carry them forward. Force a password reset for every migrated account, issued as a `password_reset` token.

---

## 10. Open decisions

Each has the default used in this draft.

1. Should one account hold several roles? **Default: yes.**
2. Do contributors have mandatory 2FA at every login, or only for sensitive actions? **Default: every login.**
3. Do customers get 2FA? **Default: opt-in.**
4. Is the CI admin panel being retired? **Default: yes, `tb_admin` goes to the archive.**
5. Visitor retention period. **Default: 12 months, no raw IPs.**
6. Link the visitor journey to the account on sign-in? **Default: yes.**
7. Per-menu permissions now, or three roles only? **Default: policies now, in the schema; minimal UI.** RBAC moves from Phase 3 in the synopsis.
8. Is `ctx_` visitor context in the PDF? **Default: yes, as assumed. Confirm.**
9. Which policies are missing from the first cut? (Section 8.)
10. Who may grant superadmin? **Default: only another superadmin. At least two accounts, one as break-glass. The last superadmin cannot be removed.**
11. Should contributors ever see another contributor's data? **Default: no.**
12. Do the 20 failed-login rows in the dump matter? **Default: drop, do not migrate.**
13. Do admins still log in by username? The sign-in mockup uses email only. **Default: email only.**

---

## 11. Table count

Auth and access tables added beyond the PDF's 113 targets: `usr_accounts`, `usr_account_roles`, `usr_contributor_links`, `usr_mfa_factors`, `usr_mfa_recovery_codes`, `usr_tokens`, `usr_permissions`, `usr_policies`, `usr_policy_permissions`, `usr_policy_assignments`, `usr_policy_assignment_filters`, `ctx_visitors`, `ctx_visits`, `eng_events`, `log_login_attempts`, `log_admin_actions`. That is 16 tables. The total moves past 113 and the PDF needs an update to match.
