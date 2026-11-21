from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"

OUTPUT_FILES = [
    "beginners-level-listing.html","class-detail-page.html","class-listing-page.html","class-search-listing-page.html",
    "dance-form-detail-page.html","dance-form-listing-page.html","free-video-detail-page.html","free-video-page.html",
    "guru-detail-page.html","guru-listing-page.html","latest-news-detail-page.html","latest-news.html","media-page.html",
    "mudra-detail-page.html","mudra-listing-page.html","photo-gallery.html","preview-video-detail-page.html",
    "preview-video-page.html","programmes-listing-page.html","video-gallery-detail-page.html","video-gallery-page.html",
    "video-listing-page.html",
]

IMAGES = [
    "assets/images/pali-01.jpg","assets/images/pali-02.jpg","assets/images/pali-03.jpg","assets/images/angika.webp",
    "assets/images/cholkettu.webp","assets/images/bharatanatyam.webp","assets/images/kathak.webp","assets/images/odissi.webp",
    "assets/images/kuchipudi.webp","assets/images/video-01.jpg","assets/images/video-02.jpg","assets/images/video-03.jpg",
    "assets/images/video-04.jpg","assets/images/news-01.jpg",
]

def read_index() -> str:
    return INDEX_PATH.read_text(encoding="utf-8")

def section_from_marker(html: str, marker: str) -> str:
    i = html.find(marker)
    if i == -1:
        raise ValueError(f"Marker not found: {marker}")
    s = html.find("<section", i)
    e = html.find("</section>", s)
    if s == -1 or e == -1:
        raise ValueError(f"Section extraction failed for marker: {marker}")
    return html[i : e + len("</section>")]

def extract_parts(index_html: str) -> dict[str, str]:
    body_match = re.search(r"<body[^>]*>", index_html, flags=re.IGNORECASE)
    if not body_match:
        raise ValueError("Could not find <body> tag")
    before_body = index_html[: body_match.start()]
    body_tag = body_match.group(0)
    nav_start = index_html.find("<!-- Section 1: Header")
    sec2_start = index_html.find("<!-- Section 2:")
    if nav_start == -1 or sec2_start == -1:
        raise ValueError("Could not extract navbar block from index.html")
    nav_block = index_html[nav_start:sec2_start].strip()
    cta = section_from_marker(index_html, "<!-- Section 12:")
    footer_start = index_html.find("<!-- Section 13: Footer")
    footer_end = index_html.find("</footer>", footer_start)
    footer = index_html[footer_start : footer_end + len("</footer>")]
    return {"before_body": before_body, "body_tag": body_tag, "nav": nav_block, "cta": cta, "footer": footer}

