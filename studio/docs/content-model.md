# Content data model

Status: **draft for review.** Covers the content domain: programmes and collections, media, articles, pricing, contributors on content, text sections, categories, tags, attributes, the content dimensions, stats and content history. Target: MySQL 8, InnoDB, utf8mb4. Table prefixes follow the architecture PDF (section 12): `cnt_` for content, `dim_` for reference data, `txn_` for orders, `eng_` for engagement, `log_` for logs, `prd_` for physical product detail, `cms_` for the page composer.

Companion document: `auth-rbac.md` (identity, roles, permissions, visitor tracking).

Items marked **Pending** are not yet decided. The decision log is section 12. Decisions outside the content domain (revenue, commerce, navigation, engagement, legacy routing) are in `adr-log.md`.

---

## 1. Principles

1. **One supertype for everything browsable.** `cnt_item` has one row per public thing: a collection, a media item, an article or a product. The page composer's slots reference content by `cnt_item.id`, so any block can show any kind of item (the content swap test in the PDF depends on this).
2. **Groupings and media are two constructs, not many.** Programmes, albums, playlists and galleries are all groupings, so they share `cnt_collection` with a `kind`. Videos, tracks, photos and documents are all media, so they share `cnt_media` with a `media_type`. Adding a new kind means adding a value, not a table.
3. **Membership is a link, not a column.** A video belongs to a programme through `cnt_membership`. Nothing stores a programme id on the video.
4. **Pricing is separate.** Prices change over time and carry two currencies, so they live in `cnt_price`, not on the item.
5. **Contributors are linked by role.** One table covers gurus, artists and producers on any item, instead of one link table per content type.
6. **Dimensions for managed lists, enums for code-driven values.** A value that admins manage, or that someone might want to rename, is a `dim_` table. A value the code branches on is an enum.
7. **No counters on content.** Views, ratings and purchases come from events and orders. `cnt_item_stats` is a rebuildable read model.
8. **Every row remembers where it came from.** `legacy_table` and `legacy_id` on the main tables let migration be verified row by row.
9. **Deletion is soft.** `deleted_at` is set and rows are never removed. Hard deletes would break the history in section 6.

---

## 2. Tables at a glance

| Table | Group | Purpose | Replaces (legacy) |
|---|---|---|---|
| `cnt_item` | Core | Supertype for every browsable item | Identity and lifecycle columns repeated on `tb_programme`, `tb_video`, `tb_music_album`, `tb_product`, `tb_pages` and others |
| `cnt_collection` | Grouping | Programmes, albums, playlists, galleries, collections | `tb_programme`, `tb_music_album`, `tb_collection`, `tb_pgallery`, `tb_vgallery`, `tb_music_list` (user rows) |
| `cnt_media` | Media | Videos, tracks, photos, documents, audio | `tb_video`, `tb_freevideo`, `tb_music_track`, `tb_picture`, `tb_vgallery_videos`, `tb_product_video`, `tb_product_image`, `tb_category_cover_images` |
| `cnt_article` | Article | Article-specific fields | `tb_latest_updates` |
| `cnt_membership` | Link | Item to collection, with trailer flag and order | `tb_programme_video`, `tb_music_list` (user rows), gallery member links |
| `cnt_item_media` | Link | Item to attached media (images, and audio for videos), by role | Image columns such as `home_page_image`, `share_img`, `banner_img`, `cover_image`, `thumb_image` |
| `cnt_item_contributor` | Link | Item to contributor, by role | `tb_programme_artist`, `tb_music_album_artist`, `tb_music_artist` links |
| `cnt_content_section` | Text | Keyed text sections on an item | `tb_programme_description`, `tb_product_description` |
| `cnt_item_category` | Link | Item to category | `tb_music_album_category`, `tb_latest_updates` category, programme and product category columns |
| `cnt_tag` | Metadata | Tag vocabulary | Comma-separated `tags` columns on `tb_programme` and `tb_video` |
| `cnt_item_tag` | Link | Item to tag | As above |
| `cnt_attribute` | Metadata | Typed key-values on any item | Ad hoc columns such as `is_artform`, `popular_track`, `album_type`, `individual_purchase` |
| `cnt_price` | Pricing | Rupee and dollar prices, access model, validity | `tb_cost_package`, `tb_music_package`, `tb_product_cost`, and the `cost_type` columns |
| `cnt_item_stats` | Read model | Views, clicks, purchases, ratings, rebuilt from events | `rate_1`–`rate_5`, `int_rate_1`–`int_rate_5`, `initial_view_count`, `actual_view_count`, `average_rating` on six tables |
| `log_content_changes` | History | Edit history for content | No equivalent. New |

Count: 14 `cnt_` tables, plus `log_content_changes`. The PDF lists 21 content tables, which is 7 more than this model. The difference comes from the consolidation: the separate music and gallery tables fold into the shared ones.

Dimensions used by content are in section 4. Shared dimensions are in section 4.3.

---

## 3. Tables in detail

### 3.1 `cnt_item`

**Why it exists.** Slots in the page composer need to point at any content. Without a common id, each slot would need a polymorphic pair (type and id) and a foreign-key check in application code. A supertype gives one id space, one slug and one status model for all browsable content.

**What a row is.** One public thing: a programme, an album, a playlist, a gallery, a video, a track, a photo, an article, or a product.

**Columns.**

- `kind`: `collection`, `media`, `article` or `product`. This says which detail table holds the rest of the row. Within collections and media, the finer type is in their own tables.
- `slug`: URL slug, unique within a kind.
- `title`, `short_description`: the card projection that every layout needs.
- `status`: `draft`, `review`, `published` or `archived`. Only `published` rows are visible to the public.
- `visibility`: `public`, `members` (signed in) or `hidden` (direct link only).
- `language_id`: the content's primary language.
- `published_from`, `published_to`: a publish window. Lets content go live and expire without a status change.
- `meta_title`, `meta_description`: search engine fields.
- `legacy_table`, `legacy_id`: migration trace.
- `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`: the audit base.

**Keys.** Unique on `(kind, slug)`. Index on `(status, visibility, published_from)` for the public listing query.

**DDL.**

