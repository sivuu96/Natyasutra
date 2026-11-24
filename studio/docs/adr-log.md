# Architecture decision records: non-content

Status: **working log.** Records decisions made while reviewing the legacy schema that belong to other domains (revenue, commerce, product, navigation, engagement) or to how legacy tables are routed. Content decisions live in `content-model.md`, section 12.

Format: each record has a status (Accepted, Open), the context, the decision, and the consequences. Numbers are stable. Superseded records stay in the log, marked as superseded.

| ADR | Title | Status | Domain |
|---|---|---|---|
| 001 | Payments stay in revenue; content references projects | Accepted | Revenue |
| 002 | Archive the legacy admin menu; design admin navigation afresh | Accepted | Admin |
| 003 | `tb_product` is the source for `prd_product`; correct PDF section 12.3 | Accepted, one check open | Commerce / product |
| 004 | Public site navigation design | Open | Composer (`cms_`) |
| 005 | Engagement migration: rating codes and activity rows | Partly open | Engagement (`eng_`) |
| 006 | Routing of legacy tables outside the content domain | Accepted | Cross-domain |

---

## ADR-001: Payments stay in revenue; content references projects

**Status:** Accepted. Chosen as option A over the recommended option B.

**Context.** `tb_project` has three rows. "Test Project" is test data. "GG Mohiniyattam" and "Gita Govindam Mohiniyattam" are real productions. `tb_class_music_payment` has eight payments to artists and gurus, from 100 to 25,000. Each payment points at a project. The second production's name matches the "Gita Govinda" collection, so the link to content is real.

**Decision.** A project is a content collection with `kind = project` in `cnt_collection`. Its two real productions migrate. "Test Project" is excluded. Each payment row references the project's `cnt_item` id, and the payment rows stay in the revenue domain (`rev_`).

**Boundary rule.** Content holds a project as a grouping. Money lives in `rev_`. Content may read payment data through the revenue design but never writes it.

**Alternative considered.** A `rev_project` table would keep the project entirely in revenue. The recommendation was that option. It was not chosen, so the boundary rule is the guard.

**Consequences.**
- The revenue design must include the payment table, with a reference to the project's content id.
- Reviews of the content schema must check that no money column has crept in.
- If a project's money needs to be reported by content kind, that report reads through the revenue design.

---

## ADR-002: Archive the legacy admin menu; design admin navigation afresh

**Status:** Accepted.

**Context.** `tb_menu` has 125 rows. All of them describe the old CodeIgniter admin sidebar. Examples are "Dashboard", "Category List/Add", "Guru List/Add", "Free Class" and "Latest updates". The URLs point at old CI routes such as `buyers/summary` and `guru/listview`. None of the rows is a menu for the public site.

**Decision.** Archive `tb_menu` with `tb_admin`, as `cms_archive_*`. Do not migrate its rows. The new admin's navigation is designed afresh.

**Consequences.**
- The old sidebar's order and grouping are not carried over automatically. If they are wanted, they're taken from the archive export by hand.
- The public site's navigation has no legacy source, so it needs its own design. That's ADR-004.

---

## ADR-003: `tb_product` is the source for `prd_product`; correct PDF section 12.3

**Status:** Accepted. One check is still open (see below).

**Context.** The architecture PDF, section 12.3, lists `products` as "orphaned, no relation to `prd_product`", and as dropped. The dump has no table called `products`. It has `tb_product`, with six rows:
- Three live products: "2021 Planner" (`NS01/2021`), "The Circle of Life" (`NS02/2022`) and "Celebrating the Natives of Kerala" (`NS03/2023`). All are active.
- Three test rows: "test", "testing" and "test31", all with status 2.

`tb_product_delivery` links 40 purchases to deliveries, and it references live products. So the products are in use, which doesn't fit "orphaned".

**Decision.** `tb_product` is the source for `prd_product`. The three live products migrate. The three test rows are excluded and listed in the exclusion report. Purchase links keep their product ids.

**Actions.**
- Ask for PDF section 12.3 to be corrected. The description doesn't match the data.
- Open check: confirm that no separate `products` table exists in another database. If one does, it's assessed separately. This check is the only open part of this ADR.

**Consequences.** Commerce keeps its purchase history for the live products. The PDF is wrong until corrected, so anyone reading it alone will be misled.

---

## ADR-004: Public site navigation design

**Status:** Open.

**Context.** The legacy data holds only the admin sidebar (ADR-002). No table describes the public site's navigation: the menus, their order, or which items show for which visitor. The page composer (`cms_`) decides what content appears, but not the navigation around it.

**Questions to answer.**
1. Are menus data (editable by admins) or code (defined in the application)?
2. How are menu items ordered, and can they be scheduled or hidden?
3. Do menu items change with visitor state, such as signed in, or with the learning-state intent from the composer?
4. Does a menu item point at a content item, a collection, a page, or an external URL?

**Dependencies.** The composer's zone and block model (`cms_zone`, `cms_block`), and the visitor context (`ctx_`).

**Consequences until decided.** The public site has no designed navigation model. Nothing is migrated for it, because there's no legacy source.

---

## ADR-005: Engagement migration: rating codes and activity rows

**Status:** Partly open. The routing of activity rows is accepted. The rating codes are open.

**Context.**
- `tb_rating_review` has 169 rows. Its `item_type` values are 1 (161), 5 (4) and NULL (4). The item ids match the video and programme ids, and the code meanings are not confirmed.
- `tb_music_list` has 3,177 rows. 591 have a user, and 2,586 don't. The rows with no user have a session id, a time and an IP address. They look like activity records, not playlist membership.

**Decision.**
- **Activity rows (accepted).** The 2,586 anonymous `tb_music_list` rows go to `eng_events`, with `event_type = legacy_music_list`. The session id and time are kept. The IP address is dropped, in line with the privacy rule in `auth-rbac.md`.
- **Rating codes (open).** Ratings migrate into `eng_rating_review` only after the `item_type` codes are confirmed. Until then, no rating row loads.

**Consequences.**
- `eng_events` must accept legacy event types, and the event type list must say which are legacy.
- `cnt_item_stats` is rebuilt after ratings are loaded, so the rating figures on content can't be migrated before the codes are settled.

---

## ADR-006: Routing of legacy tables outside the content domain

**Status:** Accepted.

**Context.** Several legacy tables were found while reviewing content, but they belong to other domains or are no longer needed. This record says where each one goes, so none is lost between domains.

**Decision.**

| Legacy table | Rows | Goes to | Reason |
|---|---|---|---|
| `tb_common_settings` | 34 | App configuration | Image size and format specs, not content |
| `tb_banner` | 1 | `cms_block` (hero) | Composer |
| `tb_whatsnew_home` | 86 | Retired | Hand-picked homepage list, replaced by composer slots |
| `tb_guru_art_forms` | 39 | `usr` (guru to category link) | Identity and profile |
| `tb_music_artist_category` | 54 | `usr` (artist to category link) | Identity and profile |
| `tb_countries` | 249 | `dim_` reference | Addresses in commerce, profiles in usr |
| `tb_states` | 37 | `dim_` reference | As above |
| `tb_mobile_country_codes` | 246 | `dim_` reference | As above |
| `tb_marital_status` | 5 | `dim_` reference | Profile data |
| `tb_product_delivery` | 40 | `txn_` (commerce) | Purchase to delivery link |
| `tb_class_music_payment` | 8 | `rev_` (revenue) | Payments, see ADR-001 |

**Consequences.** Each receiving domain's design must include the tables routed to it, or the routing becomes a loss. The usr, dim, txn and rev designs are the owners.