def update_head(before_body: str, title: str, description: str) -> str:
    updated = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", before_body, count=1, flags=re.I | re.S)
    if re.search(r'<meta\s+name="description"', updated, flags=re.I):
        updated = re.sub(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', f'<meta name="description" content="{description}">', updated, count=1, flags=re.I | re.S)
    else:
        updated = updated.replace("</head>", f'    <meta name="description" content="{description}">\n</head>')
    updated = re.sub(r"<script>\s*tailwind\.config\s*=.*?</script>\s*", "", updated, flags=re.I | re.S)
    updated = re.sub(r'<style\s+type="text/tailwindcss">.*?</style>\s*', "", updated, flags=re.I | re.S)
    updated = re.sub(r'\s*<!-- Tailwind CSS -->\s*', "\n", updated, flags=re.I)
    updated = re.sub(r'\s*<script\s+src="https://cdn\.tailwindcss\.com"></script>\s*', "\n", updated, flags=re.I)
    updated = re.sub(r'\s*<script\s+src="assets/js/tailwind-config\.js"></script>\s*', "\n", updated, flags=re.I)
    updated = re.sub(r'\s*<script\s+src="assets/js/tailwind-components\.js"></script>\s*', "\n", updated, flags=re.I)
    updated = re.sub(
        r'<link\s+rel="stylesheet"\s+href="assets/css/tailwind-components\.css"\s+type="text/tailwindcss">\s*',
        "",
        updated,
        flags=re.I,
    )
    if "assets/css/tailwind.css" not in updated:
        if "assets/css/pages.css" in updated:
            updated = updated.replace(
                '<link rel="stylesheet" href="assets/css/pages.css">',
                '<link rel="stylesheet" href="assets/css/tailwind.css">\n    <link rel="stylesheet" href="assets/css/pages.css">',
                1,
            )
        else:
            updated = updated.replace("</head>", '    <link rel="stylesheet" href="assets/css/tailwind.css">\n</head>')
    if "assets/css/pages.css" not in updated:
        updated = updated.replace("</head>", '    <link rel="stylesheet" href="assets/css/pages.css">\n</head>')
    if "assets/css/navbar.css" not in updated:
        updated = updated.replace("</head>", '    <link rel="stylesheet" href="assets/css/navbar.css">\n</head>')
    if "assets/css/responsive.css" not in updated:
        updated = updated.replace("</head>", '    <link rel="stylesheet" href="assets/css/responsive.css">\n</head>')
    return updated

def update_cta_buttons(cta_html: str) -> str:
    labels = ["Explore Classes", "Join Now"]
    def repl(m: re.Match[str]) -> str:
        label = labels.pop(0) if labels else m.group(2)
        return f"{m.group(1)}{label}{m.group(3)}"
    return re.sub(r"(<button[^>]*>)(.*?)(</button>)", repl, cta_html, count=2, flags=re.I | re.S)

def update_nav_links(nav_html: str) -> str:
    nav_html = nav_html.replace(
        'href="#" class="hover:text-brand-pink transition-colors px-4 py-4">Programmes',
        'href="programmes-listing-page.html" class="hover:text-brand-pink transition-colors px-4 py-4">Programmes',
    )
    nav_html = nav_html.replace(
        'href="#" class="text-2xl font-serif font-bold text-gray-900 hover:text-brand-pink transition-colors">Programmes',
        'href="programmes-listing-page.html" class="text-2xl font-serif font-bold text-gray-900 hover:text-brand-pink transition-colors">Programmes',
    )
    return nav_html

def footer_link_target(text: str) -> str | None:
    t = re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", "", text)).strip().lower()
    for k, v in {
        "home": "index.html","classes": "class-listing-page.html","programmes": "programmes-listing-page.html","gurus": "guru-listing-page.html",
        "dance forms": "dance-form-listing-page.html","latest news": "latest-news.html","media": "media-page.html","photo gallery": "photo-gallery.html","video gallery": "video-gallery-page.html",
    }.items():
        if k in t:
            return v
    return None

def update_footer_links(footer_html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        attrs, text = m.group(1), m.group(2)
        tgt = footer_link_target(text)
        if not tgt:
            return m.group(0)
        attrs = re.sub(r'href="[^"]*"', f'href="{tgt}"', attrs) if "href=" in attrs else attrs + f' href="{tgt}"'
        return f"<a{attrs}>{text}</a>"
    return re.sub(r"<a([^>]*)>(.*?)</a>", repl, footer_html, flags=re.I | re.S)

def breadcrumb(items):
    b = []
    for i, (label, href) in enumerate(items):
        b.append(f'<a href="{href}" class="hover:text-brand-pink">{label}</a>' if href else f'<span class="text-brand-pink font-semibold">{label}</span>')
        if i < len(items) - 1:
            b.append('<span class="mx-2 text-gray-400">/</span>')
    return f'<nav class="page-breadcrumb">{"".join(b)}</nav>'

def page_hero(title, intro, crumbs, split=True):
    cls = "page-hero page-hero--split" if split else "page-hero"
    return f'<section class="{cls}"><div class="container-custom">{breadcrumb(crumbs)}<div class="page-hero-grid"><h1 class="page-hero-title">{title}</h1><p class="page-hero-intro">{intro}</p></div></div></section>'

def sort_dropdown(label="Art forms"):
    return f'<label class="page-sort-dropdown"><span class="page-sort-dropdown-label">Sort by:</span><select class="page-sort-dropdown-select"><option>{label}</option><option>Most classes</option><option>A–Z</option></select></label>'

def filter_bar(title="Filter Courses", listing=False, preview=False):
    if preview:
        fields = (
            '<label><span>Dance Form</span><select><option>--Choose Dance Form--</option><option>Kathak</option><option>Bharatanatyam</option><option>Odissi</option><option>Kuchipudi</option></select></label>'
            '<label><span>Level</span><select><option>--Choose Dance Level--</option><option>Beginners</option><option>Intermediate</option><option>Master Class</option></select></label>'
            '<label><span>Guru</span><select><option>--Choose Guru--</option><option>Sreelakshmy Govardhanan</option><option>Guru Dr Pali Chandra</option><option>Neena Prasad</option></select></label>'
            '<button type="button" data-filter-apply class="page-filter-apply">Apply Filter</button>'
        )
    elif listing:
        fields = (
            '<label><span>Dance Form</span><select><option>---Choose Dance Form---</option><option>Kathak</option><option>Bharatanatyam</option><option>Odissi</option></select></label>'
            '<label><span>Level</span><select><option>---Choose Dance Level---</option><option>Beginners</option><option>Intermediate</option><option>Master Class</option></select></label>'
            '<label><span>Date</span><select><option>---Choose Date---</option><option>Last 30 days</option><option>Last 6 months</option></select></label>'
            '<button type="button" data-filter-apply class="page-filter-apply">Apply Filter</button>'
        )
    else:
        fields = (
            '<label><span>Dance Form</span><select><option>All Forms</option></select></label>'
            '<label><span>Level</span><select><option>All Levels</option></select></label>'
            '<label><span>Guru</span><select><option>All Gurus</option></select></label>'
            '<button type="button" data-filter-apply class="btn-primary">Apply Filter</button>'
        )
    return f'<section class="page-filter-bar"><div class="container-custom"><form data-filter-form class="page-filter-bar-inner"><h2>{title}</h2><div class="page-filter-fields">{fields}</div></form></div></section>'

def featured_class_card(title, guru, form, img, href, level, featured_enroll=False, compact=False, overlay=False):
    mods = (" page-class-card--compact" if compact else "") + (" page-class-card--featured" if overlay else "")
    heart = '<button class="page-card-heart" aria-label="Wishlist">&#9825;</button>' if overlay else ""
    btn = "btn-primary" if featured_enroll else "btn-pink-outline"
    badge = "Featured" if overlay else level
    return f'<article class="page-class-card{mods} page-reveal"><div class="page-class-card-media"><img src="{img}" alt="{title}"><span class="page-class-card-tag">{badge}</span>{heart}</div><div class="page-class-card-body"><p class="page-class-card-meta">{form} • {level}</p><h3>{title}</h3><p class="page-class-card-guru">By {guru}</p><div class="page-class-card-stats"><span>24 Lessons</span><span>7 Days</span><span>4K</span></div><a href="{href}" class="{btn}">Enroll Now</a></div></article>'

def class_grid_section(title, subtitle, cards_html, sort_label="Sort by: All Forms", view_all_btn=True, load_more=False):
    view = '<a href="class-listing-page.html" class="btn-pink-outline">View Classes</a>' if view_all_btn else ""
    load = '<button class="btn-primary">Load More</button>' if load_more else ""
    return f'<section class="page-section"><div class="container-custom"><div class="page-section-head"><div><h2 class="section-title">{title}</h2><p class="page-section-subtitle">{subtitle}</p></div><span class="page-sort-pill">{sort_label}</span></div><div class="page-class-grid">{cards_html}</div><div class="page-section-actions">{view}{load}</div></div></section>'

def carousel_section(title, slides, per_view='{"default":1,"md":2,"lg":3}', dots=True, nav=True, subtitle=None):
    sh = f'<p class="page-section-subtitle">{subtitle}</p>' if subtitle else ""
    nh = '<div class="page-carousel-nav"><button type="button" data-carousel-prev class="carousel-nav-btn">&#8592;</button><button type="button" data-carousel-next class="carousel-nav-btn">&#8594;</button></div>' if nav else ""
    da = ' data-dots="true"' if dots else ""
    dh = '<div class="flex justify-center gap-2.5 mt-8" data-carousel-dots></div>' if dots else ""
    return f'<section class="page-section"><div class="container-custom"><div class="page-section-head"><div><h2 class="section-title">{title}</h2>{sh}</div>{nh}</div><div data-carousel data-per-view=\'{per_view}\' data-step="1"{da}><div class="carousel-viewport -mx-2 sm:-mx-4"><div class="carousel-track px-2 sm:px-4">{"".join(slides)}</div></div>{dh}</div></div></section>'

def testimonials_section():
    slides = [f'<div class="carousel-slide px-2 sm:px-4"><article class="page-testimonial"><span class="page-testimonial-quote">"</span><div class="page-stars">★★★★★</div><p>{q}</p><h4>{n}</h4><span>{b}</span></article></div>' for q, n, b in [("Structured and soulful learning journey.", "Ananya", "Performer"),("The guru feedback is deeply personal.", "Meera", "Student"),("Perfect balance of theory and abhinaya.", "Rhea", "Dancer")]]
    return carousel_section("Student Testimonials", slides, per_view='{"default":1,"md":2,"lg":3}', dots=True, nav=False)

def student_stories_section():
    return section_from_marker(read_index(), "<!-- Section 8:")

def guru_listing_card(name, form, img, count, size="large", href="guru-detail-page.html"):
    size_cls = " page-guru-card-v2--large" if size == "large" else ""
    return (
        f'<article class="page-guru-card-v2{size_cls}">'
        f'<img src="{img}" alt="{name}">'
        f'<div class="page-guru-card-overlay"></div>'
        f'<div class="page-guru-card-foot"><div><h3>{name}</h3><p>{form}</p><span>{count}+ classes</span></div>'
        f'<a href="{href}" class="page-guru-profile-btn">View profile</a></div></article>'
    )

def guru_grid_section(title, gurus, grid_class="page-guru-grid--legendary", size="large"):
    cards = "".join(guru_listing_card(n, f, i, c, size=size) for n, f, i, c in gurus)
    return (
        f'<section class="page-section guru-listing-section"><div class="container-custom">'
        f'<div class="page-section-head"><h2 class="section-title">{title}</h2>{sort_dropdown()}</div>'
        f'<div class="page-guru-grid {grid_class}">{cards}</div></div></section>'
    )

def guru_carousel_section(title, gurus):
    slides = [f'<div class="carousel-slide px-2 sm:px-4">{guru_listing_card(name, form, img, count, size="medium")}</div>' for name, form, img, count in gurus]
    return carousel_section(title, slides, per_view='{"default":1,"sm":2,"lg":3}', dots=False, nav=True)

def tab_section(tab_labels, tab_panels_html, dark=False):
    tabs = "".join(f'<button type="button" class="page-tab{" is-active" if i == 0 else ""}" data-tab="{i}" aria-selected="{"true" if i == 0 else "false"}">{l}</button>' for i, l in enumerate(tab_labels))
    panels = "".join(f'<div class="page-tab-panel{" is-active" if i == 0 else ""}" data-tab-panel="{i}">{tab_panels_html[i]}</div>' for i in range(len(tab_panels_html)))
    wrap_cls = "page-tabs-wrap page-tabs-wrap--dark" if dark else "page-tabs-wrap"
    return f'<section class="{wrap_cls}"><div class="container-custom"><div data-tabs class="page-tabs">{tabs}</div><div>{panels}</div></div></section>'

def class_detail_hero_grid(title, guru, form, price, poster_img, video_src=None, level="Master Class"):
    youtube_videos = [
        "https://www.youtube.com/embed/h7TNtO-WitU?rel=0&amp;modestbranding=1&amp;playsinline=1",
        "https://www.youtube.com/embed/M7lc1UVf-VE?rel=0&amp;modestbranding=1&amp;playsinline=1",
        "https://www.youtube.com/embed/ysz5S6PUM-U?rel=0&amp;modestbranding=1&amp;playsinline=1",
        "https://www.youtube.com/embed/aqz-KE-bpKQ?rel=0&amp;modestbranding=1&amp;playsinline=1",
    ]
    playlist = [
        ("Introduction", poster_img, youtube_videos[0]),
        ("Section 1 Explanation", "assets/images/video-01.jpg", youtube_videos[1]),
        ("Section 1 Teaching", "assets/images/video-02.jpg", youtube_videos[2]),
        ("Section 2 Explanation", "assets/images/video-03.jpg", youtube_videos[3]),
    ]
    thumb_btns = "".join(
        f'<button type="button" class="{"is-active" if i == 0 else ""}" data-video-index="{i}"'
        f' data-youtube-src="{ysrc}" data-video-title="{vtitle}">'
        f'<img src="{img}" alt="{vtitle}"></button>'
        for i, (vtitle, img, ysrc) in enumerate(playlist)
    )
    course_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    star_icon = (
        '<svg class="page-class-detail-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
        '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>'
    )
    chat_icon = (
        '<svg class="page-class-detail-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>'
    )
    video_icon = (
        '<svg class="page-class-detail-stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>'
    )
    music_icon = (
        '<svg class="page-class-detail-stat-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19a3 3 0 11-6 0 3 3 0 016 0zm12-3a3 3 0 11-6 0 3 3 0 016 0z"/></svg>'
    )
    return (
        f'<div class="page-class-detail-hero-grid">'
        f'<div class="page-class-detail-player-wrap">'
        f'<div class="page-class-detail-player" data-class-detail-player data-course-id="{course_id}">'
        f'<div class="page-class-detail-video-stage">'
        f'<iframe data-class-detail-youtube src="{youtube_videos[0]}" title="{title} Introduction" loading="lazy" '
        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
        f'</div></div>'
        f'<div class="page-class-detail-thumbs-carousel" data-class-detail-thumbs-carousel>'
        f'<button type="button" class="page-class-detail-thumbs-nav page-class-detail-thumbs-nav--prev" data-class-detail-thumbs-prev aria-label="Previous lesson thumbnails"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg></button>'
        f'<div class="page-class-detail-thumbs" data-video-thumbs>{thumb_btns}</div>'
        f'<button type="button" class="page-class-detail-thumbs-nav page-class-detail-thumbs-nav--next" data-class-detail-thumbs-next aria-label="Next lesson thumbnails"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>'
        f'</div></div>'
        f'<aside class="page-class-detail-pricing">'
        f'<div class="page-class-detail-tags"><span>{level}</span><span>{form}</span></div>'
        f'<h1 class="page-class-detail-title">{title}</h1>'
        f'<p class="page-class-detail-guru">{guru}</p>'
        f'<div class="page-class-detail-meta-row">'
        f'<span class="page-class-detail-rating">{star_icon}4.4 Rating</span>'
        f'<a href="#reviews" class="page-class-detail-reviews-link">{chat_icon}Reviews</a></div>'
        f'<div class="page-class-detail-price-row">'
        f'<div><p class="page-class-detail-price">Rs.{price}</p>'
        f'<p class="page-class-detail-sub">Subscription <strong>1 Year</strong></p></div>'
        f'<button type="button" class="page-class-detail-quick-btn">Quick Answers</button></div>'
        f'<div class="page-class-detail-stats">'
        f'<div class="page-class-detail-stat-box">{video_icon}<div><strong>48 Videos</strong><span>03 hours 49 minutes</span></div></div>'
        f'<div class="page-class-detail-stat-box">{music_icon}<div><strong>1 Music</strong><span>09 min 53 sec</span></div></div></div>'
        f'<div class="page-class-detail-actions">'
        f'<button type="button" class="page-class-detail-cart-btn">Add to Cart</button>'
        f'<button type="button" class="page-class-detail-buy-btn">Buy Now</button></div>'
        f'<p class="page-class-detail-disclaimer">You have the option to buy the composition once. Renting the video(s) or copying is strictly not permitted.</p>'
        f'</aside></div>'
    )

def class_detail_tabs_inner():
    tab_labels = ["Lessons", "About The Composition", "Composition Info", "Accompanying Artist", "Dancers"]
    panels = [
        class_detail_lessons_panel(),
        "<p>Tarana composition with fast footwork, rhythmic clarity and lyrical movement transitions guided step by step.</p>",
        "<p>Raga Yaman, Tala Teentaal. Includes notation references and performance notes.</p>",
        "<p>Accompanying artists include tabla, sarangi and vocal support recorded for authentic learning context.</p>",
        "<p>Featured dancers demonstrate each segment with clear footwork, spins and expressive abhinaya.</p>",
    ]
    tabs = "".join(
        f'<button type="button" class="page-tab{" is-active" if i == 0 else ""}" data-tab="{i}" aria-selected="{"true" if i == 0 else "false"}">{l}</button>'
        for i, l in enumerate(tab_labels)
    )
    panel_html = "".join(
        f'<div class="page-tab-panel{" is-active" if i == 0 else ""}" data-tab-panel="{i}">{panels[i]}</div>'
        for i in range(len(panels))
    )
    return f'<div class="page-class-detail-tabs-wrap"><div data-tabs class="page-tabs page-class-detail-tabs">{tabs}</div><div>{panel_html}</div></div>'

def class_detail_top_section(title, guru, form, price, poster_img, video_src=None, level="Master Class"):
    return (
        f'<section class="page-class-detail-top">'
        f'<div class="container-custom">'
        f'{class_detail_hero_grid(title, guru, form, price, poster_img, video_src, level)}'
        f'{class_detail_tabs_inner()}'
        f'</div></section>'
    )

def class_detail_lessons_panel():
    lessons = [
        ("1", "Introduction", "2:34"),
        ("2", "Section 1 Explanation", "28:15"),
        ("3", "Section 1 Teaching", "9:23"),
        ("4", "Section 2 Explanation", "11:42"),
        ("5", "Section 2 Teaching", "11:29"),
        ("6", "Section 3 Explanation", "9:00"),
        ("7", "Section 3 Part I Teaching", "3:58"),
        ("8", "Performance Segment 1", "4:16"),
        ("9", "Performance Segment 2", "3:13"),
        ("10", "Performance Segment 3", "2:17"),
        ("11", "Performance Segment 4", "2:07"),
        ("12", "Performance Segment 5", "3:22"),
    ]
    visible_count = 5
    primary_rows = "".join(
        f"<tr><td>{no}</td><td>{title}</td><td>{dur}</td></tr>"
        for no, title, dur in lessons[:visible_count]
    )
    extra_rows = "".join(
        f"<tr><td>{no}</td><td>{title}</td><td>{dur}</td></tr>"
        for no, title, dur in lessons[visible_count:]
    )
    extra_panel = (
        f"<div data-curriculum-extra class='is-collapsed' aria-hidden='true'>"
        f"<table class='page-lesson-table page-lesson-table--continuation'>"
        f"<colgroup><col class='page-lesson-col-no'><col class='page-lesson-col-title'>"
        f"<col class='page-lesson-col-duration'></colgroup>"
        f"<tbody>{extra_rows}</tbody></table></div>"
        if extra_rows
        else ""
    )
    toggle_btn = (
        "<div class='page-lesson-table-foot'>"
        "<button type='button' class='page-class-detail-view-all' data-curriculum-toggle "
        "aria-expanded='false'>View All</button></div>"
        if extra_rows
        else ""
    )
    return (
        f"<div class='page-detail-grid'><div class='page-lesson-table-wrap' data-curriculum-table "
        f"data-curriculum-visible-count='{visible_count}'>"
        f"<table class='page-lesson-table'>"
        f"<colgroup><col class='page-lesson-col-no'><col class='page-lesson-col-title'>"
        f"<col class='page-lesson-col-duration'></colgroup>"
        f"<thead><tr><th>No</th><th>Title</th><th>Duration</th></tr></thead>"
        f"<tbody data-curriculum-primary>{primary_rows}</tbody></table>{extra_panel}{toggle_btn}</div>"
        f"<aside class='page-guru-mini-card page-class-detail-guru-card'>"
        f"<img src='assets/images/pali-chandra.webp' alt='Guru Dr Pali Chandra'>"
        f"<h4>Guru Dr Pali Chandra</h4>"
        f"<p>Globally acclaimed Kathak exponent, choreographer and educator with decades of stage, research and pedagogy.</p>"
        f"<a href='guru-detail-page.html' class='page-class-detail-profile-btn'>View profile</a></aside></div>"
    )

def video_hero(title, guru, form, price, poster_img, video_src=None, level="Master Class"):
    src = video_src or "assets/videos/banner.mp4"
    return (
        f'<section class="page-video-hero"><div class="container-custom"><div class="page-video-hero-grid"><div>'
        f'<div class="page-video-player" data-video-player><video poster="{poster_img}"><source src="{src}" type="video/mp4"></video>'
        f'<div class="page-video-controls"><button data-video-play>Play</button><div class="page-video-progress" data-video-progress><span data-video-progress-fill></span></div>'
        f'<span data-video-time>00:00 / 00:00</span><button data-video-mute>Mute</button><button data-video-fullscreen>Fullscreen</button></div></div>'
        f'<div class="page-video-thumbs" data-video-thumbs>'
        f'<button class="is-active" data-video-src="{src}" data-video-poster="{poster_img}"><img src="{poster_img}" alt="Main"><span>Main</span></button>'
        f'<button data-video-src="{src}" data-video-poster="assets/images/video-01.jpg"><img src="assets/images/video-01.jpg" alt="Clip"><span>Clip</span></button>'
        f'<button data-video-src="{src}" data-video-poster="assets/images/video-02.jpg"><img src="assets/images/video-02.jpg" alt="Clip"><span>Clip</span></button>'
        f'<button data-video-src="{src}" data-video-poster="assets/images/video-03.jpg"><img src="assets/images/video-03.jpg" alt="Clip"><span>Clip</span></button>'
        f'</div></div><aside class="page-pricing-card">'
        f'<div class="page-video-hero-tags"><span>{level}</span><span>{form}</span></div>'
        f'<h2>{title}</h2><p class="page-video-guru">{guru}</p>'
        f'<div class="page-video-hero-rating"><span>★ 4.8</span><em>(45 Reviews)</em></div>'
        f'<p class="page-pricing-amount">Rs. {price}</p><p class="page-pricing-sub">Subscription: 1 Year</p>'
        f'<div class="page-pricing-badges"><span>4K Video</span><span>7 Days</span></div>'
        f'<div class="page-pricing-options"><button type="button" class="is-active">All Videos<small>67 videos</small></button>'
        f'<button type="button">7 Days<small>Trial access</small></button></div>'
        f'<button class="btn-pink-outline w-full">Add to Cart</button><button class="btn-primary w-full">Buy Now</button>'
        f'</aside></div></div></section>'
    )

def review_stars(count: int) -> str:
    filled = "★" * count
    empty = "☆" * (5 - count)
    return f'<span class="page-review-card-stars" aria-label="{count} star rating">{filled}{empty}</span>'

def reviews_section():
    rows = [
        ("5 stars", "2,348", "60.8%"),
        ("4 stars", "785", "20.3%"),
        ("3 stars", "422", "10.9%"),
        ("2 stars", "189", "4.9%"),
        ("1 star", "118", "3.1%"),
    ]
    bars = "".join(
        f'<div class="page-review-bar-row"><span class="page-review-bar-label">{label}</span>'
        f'<div class="page-review-bar-track"><i style="width:{width}"></i></div>'
        f'<span class="page-review-bar-count">{count}</span></div>'
        for label, count, width in rows
    )
    items = "".join(
        f'<article class="page-review-card"><div class="page-review-card-header">'
        f'<div class="page-review-card-user"><div class="page-review-avatar" aria-hidden="true">{initial}</div>'
        f'<h4>{name}</h4></div>{review_stars(stars)}</div><p>{text}</p></article>'
        for name, initial, stars, text in [
            ("Priya Sharma", "P", 5, "The structured approach helped me improve my technique significantly. Guru Pali Chandra's explanations are crystal clear!"),
            ("Meera Krishnan", "M", 4, "As a beginner, I was hesitant to start Kathak online. This platform made it accessible and enjoyable."),
            ("Anjali Reddy", "A", 5, "The video quality and camera angles are excellent. I can see every mudra and footwork clearly."),
        ]
    )
    return (
        f'<section id="reviews" class="page-section page-reviews-section"><div class="container-custom"><div class="page-reviews-grid">'
        f'<div class="page-reviews-summary"><h2 class="section-title">Reviews &amp; Rating</h2>'
        f'<div class="page-reviews-rating"><div class="page-reviews-stars" aria-label="4.2 out of 5 stars">'
        f'<span>★</span><span>★</span><span>★</span><span>★</span><span>★</span></div>'
        f'<span class="page-reviews-rating-text">(4.2 out of 5)</span></div>'
        f'<p class="page-reviews-count">Based on 3,862 reviews</p>'
        f'<div class="page-reviews-bars">{bars}</div>'
        f'<div class="page-reviews-cta"><h3>Share your thoughts with us</h3>'
        f'<button type="button" class="page-reviews-post-btn">Post Your Review</button></div></div>'
        f'<div class="page-reviews-list">{items}</div></div></div></section>'
    )

def detail_all_classes_section():
    cards_data = [
        ("Payaliya Tarana", "Guru Dr Pali Chandra", "Kathak", "assets/images/pali-chandra.webp"),
        ("Angika Essentials", "Smitha Rajan", "Bharatanatyam", "assets/images/angika.webp"),
        ("Cholkettu Repertoire", "Neena Prasad", "Mohiniyattam", "assets/images/cholkettu.webp"),
        ("Thumri Expressions", "Guru Dr Pali Chandra", "Kathak", "assets/images/thumri.webp"),
        ("Mangalacharan Series", "Madhavi Mudgal", "Odissi", "assets/images/mangalacharan1.webp"),
        ("Kuchipudi Basics", "Rajashree Warrier", "Kuchipudi", "assets/images/kuchipudi.webp"),
    ]
    cards_html = "".join(
        guru_premium_class_card(t, g, f, i, f.lower().replace(" ", "_"))
        for t, g, f, i in cards_data
    )
    return (
        f'<section class="page-section page-all-classes-section"><div class="container-custom">'
        f'<div class="page-listing-section-head"><h2 class="section-title">All Classes</h2><p>Continue learning with related classes.</p></div>'
        f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">{cards_html}</div>'
        f'<div class="page-section-actions page-section-actions--center"><a href="class-listing-page.html" class="btn-pink-outline">View Classes</a></div>'
        f'</div></section>'
    )

def listing_class_card(title, guru, form, img, href, level, featured=False):
    category = form.lower().replace(" ", "_")
    return guru_premium_class_card(title, guru, form, img, category).replace(
        'href="class-detail-page.html"', f'href="{href}"'
    )

def listing_cards_html(count=6, first_primary=True, href="class-detail-page.html"):
    d = [
        ("Cholkettu", "Neena Prasad", "Mohiniyattam", "assets/images/cholkettu.webp", "Composition"),
        ("Mangalacharan", "Madhavi Mudgal", "Odissi", "assets/images/mangalacharan1.webp", "Master Class"),
        ("Angika", "Dr Rajasree Warrier", "Bharatanatyam", "assets/images/angika.webp", "Beginners"),
        ("Payaliya Tarana", "Guru Dr Pali Chandra", "Kathak", "assets/images/pali-chandra.webp", "Master Class"),
        ("Thumri Expressions", "Guru Dr Pali Chandra", "Kathak", "assets/images/thumri.webp", "Composition"),
        ("Kuchipudi Basics", "Rajashree Warrier", "Kuchipudi", "assets/images/kuchipudi.webp", "Beginners"),
    ]
    return "".join(listing_class_card(t, g, f, i, href, l, featured=first_primary and idx == 0) for idx, (t, g, f, i, l) in enumerate(d[:count]))

def listing_class_section(title, subtitle, cards_html):
    return (
        f'<section class="page-section"><div class="container-custom">'
        f'<div class="page-listing-section-head"><h2 class="section-title">{title}</h2><p>{subtitle}</p></div>'
        f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">{cards_html}</div>'
        f'<div class="page-section-actions page-section-actions--center"><a href="class-listing-page.html" class="btn-pink-outline">View Classes</a></div>'
        f'</div></section>'
    )

def guru_class_card(title, level, img, href="class-detail-page.html", primary=False):
    btn = "btn-primary" if primary else "btn-pink-outline"
    label = "Start Now" if primary else "Enroll Now"
    return (
        f'<article class="page-guru-class-card"><img src="{img}" alt="{title}">'
        f'<div class="page-guru-class-card-body"><p class="page-guru-class-card-meta">{level}</p>'
        f'<h3>{title}</h3><a href="{href}" class="{btn}">{label}</a></div></article>'
    )

def guru_detail_learning_paths_section():
    html = section_from_marker(read_index(), "<!-- Section 5:")
    html = html.replace(
        "Curated Learning Paths <br> for Every Stage",
        "Structured Courses For Every Stage And Everyone",
    )
    html = html.replace(
        "Embark on a structured journey of classical dance, guided from foundational steps to advanced performance repertoire.",
        "Level-wise pathways with guided milestones for every learner.",
    )
    html = html.replace(
        'class="py-24 bg-brand-cream border-t border-b border-gray-100 curated-learning-paths"',
        'class="py-24 bg-brand-cream border-t border-b border-gray-100 curated-learning-paths guru-detail-learning-paths"',
    )
    for old_id, new_id in {
        "primaryTabsContainer": "guruPrimaryTabsContainer",
        "secondaryTabsContainer": "guruSecondaryTabsContainer",
        "pathViewAllBtn": "guruPathViewAllBtn",
        "pathPanel": "guruPathPanel",
        "pathImg": "guruPathImg",
        "pathTag": "guruPathTag",
        "pathTitle": "guruPathTitle",
        "pathGuru": "guruPathGuru",
        "pathDesc": "guruPathDesc",
        "pathDuration": "guruPathDuration",
        "pathLessons": "guruPathLessons",
        "pathLevel": "guruPathLevel",
    }.items():
        html = html.replace(f'id="{old_id}"', f'id="{new_id}"')
    html = html.replace('href="#featured-classes"', 'href="class-listing-page.html"')
    return html

STAR_SVG = '<svg class="w-3.5 h-3.5 fill-current mr-1" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>'

def guru_premium_class_card(title, guru, form, img, category, hours="3.2 Hours", lessons="24 Lessons", primary_enroll: bool = False):
    enroll_cls = (
        "bg-brand-pink text-white border-brand-pink block py-3 px-4 text-sm rounded-lg"
        if primary_enroll
        else "bg-transparent block py-3 px-4 text-sm border rounded-lg group-hover:bg-brand-pink group-hover:text-white group-hover:border-brand-pink"
    )
    return (
        f'<div class="card-premium group zoom-img-container flex flex-col justify-between" data-category="{category}">'
        f'<div class="relative overflow-hidden"><div class="relative h-[495px] overflow-hidden">'
        f'<img src="{img}" alt="{title}" class="w-full h-full object-cover">'
        f'<div class="absolute top-6 left-6"><span class="bg-[rgba(17,17,17,0.50)] text-white text-[10px] font-extrabold px-4 py-1.5 rounded-full uppercase tracking-wider font-sans">{form}</span></div></div>'
        f'<div class="p-4 card-content absolute bottom-0 left-0 right-0 bg-white group-hover:opacity-100 group-hover:bg-transparent transition-all duration-700 ease-out">'
        f'<h3 class="text-xl md:text-2xl font-bold text-gray-900 mb-1.5 font-serif group-hover:text-white transition-colors">{title}</h3>'
        f'<p class="text-sm text-gray-500 font-sans font-medium mb-2 group-hover:text-white">{guru}</p>'
        f'<div class="flex justify-between items-center space-x-2 text-xs text-gray-400 group-hover:text-white font-medium font-sans">'
        f'<div class="flex items-center space-x-2"><span class="flex items-center text-brand-gold">{STAR_SVG}4.8</span>'
        f'<span>•</span><span>{hours}</span><span>•</span><span>{lessons}</span></div>'
        f'<a href="class-detail-page.html" class="{enroll_cls}">Enroll Now</a>'
        f'</div></div></div></div>'
    )

def guru_detail_classes_section():
    cards = "".join(
        guru_premium_class_card(t, g, f, i, c, h, l)
        for t, g, f, i, c, h, l in [
            ("Payaliya Tarana", "Guru Dr Pali Chandra", "Kathak", "assets/images/pali-chandra.webp", "kathak", "5.0 Hours", "28 Lessons"),
            ("Thumri Expressions", "Guru Dr Pali Chandra", "Kathak", "assets/images/thumri.webp", "kathak", "3.8 Hours", "16 Lessons"),
            ("Panchali Shapatam", "Guru Dr Pali Chandra", "Kathak", "assets/images/cholkettu.webp", "kathak", "4.5 Hours", "24 Lessons"),
            ("Shringara Lahari", "Guru Dr Pali Chandra", "Kathak", "assets/images/shringara-lahari.webp", "kathak", "4.2 Hours", "20 Lessons"),
            ("Parayatti Master Class", "Guru Dr Pali Chandra", "Kathak", "assets/images/kathak.webp", "kathak", "6.0 Hours", "22 Lessons"),
            ("Mora Re Ang...", "Guru Dr Pali Chandra", "Kathak", "assets/images/angika.webp", "kathak", "3.2 Hours", "18 Lessons"),
        ]
    )
    return (
        '<section id="guru-detail-classes" class="py-24 bg-white guru-detail-watched-classes">'
        '<div class="container-custom">'
        '<div class="flex flex-col md:flex-row justify-between items-center md:items-end gap-6 mb-12 border-b border-gray-100 pb-8">'
        '<div class="text-left"><h2 class="section-title mb-3">Guru Dr Pali Chandra\'s Classes</h2>'
        '<p class="text-gray-500 text-sm md:text-base font-sans max-w-lg">Browse courses designed and choreographed by the maestro.</p></div>'
        '<div class="relative inline-block text-left z-40"><div class="flex items-center gap-3">'
        '<span class="text-sm font-semibold text-gray-500 font-sans">Sort by:</span>'
        '<div class="relative">'
        '<button id="guruClassDropdownBtn" type="button" class="flex items-center justify-between w-52 px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm font-bold text-gray-700 shadow-sm hover:border-brand-pink/40 hover:bg-brand-cream/10 focus:outline-none transition-all duration-300">'
        '<span id="guruClassSelectedText">All Classes</span>'
        '<svg class="w-4 h-4 ml-2.5 text-gray-400 transition-transform duration-300" id="guruClassDropdownArrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 9l-7 7-7-7"></path></svg></button>'
        '<div id="guruClassDropdownMenu" class="absolute right-0 mt-2 w-52 rounded-xl bg-white border border-gray-100 shadow-[0_12px_30px_rgba(45,11,42,0.06)] py-1.5 z-50 hidden opacity-0 scale-95 origin-top-right transition-all duration-200">'
        '<button type="button" class="guru-class-dropdown-option block w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-brand-cream hover:text-brand-pink transition-colors" data-value="all">All Classes</button>'
        '<button type="button" class="guru-class-dropdown-option block w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-brand-cream hover:text-brand-pink transition-colors" data-value="kathak">Kathak</button>'
        '<button type="button" class="guru-class-dropdown-option block w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-brand-cream hover:text-brand-pink transition-colors" data-value="master_class">Master Class</button>'
        '<button type="button" class="guru-class-dropdown-option block w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-brand-cream hover:text-brand-pink transition-colors" data-value="composition">Composition</button>'
        '<button type="button" class="guru-class-dropdown-option block w-full text-left px-4 py-2.5 text-sm font-semibold text-gray-700 hover:bg-brand-cream hover:text-brand-pink transition-colors" data-value="beginners">Beginners</button>'
        '</div></div></div></div></div>'
        f'<div id="guruCompositionGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">{cards}</div>'
        '<div class="text-center mt-16"><button type="button" class="btn-pink-outline">Load More</button></div>'
        '</div></section>'
    )

def guru_detail_video_slide(title, img, href="video-gallery-page.html"):
    return (
        f'<div class="carousel-slide px-2 sm:px-3">'
        f'<a href="{href}" class="guru-video-gallery-card group block relative rounded-2xl overflow-hidden h-[220px] sm:h-[260px] md:h-[280px] zoom-img-container focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-pink focus-visible:ring-offset-2 focus-visible:ring-offset-[#0a0a0a]">'
        f'<img src="{img}" alt="{title}" class="w-full h-full object-cover">'
        f'<div class="absolute inset-0 guru-video-gallery-overlay"></div>'
        f'<div class="absolute inset-0 flex items-center justify-center pointer-events-none">'
        f'<span class="guru-video-play-btn" aria-hidden="true"><svg class="w-5 h-5 text-brand-pink ml-0.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></div>'
        f'<div class="absolute bottom-0 left-0 right-0 p-4 md:p-5"><h3 class="text-base md:text-lg font-bold font-serif text-white">{title}</h3></div>'
        f'</a></div>'
    )

def guru_detail_video_gallery_section():
    slides = "".join(
        guru_detail_video_slide(title, img)
        for title, img in [
            ("Obeisance", "assets/images/video-01.jpg"),
            ("The Journey", "assets/images/video-02.jpg"),
            ("Stage Presence", "assets/images/video-03.jpg"),
            ("Abhinaya Study", "assets/images/video-04.jpg"),
            ("Performance Clip", "assets/images/pali-01.jpg"),
            ("Gita Govinda Excerpt", "assets/images/gita-govinda.webp"),
        ]
    )
    return (
        '<section class="guru-detail-video-gallery py-16 md:py-20 bg-[#0a0a0a] text-white" aria-labelledby="guru-video-gallery-heading">'
        '<div class="container-custom">'
        '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8 md:mb-10">'
        '<h2 id="guru-video-gallery-heading" class="section-title">Video Gallery</h2>'
        '<a href="video-gallery-page.html" class="text-sm font-semibold text-white/75 hover:text-brand-pink transition-colors inline-flex items-center gap-1">Explore More <span aria-hidden="true">→</span></a>'
        '</div>'
        '<div data-carousel data-per-view=\'{"default":1,"sm":2,"md":3,"lg":4,"xl":5}\' data-step="1">'
        '<div class="flex items-center justify-end gap-2 mb-6 md:mb-8">'
        '<button type="button" data-carousel-prev class="guru-video-gallery-nav carousel-nav-btn" aria-label="Previous videos">'
        '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>'
        '<button type="button" data-carousel-next class="guru-video-gallery-nav carousel-nav-btn" aria-label="Next videos">'
        '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>'
        '</div>'
        f'<div class="carousel-viewport -mx-2 sm:-mx-3"><div class="carousel-track px-2 sm:px-3">{slides}</div></div>'
        '</div></div></section>'
    )

MEDIA_LINK_PAGE_ICON = (
    '<svg class="page-guru-media-link-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>'
)
MEDIA_LINK_PDF_ICON = (
    '<svg class="page-guru-media-link-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
)

def guru_detail_media_slide(source, date, title, img):
    return (
        f'<div class="carousel-slide px-2 sm:px-3">'
        f'<article class="page-guru-media-card">'
        f'<img src="{img}" alt="{title}">'
        f'<div class="page-guru-media-card-body">'
        f'<p class="page-guru-media-source">{source}</p>'
        f'<p class="page-guru-media-date">{date}</p>'
        f'<h3 class="page-guru-media-title">{title}</h3>'
        f'<div class="page-guru-media-links">'
        f'<a href="media-page.html" class="page-guru-media-link page-guru-media-link--primary">'
        f'{MEDIA_LINK_PAGE_ICON}<span>Link to page</span></a>'
        f'<span class="page-guru-media-link-sep" aria-hidden="true">|</span>'
        f'<a href="#" class="page-guru-media-link page-guru-media-link--muted">'
        f'{MEDIA_LINK_PDF_ICON}<span>Link to PDF</span></a>'
        f'</div></div></article></div>'
    )

def guru_detail_media_section():
    slides = "".join(
        guru_detail_media_slide(source, date, title, img)
        for source, date, title, img in [
            ("THE HINDU", "22, September, 2023", "Gita Govind At A Glance", "assets/images/gita-govinda.webp"),
            ("THE HINDU", "22, September, 2023", "Consent Of A Women", "assets/images/pali-02.jpg"),
            ("THE HINDU", "10, January, 2026", "Kathak Performed At Al Jadaf", "assets/images/news-01.jpg"),
            ("INDIAN EXPRESS", "22, February, 2026", "Global Students In One Classroom", "assets/images/video-02.jpg"),
        ]
    )
    return (
        '<section class="page-section guru-detail-media" aria-labelledby="guru-detail-media-heading">'
        '<div class="container-custom">'
        '<div data-carousel data-per-view=\'{"default":1,"md":2}\' data-step="1" class="guru-detail-media-carousel">'
        '<h2 id="guru-detail-media-heading" class="section-title guru-detail-media-title">Media</h2>'
        '<div class="guru-detail-media-nav">'
        '<button type="button" data-carousel-prev class="carousel-nav-btn guru-detail-media-nav-btn" aria-label="Previous media">'
        '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7 7-7"/></svg></button>'
        '<button type="button" data-carousel-next class="carousel-nav-btn guru-detail-media-nav-btn" aria-label="Next media">'
        '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>'
        '</div>'
        '<p class="guru-detail-media-subtitle">Find the latest news and information about our gurus and the platform published in various media.</p>'
        f'<div class="carousel-viewport guru-detail-media-viewport -mx-2 sm:-mx-3"><div class="carousel-track px-2 sm:px-3">{slides}</div></div>'
        '</div></div></section>'
    )

PROGRAMMES_CLOCK_ICON = (
    '<svg class="page-programmes-meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 7v5l3 2"/></svg>'
)
PROGRAMMES_LESSONS_ICON = (
    '<svg class="page-programmes-meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
)
PROGRAMMES_STAR_ICON = (
    '<svg class="page-programmes-stat-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
    '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>'
)
PROGRAMMES_MUSIC_ICON = (
    '<svg class="page-programmes-stat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" d="M9 19V6l12-3v13M9 19a3 3 0 11-6 0 3 3 0 016 0zm12-3a3 3 0 11-6 0 3 3 0 016 0z"/></svg>'
)
def programmes_lesson_tab(
    label: str,
    kicker: str,
    title: str,
    guru: str,
    description: str,
    img: str,
    duration: str,
    lessons: str,
    level: str,
    active: bool = False,
) -> str:
    active_cls = " is-active" if active else ""
    return (
        f'<button type="button" class="page-programmes-lesson-tab{active_cls}"'
        f' data-featured-kicker="{kicker}" data-featured-title="{title}"'
        f' data-featured-guru="{guru}" data-featured-desc="{description}"'
        f' data-featured-img="{img}" data-featured-duration="{duration}"'
        f' data-featured-lessons="{lessons}" data-featured-level="{level}">{label}</button>'
    )

def programmes_featured_metrics(duration: str, lessons: str, level: str) -> str:
    return (
        f'<div class="page-programmes-featured-metrics">'
        f'<div class="page-programmes-metric"><span class="page-programmes-metric-label">Duration</span>'
        f'<strong class="page-programmes-metric-value">{duration}</strong></div>'
        f'<div class="page-programmes-metric"><span class="page-programmes-metric-label">Lessons</span>'
        f'<strong class="page-programmes-metric-value">{lessons}</strong></div>'
        f'<div class="page-programmes-metric"><span class="page-programmes-metric-label">Level</span>'
        f'<strong class="page-programmes-metric-value">{level}</strong></div>'
        f'</div>'
    )

def programmes_featured_card(
    kicker: str,
    title: str,
    guru: str,
    description: str,
    img: str,
    duration: str,
    lessons: str,
    level: str,
) -> str:
    return (
        f'<article class="page-programmes-featured-card" data-programmes-featured>'
        f'<img src="{img}" alt="{title}" data-featured-image>'
        f'<div class="page-programmes-featured-body">'
        f'<p class="page-programmes-featured-kicker" data-featured-kicker>{kicker}</p>'
        f'<h3 class="page-programmes-featured-title" data-featured-title>{title}</h3>'
        f'<p class="page-programmes-featured-guru" data-featured-guru>{guru}</p>'
        f'<p class="page-programmes-featured-desc" data-featured-desc>{description}</p>'
        f'<div data-featured-metrics>{programmes_featured_metrics(duration, lessons, level)}</div>'
        f'<div class="page-programmes-featured-actions">'
        f'<button type="button" class="btn-primary">Start Learning</button>'
        f'<button type="button" class="btn-pink-outline">Preview</button>'
        f'</div></div></article>'
    )

def programmes_level_block(heading: str, level_id: str, lessons: list[dict[str, str]]) -> str:
    first = lessons[0]
    lesson_tabs = "".join(
        programmes_lesson_tab(
            lesson["label"],
            lesson["kicker"],
            lesson["title"],
            lesson["guru"],
            lesson["description"],
            lesson["img"],
            lesson["duration"],
            lesson["lessons"],
            lesson["level"],
            active=(i == 0),
        )
        for i, lesson in enumerate(lessons)
    )
    return (
        f'<article class="page-programmes-level-block" id="programmes-{level_id}" data-programme-level="{level_id}">'
        f'<div class="page-programmes-level-head"><h2 class="section-title">{heading}</h2></div>'
        f'<div class="page-programmes-lesson-row" data-programmes-lesson-tabs>'
        f'<div class="page-programmes-lesson-scroll" data-pill-tabs>{lesson_tabs}</div>'
        f'<a href="class-listing-page.html" class="page-programmes-view-all btn-pink-outline">View All</a>'
        f'</div>'
        f'{programmes_featured_card(first["kicker"], first["title"], first["guru"], first["description"], first["img"], first["duration"], first["lessons"], first["level"])}'
        f'</article>'
    )

def programmes_listing_section() -> str:
    category_pills = [
        ("beginners", "Beginners", True),
        ("master-class", "Master Class", False),
        ("compositions", "Compositions", False),
        ("intermediate", "Intermediate", False),
        ("performance", "Performance", False),
        ("techniques", "Techniques", False),
    ]
    pill_buttons = "".join(
        f'<button type="button" class="page-programmes-category-pill{" is-active" if active else ""}" '
        f'data-programmes-target="{target}">{label}</button>'
        for target, label, active in category_pills
    )
    def _lesson(**kw):
        return kw

    beginners_lessons = [
        _lesson(
            label="Pasyathi Dishi Dishi",
            kicker="BEGINNERS PATH • MOHINIYATTAM",
            title="Pasyathi Dishi Dishi - Beginners Foundation",
            guru="Guided by Guru Dr. Rajasree Warrier",
            description="Master the basic adavus, postures, and initial mudras required for the expressive Ashtapadi 'Pasyathi Dishi Dishi'.",
            img="assets/images/mohiniyattam.webp",
            duration="4.5 Hours",
            lessons="12 Lessons",
            level="Beginner",
        ),
        _lesson(
            label="Revathi Raga Thillana",
            kicker="BEGINNERS PATH • BHARATANATYAM",
            title="Revathi Raga Thillana - Beginners Foundation",
            guru="Guided by Rama Vaidyanathan",
            description="Learn foundational adavus, araimandi posture and rhythmic patterns through this accessible thillana introduction.",
            img="assets/images/bharatanatyam.webp",
            duration="3.5 Hours",
            lessons="10 Lessons",
            level="Beginner",
        ),
        _lesson(
            label="Ananthabhairavi Swarajathi",
            kicker="BEGINNERS PATH • BHARATANATYAM",
            title="Ananthabhairavi Swarajathi - Beginners Foundation",
            guru="Guided by Dr Rajashree Warrier",
            description="Step-by-step instruction in swarajathi repertoire with clear explanations of hastas, footwork and expression.",
            img="assets/images/angika.webp",
            duration="5 Hours",
            lessons="14 Lessons",
            level="Beginner",
        ),
    ]
    master_class_lessons = [
        _lesson(
            label="Payaliya Shubh Dinni",
            kicker="MASTER CLASS • KATHAK",
            title="Payaliya Shubh Dinni",
            guru="Guided by Guru Dr Pali Chandra",
            description="An advanced master class exploring intricate footwork, spins and abhinaya in this celebrated tarana composition.",
            img="assets/images/pali-chandra.webp",
            duration="6 Hours",
            lessons="18 Lessons",
            level="Advanced",
        ),
        _lesson(
            label="Tarana in Yaman",
            kicker="MASTER CLASS • KATHAK",
            title="Tarana in Yaman - Master Class",
            guru="Guided by Guru Dr Pali Chandra",
            description="Deep dive into yaman raga, rhythmic bols and performance presentation for experienced Kathak learners.",
            img="assets/images/cholkettu.webp",
            duration="5.5 Hours",
            lessons="16 Lessons",
            level="Advanced",
        ),
        _lesson(
            label="Thumri Excerpt",
            kicker="MASTER CLASS • KATHAK",
            title="Thumri Excerpt - Master Class",
            guru="Guided by Guru Dr Pali Chandra",
            description="Refine expressive abhinaya and subtle lasya through guided study of a classic thumri excerpt.",
            img="assets/images/kathak.webp",
            duration="4 Hours",
            lessons="12 Lessons",
            level="Advanced",
        ),
    ]
    composition_lessons = [
        _lesson(
            label="Alarippu",
            kicker="COMPOSITION • BHARATANATYAM",
            title="Alarippu - Composition Study",
            guru="Guided by Rama Vaidyanathan",
            description="Study the opening alarippu with detailed breakdown of adavus, tala and stage presentation techniques.",
            img="assets/images/bharatanatyam.webp",
            duration="3 Hours",
            lessons="8 Lessons",
            level="Intermediate",
        ),
        _lesson(
            label="Pushpanjali",
            kicker="COMPOSITION • BHARATANATYAM",
            title="Pushpanjali - Composition Study",
            guru="Guided by Dr Rajashree Warrier",
            description="Learn this invocatory piece with focus on nritta, hasta vocabulary and devotional expression.",
            img="assets/images/angika.webp",
            duration="3.5 Hours",
            lessons="9 Lessons",
            level="Intermediate",
        ),
        _lesson(
            label="Kriti",
            kicker="COMPOSITION • BHARATANATYAM",
            title="Kriti - Composition Study",
            guru="Guided by Rama Vaidyanathan",
            description="Explore sahitya, bhava and rhythmic structure in this kriti with guru-led annotations.",
            img="assets/images/cholkettu.webp",
            duration="4 Hours",
            lessons="11 Lessons",
            level="Intermediate",
        ),
    ]
    intermediate_lessons = [
        _lesson(
            label="Mangalacharan",
            kicker="INTERMEDIATE • ODISSI",
            title="Mangalacharan Foundation",
            guru="Guided by Madhavi Mudgal",
            description="Build tribhangi posture, chauka stance and foundational odissi movement vocabulary for intermediate learners.",
            img="assets/images/odissi.webp",
            duration="4.5 Hours",
            lessons="13 Lessons",
            level="Intermediate",
        ),
        _lesson(
            label="Batu",
            kicker="INTERMEDIATE • ODISSI",
            title="Batu - Intermediate Repertoire",
            guru="Guided by Madhavi Mudgal",
            description="Progress through pure dance sequences with emphasis on rhythm, stamina and sculptural line.",
            img="assets/images/odissi.webp",
            duration="5 Hours",
            lessons="15 Lessons",
            level="Intermediate",
        ),
        _lesson(
            label="Pallavi",
            kicker="INTERMEDIATE • ODISSI",
            title="Pallavi - Intermediate Repertoire",
            guru="Guided by Madhavi Mudgal",
            description="Develop musicality and expressive range through guided pallavi study and performance notes.",
            img="assets/images/odissi.webp",
            duration="5.5 Hours",
            lessons="16 Lessons",
            level="Intermediate",
        ),
    ]
    level_blocks = "".join([
        programmes_level_block("Beginners", "beginners", beginners_lessons),
        programmes_level_block("Master Class", "master-class", master_class_lessons),
        programmes_level_block("Composition", "compositions", composition_lessons),
        programmes_level_block("Intermediate", "intermediate", intermediate_lessons),
    ])
    return (
        f'<section class="page-programmes-listing" aria-labelledby="programmes-listing-heading">'
        f'<div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Programmes", None)])}'
        f'<div class="page-programmes-listing-hero">'
        f'<h1 id="programmes-listing-heading" class="page-programmes-listing-title">'
        f'Structured Courses For Every Stage And Everyone</h1>'
        f'<p class="page-programmes-listing-intro">Excellent classes designed for beginners, intermediate and advanced students, '
        f'as well as teachers, researchers and art lovers.</p>'
        f'</div>'
        f'<div class="page-programmes-category-pills" data-programmes-filter>{pill_buttons}</div>'
        f'<div class="page-programmes-level-stack">{level_blocks}</div>'
        f'</div></section>'
    )

def programme_block(heading, courses, featured_title, featured_guru, featured_img):
    pills = "".join(f'<button type="button" class="page-pill-tab{" is-active" if i == 0 else ""}">{c}</button>' for i, c in enumerate(courses))
    return f'<section class="page-programme-section page-reveal"><div class="container-custom"><div class="page-section-head"><h3 class="page-programme-title">{heading}</h3><a href="class-listing-page.html" class="page-link-arrow">Explore all →</a></div><div class="page-programme-pills">{pills}</div><article class="page-programme-featured-card"><img src="{featured_img}" alt="{featured_title}"><div><p class="page-class-card-meta">{heading}</p><h4>{featured_title}</h4><p>With {featured_guru}</p><div class="page-programme-actions"><button class="btn-pink-outline">Preview</button><button class="btn-primary">Start Learning</button></div></div></article></div></section>'

def media_card_horizontal(source, date, title, excerpt, img):
    return f'<article class="page-media-card"><img src="{img}" alt="{title}"><div><p class="page-card-kicker">{source} • {date}</p><h3>{title}</h3><p>{excerpt}</p><a href="media-page.html" class="page-link-arrow">Link to page →</a> <a href="#" class="page-link-arrow">Link to PDF →</a></div></article>'

def news_card_horizontal(date, title, excerpt, img, href):
    return f'<article class="page-news-card"><img src="{img}" alt="{title}"><div><p class="page-card-kicker">{date}</p><h3>{title}</h3><p>{excerpt}</p><a href="{href}" class="page-link-arrow">Read more →</a></div></article>'

def gallery_card(title, img, href="#"):
    return f'<article class="page-gallery-card page-reveal"><img src="{img}" alt="{title}"><div><h3>{title}</h3><a href="{href}" class="page-link-arrow">Explore →</a></div></article>'

def gallery_page_top(title: str, crumbs: list[tuple[str, str | None]]) -> str:
    return (
        f'<section class="page-gallery-top"><div class="container-custom">'
        f'{breadcrumb(crumbs)}'
        f'<h1 class="page-gallery-title">{title}</h1>'
        f'</div></section>'
    )

def photo_album_card(title: str, img: str, href: str, feature: bool = False) -> str:
    cls = "page-photo-album-card page-photo-album-card--feature" if feature else "page-photo-album-card"
    return (
        f'<article class="{cls} page-reveal">'
        f'<a href="{href}" class="page-photo-album-thumb"><img src="{img}" alt="{title}"></a>'
        f'<div class="page-photo-album-body"><h3>{title}</h3>'
        f'<a href="{href}" class="page-link-arrow">Explore →</a></div></article>'
    )

def mudra_grid_card(title: str, img: str, href: str = "mudra-detail-page.html") -> str:
    return (
        f'<article class="page-mudra-card page-reveal">'
        f'<a href="{href}" class="page-mudra-thumb"><img src="{img}" alt="{title}"></a>'
        f'<div class="page-mudra-body"><h3>{title}</h3>'
        f'<a href="{href}" class="page-link-arrow">Explore →</a></div></article>'
    )

PHOTO_GALLERY_CRUMBS = [("Home", "index.html"), ("Photo Gallery", None)]
PHOTO_GALLERY_ALBUMS = [
    ("Asamyuta Hasta Mudras", "assets/images/01_Pataka.jpg", "mudra-listing-page.html"),
    ("Samyuta Hasta Mudras", "assets/images/pali-02.jpg", "mudra-listing-page.html"),
    ("Kerala Folk Art Forms", "assets/images/gopi-kalamandalam.webp", "photo-gallery.html"),
    ("International Women's Day 2021", "assets/images/news-01.jpg", "photo-gallery.html"),
    ("Dance Day 2020", "assets/images/video-03.jpg", "photo-gallery.html"),
    ("International Women's Day 2023", "assets/images/pali-03.jpg", "photo-gallery.html"),
]

ASAMYUTA_MUDRAS = [
    ("Pataka", "assets/images/01_Pataka.jpg"),
    ("Tripataka", "assets/images/01_Pataka.jpg"),
    ("Ardhapataka", "assets/images/01_Pataka.jpg"),
    ("Kartarimukha", "assets/images/01_Pataka.jpg"),
    ("Mayura", "assets/images/01_Pataka.jpg"),
    ("Bhramara", "assets/images/01_Pataka.jpg"),
    ("Shukatunda", "assets/images/01_Pataka.jpg"),
    ("Shivalinga", "assets/images/01_Pataka.jpg"),
    ("Kataka", "assets/images/01_Pataka.jpg"),
]

MUDRA_PHOTO_FEATURE_ALBUMS = [
    ("Samyuta Hasta Mudras", "assets/images/pali-02.jpg", "mudra-listing-page.html"),
    ("Kerala Folk Art Forms", "assets/images/gopi-kalamandalam.webp", "photo-gallery.html"),
]

MUDRA_DETAIL_RELATED = [
    ("Asamyuta Hasta Mudras", "assets/images/01_Pataka.jpg", "mudra-listing-page.html"),
    ("Samyuta Hasta Mudras", "assets/images/pali-02.jpg", "mudra-listing-page.html"),
    ("Kerala Folk Art Forms", "assets/images/gopi-kalamandalam.webp", "photo-gallery.html"),
]

MUDRA_DETAIL_PHOTO_ALBUMS = [
    ("Samyuta Hasta Mudras", "assets/images/pali-02.jpg", "mudra-listing-page.html"),
    ("Kerala Folk Art Forms", "assets/images/gopi-kalamandalam.webp", "photo-gallery.html"),
]

PATAKA_MUDRA_DESCRIPTION = (
    "<p>The Pataka Mudra (Flag) is formed with the hand held upright, palm facing forward, fingers extended "
    "and held together, and the thumb bent slightly toward the palm. In Indian classical dance, this gesture "
    "is one of the foundational asamyuta hastas and appears across Bharatanatyam, Kuchipudi, Kathak and related forms.</p>"
    "<p>Pataka may denote a cloud, forest, river, wind, horse, chariot, door, pillar, warrior, king, flag, "
    "crown, tree, mountain, night, day, arrow, and numerous other symbolic meanings depending on context, "
    "accompanying hastas and abhinaya. It is also used for blessing, invocation, stopping, emphasis and "
    "directional indication on stage.</p>"
    "<p>Students learn to keep the fingers aligned without gaps, maintain a steady wrist, and pair the mudra "
    "with clear eye and head movement so the gesture reads cleanly from a distance — a discipline central to "
    "natyasutra&rsquo;s visual reference guides.</p>"
)

CAROUSEL_PREV_SVG = (
    '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>'
)
CAROUSEL_NEXT_SVG = (
    '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'
)

def dance_form_card(title, desc, img, href="dance-form-detail-page.html"):
    return (
        f'<article class="page-dance-form-card page-reveal zoom-img-container group">'
        f'<img src="{img}" alt="{title}">'
        f'<div class="page-dance-form-overlay"><h3>{title}</h3><p class="page-dance-form-desc">{desc}</p>'
        f'<a href="{href}" class="page-link-arrow">Explore →</a></div></article>'
    )

def index_masters_guru_slide(name, form, img, count, href="guru-detail-page.html"):
    return (
        f'<div class="carousel-slide px-2 sm:px-3">'
        f'<article class="group relative rounded-2xl overflow-hidden cursor-pointer h-[300px] md:h-[340px] zoom-img-container">'
        f'<img src="{img}" alt="{name}" class="w-full h-full object-cover">'
        f'<div class="absolute inset-0 guru-card-overlay"></div>'
        f'<div class="absolute bottom-0 left-0 right-0 p-4 md:p-5 flex items-end justify-between gap-2">'
        f'<div class="text-white"><h4 class="text-base md:text-lg font-bold font-serif mb-0.5">{name}</h4>'
        f'<p class="text-xs md:text-sm text-white/90 font-sans">{form}</p>'
        f'<p class="text-[10px] md:text-xs text-white/70 font-sans mt-0.5">{count}+ classes</p></div>'
        f'<a href="{href}" class="shrink-0 px-3 py-1.5 rounded-full border border-white/80 text-white text-[10px] md:text-xs font-bold font-sans hover:bg-white hover:text-gray-900 transition-colors">View profile</a>'
        f'</div></article></div>'
    )

def dance_forms_listing_top():
    return (
        f'<section class="page-dance-forms-top"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Dance forms", None)])}'
        f'<h1 class="page-dance-forms-title">Dance forms</h1></div></section>'
    )

def prepare_popular_classes_html(html: str, section_id: str = "popular-classes", centered: bool = False) -> str:
    html = re.sub(
        r'<section\s+id="featured-classes"(?:\s+data-popular-classes)?',
        f'<section data-popular-classes id="{section_id}"',
        html,
        count=1,
    )
    for elem_id, data_attr in (
        ("classDropdownBtn", "data-popular-classes-trigger"),
        ("classDropdownMenu", "data-popular-classes-menu"),
        ("classDropdownArrow", "data-popular-classes-arrow"),
        ("classSelectedText", "data-popular-classes-selected"),
        ("compositionGrid", "data-popular-classes-grid"),
    ):
        html = re.sub(
            rf'(id="{elem_id}")(?!\s+{re.escape(data_attr)})',
            rf'\1 {data_attr}',
            html,
        )
    if centered:
        html = html.replace('class="text-left"', 'class="text-center mx-auto"', 1)
        html = html.replace(
            'class="py-24 bg-white"',
            'class="py-24 bg-white dance-forms-popular-section"',
            1,
        )
    if section_id in ("preview-video-popular-classes", "beginners-level-classes"):
        html = html.replace(
            '<button class="bg-transparent block py-3 px-4 text-sm border rounded-lg group-hover:bg-brand-pink group-hover:text-white group-hover:border-brand-pink">Enroll Now</button>',
            '<button class="bg-brand-pink text-white border-brand-pink block py-3 px-4 text-sm border rounded-lg group-hover:bg-brand-pink group-hover:text-white group-hover:border-brand-pink">Enroll Now</button>',
            1,
        )
    html = html.replace(
        '<button class="btn-primary">View All Classes</button>',
        '<a href="class-listing-page.html" class="btn-pink-outline">View Classes</a>',
    )
    return html


def popular_classes_section(section_id: str = "popular-classes", centered: bool = True) -> str:
    html = section_from_marker(read_index(), "<!-- Section 4:")
    return prepare_popular_classes_html(html, section_id=section_id, centered=centered)

def learn_from_best_section():
    gurus = [
        ("Rama Vaidyanathan", "Bharatanatyam", "assets/images/ramavaidyanathan.webp", "17"),
        ("Guru Dr Pali Chandra", "Kathak", "assets/images/guru-pali.jpg", "24"),
        ("Dr Neena Prasad", "Mohiniyattam", "assets/images/neena-prasadneena-prasad-mohiniyattam-dancer.webp", "20"),
        ("Dr Rajashree Warrier", "Bharatanatyam", "assets/images/rajashree-warrier.webp", "20"),
        ("Dr Deepti Omchery Bhalla", "Mohiniyattam", "assets/images/dr-deepti-omchery-bhalladeepthi-omchery-bhalla1.webp", "20"),
        ("Pallavi Krishnan", "Mohiniyattam", "assets/images/mohiniyattam.webp", "18"),
        ("Madhavi Mudgal", "Odissi", "assets/images/madhavi-mudgalmadhavi-mudgal_odissi.webp", "16"),
        ("Gopi Kalamandalam", "Kathakali", "assets/images/gopi-kalamandalam.webp", "18"),
    ]
    slides = "".join(index_masters_guru_slide(name, form, img, count) for name, form, img, count in gurus)
    return (
        f'<section class="py-24 bg-white dance-forms-guru-section"><div class="container-custom">'
        f'<div class="text-center mb-16 max-w-3xl mx-auto">'
        f'<h2 class="section-title mb-4">Learn From The Best <br> Anywhere In The World</h2>'
        f'<p class="text-gray-500 text-sm md:text-base font-sans leading-relaxed">'
        f'Meet the revered masters and renowned performers curating <br> and creating classes in different disciplines</p>'
        f'</div>'
        f'<div data-carousel data-per-view=\'{{"default":1,"sm":2,"md":3,"lg":4}}\' data-step="1">'
        f'<div class="flex items-center justify-end mb-8 gap-4">'
        f'<div class="flex items-center gap-2 shrink-0">'
        f'<button type="button" data-carousel-prev class="carousel-nav-btn" aria-label="Previous gurus">{CAROUSEL_PREV_SVG}</button>'
        f'<button type="button" data-carousel-next class="carousel-nav-btn" aria-label="Next gurus">{CAROUSEL_NEXT_SVG}</button>'
        f'</div></div>'
        f'<div class="carousel-viewport -mx-2 sm:-mx-6"><div class="carousel-track px-2 sm:px-3">{slides}</div></div>'
        f'</div></div></section>'
    )

def dance_form_detail_hero():
    return (
        f'<section class="page-dance-form-detail-hero"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Dance forms", "dance-form-listing-page.html"), ("Bharatanatyam", None)])}'
        f'<div class="page-dance-form-detail-hero-grid"><div class="page-dance-form-detail-hero-text">'
        f'<h1>Bharatanatyam</h1>'
        f'<p>One of the oldest classical dance forms of India, Bharatanatyam blends geometric footwork, expressive abhinaya and rhythmic precision. Explore repertoire, history and pedagogy through curated classes from revered gurus.</p>'
        f'<div class="page-dance-form-stats"><span>702 Videos</span><span>45 Audios</span><span>40 Years</span></div>'
        f'<div class="page-dance-form-detail-actions">'
        f'<a href="class-listing-page.html" class="btn-primary">Start Learning</a>'
        f'<button type="button" class="btn-pink-outline">Join Now</button>'
        f'</div></div>'
        f'<figure class="page-dance-form-detail-hero-image"><img src="assets/images/bharatanatyam.webp" alt="Bharatanatyam dancer"></figure>'
        f'</div></div></section>'
    )

def dance_form_quote_section():
    return (
        '<section class="page-quote-section page-guru-quote page-dance-form-quote"><div class="container-custom">'
        '<span class="page-quote-mark page-quote-mark--open" aria-hidden="true">&ldquo;</span>'
        '<blockquote>Kathak is a prayer in motion. From the delicate mudras to the ecstatic chakras (spins), it\'s a path to connect the mortal self with the divine.</blockquote>'
        '<span class="page-quote-mark page-quote-mark--close" aria-hidden="true">&rdquo;</span>'
        '</div></section>'
    )

def dance_form_about_section():
    return (
        '<section class="page-section page-dance-form-about page-guru-about-section"><div class="container-custom page-guru-detail-grid">'
        '<div><div data-accordion class="page-accordion page-guru-accordion">'
        '<article class="is-open"><button data-accordion-trigger><span>History of Bharatanatyam</span>'
        '<em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Developed from temple and court traditions of Tamil Nadu, Bharatanatyam evolved as a sacred art of devotion and storytelling. Sculptural poses, rhythmic adavus and abhinaya became the foundation of a form practiced across generations.</p></div></article>'
        '<article><button data-accordion-trigger><span>Style of Bharatanatyam</span>'
        '<em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Defined by geometry, storytelling and rhythmic precision, the style balances nritta (pure dance), nritya (expressive dance) and natya (dramatic narrative) within a disciplined repertoire.</p></div></article>'
        '<article><button data-accordion-trigger><span>Bharatanatyam Today</span>'
        '<em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Practiced globally in traditional and contemporary formats, Bharatanatyam continues to inspire performers, teachers and students through stage, pedagogy and digital learning.</p></div></article>'
        '</div></div>'
        '<figure class="page-dance-form-about-image"><img src="assets/images/bharatanatyam1.jpg" alt="Bharatanatyam dancers in performance"></figure>'
        '</div></section>'
    )

def dance_form_classes_section():
    cards_data = [
        ("Angika", "Dr Rajasree Warrier", "Bharatanatyam", "assets/images/angika.webp"),
        ("Cholkettu", "Neena Prasad", "Bharatanatyam", "assets/images/cholkettu.webp"),
        ("Mangalacharan", "Madhavi Mudgal", "Bharatanatyam", "assets/images/mangalacharan1.webp"),
        ("Thumri Expressions", "Guru Dr Pali Chandra", "Bharatanatyam", "assets/images/thumri.webp"),
        ("Payaliya Tarana", "Guru Dr Pali Chandra", "Bharatanatyam", "assets/images/pali-chandra.webp"),
        ("Kuchipudi Basics", "Rajashree Warrier", "Bharatanatyam", "assets/images/kuchipudi.webp"),
    ]
    cards_html = "".join(
        guru_premium_class_card(t, g, f, i, f.lower().replace(" ", "_"))
        for t, g, f, i in cards_data
    )
    return (
        f'<section class="page-section dance-form-classes-section"><div class="container-custom">'
        f'<div class="page-listing-section-head"><h2 class="section-title">Bharatanatyam Classes</h2>'
        f'<p>Form-specific classes curated for learners at every stage.</p></div>'
        f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">{cards_html}</div>'
        f'<div class="page-section-actions page-section-actions--center"><a href="class-listing-page.html" class="btn-pink-outline">View Classes</a></div>'
        f'</div></section>'
    )

FREE_VIDEO_ARCHIVES = [
    ("Kathakali", "assets/images/free-lesson/free-lesson-01.jpg"),
    ("Satriya", "assets/images/free-lesson/free-lesson-02.jpg"),
    ("Ottan Thullal", "assets/images/free-lesson/free-lesson-03.jpg"),
    ("Kutiyattam", "assets/images/free-lesson/free-lesson-04.jpg"),
]

def free_video_overlay_card(title, img, href="free-video-detail-page.html"):
    return (
        f'<a href="{href}" class="free-video-archive-card group block relative rounded-2xl overflow-hidden zoom-img-container '
        f'focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-pink focus-visible:ring-offset-2">'
        f'<img src="{img}" alt="{title}" class="w-full h-full object-cover">'
        f'<div class="absolute inset-0 archive-card-overlay"></div>'
        f'<div class="absolute bottom-0 left-0 right-0 p-5 md:p-6 text-white">'
        f'<h3 class="text-lg md:text-xl font-bold font-serif mb-1">{title}</h3>'
        f'<span class="text-sm font-semibold font-sans text-white/90 group-hover:text-white inline-flex items-center gap-1 transition-colors">'
        f'Explore <span aria-hidden="true">→</span></span></div></a>'
    )

def free_video_listing_top():
    return (
        f'<section class="free-video-listing-top"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Free Videos", None)])}'
        f'<h1 class="free-video-listing-title">Performances from Our Archives</h1>'
        f'</div></section>'
    )

def free_video_archives_carousel_section():
    slides = "".join(
        f'<div class="carousel-slide px-2 sm:px-3">{free_video_overlay_card(title, img)}</div>'
        for title, img in FREE_VIDEO_ARCHIVES
    )
    return (
        f'<section class="py-16 md:py-20 bg-white free-video-archives-carousel" aria-labelledby="free-video-archives-heading">'
        f'<div class="container-custom">'
        f'<div class="text-center mb-8 md:mb-10 max-w-3xl mx-auto">'
        f'<h2 id="free-video-archives-heading" class="section-title mb-3">'
        f'Performances from Our Archives</h2>'
        f'<p class="text-gray-500 text-sm md:text-base font-sans">Rare recordings preserving the beauty, history, and legacy of Indian classical dance.</p>'
        f'</div>'
        f'<div data-carousel data-per-view=\'{{"default":1,"sm":2,"md":3,"lg":4}}\' data-step="1">'
        f'<div class="flex items-center justify-end gap-2 mb-6 md:mb-8">'
        f'<button type="button" data-carousel-prev class="carousel-nav-btn" aria-label="Previous archives">{CAROUSEL_PREV_SVG}</button>'
        f'<button type="button" data-carousel-next class="carousel-nav-btn" aria-label="Next archives">{CAROUSEL_NEXT_SVG}</button>'
        f'</div>'
        f'<div class="carousel-viewport -mx-2 sm:-mx-6"><div class="carousel-track px-2 sm:px-3">{slides}</div></div>'
        f'</div></div></section>'
    )

def free_video_detail_player(youtube_src: str, title: str) -> str:
    return (
        f'<div class="page-free-video-detail-player" data-free-video-player data-course-id="bharatanatyam-free-video">'
        f'<div class="page-free-video-detail-video-stage">'
        f'<iframe data-free-video-iframe src="{youtube_src}" title="{title}" loading="lazy" '
        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
        f'</div></div>'
    )

def free_video_playlist_item(
    index: int,
    title: str,
    artist: str,
    description: str,
    img: str,
    youtube_src: str,
    active: bool = False,
) -> str:
    active_cls = " is-active" if active else ""
    return (
        f'<button type="button" class="page-free-video-playlist-item{active_cls}" data-video-index="{index}"'
        f' data-youtube-src="{youtube_src}" data-video-title="{title}">'
        f'<div class="page-free-video-playlist-copy">'
        f'<strong>{title}</strong>'
        f'<em class="page-free-video-playlist-artist">{artist}</em>'
        f'<span class="page-free-video-playlist-desc">{description}</span>'
        f'</div>'
        f'<img src="{img}" alt="{title}">'
        f'</button>'
    )

def free_video_detail_hero():
    youtube_src = "https://www.youtube.com/embed/h7TNtO-WitU?rel=0&amp;modestbranding=1&amp;playsinline=1"
    poster = "assets/images/bharatanatyam.webp"
    playlist = [
        (
            "Traditional Bharatanatyam",
            "Anita Ratnam",
            "Anita Ratnam, Founder of Arangham, is a celebrated Bharatanatyam dancer and choreographer.",
            poster,
            youtube_src,
        ),
        (
            "Bharatanatyam - A poem in motion",
            "Anita Ratnam",
            "A lyrical excerpt exploring abhinaya, geometry and rhythmic storytelling in Bharatanatyam.",
            "assets/images/video-01.jpg",
            youtube_src,
        ),
        (
            "Bharatanatyam - A poem in motion",
            "Anita Ratnam",
            "Archive footage capturing stage presence, lasya and devotional expression.",
            "assets/images/video-02.jpg",
            youtube_src,
        ),
    ]
    playlist_btns = "".join(
        free_video_playlist_item(i, title, artist, desc, img, ysrc, active=(i == 0))
        for i, (title, artist, desc, img, ysrc) in enumerate(playlist)
    )
    compositions = [
        "Ambika Pallavi",
        "Nadaloludhunam - Krishnaveni Lakshman",
        "Cholkettu - Lalita Srinivasan",
        "Oubavai Vilayattu - Smitha Rajan",
        "Swagatham - Chandrika Shar",
        "ABHINAYA - Expressions in Dance - Guru Anita Rathan",
        "Thillana - Guru Anita Rathan",
    ]
    comp_list = "".join(f"<li>{item}</li>" for item in compositions)
    player = free_video_detail_player(youtube_src, "Traditional Bharatanatyam")
    return (
        f'<section class="page-free-video-detail-top"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Free Videos", "free-video-page.html"), ("Bharatanatyam", None)])}'
        f'<h1 class="page-free-video-detail-title">Bharatanatyam Free Video</h1>'
        f'</div></section>'
        f'<section class="page-free-video-detail-stage"><div class="container-custom">'
        f'<div class="page-free-video-detail-grid">'
        f'<div class="page-free-video-detail-main">'
        f'{player}'
        f'<div class="page-free-video-detail-copy">'
        f'<p>Bharatanatyam is one of the oldest classical dance traditions of India, celebrated for its sculptural geometry, expressive abhinaya, and rhythmic precision. This archive recording captures repertoire and performance elements for learners and rasikas alike.</p>'
        f'<p>Anita Ratnam, Founder of Arangham, is a celebrated Bharatanatyam dancer and choreographer. Her work bridges traditional repertoire with contemporary stagecraft, making classical dance accessible to global audiences.</p>'
        f'<p class="page-free-video-subtitles"><strong>Subtitles :</strong> English</p>'
        f'<div class="page-free-video-compositions"><h2 class="section-title">Compositions</h2><ol>{comp_list}</ol></div>'
        f'</div></div>'
        f'<aside class="page-free-video-detail-playlist" data-free-video-playlist>'
        f'<button type="button" class="page-free-video-playlist-nav" data-free-video-playlist-prev aria-label="Previous videos"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/></svg></button>'
        f'<div class="page-free-video-playlist-viewport" data-free-video-playlist-viewport><div class="page-free-video-playlist-track" data-video-thumbs>{playlist_btns}</div></div>'
        f'<button type="button" class="page-free-video-playlist-nav" data-free-video-playlist-next aria-label="Next videos"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg></button>'
        f'</aside>'
        f'</div></div></section>'
    )

def archive_card(title, img, href="free-video-detail-page.html"):
    return f'<article class="page-archive-card"><img src="{img}" alt="{title}"><div><h3>{title}</h3><a href="{href}" class="page-link-arrow">Explore →</a></div></article>'

def pagination():
    return '<nav data-pagination class="page-pagination"><button data-page="1" class="is-active">1</button><button data-page="2">2</button><button data-page="3">3</button><button data-page="4">4</button><button data-page-next>Next</button></nav>'

def cards_html(count=6, compact=False, overlay_first=False, first_primary=False, href="class-detail-page.html"):
    d = [("Payaliya Tarana", "Guru Dr Pali Chandra", "Kathak", "assets/images/pali-chandra.webp", "Master Class"),("Angika Essentials", "Smitha Rajan", "Bharatanatyam", "assets/images/angika.webp", "Beginners"),("Cholkettu Repertoire", "Neena Prasad", "Mohiniyattam", "assets/images/cholkettu.webp", "Intermediate"),("Thumri Expressions", "Guru Dr Pali Chandra", "Kathak", "assets/images/thumri.webp", "Master Class"),("Mangalacharan Series", "Madhavi Mudgal", "Odissi", "assets/images/mangalacharan1.webp", "Intermediate"),("Kuchipudi Basics", "Rajashree Warrier", "Kuchipudi", "assets/images/kuchipudi.webp", "Beginners")]
    return "".join(featured_class_card(t,g,f,i,href,l,first_primary and idx==0,compact,overlay_first and idx==0) for idx, (t,g,f,i,l) in enumerate(d[:count]))

def gita_govinda_highlight():
    return '<section class="gita-govinda-highlight relative overflow-hidden text-white"><div class="container-custom"><div class="flex flex-col lg:flex-row"><div class="lg:w-[42%] py-14"><figure class="mb-6"><img src="assets/images/logo-gita-govinda.webp" alt="Logo" class="w-full max-w-[320px]"></figure><p class="text-[#C5A059] text-sm">The eternal story of Keli, Viraha and Samyoga</p><p id="gita-govinda-heading" class="text-lg font-bold mt-2">Guru Dr Pali Chandra</p><ul class="flex flex-wrap gap-2 text-sm mt-4"><li>24 classes</li><li>|</li><li>600 videos</li><li>|</li><li>50 hours</li><li>|</li><li>24 audios</li></ul><p class="text-2xl font-bold mt-4">Timeless Classic Recrafted</p><button type="button" class="gg-highlight-btn mt-5">Explore Gita Govinda</button></div><div class="lg:w-[58%]"><img src="assets/images/gita-govinda.webp" alt="Gita Govinda" class="w-full h-full object-contain"></div></div></div></section>'

def page_class_listing():
    top = f'<section class="page-listing-top"><div class="container-custom">{breadcrumb([("Home", "index.html"), ("All Classes", None)])}</div></section>'
    return "\n".join([
        top,
        filter_bar(listing=True),
        listing_class_section("Latest Classes", "Newly added curriculum and compositions.", listing_cards_html(first_primary=True)),
        listing_class_section("Popular Classes", "Most enrolled classes this month.", listing_cards_html(first_primary=True)),
        listing_class_section("Top Rated Classes", "Highest reviewed classes from learners.", listing_cards_html(first_primary=True)),
    ])

def page_class_detail():
    breadcrumb_only = f'<section class="page-listing-top"><div class="container-custom">{breadcrumb([("Home", "index.html"), ("Kathak Courses", "class-listing-page.html"), ("Payaliya Tarana", None)])}</div></section>'
    all_classes = detail_all_classes_section()
    top = class_detail_top_section("Payaliya Tarana", "Guru Dr Pali Chandra", "Kathak", "7000", "assets/images/pali-01.jpg")
    return "\n".join([breadcrumb_only, top, all_classes, guru_detail_learning_paths_section(), reviews_section(), student_stories_section()])

def page_guru_listing():
    legendary = [
        ("Madhavi Mudgal", "Odissi", "assets/images/madhavi-mudgalmadhavi-mudgal_odissi.webp", "20"),
        ("Kalamandalam Gopi", "Kathakali", "assets/images/gopi-kalamandalam.webp", "20"),
        ("Rama Vaidyanathan", "Bharatanatyam", "assets/images/ramavaidyanathan.webp", "20"),
    ]
    masters = [
        ("Rama Vaidyanathan", "Bharatanatyam", "assets/images/ramavaidyanathan.webp", "20"),
        ("Guru Dr Pali Chandra", "Kathak", "assets/images/guru-pali.jpg", "24"),
        ("Dr Neena Prasad", "Mohiniyattam", "assets/images/neena-prasadneena-prasad-mohiniyattam-dancer.webp", "20"),
        ("Dr Rajashree Warrier", "Bharatanatyam", "assets/images/rajashree-warrier.webp", "20"),
        ("Dr Deepti Omchery Bhalla", "Mohiniyattam", "assets/images/dr-deepti-omchery-bhalladeepthi-omchery-bhalla1.webp", "20"),
        ("Pallavi Krishnan", "Mohiniyattam", "assets/images/mohiniyattam.webp", "20"),
        ("Gopi Kalamandalam", "Kathakali", "assets/images/gopi-kalamandalam.webp", "18"),
        ("Madhavi Mudgal", "Odissi", "assets/images/madhavi-mudgalmadhavi-mudgal_odissi.webp", "16"),
    ]
    featured = [
        ("Neena Prasad", "Mohiniyattam", "assets/images/neena-prasadneena-prasad-mohiniyattam-dancer.webp", "19"),
        ("Madhavi Mudgal", "Odissi", "assets/images/madhavi-mudgalmadhavi-mudgal_odissi.webp", "16"),
        ("Gopi Kalamandalam", "Mohiniyattam", "assets/images/gopi-kalamandalam.webp", "18"),
        ("Guru Dr Pali Chandra", "Kathak", "assets/images/pali-01.jpg", "24"),
    ]
    hero = (
        f'<section class="page-guru-listing-hero"><div class="container-custom">{breadcrumb([("Home", "index.html"), ("Gurus", None)])}'
        f'<h1>Learn From The Best<br>Anywhere In The World</h1>'
        f'<p>Meet the revered masters and renowned performers curating and creating classes in different disciplines.</p>'
        f'</div></section>'
    )
    student_stories = section_from_marker(read_index(), "<!-- Section 8:")
    return "\n".join([
        hero,
        guru_grid_section("Legendary Gurus", legendary, "page-guru-grid--legendary", "large"),
        guru_grid_section("Meet the Masters", masters, "page-guru-grid--masters", "medium"),
        guru_grid_section("Featured Artists", featured, "page-guru-grid--featured", "medium"),
        popular_classes_section(section_id="guru-listing-popular-classes", centered=False),
        student_stories,
    ])

def page_guru_detail():
    hero = (
        f'<section class="page-guru-detail-hero"><div class="container-custom">{breadcrumb([("Home", "index.html"), ("About", "guru-listing-page.html"), ("Dr Pali Chandra", None)])}'
        f'<div class="page-guru-detail-hero-grid"><div class="page-guru-detail-hero-text">'
        f'<h1>Guru Dr Pali Chandra</h1>'
        f'<p>A world-renowned Kathak exponent whose choreography, research and performance have introduced generations of dancers to the depth, grace and storytelling power of the form.</p>'
        f'<button type="button" class="btn-primary">Start Learning</button></div>'
        f'<figure class="page-guru-detail-hero-image"><img src="assets/images/pali-01.jpg" alt="Guru Dr Pali Chandra with students"></figure>'
        f'</div></div></section>'
    )
    quote = (
        '<section class="page-quote-section page-guru-quote"><div class="container-custom">'
        '<span class="page-quote-mark page-quote-mark--open" aria-hidden="true">&ldquo;</span>'
        '<blockquote>Kathak is soul set in motion. From the delicate mudras to the ecstatic chakras (spins), it\'s a path to connect the mortal self with the divine.</blockquote>'
        '<span class="page-quote-mark page-quote-mark--close" aria-hidden="true">&rdquo;</span>'
        '</div></section>'
    )
    about = (
        '<section class="page-section page-guru-about-section"><div class="container-custom page-guru-detail-grid"><div>'
        '<div data-accordion class="page-accordion page-guru-accordion">'
        '<article class="is-open"><button data-accordion-trigger><span>About the Guru</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Globally acclaimed Kathak exponent, choreographer and educator with decades of stage, research and pedagogy. Her work bridges traditional parampara with contemporary performance and digital learning.</p></div></article>'
        '<article><button data-accordion-trigger><span>Journey in Europe</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Decades of teaching, residencies and performances across European institutions and festivals, bringing Kathak to international audiences.</p></div></article>'
        '<article><button data-accordion-trigger><span>Digital Journey</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Pioneering online Kathak pedagogy through structured compositions, annotated lessons and global student communities.</p></div></article>'
        '<article><button data-accordion-trigger><span>Gurukul, the Dance School</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Training generations of dancers through immersive repertoire, abhinaya and performance pathways.</p></div></article>'
        '<article><button data-accordion-trigger><span>Work and Awards</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>National recognitions, landmark choreographic works and collaborations across continents.</p></div></article>'
        '<article><button data-accordion-trigger><span>Bond with NatyasutraOnline</span><em class="page-accordion-icon" aria-hidden="true"></em></button>'
        '<div data-accordion-panel><p>Exclusive masterclasses and digital archives curated for learners worldwide through NatyasutraOnline.</p></div></article>'
        '</div></div><div class="page-gallery-stack">'
        '<img src="assets/images/pali-02.jpg" alt="Guru Dr Pali Chandra">'
        '<div class="page-gallery-stack-row"><img src="assets/images/pali-03.jpg" alt="Performance"><img src="assets/images/pali-chandra.webp" alt="Kathak pose"></div>'
        '</div></div></section>'
    )
    classes_section = guru_detail_classes_section()
    video_gallery = guru_detail_video_gallery_section()
    media_section = guru_detail_media_section()
    testimonials = section_from_marker(read_index(), "<!-- Section 8:")
    return "\n".join([hero, quote, about, classes_section, gita_govinda_highlight(), guru_detail_learning_paths_section(), video_gallery, media_section, testimonials])

def page_class_search():
    return "\n".join([page_hero("Search Results", "Showing 42 results for selected filters.", [("Home", "index.html"), ("All Classes", "class-listing-page.html"), ("Search Results", None)]), filter_bar(), class_grid_section("Search Results", "42 classes found", cards_html(compact=True, overlay_first=True), sort_label="Sort by: Relevance", view_all_btn=False), pagination()])

def page_programmes():
    return programmes_listing_section()

def beginners_listing_top() -> str:
    return (
        f'<section class="page-beginners-listing-top"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Programmes", "programmes-listing-page.html"), ("Beginners", None)])}'
        f'</div></section>'
    )

def beginners_courses_section() -> str:
    html = popular_classes_section(section_id="beginners-level-classes", centered=True)
    return (
        html.replace(
            "Explore Our Most <br>Popular Classes",
            "Beginners",
        ).replace(
            "Explore the lessons students, performers, teachers, and rasikas return to again and again.",
            "Curated beginner programmes designed to build strong foundations across classical dance forms.",
        )
    )

def beginners_student_stories_section() -> str:
    html = student_stories_section()
    return (
        html.replace(
            "Shared Stories Of Passion, <br> Dance And Performance",
            "Student Stories",
        ).replace(
            "Testimonials of our students' transformative journeys",
            "Hear from our community of dedicated learners",
        )
    )

def page_beginners():
    return "\n".join([
        beginners_listing_top(),
        filter_bar(title="Filter Courses", preview=True),
        beginners_courses_section(),
        beginners_student_stories_section(),
    ])
def page_dance_forms():
    forms = [
        ("Bharatanatyam", "Temple-born geometry of movement, abhinaya and rhythmic precision.", "assets/images/bharatanatyam.webp"),
        ("Kathak", "Spinning narratives through footwork, grace and expressive storytelling.", "assets/images/kathak.webp"),
        ("Mohiniyattam", "Lasya-rich movements evoking the enchantress of Kerala tradition.", "assets/images/mohiniyattam.webp"),
        ("Kuchipudi", "Dynamic drama and rhythm from the Andhra performance tradition.", "assets/images/kuchipudi.webp"),
        ("Odissi", "Tribhangi sculptural grace from the temples of Odisha.", "assets/images/odissi.webp"),
        ("Kathakali", "Vivid abhinaya and elaborate costuming from Kerala's theatre heritage.", "assets/images/gita-govinda.webp"),
    ]
    grid = (
        f'<section class="page-section page-dance-forms-grid-section"><div class="container-custom">'
        f'<div class="page-form-grid">{"".join(dance_form_card(n, d, i) for n, d, i in forms)}</div>'
        f'</div></section>'
    )
    return "\n".join([
        dance_forms_listing_top(),
        grid,
        popular_classes_section(section_id="dance-forms-popular-classes", centered=True),
        learn_from_best_section(),
        student_stories_section(),
    ])

def page_dance_form_detail():
    return "\n".join([
        dance_form_detail_hero(),
        dance_form_quote_section(),
        dance_form_about_section(),
        dance_form_classes_section(),
        learn_from_best_section(),
        student_stories_section(),
    ])

def page_latest_news():
    cards = "".join([news_card_horizontal("05 Jun 2026", "Natyasutra Summer Residency", "Immersive residency for advanced learners.", "assets/images/news-01.jpg", "latest-news-detail-page.html"), news_card_horizontal("29 May 2026", "Odissi Weekend Intensive", "Focused notation and stage training.", "assets/images/video-01.jpg", "latest-news-detail-page.html"), news_card_horizontal("20 May 2026", "Scholarship Announcements", "Merit-based access for students.", "assets/images/video-02.jpg", "latest-news-detail-page.html"), news_card_horizontal("08 May 2026", "Performance Calendar Updated", "Public showcases announced.", "assets/images/video-03.jpg", "latest-news-detail-page.html")])
    media = [f'<div class="carousel-slide px-2 sm:px-4">{media_card_horizontal("Media", "2026", f"Media Highlight {i}", "Coverage and interviews.", img)}</div>' for i, img in enumerate(["assets/images/video-01.jpg","assets/images/video-02.jpg","assets/images/video-03.jpg"], start=1)]
    return "\n".join([page_hero("News & Updates", "Latest announcements and highlights.", [("Home", "index.html"), ("Latest News", None)]), f'<section class="page-section"><div class="container-custom"><div class="page-news-stack">{cards}</div></div></section>', carousel_section("Media", media, per_view='{"default":1,"md":2}', dots=True, nav=True), class_grid_section("Popular Classes", "Most viewed classes this month.", cards_html(), view_all_btn=False)])

def page_latest_news_detail():
    article = '<section class="page-section"><div class="container-custom page-two-col-article"><article><p class="page-card-kicker">05 Jun 2026 • News</p><h1 class="page-section-title">Natyasutra Summer Residency Opens for 2026</h1><img src="assets/images/news-01.jpg"><figcaption>Residency orientation with live guru sessions.</figcaption><p>Residency combines technique, abhinaya, and stage discipline.</p><p>Students receive weekly evaluations and rehearsals.</p></article><aside class="page-side-card"><h3>Related updates</h3><a href="latest-news-detail-page.html">Scholarship Schedule</a><a href="latest-news-detail-page.html">Performance Calendar</a><a href="latest-news-detail-page.html">Masterclass Registration</a></aside></div></section>'
    news = [f'<div class="carousel-slide px-2 sm:px-4">{news_card_horizontal("2026", f"Related Story {i}", "Short update excerpt.", img, "latest-news-detail-page.html")}</div>' for i, img in enumerate(["assets/images/video-01.jpg","assets/images/video-02.jpg","assets/images/video-03.jpg"], start=1)]
    return "\n".join([article, carousel_section("News Carousel", news, per_view='{"default":1,"md":2,"lg":3}', dots=True, nav=True), class_grid_section("All Classes", "Continue learning with our full class catalogue.", cards_html(), view_all_btn=False)])

def page_media():
    cards = "".join([media_card_horizontal("The Hindu", "01 Jun 2026", "Heritage in Motion", "Interview transcript.", "assets/images/video-01.jpg"), media_card_horizontal("Indian Express", "20 May 2026", "Digital Classrooms", "Production notes.", "assets/images/video-02.jpg"), media_card_horizontal("NDTV", "08 May 2026", "Learning from Legends", "Feature clips.", "assets/images/video-03.jpg"), media_card_horizontal("Times", "25 Apr 2026", "Pedagogy at Scale", "Detailed coverage.", "assets/images/video-04.jpg")])
    return "\n".join([page_hero("Media", "Press coverage, interviews and long-form features.", [("Home", "index.html"), ("Media", None)]), f'<section class="page-section"><div class="container-custom"><div class="page-news-stack">{cards}</div></div></section>', class_grid_section("Popular Classes", "Top learner picks this week.", cards_html(), view_all_btn=False)])

def page_photo_gallery():
    albums = "".join(photo_album_card(title, img, href) for title, img, href in PHOTO_GALLERY_ALBUMS)
    return "\n".join([
        gallery_page_top("Photo Gallery", PHOTO_GALLERY_CRUMBS),
        f'<section class="page-section page-photo-gallery-section"><div class="container-custom">'
        f'<div class="page-photo-gallery-grid">{albums}</div></div></section>',
    ])

def page_mudra_listing():
    cards = "".join(mudra_grid_card(title, img) for title, img in ASAMYUTA_MUDRAS)
    feature_slides = [
        f'<div class="carousel-slide px-2 sm:px-4">{photo_album_card(title, img, href, feature=True)}</div>'
        for title, img, href in MUDRA_PHOTO_FEATURE_ALBUMS
    ]
    return "\n".join([
        gallery_page_top("Asamyuta Hasta Mudras", PHOTO_GALLERY_CRUMBS),
        f'<section class="page-section page-mudra-listing-section"><div class="container-custom">'
        f'<div class="page-mudra-grid">{cards}</div></div></section>',
        carousel_section(
            "Photo Gallery",
            feature_slides,
            per_view='{"default":1,"md":2}',
            dots=False,
            nav=True,
        ),
    ])

def page_mudra_detail():
    related = [
        f'<div class="carousel-slide px-2 sm:px-4">{mudra_grid_card(title, img, href)}</div>'
        for title, img, href in MUDRA_DETAIL_RELATED
    ]
    photos = [
        f'<div class="carousel-slide px-2 sm:px-4">{photo_album_card(title, img, href, feature=True)}</div>'
        for title, img, href in MUDRA_DETAIL_PHOTO_ALBUMS
    ]
    hero = (
        f'<section class="page-mudra-detail-hero"><div class="container-custom">'
        f'{breadcrumb(PHOTO_GALLERY_CRUMBS)}'
        f'<h1 class="page-gallery-title">Pataka</h1>'
        f'<figure class="page-mudra-detail-figure">'
        f'<img src="assets/images/01_Pataka.jpg" alt="Pataka mudra"></figure>'
        f'<div class="page-mudra-detail-copy">{PATAKA_MUDRA_DESCRIPTION}</div>'
        f'</div></section>'
    )
    return "\n".join([
        hero,
        carousel_section(
            "Asamyuta Hasta Mudras",
            related,
            per_view='{"default":1,"sm":2,"md":3}',
            dots=False,
            nav=True,
        ),
        carousel_section(
            "Photo Gallery",
            photos,
            per_view='{"default":1,"md":2}',
            dots=False,
            nav=True,
        ),
    ])
def page_free_video():
    cards = "".join(free_video_overlay_card(title, img) for title, img in FREE_VIDEO_ARCHIVES * 4)
    return "\n".join([
        free_video_listing_top(),
        f'<section class="page-section free-video-archive-section"><div class="container-custom">'
        f'<div class="free-video-archive-grid">{cards}</div></div></section>',
    ])

def page_free_video_detail():
    return "\n".join([
        free_video_detail_hero(),
        free_video_archives_carousel_section(),
        popular_classes_section(section_id="free-video-popular-classes", centered=True),
    ])

PREVIEW_VIDEO_ITEMS = [
    ("Virachita Chaadu Vachana", "Guru Dr Pali Chandra", "assets/images/pali-chandra.webp"),
    ("Moksha Prabandham", "Guru Dr Pali Chandra", "assets/images/cholkettu.webp"),
    ("Kuchipudi beginners", "Sreelakshmy Govardhanan", "assets/images/kuchipudi.webp"),
    ("Adavus Pushpanjali", "Guru Dr Pali Chandra", "assets/images/kathak.webp"),
    ("Kathak fundamentals", "Guru Dr Pali Chandra", "assets/images/pali-chandra.webp"),
    ("Drishti Bhedas", "Guru Dr Pali Chandra", "assets/images/angika.webp"),
    ("Alarippu Study", "Dr Rajasree Warrier", "assets/images/angika.webp"),
    ("Cholkettu Basics", "Neena Prasad", "assets/images/cholkettu.webp"),
    ("Mangalacharan", "Madhavi Mudgal", "assets/images/odissi.webp"),
    ("Tarana in Yaman", "Guru Dr Pali Chandra", "assets/images/kathak.webp"),
    ("Pushpanjali", "Smitha Rajan", "assets/images/angika.webp"),
    ("Batu Sequence", "Madhavi Mudgal", "assets/images/odissi.webp"),
]

PREVIEW_CLIP_ITEMS = [
    ("Virachita Chaadu Vachana", "Guru Dr Pali Chandra", "assets/images/pali-chandra.webp"),
    ("Moksha Prabandham", "Guru Dr Pali Chandra", "assets/images/cholkettu.webp"),
    ("Kuchipudi beginners", "Sreelakshmy Govardhanan", "assets/images/kuchipudi.webp"),
    ("Adavus Pushpanjali", "Guru Dr Pali Chandra", "assets/images/kathak.webp"),
    ("Kathak fundamentals", "Guru Dr Pali Chandra", "assets/images/pali-chandra.webp"),
    ("Drishti Bhedas", "Guru Dr Pali Chandra", "assets/images/angika.webp"),
]

PREVIEW_MEDIA_PLAY = (
    '<span class="page-preview-media-play" aria-hidden="true">'
    '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>'
)

def preview_media_card(title: str, guru: str, img: str, href: str = "preview-video-detail-page.html") -> str:
    return (
        f'<article class="page-preview-media-card">'
        f'<a href="{href}" class="page-preview-media-thumb">'
        f'<img src="{img}" alt="{title}">{PREVIEW_MEDIA_PLAY}</a>'
        f'<div class="page-preview-media-foot">'
        f'<div class="page-preview-media-copy">'
        f'<h3>{title}</h3>'
        f'<p class="page-preview-media-guru">{guru}</p>'
        f'</div>'
        f'<a href="{href}" class="page-preview-media-btn">Preview</a>'
        f'</div></article>'
    )

def preview_video_listing_top() -> str:
    return (
        f'<section class="page-preview-video-listing-top"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Beginners", "beginners-level-listing.html"), ("Previews", None)])}'
        f'<div class="page-preview-video-listing-hero">'
        f'<h1 class="page-preview-video-listing-title">Explore Before You Begin</h1>'
        f'<p class="page-preview-video-listing-intro">Discover free lessons, class previews, and exclusive trailers that help you experience each dance form, teaching style and curriculum before you commit to a full course.</p>'
        f'</div></div></section>'
    )

PREVIEW_DETAIL_PLAYLIST = [
    ("Nada", "Kuchipudi Beginners Lessons", "Sreelakshmy Govardhanan", "assets/images/kuchipudi.webp"),
    ("Kartharinattu Adavu", "Beginners Foundation", "Sreelakshmy Govardhanan", "assets/images/video-01.jpg"),
    ("Pada Bhedas", "Technique Study", "Sreelakshmy Govardhanan", "assets/images/video-02.jpg"),
    ("Adavu Patterns", "Rhythm Training", "Sreelakshmy Govardhanan", "assets/images/video-03.jpg"),
    ("Abhinaya Intro", "Expression Basics", "Sreelakshmy Govardhanan", "assets/images/pali-02.jpg"),
]

def preview_video_detail_stage(poster_img: str, video_src: str | None = None) -> str:
    src = video_src or "assets/videos/banner.mp4"
    thumb_btns = "".join(
        f'<button type="button" class="page-preview-detail-thumb{" is-active" if i == 0 else ""}"'
        f' data-video-index="{i}" data-video-src="{src}" data-video-poster="{img}" data-video-title="{title}">'
        f'<img src="{img}" alt="{title}">'
        f'<span class="page-preview-detail-thumb-copy">'
        f'<strong>{title}</strong><em>{subtitle}</em><small>{guru}</small></span></button>'
        for i, (title, subtitle, guru, img) in enumerate(PREVIEW_DETAIL_PLAYLIST)
    )
    return (
        f'<section class="page-preview-detail-stage"><div class="container-custom">'
        f'<div class="page-preview-detail-player-wrap">'
        f'<div class="page-preview-detail-player" data-class-detail-player data-course-id="kuchipudi-beginners-preview">'
        f'<div class="page-preview-detail-video-stage">'
        f'<video poster="{poster_img}" playsinline><source src="{src}" type="video/mp4"></video>'
        f'<div class="page-preview-detail-brand" aria-hidden="true">'
        f'<img src="assets/images/natyasutra-logo-white.png" alt="">'
        f'<p>Learn Art &amp; Culture from the Masters</p></div>'
        f'<div class="page-preview-detail-video-label" aria-hidden="true">'
        f'<span class="page-preview-detail-video-kicker">Nada</span>'
        f'<strong>Kuchipudi Beginners Lessons</strong>'
        f'<em>Sreelakshmy Govardhanan</em></div>'
        f'<button type="button" class="page-preview-detail-play-overlay" data-video-play aria-label="Play video">'
        f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></button>'
        f'<div class="page-preview-detail-overlay">'
        f'<div class="page-preview-detail-progress-row">'
        f'<span class="page-preview-detail-time-current" data-video-time-current>12:45</span>'
        f'<div class="page-preview-detail-progress-track" data-video-progress>'
        f'<span class="page-preview-detail-progress-fill" data-video-progress-fill style="width:35%"></span></div>'
        f'<span class="page-preview-detail-time-total" data-video-time-total>36:20</span></div>'
        f'<div class="page-preview-detail-controls">'
        f'<div class="page-preview-detail-controls-left">'
        f'<button type="button" class="page-preview-detail-ctrl" data-video-prev aria-label="Previous video">'
        f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6V6zm3.5 6l8.5 6V6l-8.5 6z"/></svg></button>'
        f'<button type="button" class="page-preview-detail-ctrl" data-video-play aria-label="Play">'
        f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></button>'
        f'<button type="button" class="page-preview-detail-ctrl" data-video-next aria-label="Next video">'
        f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16 18h2V6h-2v12zM6 18l8.5-6L6 6v12z"/></svg></button>'
        f'<button type="button" class="page-preview-detail-ctrl" data-video-mute aria-label="Mute">'
        f'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/></svg></button>'
        f'<span class="page-preview-detail-complete" data-course-progress-label>35% complete</span></div>'
        f'<div class="page-preview-detail-controls-right">'
        f'<button type="button" class="page-preview-detail-ctrl" aria-label="Settings">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg></button>'
        f'<button type="button" class="page-preview-detail-ctrl page-preview-detail-speed" aria-label="Playback speed">1x</button>'
        f'<button type="button" class="page-preview-detail-ctrl" aria-label="Bookmark">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg></button>'
        f'<button type="button" class="page-preview-detail-ctrl" data-video-fullscreen aria-label="Fullscreen">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5"/></svg></button>'
        f'</div></div></div></div></div>'
        f'<div class="page-preview-detail-playlist-wrap" data-preview-thumbnail-carousel>'
        f'<button type="button" class="page-preview-detail-playlist-prev" data-preview-playlist-prev aria-label="Scroll playlist back">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg></button>'
        f'<div class="page-preview-detail-playlist" data-video-thumbs>{thumb_btns}</div>'
        f'<button type="button" class="page-preview-detail-playlist-next" data-preview-playlist-next aria-label="Scroll playlist">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg></button>'
        f'</div>'
        f'<div class="page-preview-detail-cta">'
        f'<h2 class="section-title">A True E-learning Experience Awaits</h2>'
        f'<p>Step into structured lessons with expert gurus, cinematic video quality and guided milestones that take you from first adavus to confident performance.</p>'
        f'<a href="class-detail-page.html" class="btn-primary">Start Learning</a>'
        f'</div></div></div></section>'
    )

def preview_video_detail_intro() -> str:
    return (
        f'<section class="page-preview-detail-intro"><div class="container-custom">'
        f'{breadcrumb([("Home", "index.html"), ("Beginners", "beginners-level-listing.html"), ("Kuchipudi", None)])}'
        f'<h1 class="page-preview-detail-title">Kuchipudi Beginners Preview Videos</h1>'
        f'<p class="page-preview-detail-sub">Preview Classes by <strong>Sreelakshmy Govardhanan</strong></p>'
        f'</div></section>'
    )

def preview_video_detail_hero() -> str:
    return "\n".join([
        preview_video_detail_intro(),
        preview_video_detail_stage("assets/images/kuchipudi.webp"),
    ])

def preview_video_clips_section() -> str:
    clips = "".join(
        preview_media_card(title, guru, img)
        for title, guru, img in PREVIEW_CLIP_ITEMS
    )
    return (
        f'<section class="page-section page-preview-clips-section"><div class="container-custom">'
        f'<h2 class="section-title page-preview-clips-heading">Preview</h2>'
        f'<div class="page-preview-media-grid">{clips}</div>'
        f'<div class="page-section-actions page-section-actions--center">'
        f'<a href="preview-video-page.html" class="btn-pink-outline">View Previews</a></div>'
        f'</div></section>'
    )

def preview_video_all_classes_section() -> str:
    cards_data = [
        ("Kuchipudi beginners lessons", "Sreelakshmy Govardhanan", "Kuchipudi", "assets/images/kuchipudi.webp", "technique", "2 hrs", "34 Lessons"),
        ("Cholkettu repertoire", "Neena Prasad", "Mohiniyattam", "assets/images/cholkettu.webp", "composition", "2 hrs", "24 Lessons"),
        ("Angika essentials", "Dr Rajasree Warrier", "Bharatanatyam", "assets/images/angika.webp", "beginners", "2 hrs", "24 Lessons"),
        ("Payaliya tarana", "Guru Dr Pali Chandra", "Kathak", "assets/images/pali-chandra.webp", "master_class", "2 hrs", "24 Lessons"),
        ("Mangalacharan series", "Madhavi Mudgal", "Odissi", "assets/images/mangalacharan1.webp", "intermediate", "2 hrs", "24 Lessons"),
        ("Thumri expressions", "Guru Dr Pali Chandra", "Kathak", "assets/images/thumri.webp", "composition", "2 hrs", "24 Lessons"),
    ]
    cards = "".join(
        guru_premium_class_card(title, guru, form, img, category, hours, lessons, primary_enroll=idx == 0)
        for idx, (title, guru, form, img, category, hours, lessons) in enumerate(cards_data)
    )
    return (
        f'<section class="page-section page-preview-all-classes"><div class="container-custom">'
        f'<div class="page-preview-section-head">'
        f'<div class="page-listing-section-head"><h2 class="section-title">All Classes</h2>'
        f'<p>Choose from our bouquet of curated courses.</p></div>'
        f'{sort_dropdown("All classes")}</div>'
        f'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">{cards}</div>'
        f'<div class="page-section-actions page-section-actions--center">'
        f'<a href="class-listing-page.html" class="btn-pink-outline">View Classes</a></div>'
        f'</div></section>'
    )

def page_preview_video():
    cards = "".join(preview_media_card(title, guru, img) for title, guru, img in PREVIEW_VIDEO_ITEMS)
    return "\n".join([
        preview_video_listing_top(),
        filter_bar(title="Filter Courses", preview=True),
        f'<section class="page-section page-preview-video-section"><div class="container-custom">'
        f'<div class="page-preview-media-grid">{cards}</div></div></section>',
        popular_classes_section(section_id="preview-video-popular-classes", centered=True),
    ])

def page_preview_video_detail():
    return "\n".join([
        preview_video_detail_hero(),
        preview_video_clips_section(),
        preview_video_all_classes_section(),
    ])

def page_video_listing():
    episodes = "".join(gallery_card(f"Episode {i}", IMAGES[i % len(IMAGES)], "video-gallery-detail-page.html") for i in range(1, 9))
    shorts = [f'<div class="carousel-slide px-2 sm:px-4">{archive_card(f"Short {i}", IMAGES[(i + 4) % len(IMAGES)], "video-gallery-detail-page.html")}</div>' for i in range(1, 6)]
    gallery = [f'<div class="carousel-slide px-2 sm:px-4">{archive_card(f"Gallery {i}", IMAGES[(i + 7) % len(IMAGES)], "video-gallery-detail-page.html")}</div>' for i in range(1, 6)]
    return "\n".join([page_hero("Video Listing", "Episodes, shorts and curated galleries.", [("Home", "index.html"), ("Video Listing", None)]), f'<section class="page-section"><div class="container-custom"><div class="page-gallery-grid">{episodes}</div></div></section>', carousel_section("Shorts Carousel", shorts, per_view='{"default":1,"sm":2,"md":3}', dots=True, nav=True), carousel_section("Gallery Carousel", gallery, per_view='{"default":1,"sm":2,"md":3}', dots=True, nav=True)])

def page_video_gallery():
    cards = "".join(gallery_card(n, i, "video-gallery-detail-page.html") for n, i in [("Performances", "assets/images/video-01.jpg"),("Workshops", "assets/images/video-02.jpg"),("Lecture Demos", "assets/images/video-03.jpg"),("Behind The Scenes", "assets/images/video-04.jpg"),("Festival Cuts", "assets/images/news-01.jpg"),("Special Archives", "assets/images/gita-govinda-banner.webp")])
    return "\n".join([page_hero("Video Gallery", "Category-wise watch lists and curated archives.", [("Home", "index.html"), ("Video Gallery", None)]), f'<section class="page-section"><div class="container-custom"><div class="page-gallery-grid">{cards}</div></div></section>'])

def page_video_gallery_detail():
    player = '<section class="page-video-hero"><div class="container-custom"><h1>Video Gallery Detail</h1><div class="page-video-player" data-video-player><video poster="assets/images/video-03.jpg"><source src="assets/videos/banner.mp4" type="video/mp4"></video><div class="page-video-controls"><button data-video-play>Play</button><div class="page-video-progress" data-video-progress><span data-video-progress-fill></span></div><span data-video-time>00:00 / 00:00</span><button data-video-mute>Mute</button><button data-video-fullscreen>Fullscreen</button></div></div><div class="page-video-pink-progress"></div><p class="page-video-description">Episode notes and context annotations.</p></div></section>'
    related = [f'<div class="carousel-slide px-2 sm:px-4">{archive_card(f"Related Video {i}", IMAGES[i % len(IMAGES)], "video-gallery-detail-page.html")}</div>' for i in range(1, 6)]
    shorts = [f'<div class="carousel-slide px-2 sm:px-4">{archive_card(f"Short Clip {i}", IMAGES[(i + 4) % len(IMAGES)], "video-gallery-detail-page.html")}</div>' for i in range(1, 6)]
    gallery = [f'<div class="carousel-slide px-2 sm:px-4">{archive_card(f"Gallery Clip {i}", IMAGES[(i + 7) % len(IMAGES)], "video-gallery-detail-page.html")}</div>' for i in range(1, 6)]
    return "\n".join([player, carousel_section("Related Videos", related, per_view='{"default":1,"sm":2,"md":3}', dots=True, nav=True), carousel_section("Shorts Carousel", shorts, per_view='{"default":1,"sm":2,"md":3}', dots=True, nav=True), carousel_section("Gallery Carousel", gallery, per_view='{"default":1,"sm":2,"md":3}', dots=True, nav=True)])

PAGE_BUILDERS = {
    "beginners-level-listing.html": ("Beginners Programmes | Natyasutra", "Beginner courses and curated programme pathways.", page_beginners),
    "class-detail-page.html": ("Class Detail | Natyasutra", "Class lesson plan, guru profile, and reviews.", page_class_detail),
    "class-listing-page.html": ("All Classes | Natyasutra", "Latest, popular, and top rated dance classes.", page_class_listing),
    "class-search-listing-page.html": ("Class Search Results | Natyasutra", "Filtered class results for your search.", page_class_search),
    "dance-form-detail-page.html": ("Dance Form Detail | Natyasutra", "Dive into Bharatanatyam history, style, and classes.", page_dance_form_detail),
    "dance-form-listing-page.html": ("Dance Forms | Natyasutra", "Explore all dance forms and related classes.", page_dance_forms),
    "free-video-detail-page.html": ("Free Video Detail | Natyasutra", "Watch archive recordings with guided context.", page_free_video_detail),
    "free-video-page.html": ("Free Videos | Natyasutra", "Performances from the dance archives.", page_free_video),
    "guru-detail-page.html": ("Guru Detail | Natyasutra", "Guru biography, classes, and media features.", page_guru_detail),
    "guru-listing-page.html": ("Guru Listing | Natyasutra", "Meet the gurus and featured artists.", page_guru_listing),
    "latest-news-detail-page.html": ("News Detail | Natyasutra", "Full article with related updates.", page_latest_news_detail),
    "latest-news.html": ("Latest News | Natyasutra", "News and updates from the academy.", page_latest_news),
    "media-page.html": ("Media | Natyasutra", "Press coverage and interviews.", page_media),
    "mudra-detail-page.html": ("Pataka Mudra | Natyasutra", "Pataka hasta mudra explanation with related references.", page_mudra_detail),
    "mudra-listing-page.html": ("Asamyuta Hasta Mudras | Natyasutra", "Asamyuta hasta mudras visual catalogue.", page_mudra_listing),
    "photo-gallery.html": ("Photo Gallery | Natyasutra", "Albums from classes and performances.", page_photo_gallery),
    "preview-video-detail-page.html": ("Preview Video Detail | Natyasutra", "Watch preview videos and start learning.", page_preview_video_detail),
    "preview-video-page.html": ("Preview Videos | Natyasutra", "Explore class previews before enrolling.", page_preview_video),
    "programmes-listing-page.html": ("Programmes | Natyasutra", "Structured courses for every learning stage.", page_programmes),
    "video-gallery-detail-page.html": ("Video Gallery Detail | Natyasutra", "Detailed player with related videos and shorts.", page_video_gallery_detail),
    "video-gallery-page.html": ("Video Gallery | Natyasutra", "Category-wise dance video collections.", page_video_gallery),
    "video-listing-page.html": ("Video Listing | Natyasutra", "Gita Govinda episodes, shorts, and gallery.", page_video_listing),
}

def normalize_section_headings(html: str) -> str:
    html = html.replace('h2 class="page-section-title"', 'h2 class="section-title"')
    html = re.sub(
        r'<h2 class="text-3xl md:text-\[2\.75rem\] font-extrabold text-gray-900 leading-tight font-serif mb-4">',
        '<h2 class="section-title mb-4">',
        html,
    )
    html = html.replace(
        '<h2>A True E-learning Experience Awaits</h2>',
        '<h2 class="section-title">A True E-learning Experience Awaits</h2>',
    )
    html = re.sub(
        r'(<div class="page-listing-section-head">)\s*<h2>',
        r'\1<h2 class="section-title">',
        html,
    )
    html = re.sub(
        r'(<div class="page-section-head">\s*<div>\s*)<h2>',
        r'\1<h2 class="section-title">',
        html,
    )
    return html

def render_page(head: str, body_tag: str, nav: str, page_content: str, cta: str, footer: str, extra_scripts: str = "") -> str:
    page_content = normalize_section_headings(page_content)
    cta = normalize_section_headings(cta)
    return (
        f"{head}{body_tag}\n"
        f"{nav}\n"
        '<main id="main-content">\n'
        f"{page_content}\n"
        f"{cta}\n"
        "</main>\n"
        f"{footer}\n"
        f"{extra_scripts}"
        '<script src="assets/js/popular-classes-filter.js"></script>\n'
        '<script src="assets/js/site-core.js"></script>\n'
        '<script src="assets/js/back-to-top.js" defer></script>\n'
        "</body>\n"
        "</html>\n"
    )

def main() -> None:
    index_html = read_index()
    parts = extract_parts(index_html)
    cta = update_cta_buttons(parts["cta"])
    footer = update_footer_links(parts["footer"])
    nav = update_nav_links(parts["nav"])
    created, errors = [], []
    for filename in OUTPUT_FILES:
        try:
            title, description, builder = PAGE_BUILDERS[filename]
            head = update_head(parts["before_body"], title, description)
            body_tag = parts["body_tag"]
            if filename == "class-detail-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white class-detail-page"')
            elif filename == "free-video-detail-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white free-video-detail-page"')
            elif filename == "programmes-listing-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white programmes-listing-page"')
            elif filename == "beginners-level-listing.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white beginners-level-listing-page"')
            elif filename == "preview-video-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white preview-video-page"')
            elif filename == "preview-video-detail-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white preview-video-detail-page"')
            elif filename == "photo-gallery.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white photo-gallery-page"')
            elif filename == "mudra-listing-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white mudra-listing-page"')
            elif filename == "mudra-detail-page.html":
                body_tag = body_tag.replace('class="bg-white"', 'class="bg-white mudra-detail-page"')
            extra_scripts = ""
            if filename == "guru-detail-page.html":
                extra_scripts = '<script src="assets/js/guru-detail-paths.js"></script>\n<script src="assets/js/guru-detail-classes.js"></script>\n'
            elif filename == "class-detail-page.html":
                extra_scripts = (
                    '<script src="assets/js/guru-detail-paths.js"></script>\n'
                    '<script src="assets/js/class-detail-player.js"></script>\n'
                    '<script src="assets/js/class-detail-curriculum.js"></script>\n'
                )
            elif filename == "free-video-detail-page.html":
                extra_scripts = '<script src="assets/js/free-video-detail-player.js"></script>\n'
            elif filename == "preview-video-detail-page.html":
                extra_scripts = '<script src="assets/js/class-detail-player.js"></script>\n<script src="assets/js/preview-video-detail-player.js"></script>\n'
            html = render_page(head, body_tag, nav, builder(), cta, footer, extra_scripts)
            (ROOT / filename).write_text(html, encoding="utf-8")
            created.append(filename)
        except Exception as exc:
            errors.append(f"{filename}: {exc}")
    print(f"Created {len(created)} files")
    for name in created:
        print(f" - {name}")
    if errors:
        print("Errors:")
        for err in errors:
            print(f" - {err}")

    index_path = ROOT / "index.html"
    index_path.write_text(normalize_section_headings(index_path.read_text(encoding="utf-8")), encoding="utf-8")

if __name__ == "__main__":
    main()