```sql
CREATE TABLE cnt_item (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  kind              ENUM('collection','media','article','product') NOT NULL,
  slug              VARCHAR(190) NOT NULL,
  title             VARCHAR(255) NOT NULL,
  short_description VARCHAR(500) NULL,
  status            ENUM('draft','review','published','archived') NOT NULL DEFAULT 'draft',
  visibility        ENUM('public','members','hidden') NOT NULL DEFAULT 'public',
  language_id       SMALLINT UNSIGNED NULL,
  published_from    DATETIME NULL,
  published_to      DATETIME NULL,
  meta_title        VARCHAR(255) NULL,
  meta_description  VARCHAR(500) NULL,
  legacy_table      VARCHAR(40) NULL,
  legacy_id         BIGINT UNSIGNED NULL,
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by        BIGINT UNSIGNED NOT NULL,
  updated_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_by        BIGINT UNSIGNED NULL,
  deleted_at        DATETIME NULL,
  UNIQUE KEY uq_item_kind_slug (kind, slug),
  KEY ix_item_status (status, visibility, published_from),
  KEY ix_item_legacy (legacy_table, legacy_id),
  CONSTRAINT fk_item_language FOREIGN KEY (language_id) REFERENCES dim_language(id),
  CONSTRAINT fk_item_created_by FOREIGN KEY (created_by) REFERENCES usr_accounts(id),
  CONSTRAINT fk_item_updated_by FOREIGN KEY (updated_by) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** Every row in `tb_programme`, `tb_video` (free and paid alike; price is separate), `tb_music_track`, `tb_music_album`, `tb_collection`, `tb_pgallery`, `tb_vgallery`, `tb_picture`, `tb_product`, `tb_latest_updates` and `tb_freeclass` gets one row here.

---

### 3.2 `cnt_collection`

**Why it exists.** A programme, an album, a playlist and a gallery share one shape: a named container with members. A single table with a `kind` column means one query path for "list the members of X", one set of membership rules and one place for the hierarchy.

**What a row is.** A grouping. Its members are rows in `cnt_membership`.

**Columns.**

- `item_id`: primary key and foreign key to `cnt_item`. One-to-one with the item.
- `kind`: `programme`, `album`, `playlist`, `gallery`, `collection` or `project`.
  - `programme`: a class or course. Members are videos.
  - `album`: a music album. Members are tracks.
  - `playlist`: a user-curated list of tracks. Members can be any media. Decided (decision 2, option A): kept, with the owner held on `cnt_item.created_by`. Only rows with a known user become playlists. Anonymous rows go to `eng_` (see section 6.2).
  - `gallery`: a photo or video gallery. Members are media.
  - `collection`: a bundle of programmes, used for series and packages. Members are programmes, linked through `cnt_membership`. Decided (decision 3, option A). A programme can belong to more than one collection.
- `parent_id`: optional parent collection. Covers the programme hierarchy in `tb_programme.parent_id`.
- `level_id`: the difficulty level from `dim_level`. Used by programmes; null for the other kinds.
- `starts_at`, `ends_at`: the webinar window for programmes, or the release window for albums. Null otherwise.
- `max_participants`: for webinars. Null otherwise.

**Why the nullable columns are acceptable.** There are four nullable columns, and each applies to one kind. Moving them into attributes would make the most common filters (level, webinar time) slow and awkward. A check constraint in application code enforces which kind may set which column.

**Keys.** Primary key `item_id`. Index on `kind`. Foreign key on `parent_id` to itself.

**DDL.**

```sql
CREATE TABLE cnt_collection (
  item_id          BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  kind             ENUM('programme','album','playlist','gallery','collection','project') NOT NULL,
  parent_id        BIGINT UNSIGNED NULL,
  level_id         SMALLINT UNSIGNED NULL,
  starts_at        DATETIME NULL,
  ends_at          DATETIME NULL,
  max_participants SMALLINT UNSIGNED NULL,
  KEY ix_coll_kind (kind),
  CONSTRAINT fk_coll_item   FOREIGN KEY (item_id)   REFERENCES cnt_item(id),
  CONSTRAINT fk_coll_parent FOREIGN KEY (parent_id) REFERENCES cnt_collection(item_id),
  CONSTRAINT fk_coll_level  FOREIGN KEY (level_id)  REFERENCES dim_level(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

| Legacy | Target `kind` | Notes |
|---|---|---|
| `tb_programme` (184) | `programme` | `parent_id` maps to `parent_id`. `collection_id` maps to a `cnt_membership` row into the collection (73 programmes). The column is then dropped. Programmes with `0` or `NULL` (111) get no membership |
| `tb_music_album` (43) | `album` | `released_on` maps to `starts_at` |
| `tb_collection` (1) | `collection` | Decided (decision 3, option A). "Gita Govinda". Its description fields are empty, so title and status are migrated and the rest are filled in by the content team |
| `tb_pgallery` (13) | `gallery` | Photo galleries |
| `tb_vgallery` (13) | `gallery` | Video galleries. `event_id`, `from_date` and `to_date` become attributes |
| `tb_music_list` (3,177) | `playlist` (591 rows with a known user, grouped by user) and `eng_` activity (2,586 rows with no user) | Decided (decision 2, option A). See section 6.2 and section 12 |

---

### 3.3 `cnt_media`

**Why it exists.** Videos, tracks, photos and documents are all something you open or play, have a file or embed behind them, and carry the same technical facts: a source, a checksum, dimensions or a duration. Keeping one table means one upload pipeline, one deduplication check (by checksum) and one place to fix storage paths. It replaces four overlapping tables, and the synopsis already describes media this way.

**What a row is.** One playable or viewable unit.

**Columns.**

- `item_id`: primary key and foreign key to `cnt_item`.
- `media_type`: `video`, `track`, `photo`, `document` or `audio`. Tells the player and the layout what to render. `audio` is used for the legacy `tb_music` rows, attached to videos. `track` is an album track.
- `source`: `upload`, `youtube`, `vimeo`, `embed` or `external`. Says where the bytes live.
  - Legacy `tb_video` stores embed code for YouTube in `main_video_embed_code`. The embed code becomes a `youtube` source with the video id in `external_ref`.
- `external_ref`: video id, embed code or URL, for non-upload sources.
- `storage_key`: path in object storage, for uploads.
- `mime_type`, `bytes`, `checksum_sha256`: file facts. The checksum lets migration detect duplicate uploads.
- `width`, `height`: for photos and video posters.
- `duration_s`: playing length in seconds. Replaces the free-text `duration` columns.
- `alt_text`: accessibility text for photos and posters.

**Why embed code is not stored as raw HTML.** Legacy `tb_freevideo.video_embed_code` holds full iframe markup with HTML entities. Storing only the video id (`external_ref`) and rendering the iframe in the template is safer and lets the player change without a data migration.

**Keys.** Primary key `item_id`. Index on `media_type`. Index on `checksum_sha256` for deduplication.

**DDL.**

```sql
CREATE TABLE cnt_media (
  item_id         BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  media_type      ENUM('video','track','photo','document','audio') NOT NULL,
  source          ENUM('upload','youtube','vimeo','embed','external') NOT NULL,
  external_ref    VARCHAR(500) NULL,
  storage_key     VARCHAR(500) NULL,
  mime_type       VARCHAR(100) NULL,
  bytes           BIGINT UNSIGNED NULL,
  checksum_sha256 CHAR(64) NULL,
  width           SMALLINT UNSIGNED NULL,
  height          SMALLINT UNSIGNED NULL,
  duration_s      INT UNSIGNED NULL,
  alt_text        VARCHAR(255) NULL,
  KEY ix_media_type (media_type),
  KEY ix_media_checksum (checksum_sha256),
  CONSTRAINT fk_media_item FOREIGN KEY (item_id) REFERENCES cnt_item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

| Legacy | Rows | Target | Notes |
|---|---|---|---|
| `tb_video` | 4,388 | `media_type = video` | `cost_type` moves to `cnt_price`. `track_type_id` maps to `dim_track_type` or an attribute (decision in section 4.1) |
| `tb_freevideo` | 125 | `media_type = video` | `free_class_id` becomes a membership in a programme. Its `video_type = 2` (all rows) is a YouTube source |
| `tb_music_track` | 8,988 | `media_type = track` | `album_id` becomes a membership in an album. `popular_track` becomes an attribute. `trailer` becomes `is_trailer` on membership |
| `tb_picture` | 98 | `media_type = photo` | `image_name` and `large_image` become a file reference. Gallery membership goes to `cnt_membership` |
| `tb_vgallery_videos` | 122 | `media_type = video` | Gallery membership. `v_code` becomes `external_ref` |
| `tb_product_video` | 7 | `media_type = video` | Product media. Linked to the product item through `cnt_item_media` |
| `tb_product_image` | 4 | `media_type = photo` | Linked to the product item |
| `tb_category_cover_images` | 52 | `media_type = photo` | Linked to a category through `cnt_item_media` if categories become items, otherwise kept as a `dim_category` image column |
| `tb_music` | 11,671 | `cnt_media` (`media_type = audio`), attached to the video through `cnt_item_media` (role `audio`) | Decided (option A). Rows point at 62 video ids, all of which match `tb_video`. Audio is included with the video's price. `source` is `upload` where a filename is present, otherwise `external`. Share-service URLs are checked in Phase 4, and dead links go to the exclusion report |

---

### 3.4 `cnt_article`

**Why it exists.** Articles have fields that no other kind uses: a source name and URL for republished news, a display date that differs from the publish window, and a read time. Keeping them in a detail table keeps `cnt_item` clean.

**What a row is.** A written piece: news, a feature, a note from a guru.

**Columns.**

- `item_id`: primary key and foreign key to `cnt_item`.
- `article_type_id`: `dim_article_type`. Replaces the numeric `type_id` in `tb_latest_updates`.
- `source_name`, `source_url`: for pieces republished from elsewhere. Replaces `newspaper` and `website_url`.
- `published_on`: the date shown to readers. Separate from `published_from` on the item, which controls visibility.
- `read_minutes`: estimated reading time.
- `parent_item_id`: optional parent article, for the editorial trees in legacy `tb_pages` (up to four levels). Null for flat articles such as news. Decided (decision 6, option A).

**Body text.** Article body is stored as `cnt_content_section` rows, not on this table. That keeps one way to store long text and lets an article have several sections.

**DDL.**

```sql
CREATE TABLE cnt_article (
  item_id         BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  article_type_id SMALLINT UNSIGNED NULL,
  source_name     VARCHAR(160) NULL,
  source_url      VARCHAR(500) NULL,
  published_on    DATE NULL,
  read_minutes    SMALLINT UNSIGNED NULL,
  parent_item_id  BIGINT UNSIGNED NULL,
  KEY ix_article_parent (parent_item_id),
  CONSTRAINT fk_article_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_article_parent FOREIGN KEY (parent_item_id) REFERENCES cnt_article(item_id),
  CONSTRAINT fk_article_type FOREIGN KEY (article_type_id) REFERENCES dim_article_type(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** `tb_latest_updates` (59 rows). `type_id` maps to `article_type_id` once the values are confirmed. `pgm_type` (values `d` or empty) is **Pending**; it may describe the linked programme type and need not carry over. `programme_id` becomes a membership or a related-item link. `file_upload` and `media_file` become media rows. The guru link becomes `cnt_item_contributor`.

---

### 3.5 `cnt_membership`

**Why it exists.** Programmes contain videos, albums contain tracks, galleries contain photos, and playlists contain anything. These are all the same relationship: an item sits inside a collection in an order, sometimes as the trailer. One link table replaces four.

**What a row is.** One item placed in one collection.

**Columns.**

- `collection_id`: the grouping.
- `item_id`: the member. Can be any `cnt_item`.
- `is_trailer`: marks a preview item of a programme or album. **Pending decision 10.** The legacy data has several flagged items per programme, so the "one trailer" rule is not applied until the meaning is settled.
- `display_order`: position within the collection.

**Why the primary key is `(collection_id, item_id)`.** An item appears in a collection once. If the same video is used twice in one programme, that's a data error, not a design case.

**DDL.**

```sql
CREATE TABLE cnt_membership (
  collection_id BIGINT UNSIGNED NOT NULL,
  item_id       BIGINT UNSIGNED NOT NULL,
  is_trailer    TINYINT(1) NOT NULL DEFAULT 0,
  display_order SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (collection_id, item_id),
  KEY ix_member_item (item_id),
  CONSTRAINT fk_mem_coll FOREIGN KEY (collection_id) REFERENCES cnt_collection(item_id),
  CONSTRAINT fk_mem_item FOREIGN KEY (item_id) REFERENCES cnt_item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

- `tb_programme_video` (4,384 rows): `programme_id` becomes `collection_id`, `video_id` becomes `item_id`, `is_trailor` becomes `is_trailer`, and `display_order` carries over. The legacy table has 2 rows with a `programme_id` that doesn't resolve to `tb_programme`. Those need a decision before loading.
- `tb_music_track` (8,988): `album_id` becomes `collection_id`.
- `tb_vgallery_videos` and `tb_picture`: gallery members.
- `tb_freevideo`: `free_class_id` becomes the programme.

---

### 3.6 `cnt_item_media`

**Why it exists.** Images attach to items in the same way for every kind: a cover, a thumbnail, a share image, a banner, a homepage image. Legacy tables put these as columns (`home_page_image`, `share_img`, `banner_img`, `cover_image`, `thumb_image`, `custom_video_thumb`, `alt_value`) on each content table, each with slightly different names. A role column removes those columns and gives one place for an item's images.

**What a row is.** One media file attached to one item, in one role. The main use is images. It's also how the legacy `tb_music` audio is attached to its video (decision 1: option A).

**Columns.**

- `item_id`, `media_id`: the item and the media file. For images, a `cnt_media` row with `media_type = photo`. For attached audio, a `cnt_media` row with `media_type = audio`.
- `role`: `cover`, `thumbnail`, `share`, `banner`, `home`, `profile` or `audio`. This is an enum because the layouts and the page composer depend on these roles. `audio` is the attached audio for a video item.
- `display_order`: when an item has several images in one role, which one comes first.

**Why the primary key includes `role`.** The same image can be a cover and a share image. The key allows that and stops duplicate rows.

**DDL.**

```sql
CREATE TABLE cnt_item_media (
  item_id       BIGINT UNSIGNED NOT NULL,
  media_id      BIGINT UNSIGNED NOT NULL,
  role          ENUM('cover','thumbnail','share','banner','home','profile','audio') NOT NULL,
  display_order SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (item_id, media_id, role),
  CONSTRAINT fk_im_item  FOREIGN KEY (item_id)  REFERENCES cnt_item(id),
  CONSTRAINT fk_im_media FOREIGN KEY (media_id) REFERENCES cnt_media(item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** Every image column on the content tables. Concretely: `tb_programme` (`home_page_image`, `share_img`, `banner_img`, `cover_image`, `music_section_thumb`), `tb_video` (`custom_video_thumb`, `share_img`), `tb_music_album` (`banner_image`, `share_image`, `cover_image`), `tb_music_artist` (`profile_image`, `share_image`, `thumb_image`), `tb_product` (`cover_image`, `share_img`), `tb_freeclass` (`home_page_image`, `share_img`, `banner_img`, `cover_image`), `tb_collection` and `tb_pages`. The `alt_value` and `alttag` columns move to `cnt_media.alt_text`.

Image files need a copy into object storage and a checksum during migration. Filenames alone are not enough.

---

### 3.7 `cnt_item_contributor`

**Why it exists.** A programme has a primary guru and may have co-teachers. An album has artists and a producer. A track has artists. Legacy keeps these as separate link tables with slightly different columns (`tb_programme_artist`, `tb_music_album_artist`, `tb_music_artist_category`). One table with a role covers all of them, and the contributor record lives in the Gurus group.

**What a row is.** One contributor credited on one item, in one role.

**Columns.**

- `item_id`: the item.
- `contributor_id`: the guru, artist or producer record. Points to the contributor registry in the Gurus group, pending that group's design.
- `role_id`: `dim_contributor_role`. Replaces an enum so admins can add roles without a migration. Values at launch: primary, co-teacher, artist, producer, credit.
- `display_order`: credit order on the page.

**Why contributors on items and not on the contributor.** A guru teaches many programmes and an artist plays many albums, so the relationship is many-to-many. Putting it on the contributor side would hide which items they're credited on.

**DDL.**

```sql
CREATE TABLE cnt_item_contributor (
  item_id        BIGINT UNSIGNED NOT NULL,
  contributor_id BIGINT UNSIGNED NOT NULL,
  role_id        SMALLINT UNSIGNED NOT NULL,
  display_order  SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (item_id, contributor_id, role_id),
  KEY ix_ic_contributor (contributor_id),
  CONSTRAINT fk_ic_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_ic_role FOREIGN KEY (role_id) REFERENCES dim_contributor_role(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

- `tb_programme.guru_id` (the primary guru) becomes one `primary` row per programme. The guru column on `tb_programme` goes away.
- `tb_programme_artist` (3,161 rows): `guru_id` becomes a `co_teacher` row.
- `tb_music_album_artist` (425 rows): each becomes an `artist` row.
- `tb_video.guru_id` becomes a `primary` row on the video.
- `tb_other_artist` (6 rows): artists without a login. Migrated as contributor records in the Gurus group, then linked here.
- `tb_freeclass.guru_text` is free text, not a guru id. It needs matching or manual review. Do not guess.

---

### 3.8 `cnt_content_section`

**Why it exists.** A programme page has several text blocks: what you learn, requirements, what's included, and a longer description. Legacy has these as columns (`what_you_learn`, `requirements`, `course_includes`) and as a separate description table (`tb_programme_description`, which holds extra sections keyed by `item_type`). A section table makes the sections extensible without adding columns.

**What a row is.** One titled block of text on an item.

**Columns.**

- `item_id`: the item.
- `section_type_id`: `dim_section_type`. Values at launch: `what_you_learn`, `requirements`, `includes`, `description`, `extra`.
- `title`: optional heading.
- `body`: the text, as Markdown or sanitised HTML. Decision pending on the format (section 12).
- `display_order`: order within the item.

**Why a unique key on `(item_id, section_type_id, display_order)`.** Prevents two rows with the same position in the same section, which would render unpredictably.

**DDL.**

```sql
CREATE TABLE cnt_content_section (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  item_id         BIGINT UNSIGNED NOT NULL,
  section_type_id SMALLINT UNSIGNED NOT NULL,
  title           VARCHAR(255) NULL,
  body            MEDIUMTEXT NOT NULL,
  display_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  UNIQUE KEY uq_section_position (item_id, section_type_id, display_order),
  CONSTRAINT fk_section_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_section_type FOREIGN KEY (section_type_id) REFERENCES dim_section_type(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

- `tb_programme.what_you_learn`, `requirements`, `course_includes`, `description`, `sub_head_1`, `sub_head_2`, `sub_head`: become sections. The short fields may stay on `cnt_item.short_description` if they're short; decision in section 12.
- `tb_programme_description` (349 rows): `item_type = 1` means programme. Each row becomes an `extra` section on that programme.
- `tb_product_description` (3 rows): sections on products.
- `tb_video.includes`, `what_you_learn`, `requirements`, `description`: sections on videos.
- `tb_latest_updates.description`: the article body.

---

### 3.9 `cnt_item_category`

**Why it exists.** Items belong to categories: dance forms, music genres, product types. Legacy has three category tables and a category id column on each content table. One link table with `dim_category` (which has a `domain` column) gives one query path. An item can have several categories, and one is marked primary for URLs and breadcrumbs.

**What a row is.** One category assigned to one item.

**Columns.**

- `item_id`, `category_id`: the link.
- `is_primary`: exactly one row per item should be primary. Enforced in application code.

**DDL.**

```sql
CREATE TABLE cnt_item_category (
  item_id     BIGINT UNSIGNED NOT NULL,
  category_id SMALLINT UNSIGNED NOT NULL,
  is_primary  TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (item_id, category_id),
  KEY ix_ic_category (category_id),
  CONSTRAINT fk_icat_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_icat_category FOREIGN KEY (category_id) REFERENCES dim_category(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** `tb_programme.category_id` and `topic_related_category_id` (the second one becomes a non-primary link). `tb_video.category_id`. `tb_music_album_category` (783 rows). `tb_product.category_id`. `tb_freeclass.category_id` and `category_text`. `tb_latest_updates` category links, where they exist. Category ids map to `dim_category` after its load.

---

### 3.10 `cnt_tag` and `cnt_item_tag`

**Why they exist.** `tb_programme.tags` and `tb_video.tags` are free text, comma-separated. That can't be searched, counted or filtered reliably, and the same tag appears in different spellings. A tag vocabulary with a link table fixes that. The composer's eligibility filters also need tags to be queryable.

**`cnt_tag` columns.** `id`, `slug` (unique, lowercased), `label`.

**`cnt_item_tag` columns.** `item_id`, `tag_id`. Primary key on both.

**DDL.**

```sql
CREATE TABLE cnt_tag (
  id    INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug  VARCHAR(80) NOT NULL,
  label VARCHAR(120) NOT NULL,
  UNIQUE KEY uq_tag_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE cnt_item_tag (
  item_id BIGINT UNSIGNED NOT NULL,
  tag_id  INT UNSIGNED NOT NULL,
  PRIMARY KEY (item_id, tag_id),
  KEY ix_it_tag (tag_id),
  CONSTRAINT fk_it_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_it_tag  FOREIGN KEY (tag_id)  REFERENCES cnt_tag(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Migration.** Split each `tags` value on commas, trim, lowercase, create tags as needed, and link. The `meta_keywords` columns are a separate question: search engines have ignored them for years. **Pending:** keep them as text on `cnt_item`, or drop them.

---

### 3.11 `cnt_attribute`

**Why it exists.** Some facts are real but apply to only some items, and there are many of them: whether a programme is an art form, whether a track is popular, the album type, whether an album is sold individually, the gallery event. Adding a column for each would widen every content table. Typed key-values hold these without schema change. The key must be known, which is what `dim_attribute_key` is for.

**Why typed columns and not a single text value.** A text-only key-value table makes numeric filters (price, duration, year) slow and wrong. Typed columns (string, number, boolean, date) keep filters indexable.

**What a row is.** One fact about one item, for one key.

**Columns.**

- `item_id`: the item.
- `attr_key_id`: `dim_attribute_key`. Only registered keys are allowed, and the key's `value_type` says which value column is used.
- `value_str`, `value_num`, `value_bool`, `value_date`: one is set, depending on the key's type.

**Multi-valued keys.** A key can appear more than once on an item. Each value is a separate row.

**Keys.** Index on `(attr_key_id, value_str)` and `(attr_key_id, value_num)` for filters. Index on `(item_id, attr_key_id)` for reads.

**DDL.**

```sql
CREATE TABLE cnt_attribute (
  id           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  item_id      BIGINT UNSIGNED NOT NULL,
  attr_key_id  SMALLINT UNSIGNED NOT NULL,
  value_str    VARCHAR(255) NULL,
  value_num    DECIMAL(12,2) NULL,
  value_bool   TINYINT(1) NULL,
  value_date   DATE NULL,
  KEY ix_attr_str (attr_key_id, value_str),
  KEY ix_attr_num (attr_key_id, value_num),
  KEY ix_attr_item (item_id, attr_key_id),
  CONSTRAINT fk_attr_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_attr_key  FOREIGN KEY (attr_key_id) REFERENCES dim_attribute_key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

- `tb_programme.is_artform` (`y`/`n`): key `is_art_form`, boolean.
- `tb_music_track.popular_track`: key `popular_track`, number. Values are spread widely (0, 1, 2, 5, 7 and several in the hundreds or thousands), so the meaning needs confirming before a key is registered. It may be a rank or a play count.
- `tb_music_album.album_type` (`f`/`p`): key `album_type`, string.
- `tb_music_album.individual_purchase`, `subscription`: booleans.
- `tb_vgallery.event_id` (number), `from_date` and `to_date` (dates).
- `tb_video.track_type_id`: see section 4.1.
- `tb_video.accessibility_type`: string.

---

### 3.12 `cnt_price`

**Why it exists.** Prices change, carry two currencies, and differ by access model. Legacy keeps prices in separate cost tables (`tb_cost_package`, `tb_music_package`, `tb_product_cost`) with three currencies and different validity columns, and `cost_type` sits on each content table with different codes. One table gives one way to answer "what does this cost, and from when".

**What a row is.** One price for one item, valid for one window. Price history comes from keeping old rows, not from editing them. A new price is a new row with a later `valid_from`, and the old row gets `is_active = 0`. Orders snapshot the price they used, so history stays right.

**Columns.**

- `item_id`: the item being sold. Any `cnt_item` can be priced, including products.
- `access_model`: `free`, `purchase` (one-time) or `subscription`. Replaces `cost_type`. `free` rows have a zero price, so the model is always explicit.
- `price_inr`, `price_usd`: rupees and dollars on the row, as the brief requires.
- `price_eur`: kept but unused. Decided (decision 8, option B). No legacy row sets a euro value (0 of 364), so the column is empty at launch. It's there so euro can be added without a schema change. The rule is that the column is never set by the application until euro is a supported currency.
- `validity_value`, `validity_unit`: how long the access lasts. For example 12 months, or lifetime. Replaces `valid_days` and `valid_type`.
- `renew_before_days`: when renewal reminders start. Carries over from `renew_before`.
- `valid_from`, `valid_to`: the window in which this price applies.
- `is_active`: whether this is the current price row. Used for quick lookups.
- `created_at`, `created_by`: who set the price and when.

**Why both currencies on one row.** A price in rupees and dollars is one decision, and they should change together. Separate rows per currency would let them drift.

**DDL.**

```sql
CREATE TABLE cnt_price (
  id                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  item_id           BIGINT UNSIGNED NOT NULL,
  access_model      ENUM('free','purchase','subscription') NOT NULL,
  price_inr         DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  price_usd         DECIMAL(10,2) NULL,
  price_eur         DECIMAL(10,2) NULL,          -- unused at launch; see decision 8
  validity_value    SMALLINT UNSIGNED NULL,
  validity_unit     ENUM('days','months','years','lifetime') NULL,
  renew_before_days SMALLINT UNSIGNED NULL,
  valid_from        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  valid_to          DATETIME NULL,
  is_active         TINYINT(1) NOT NULL DEFAULT 1,
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_by        BIGINT UNSIGNED NOT NULL,
  KEY ix_price_item (item_id, is_active, valid_from),
  CONSTRAINT fk_price_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_price_created_by FOREIGN KEY (created_by) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.**

| Legacy | Rows | Target | Notes |
|---|---|---|---|
| `tb_cost_package` | 364 | `cnt_price` | `item_type = 1` is video, verified: all 173 distinct item ids match `tb_video`. Prices (INR and USD) migrate for all rows. The `r` (189) and `f` (175) codes are **held**: the validity and renewal interpretation waits for confirmation. See decision 9 |
| `tb_music_package` | 33 | `cnt_price` | `type = 'i'` (individual) on all rows. `duration_type` maps to `validity_unit` |
| `tb_product_cost` | 4 | `cnt_price` | Product prices |
| `tb_programme.cost_type` | 184 | `cnt_price.access_model` | `1` → `free` (3 rows), `2` → `purchase` (169 rows). `0` → **held** (12 rows) |
| `tb_video.cost_type` | 4,388 | `cnt_price.access_model` | `1` → `free` (469), `2` → `purchase` (3,919) |
| `tb_music.cost_type` | 11,671 | Audio inherits the video's price, so no separate `cnt_price` rows | `2` (11,655) → mapped, but only matters if audio is sold separately. `3` (5) and `0` (11) are **held** |

Decided (decision 9, option B). Codes with a clear meaning are mapped: `1` is free and `2` is purchase, for each table. Rows with an unclear code are held in a list and loaded after the business owners confirm the meaning. The held rows are:
- `tb_programme` `cost_type` `0`: 12 rows.
- `tb_music` `cost_type` `0` and `3`: 16 rows.
- `tb_cost_package` `cost_type` `r` and `f`: the validity and renewal fields only. The price amounts are not held (see decision 9).

Prices for the paid rows need a rupee and dollar value. Where a dollar value is missing, the migration report lists the row and the item, and does not invent a figure.

---

### 3.13 `cnt_item_stats`

**Why it exists.** Ratings, view counts and purchase counts are on six legacy tables as stored columns, and they go stale or disagree with each other. Rating columns (`rate_1` to `rate_5`, `int_rate_1` to `int_rate_5`) exist on `tb_programme`, `tb_video`, `tb_freeclass`, `tb_collection`, `tb_music_album` and `tb_product`. The authoritative data is in `eng_rating_review` and in `eng_events`. This table caches the numbers for display and is rebuilt from source.

**What a row is.** The current summary for one item. One row per item, updated by a job.

**Columns.**

- `item_id`: primary key.
- `views_total`, `views_30d`, `clicks_30d`, `purchases_30d`: counts over all time and over the last 30 days.
- `ratings_count`, `avg_rating`: from `eng_rating_review`.
- `refreshed_at`: when the job last ran. Lets the UI show freshness.

**Why not compute on read.** The composer reads many items per page. Counting events at render time would be slow. The read model is refreshed on a schedule, and the composer reads one row.

**DDL.**

```sql
CREATE TABLE cnt_item_stats (
  item_id        BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  views_total    INT UNSIGNED NOT NULL DEFAULT 0,
  views_30d      INT UNSIGNED NOT NULL DEFAULT 0,
  clicks_30d     INT UNSIGNED NOT NULL DEFAULT 0,
  purchases_30d  INT UNSIGNED NOT NULL DEFAULT 0,
  ratings_count  INT UNSIGNED NOT NULL DEFAULT 0,
  avg_rating     DECIMAL(3,2) NULL,
  refreshed_at   DATETIME NOT NULL,
  CONSTRAINT fk_stats_item FOREIGN KEY (item_id) REFERENCES cnt_item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** The counter and rating columns are not migrated. They're rebuilt from events and ratings after those are loaded. The legacy values are kept on a one-time snapshot table for comparison during migration, then dropped.

---

### 3.14 `log_content_changes`

**Why it exists.** Legacy has no record of who changed a programme, what they changed, or what it said before. The `deleted_*` and `last_updated_*` columns record only the last change. Content history is needed for editorial accountability, for undoing mistakes, and for explaining why a page changed.

**What a row is.** One change to one item: who, when, what action, and the values before and after.

**Columns.**

- `item_id`: the item changed.
- `actor_account_id`: who made the change. Points at `usr_accounts`.
- `action`: `create`, `update`, `publish`, `unpublish`, `archive`, `delete` or `restore`.
- `changed_fields`: list of field names changed, for quick filtering.
- `before_json`, `after_json`: the relevant values, as JSON. Stores only changed fields in `update`.
- `created_at`: millisecond precision, so rapid edits order correctly.

**Why JSON for before and after.** The content tables have many columns, and a history table per content table would multiply the schema. JSON keeps one history table for all kinds. The cost is that querying inside JSON is slower, which is acceptable for an audit trail.

**Why the same shape as `log_admin_actions`.** The auth design already uses this shape for admin actions. Using one pattern means one audit viewer.

**DDL.**

```sql
CREATE TABLE log_content_changes (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  item_id          BIGINT UNSIGNED NOT NULL,
  actor_account_id BIGINT UNSIGNED NOT NULL,
  action           ENUM('create','update','publish','unpublish','archive','delete','restore') NOT NULL,
  changed_fields   JSON NULL,
  before_json      JSON NULL,
  after_json       JSON NULL,
  created_at       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  KEY ix_ccl_item (item_id, created_at),
  KEY ix_ccl_actor (actor_account_id, created_at),
  CONSTRAINT fk_ccl_item FOREIGN KEY (item_id) REFERENCES cnt_item(id),
  CONSTRAINT fk_ccl_actor FOREIGN KEY (actor_account_id) REFERENCES usr_accounts(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Map from legacy.** None. This is new. Migration starts the history at go-live. Earlier changes are not reconstructed from the `last_updated_*` columns, because those columns don't hold the before values.

---

## 4. Dimensions

Dimensions are reference tables that admins manage. Each follows the same shape, shown here once and then not repeated for each table.

```sql
-- Template. Each dim table adds its own specific columns.
CREATE TABLE dim_example (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  label        VARCHAR(120) NOT NULL,
  description  VARCHAR(500) NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_example_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`code` is the stable identifier the code uses. `label` is what people see and can change. Keeping them apart means a label can be fixed without breaking code.

Deactivate rather than delete. `is_active = 0` hides a value from new choices but keeps it valid on old rows.

### 4.1 Content-owned dimensions

**`dim_category`** (PDF). Dance forms, music genres and product categories in one table. Adds `domain` (`dance`, `music` or `product`) and `parent_id` for hierarchy.

```sql
CREATE TABLE dim_category (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  domain       ENUM('dance','music','product') NOT NULL,
  parent_id    SMALLINT UNSIGNED NULL,
  label        VARCHAR(120) NOT NULL,
  description  VARCHAR(500) NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_category_code (code),
  CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES dim_category(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Why one table: the PDF already decided this, and it replaces three legacy hierarchies (`tb_category` 20 rows, `tb_music_category` 17, `tb_product_category` 2). Legacy `tb_category` also carries `mudra_image` and `mudra_text`, which are content and move to `cnt_item_media` and `cnt_content_section` for the category page, if categories become browsable items. Decision in section 12.

**`dim_level`** (proposed; the PDF says "levels" are in the reference domain without naming the table). Beginner, intermediate and so on, with `parent_id` for sub-levels.

```sql
CREATE TABLE dim_level (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  parent_id    SMALLINT UNSIGNED NULL,
  label        VARCHAR(120) NOT NULL,
  description  VARCHAR(500) NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_level_code (code),
  CONSTRAINT fk_level_parent FOREIGN KEY (parent_id) REFERENCES dim_level(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Why a table and not an enum: the values are admin-managed and `tb_level` already has 11 rows, with `tb_level_sub` (4 rows) as sub-levels. The legacy `course_prefix` column is a URL or code concern and is kept as an attribute if needed. `dp_level_name` on `tb_programme` and `tb_video` is a denormalised copy of the level name and is dropped.

**`dim_language`** (proposed; the PDF names languages in the reference domain). Used by `cnt_item.language_id`.

```sql
CREATE TABLE dim_language (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(10) NOT NULL,              -- BCP 47, for example 'en', 'ml', 'hi'
  label        VARCHAR(120) NOT NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_language_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Why BCP 47 codes: they're the standard for language tags, and they're what browsers and search engines expect. Legacy `tb_language` (12 rows) has only a name and status, so codes are assigned during migration. Current `tb_programme.language_id` values map to these rows. Free-text language fields in `tb_video` and `tb_freeclass` are not used by this table and are migrated only where they match a known language.

**`dim_track_type`** (proposed). Video track types from `tb_video_track_type` (4 rows).

```sql
CREATE TABLE dim_track_type (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  label        VARCHAR(120) NOT NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_track_type_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Decision pending.** `tb_video.track_type_id` is NULL on 3,775 of 4,388 videos, and `tb_cost_package.video_track_type_id` also references it. If the table is only four values, a `cnt_attribute` key (`track_type`, string) may be simpler. If it's used in pricing (through `cnt_price`), keep the table.

**`dim_article_type`** (proposed). News and other article kinds, from the values of `tb_latest_updates.type_id` (1 and 2 in the dump). The meaning of those values has to be confirmed before the table can be seeded.

```sql
CREATE TABLE dim_article_type (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  label        VARCHAR(120) NOT NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  legacy_table VARCHAR(40) NULL,
  legacy_id    INT UNSIGNED NULL,
  UNIQUE KEY uq_article_type_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**`dim_contributor_role`** (decided: a table, so new roles can be added without a migration). Primary, co-teacher, artist, producer, credit.

```sql
CREATE TABLE dim_contributor_role (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  label        VARCHAR(120) NOT NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_contributor_role_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Why a table here and an enum for `cnt_media.media_type`: roles on a credit list are the kind of thing an editor wants to add ("assistant teacher", "translator") without a deployment. Media types are used by the player and the layouts, so they stay code-driven.

**`dim_attribute_key`** (proposed). The registry of allowed `cnt_attribute` keys. Each key has a name, a value type and a description.

```sql
CREATE TABLE dim_attribute_key (
  id            SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code          VARCHAR(60) NOT NULL,
  value_type    ENUM('string','number','boolean','date') NOT NULL,
  is_filterable TINYINT(1) NOT NULL DEFAULT 0,
  description   VARCHAR(500) NULL,
  is_active     TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_attr_key_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Why a table and not only code: the composer's eligibility filters and the admin screens need to list valid keys, and `value_type` must be checked when a value is written. `is_filterable` controls which keys the composer may use in selection rules.

**`dim_section_type`** (proposed). `what_you_learn`, `requirements`, `includes`, `description`, `extra`.

```sql
CREATE TABLE dim_section_type (
  id           SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  code         VARCHAR(60) NOT NULL,
  label        VARCHAR(120) NOT NULL,
  sort_order   SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  is_active    TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_section_type_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 4.2 Enums kept in code

These are not tables, because the code branches on them and they don't change with content:

| Enum | Values | Where |
|---|---|---|
| `cnt_item.kind` | collection, media, article, product | `cnt_item` |
| `cnt_collection.kind` | programme, album, playlist, gallery, collection, project | `cnt_collection` |
| `cnt_media.source` | upload, youtube, vimeo, embed, external | `cnt_media` |
| `cnt_item_media.role` | cover, thumbnail, share, banner, home, profile, audio | `cnt_item_media` |
| `cnt_media.media_type` | video, track, photo, document, audio | `cnt_media` |
| `cnt_price.access_model` | free, purchase, subscription | `cnt_price` |
| `cnt_price.validity_unit` | days, months, years, lifetime | `cnt_price` |
| `cnt_item.status` | draft, review, published, archived | `cnt_item` |
| `cnt_item.visibility` | public, members, hidden | `cnt_item` |

Adding a value to one of these is a code change and a migration, which is intended. These values change the rules of the system, so they should not be editable by admins.

### 4.3 Shared dimensions

These are owned by other domains but content depends on them:

- **`dim_learning_state`** (PDF). The learner's state, such as beginner or intermediate. Content uses it as an eligibility filter for the composer, through `cnt_attribute` with a `learning_state` key, or as a link table if that proves simpler. The usr group owns the table.
- **`dim_language`** (section 4.1). Owned by content for now, used by usr.

### 4.4 Dimensions in the reference domain that aren't content

Listed so the full extent is visible. They're designed in other groups:

- `dim_countries` (legacy `tb_countries`, 249 rows), `dim_states` (`tb_states`, 37), and the mobile codes (`tb_mobile_country_codes`, 246). Used by addresses in commerce and profiles in usr.
- `dim_marital_status` (`tb_marital_status`, 5). Used by profiles.
- `dim_experience`, `dim_journey_step`, `dim_conversion_trigger`, `dim_intent_dimension` and `dim_referral_source` (PDF). Used by visitor context and the composer.

---

## 5. History

Content history has three layers, each answering a different question.

| Question | Source | Table |
|---|---|---|
| Who viewed or clicked, when, and from which block? | Events | `eng_events` (defined in `auth-rbac.md`) |
| Who bought, when, at what price? | Orders | `txn_order_item`, which references `cnt_item.id` and the `cnt_price` row used |
| Who changed this item, what did it say before? | Edits | `log_content_changes` |
| What are the totals right now? | Read model | `cnt_item_stats` |

**Events.** `eng_events` already has `subject_type` and `subject_id`. For content, `subject_type = 'cnt_item'`. Add two nullable columns, `placement_block_id` and `placement_slot_id`, so that a click can be traced to the composer block and slot that produced it. That answers "which placement drove this purchase", which the composer needs to learn from.

**Purchases.** They come from orders, not events, because an order is the record of money. `txn_order_item` stores the `cnt_price` row that applied, so an old price is still known after the price changes.

**Edits.** `log_content_changes` records each change with before and after values. Publication changes (`publish`, `unpublish`, `archive`) are logged as their own actions, so the public status history can be read directly.

**Stats.** `cnt_item_stats` is recalculated from events and ratings. It's not the source of truth. If the numbers look wrong, rebuild the table from source.

---

## 6. Mapping: legacy to target

The full list. Counts are from the dump. Rows marked **Pending** are covered in section 12.

### 6.1 Dance programmes and videos

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_programme` | 184 | `cnt_item` (kind collection) + `cnt_collection` (kind programme) | Migrate. Split the 71 columns across the target tables; drop rating columns and the `dp_level_name` copy |
| `tb_programme_description` | 349 | `cnt_content_section` (type `extra`) | Migrate |
| `tb_programme_artist` | 3,161 | `cnt_item_contributor` (role `co_teacher`) | Migrate |
| `tb_programme_video` | 4,384 | `cnt_membership` | Migrate. Resolve 2 orphan `programme_id` values first |
| `tb_video` | 4,388 | `cnt_item` (kind media) + `cnt_media` (type video) | Migrate. `cost_type` goes to `cnt_price`. Drop rating and view counters |
| `tb_freevideo` | 125 | `cnt_item` + `cnt_media` (type video) + `cnt_membership` into the free programme | Migrate. All rows are YouTube embeds |
| `tb_freeclass` | 23 | `cnt_item` (kind collection) + `cnt_collection` (kind programme, free) | Migrate after removing test rows. `guru_text` and `category_text` need matching, not copying |
| `tb_collection` | 1 | `cnt_item` (kind collection) + `cnt_collection` (kind collection) | Decided (decision 3, option A). The 73 programme links come from `tb_programme.collection_id` through `cnt_membership` |
| `tb_level` | 11 | `dim_level` | Migrate |
| `tb_level_sub` | 4 | `dim_level` with `parent_id` | Migrate |
| `tb_category` | 20 | `dim_category` (domain dance) | Migrate. Image columns decision in section 12 |
| `tb_category_cover_images` | 52 | `cnt_item_media` if categories are items, else category image column | Migrate. **Pending** the category decision |
| `tb_language` | 12 | `dim_language` | Migrate. Assign codes |
| `tb_video_track_type` | 4 | `dim_track_type` or attribute | **Pending** |
| `tb_guru_art_forms` | 39 | `usr` group (guru to category link) | Not content. Covered in the usr design |

### 6.2 Music

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_music_album` | 43 | `cnt_item` (kind collection) + `cnt_collection` (kind album) | Migrate |
| `tb_music_track` | 8,988 | `cnt_item` (kind media) + `cnt_media` (type track) + `cnt_membership` into the album | Migrate. Verify the album link: about 200 tracks per album is unusual |
| `tb_music_album_artist` | 425 | `cnt_item_contributor` (role `artist`) | Migrate |
| `tb_music_album_category` | 783 | `cnt_item_category` | Migrate. Ratio is high; verify |
| `tb_music_artist` | 24 | `usr` group (contributor records) | Migrate the contributor part. Images go to `cnt_item_media` |
| `tb_music_artist_category` | 54 | `usr` group (artist to category) | Not content. Covered in the usr design |
| `tb_music_category` | 17 | `dim_category` (domain music) | Migrate |
| `tb_music_package` | 33 | `cnt_price` | Migrate |
| `tb_music_list`, rows with a `user_id` | 591 (47 users) | `cnt_item` (kind collection) + `cnt_collection` (kind playlist), one playlist per user; `cnt_membership` for each track | Decided (decision 2, option A). `created_by` = the user. Member order = legacy `id` order. Track ids are checked against `tb_music_track` in the Phase 5 exit check |
| `tb_music_list`, rows with no `user_id` | 2,586 | `eng_events` (activity) | Decided. No owner, so they can't be a playlist. Keep for analysis, not for display. Recorded as `event_type = legacy_music_list` with `session_id` and `added_on`. IP is dropped, per the privacy rule in `auth-rbac.md` |
| `tb_music_playlist_master` | 0 | Not migrated | Empty. The legacy master table has no rows, so no playlist records exist there |
| `tb_music` | 11,671 | `cnt_media` (audio) + `cnt_item_media` (role `audio`) | Decided (option A). Dead-link check in Phase 4. See section 12, decision 1 |
| `tb_other_artist` | 6 | `usr` group (contributor records) | Migrate |

### 6.3 Products

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_product` | 6 | `cnt_item` (kind product) + `prd_product` | Decided (decision 7, option A). Migrate the three live products ("2021 Planner", "The Circle of Life", "Celebrating the Natives of Kerala"). Drop the three test rows, listed in the exclusion report. Purchase links in `tb_product_delivery` (40 rows) keep their product ids |
| `tb_product_category` | 2 | `dim_category` (domain product) | Migrate |
| `tb_product_cost` | 4 | `cnt_price` | Migrate |
| `tb_product_description` | 3 | `cnt_content_section` | Migrate |
| `tb_product_image` | 4 | `cnt_media` (photo) + `cnt_item_media` | Migrate |
| `tb_product_video` | 7 | `cnt_media` (video) + `cnt_item_media` | Migrate |
| `tb_product_delivery` | 40 | `txn_` (commerce) | Not content |

### 6.4 Galleries

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_pgallery` | 13 | `cnt_item` (kind collection) + `cnt_collection` (kind gallery) | Migrate |
| `tb_picture` | 98 | `cnt_item` (kind media) + `cnt_media` (type photo) + `cnt_membership` | Migrate |
| `tb_vgallery` | 13 | `cnt_item` + `cnt_collection` (kind gallery). `event_id`, `from_date`, `to_date` become attributes | Migrate |
| `tb_vgallery_videos` | 122 | `cnt_item` + `cnt_media` (type video) + `cnt_membership` | Migrate |

### 6.5 Articles and news

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_latest_updates` | 59 | `cnt_item` (kind article) + `cnt_article` + `cnt_content_section` | Migrate. `type_id` mapping **Pending**. `pgm_type` **Pending** |
| `tb_pages` | 37 | `cnt_item` (kind article) + `cnt_article` (with `parent_item_id`) + `cnt_content_section` + `cnt_membership` | Decided (decision 6, option A). See section 6.7 |
| `tb_whatsnew_home` | 86 | Retired | Hand-picked homepage list. Replaced by composer slots. Export for reference, then drop |

### 6.6 Pricing

| Legacy table | Rows | Target | Action |
|---|---|---|---|
| `tb_cost_package` | 364 | `cnt_price` | Migrate rupees and dollars for all rows. Euro is unused (0 rows set it). The `r` and `f` codes are held for the validity and renewal fields only (decision 9) |
| `tb_music_package` | 33 | `cnt_price` | Migrate |
| `tb_product_cost` | 4 | `cnt_price` | Migrate |

### 6.7 Content-related, not in this model

| Legacy table | Rows | Where it goes | Note |
|---|---|---|---|
| `tb_banner` | 1 | `cms_block` (hero) | Composer |
| `tb_pages` | 37 | `cnt_item` (kind article) + `cnt_article` (with `parent_item_id`) + `cnt_content_section` + `cnt_membership` into the Gita Govinda collection (36 rows) | Decided (decision 6, option A). Row 37 ("Women in Ramayana") has no collection and is migrated as a flat article. `youtube_link` becomes a media row. `file_name` becomes `slug` |
| `tb_menu` | 125 | Archived with the old CI admin panel (`cms_archive_*`), not migrated | Decided in ADR-002. All rows are the old admin sidebar. Public site navigation is open in ADR-004 |
| `tb_common_settings` | 34 | App configuration | Image size and format specs. Not content (ADR-006) |
| `tb_faq` | 0 | Drop unless planned | Empty |
| `tb_editor_images` | 0 | Replaced by `cnt_media` | Empty |
| `tb_rating_review` | 169 | `eng_rating_review` | Engagement, not content. Item type codes pending (ADR-005) |
| `tb_project` | 3 | `cnt_item` (kind collection) + `cnt_collection` (kind project) | Decided (decision 4, option A). "Test Project" is excluded as test data. Two real productions remain: "GG Mohiniyattam" and "Gita Govindam Mohiniyattam" |
| `tb_class_music_payment` | 8 | Payment rows stay in the revenue domain (`rev_`). Each row references the project's `cnt_item` id | Decided in ADR-001. Content never writes payment data |

### 6.8 Columns dropped everywhere

- Rating and counter columns: `rate_1`–`rate_5`, `int_rate_1`–`int_rate_5`, `average_rating`, `initial_view_count`, `actual_view_count`. Rebuilt in `cnt_item_stats`.
- Denormalised names: `dp_level_name`, `guru_text`, `category_text` (after matching), `newspaper` (moved to `source_name`).
- Free-text duplicates of relations: `tags` (moved to `cnt_tag`).
- Repeated audit columns: `added_on`, `added_by`, `added_ip`, `last_updated_*`, `deleted_*`. Replaced by the standard audit base on `cnt_item`, and by `log_content_changes`. IP columns are dropped, in line with the privacy rule in `auth-rbac.md`.
- Typo and spelling variants: `trailor_video_embed_code`, `int_rat_1`, `seperate_page`, `dimention_in`, `webinar_dispaly_upto`. Their meaning is carried over under the correct names.

---

## 7. Migration plan

The plan runs in phases. Each phase has an exit check, and a phase does not start until the previous one passes.

**Phase 0. Decide the open items (section 12).** Nothing loads until the pending items are resolved or explicitly deferred with a default. This is the longest phase in practice, because several items need the business owners.

**Phase 1. Build the target schema.** Create every `cnt_`, `dim_` and `log_` table from this document. Create the dimension tables with seed codes but no data.

**Phase 2. Load the dimensions.** Migrate `tb_language`, `tb_level`, `tb_level_sub`, `tb_category`, `tb_music_category`, `tb_product_category`, `tb_video_track_type`. Assign codes and record `legacy_table` and `legacy_id` on each.
*Exit check:* row count in each dim matches the legacy count, and every legacy id maps to exactly one code.

**Phase 3. Load collections.** `tb_programme`, `tb_freeclass` (after test rows are removed), `tb_music_album`, `tb_pgallery`, `tb_vgallery`, and `tb_collection` if confirmed. Create one `cnt_item` row per legacy row, then the detail row.
*Exit check:* counts match the legacy table minus the excluded rows, which are listed in a written exclusion report.

**Phase 4. Load media.** `tb_video`, `tb_freevideo`, `tb_music_track`, `tb_picture`, `tb_vgallery_videos`, `tb_product_video`, `tb_product_image`. Copy image and file assets into object storage. Compute checksums. Deduplicate by checksum and record the mapping.
*Exit check:* every media row has a `storage_key` or an `external_ref`, and no `cnt_media` row points at a missing file.

**Phase 5. Load links.** `cnt_membership` from `tb_programme_video`, `tb_music_track`, and gallery members. Then `cnt_item_contributor`, `cnt_item_category`, `cnt_item_media`.
*Exit check:* no orphan links. The 2 orphan `programme_id` values in `tb_programme_video` are resolved or reported.

**Phase 6. Load text and tags.** `cnt_content_section` from the description and long-text columns. `cnt_tag` and `cnt_item_tag` from the `tags` columns.
*Exit check:* spot-check 20 programmes against the legacy pages, field by field.

**Phase 7. Load prices.** `cnt_price` from `tb_cost_package`, `tb_music_package` and `tb_product_cost`, and from the `cost_type` columns. Clear codes load now. Held rows (decision 9) load in a second pass once confirmed. Rows with no dollar value are listed in the report.
*Exit check:* every paid item has a current price row (`is_active = 1`). Every free item has a `free` row.

**Phase 8. Load articles and attributes.** `cnt_article` from `tb_latest_updates`. `cnt_attribute` for the keys in section 3.11.
*Exit check:* attribute values are valid for their key's type. No value fails the type check.

**Phase 9. Build the read model.** Load the legacy counters into a snapshot table for comparison. Populate `cnt_item_stats` from events and ratings, once those are migrated under the auth and engagement work.

**Phase 10. Verify and cut over.** Run the reconciliation report: row counts by table, orphan counts, and a sample of 20 items per kind checked against the live site.
*Exit check:* sign-off from the owner of each content kind.

**Phase 11. Retire legacy.** Move the legacy content tables to `cms_archive_*` or the retained-historical list in the PDF (section 12.3). Keep them readable for at least one release. Drop only after the archive has been checked.

### 7.1 Reconciliation targets

These are the counts the migration must reproduce, from the dump:

| Legacy | Expected target count | Notes |
|---|---|---|
| `tb_programme` | 184 `cnt_collection` (programme) | |
| `tb_freeclass` | 23 minus test rows | Count of test rows to be confirmed in the exclusion report |
| `tb_video` | 4,388 `cnt_media` (video) | |
| `tb_freevideo` | 125 `cnt_media` (video) | |
| `tb_music` | 11,671 `cnt_media` (audio), before dead-link check | Count may fall after the dead-link check. Removed rows go in the exclusion report |
| `tb_music_list` (user rows) | 591 `cnt_membership` across 47 playlists | Rows with a user only |
| `tb_music_list` (anonymous rows) | 2,586 `eng_events` | No owner, so activity only |
| `tb_programme.collection_id` (non-zero) | 73 `cnt_membership` rows into the Gita Govinda collection | Programmes with `0` or `NULL` get no membership |
| `tb_project` | 2 `cnt_collection` (kind project) | "Test Project" excluded and listed in the exclusion report |
| `tb_pages` | 37 `cnt_article` | 36 in the Gita Govinda collection through `cnt_membership`. Parent links are checked against the tree |
| `tb_class_music_payment` | 8 `rev_` payment rows, each referencing a project | Counts checked against the revenue design |
| `tb_music_album` | 43 `cnt_collection` (album) | |
| `tb_music_track` | 8,988 `cnt_media` (track) | |
| `tb_picture` | 98 `cnt_media` (photo) | |
| `tb_vgallery_videos` | 122 `cnt_media` (video) | |
| `tb_programme_video` | 4,384 `cnt_membership` rows | 2 orphan rows to resolve first |
| `tb_programme_artist` | 3,161 `cnt_item_contributor` | |
| `tb_music_album_artist` | 425 `cnt_item_contributor` | |
| `tb_music_album_category` | 783 `cnt_item_category` | |
| `tb_latest_updates` | 59 `cnt_article` | |
| `tb_cost_package` | 364 `cnt_price` | |
| `tb_product` | 3 `cnt_item` (product) | Three test rows excluded and listed in the exclusion report |

Any difference from these numbers must appear in the exclusion report with a reason. No row is dropped silently.

---

## 8. Constraints the code enforces

Some rules can't be expressed in MySQL 8 without triggers, and triggers are harder to test. These are enforced in the application layer, with a nightly check that reports violations:

- A `cnt_collection` row's `kind` decides which nullable columns may be set (`level_id` only for programmes, `starts_at` and `ends_at` only for programmes and albums).
- Trailer rule: pending decision 10. Do not enforce "one trailer per collection" until it's decided.
- At most one `is_primary = 1` row per item in `cnt_item_category`.
- At most one active (`is_active = 1`) price per item and currency window.
- `cnt_attribute` values must match the key's `value_type` in `dim_attribute_key`.
- A `cnt_item` of kind `media` must have exactly one `cnt_media` row. An item of other kinds must not.

---

## 9. Search and composer reads

The composer reads content by kind, status, visibility, category, tag, attribute and level, and it needs each item's card fields in one query. Indexes in this model cover those access paths:

- `cnt_item (status, visibility, published_from)` for the public listing.
- `cnt_item (kind, slug)` for URLs.
- `cnt_item_category (category_id)` for category pages.
- `cnt_item_tag (tag_id)` for tag pages.
- `cnt_attribute (attr_key_id, value_str)` and `(attr_key_id, value_num)` for composer filters.
- `cnt_membership (item_id)` for "which collections is this in".
- `cnt_item_stats` as one row per item, joined on `item_id`.

Card fields (title, short description, cover image, primary contributor, level, price) come from a view, `v_cnt_card`, that joins the item, its cover from `cnt_item_media` and its current price. The view is for reads only. Writes go to the tables.

---

## 10. Why not the alternatives

- **One table per content type, as in the legacy schema.** This is what the PDF started from. It means the composer needs a polymorphic reference for every slot, and every new type needs a new membership table, a new image table and a new price table. The supertype and shared link tables remove that repetition.
- **One table for all media with all the file columns.** Simpler than the current model, but it hides the difference between a programme and an album, which the composer and pricing both need. `cnt_collection` keeps that difference explicit.
- **JSON columns for everything.** Flexible, but the composer's filters would need generated columns and indexes for every key, and the referential checks would be lost. Typed attributes with a registry keep the flexibility and the checks.
- **Pricing on the item.** Simpler to start with, but a price change would overwrite history, and orders would need to snapshot it anyway. A price table keeps the history and gives the same snapshot.
- **Counters on the item.** Simpler to read, but they go stale, and they disagree with the events they came from. A rebuildable read model is cheaper to trust.

---

## 11. Dimension and enum summary

| Name | Kind | Owner | Used by |
|---|---|---|---|
| `dim_category` | Dimension | Content | `cnt_item_category` |
| `dim_level` | Dimension | Content | `cnt_collection` |
| `dim_language` | Dimension | Content (shared with usr) | `cnt_item` |
| `dim_track_type` | Dimension, **Pending** | Content | `cnt_media` (optional) |
| `dim_article_type` | Dimension | Content | `cnt_article` |
| `dim_contributor_role` | Dimension | Content | `cnt_item_contributor` |
| `dim_attribute_key` | Dimension | Content | `cnt_attribute` |
| `dim_section_type` | Dimension | Content | `cnt_content_section` |
| `dim_learning_state` | Dimension (PDF) | usr | Composer eligibility |
| Enums (section 4.2) | Code | Content | Several |

---

## 12. Decision log

The numbers match the review, so references elsewhere in this document still work. Non-content decisions live in `adr-log.md`.

### 12.1 Status

| # | Topic | Status | Outcome, or where it's recorded |
|---|---|---|---|
| 1 | `tb_music` (11,671 rows) | Decided | Audio media, attached to videos (option A). See 3.3 |
| 2 | Playlists | Decided | `playlist` kind for the 591 user rows. The 2,586 anonymous rows go to `eng_` (ADR-005) |
| 3 | Collections | Decided | `collection` kind. 73 programme memberships. See 3.2 |
| 4 | `tb_project` | Decided | `project` kind in content. Payments stay in `rev_` (ADR-001) |
| 5 | `tb_menu` | Moved | Archived with the old admin panel (ADR-002) |
| 6 | `tb_pages` | Decided | Articles with `parent_item_id`. 36 join the Gita Govinda collection. See 3.4 |
| 7 | `tb_product` vs the PDF's `products` | Moved | `tb_product` is the source for `prd_product` (ADR-003) |
| 8 | Euro prices | Decided | Empty `price_eur` column, unused until euro is supported. See 3.12 |
| 9 | Cost codes | Decided | Clear codes map now. Unclear rows are held. Refinement to confirm (see 12.2) |
| 10 | Trailer | Open | Question below |
| 11 | Track type | Open | Default: `dim_track_type` table |
| 12 | Article type | Open | Meaning of `tb_latest_updates.type_id` values 1 and 2, and `pgm_type` |
| 13 | Text format | Open | Default: Markdown, sanitised on output |
| 14 | Short fields | Open | Default: short text stays on `cnt_item`, longer text moves to sections |
| 15 | Meta keywords | Open | Default: drop |
| 16 | Category images and `mudra` fields | Open | Default: `cnt_item_media` if categories become items |
| 17 | Status meanings | Open | Codes differ per table. Confirm each with the business owners |
| 18 | Rating type codes | Moved | Engagement (ADR-005) |
| 19 | `tb_freeclass` test rows | Open | Default: exclude test rows, listed in the exclusion report |
| 20 | Contributor registry | Open | Depends on the Gurus group design |
| 21 | Translations | Deferred | Content is single-language for now |
| 22 | Public site navigation | Moved | Open in ADR-004 |

### 12.2 Decisions to confirm

- **Decision 9, refinement.** The `r` and `f` package codes affect validity and renewal, not the price amounts. So prices migrate for all 364 rows, and only the access interpretation is held. Without this split, most video prices would wait on the `r` and `f` answer.

### 12.3 Next open question

- **Decision 10, trailer.** The legacy link table marks 350 rows as trailers, across 103 programmes. 68 of those programmes have more than one. The doc's original rule of one trailer per collection doesn't match the data. The options are:
  - **A.** Keep one flag and allow several per programme. Simple, but "trailer" keeps two meanings.
  - **B.** Enforce one trailer per programme and clear the rest. Matches the model, but loses flags that may be intended preview lessons.
  - **C.** Split the meaning: `trailer_item_id` on `cnt_collection` for the single hero teaser, and `is_preview` on `cnt_membership` for sample lessons. The 350 flags migrate into `is_preview`. Recommended.

---

## 13. Glossary

- **Item.** Any browsable thing. Every row in `cnt_item`.
- **Collection.** A named container of members. Programmes, albums, playlists, galleries and bundles.
- **Media.** A playable or viewable unit with a file or an embed. Videos, tracks, photos and documents.
- **Membership.** A placement of an item in a collection.
- **Trailer.** The preview member of a programme or album.
- **Contributor.** A guru, artist or producer credited on an item.
- **Card projection.** The fields every layout needs: title, short description, cover, primary contributor, level and price.
- **Read model.** A table that caches numbers derived from events. Rebuildable, never the source of truth.
- **Legacy trace.** `legacy_table` and `legacy_id`, kept on rows so migration can be checked.
