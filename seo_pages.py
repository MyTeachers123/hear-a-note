"""
seo_pages.py - builds the pages that search engines and AI assistants read.

  static/learn/<lang>/index.html  one information page per language (for parents and teachers),
                                  with meta tags, Open Graph, hreflang and JSON-LD structured data
  static/sitemap.xml              every page + its language versions
  static/robots.txt               allows search engines and AI assistants; points to the sitemap
  static/llms.txt                 short plain-text summary for AI assistants
  static/<INDEXNOW_KEY>.txt       IndexNow key file (Bing, Yandex, Seznam, Naver...)

Text lives in seo_i18n.py (12 languages). All output is plain ASCII: non-ASCII characters are written
as HTML character references (&#x...;), which every browser and crawler reads normally.
Run after changing seo_i18n.py:  python seo_pages.py
"""
import datetime
import html
import json
from pathlib import Path

import i18n
from seo_i18n import PAGES

BRAND = "Hear-a-Note for Toddlers"
# local names of the same brand (Traditional / Simplified Chinese)
ALT_NAMES = ["\u807d\u97f3\u5bf6", "\u542c\u97f3\u5b9d"]

SITE = "https://kids.myteachers123.com"
ORG_URL = "https://myteachers123.com/"
GITHUB = "https://github.com/MyTeachers123/hear-a-note"
INDEXNOW_KEY = "7d3f9c2a1b8e4f6a9c0d5e2b7a1f4c8d"
ROOT = Path(__file__).parent / "static"
TODAY = datetime.date.today().isoformat()

SLUG = {"en": "en", "es": "es", "zh-Hant": "zh-hant", "zh-Hans": "zh-hans", "ko": "ko", "ja": "ja",
        "vi": "vi", "fr": "fr", "it": "it", "ru": "ru", "de": "de", "hi": "hi"}
OG_LOCALE = {"en": "en_US", "es": "es_ES", "zh-Hant": "zh_TW", "zh-Hans": "zh_CN", "ko": "ko_KR", "ja": "ja_JP",
             "vi": "vi_VN", "fr": "fr_FR", "it": "it_IT", "ru": "ru_RU", "de": "de_DE", "hi": "hi_IN"}
CODES = [c for c, _ in i18n.LANGS]
LANG_NAME = dict(i18n.LANGS)
OG_IMAGE = f"{SITE}/og/og-1200x630.png"   # English; each language page uses og/og-<slug>.png


def og_image(code):
    return f"{SITE}/og/og-{SLUG[code]}.png"
SHOT = f"{SITE}/og/screenshot-1280x720.png"
SCENE = f"{SITE}/og/real-piano-scene.png"          # the tablet on a real piano: the app's main feature
# YouTube companion video. Fill in "id" (the part after watch?v=) and "upload_date" after uploading,
# then run: python seo_pages.py  -> every page gets a link + VideoObject structured data.
YOUTUBE = {"id": None, "upload_date": None, "duration": "PT26M29S"}
UTM = "?utm_source=kids.myteachers123.com&utm_medium=referral&utm_campaign=hear_a_note"


def url(code):
    return f"{SITE}/learn/{SLUG[code]}/"


def ascii_html(s):
    """Plain ASCII: every non-ASCII character becomes &#x...; (the repository has no raw non-ASCII text)."""
    return s.encode("ascii", "xmlcharrefreplace").decode("ascii")


def fill(code, s):
    t = i18n.STRINGS[code]
    return (s.replace("{app}", t["appName"]).replace("{treble}", t["treble"]).replace("{bass}", t["bass"])
             .replace("{modePiano}", t["modePiano"]))


def esc(s):
    return html.escape(s, quote=True)


def songs(code):
    t = i18n.STRINGS[code]
    return ", ".join(t[k] for k in ("twinkle", "mary", "ode", "jingle"))


def languages_text():
    return ", ".join(name for _, name in i18n.LANGS)


def brand_html(name):
    # "Hear-a-Note for Toddlers" wraps between the two parts, never inside them
    a, sep, b = name.partition(" for ")
    if not sep:
        return esc(name)
    return f'<span class="nw">{esc(a)}</span> <span class="nw">for {esc(b)}</span>'

def jsonld(code, p):
    t = i18n.STRINGS[code]
    page = url(code)
    app = {
        "@type": "WebApplication",
        "@id": f"{SITE}/#app",
        "name": BRAND,
        "alternateName": ALT_NAMES,
        "url": f"{SITE}/",
        "description": fill(code, p["desc"]),
        "applicationCategory": "EducationalApplication",
        "applicationSubCategory": "Music education game for young children",
        "operatingSystem": "Any modern web browser (iOS, iPadOS, Android, ChromeOS, Windows, macOS)",
        "browserRequirements": "Requires JavaScript and Web Audio",
        "isAccessibleForFree": True,
        "isFamilyFriendly": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "inLanguage": CODES,
        "typicalAgeRange": "1.5-3",
        "audience": [
            {"@type": "ParentAudience", "childMinAge": 1.5, "childMaxAge": 3},
            {"@type": "EducationalAudience", "educationalRole": "teacher"},
        ],
        "educationalUse": ["Music education", "Early childhood music", "Piano practice"],
        "teaches": ["Treble clef note reading", "Bass clef note reading", "Piano keyboard basics",
                    "Matching notes on the staff to piano keys"],
        "featureList": [fill(code, p["real_p"]), *[fill(code, x) for x in p["why"]], p["f_modes_v"], p["f_offline_v"], p["f_account_v"], fill(code, p["f_music_v"])],
        "screenshot": [SCENE, SHOT],
        "image": og_image(code),
        "license": "https://opensource.org/licenses/MIT",
        "sameAs": [GITHUB],
        "author": {"@id": ORG_URL + "#org"},
        "publisher": {"@id": ORG_URL + "#org"},
    }
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": ORG_URL + "#org", "name": "MyTeachers123", "url": ORG_URL,
             "logo": f"{SITE}/og/logo-myteachers123.png"},
            {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": BRAND, "alternateName": ALT_NAMES,
             "inLanguage": CODES, "publisher": {"@id": ORG_URL + "#org"}},
            app,
            {"@type": ["WebPage", "FAQPage"], "@id": page + "#webpage", "url": page, "name": fill(code, p["title"]),
             "description": fill(code, p["desc"]), "inLanguage": code, "isPartOf": {"@id": f"{SITE}/#website"},
             "about": {"@id": f"{SITE}/#app"}, "primaryImageOfPage": SHOT, "dateModified": TODAY,
             "breadcrumb": {"@id": page + "#breadcrumb"},
             "mainEntity": [{"@type": "Question", "name": fill(code, q),
                             "acceptedAnswer": {"@type": "Answer", "text": fill(code, a)}} for q, a in p["faq"]]},
            *([{"@type": "VideoObject", "@id": f"{SITE}/#video", "name": fill(code, p["video_h"]),
                "description": fill(code, p["video_p"]), "thumbnailUrl": f"https://i.ytimg.com/vi/{YOUTUBE['id']}/maxresdefault.jpg",
                "uploadDate": YOUTUBE["upload_date"], "duration": YOUTUBE["duration"],
                "embedUrl": f"https://www.youtube.com/embed/{YOUTUBE['id']}", "url": f"https://www.youtube.com/watch?v={YOUTUBE['id']}",
                "inLanguage": CODES, "isFamilyFriendly": True, "about": {"@id": f"{SITE}/#app"},
                "publisher": {"@id": ORG_URL + "#org"}}] if YOUTUBE["id"] else []),
            {"@type": "BreadcrumbList", "@id": page + "#breadcrumb", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["appName"], "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": fill(code, p["what_h"]), "item": page}]},
        ],
    }


def video_section(code, p):
    if not YOUTUBE["id"]:
        return ""
    return f"""    <section id="video">
      <h2>{esc(p["video_h"])}</h2>
      <p>{esc(p["video_p"])}</p>
      <p class="cta"><a class="btn alt" href="https://www.youtube.com/watch?v={YOUTUBE['id']}">{esc(p["video_cta"])}</a></p>
    </section>
"""


def page_html(code):
    p = {k: (fill(code, v) if isinstance(v, str) else v) for k, v in PAGES[code].items()}
    t = i18n.STRINGS[code]
    f = lambda s: esc(fill(code, s))
    play = f"/?lang={code}"
    alternates = "\n".join(f'  <link rel="alternate" hreflang="{c}" href="{url(c)}">' for c in CODES)
    alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{url("en")}">'
    og_alt = "\n".join(f'  <meta property="og:locale:alternate" content="{OG_LOCALE[c]}">' for c in CODES if c != code)
    facts = [
        (p["f_age"], p["f_age_v"]), (p["f_price"], p["f_price_v"]), (p["f_account"], p["f_account_v"]),
        (p["f_devices"], p["f_devices_v"]), (p["f_offline"], p["f_offline_v"]), (p["f_music"], p["f_music_v"]),
        (p["f_songs"], songs(code)), (p["f_modes"], p["f_modes_v"]), (p["f_langs"], languages_text()),
    ]
    rows = "\n".join(f"        <tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in facts)
    li = lambda items: "\n".join(f"        <li>{f(x)}</li>" for x in items)
    faq = "\n".join(f"      <details><summary>{f(q)}</summary><p>{f(a)}</p></details>" for q, a in p["faq"])
    cur = ' aria-current="page"'
    langs = "\n".join(
        f'        <li><a href="{url(c)}" hreflang="{c}" lang="{c}"{cur if c == code else ""}>{esc(LANG_NAME[c])}</a></li>'
        for c in CODES)
    ld = json.dumps(jsonld(code, PAGES[code]), ensure_ascii=False, indent=1).replace("</", "<\\/")
    doc = f"""<!doctype html>
<html lang="{code}" itemscope itemtype="https://schema.org/WebPage">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(p["title"])}</title>
  <meta name="description" content="{esc(p["desc"])}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <link rel="canonical" href="{url(code)}">
{alternates}
  <meta name="theme-color" content="#FFF5F8">
  <link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{esc(i18n.STRINGS[code]["appName"])}">
  <meta property="og:title" content="{esc(p["title"])}">
  <meta property="og:description" content="{esc(p["desc"])}">
  <meta property="og:url" content="{url(code)}">
  <meta property="og:image" content="{og_image(code)}">
  <meta property="og:image:secure_url" content="{og_image(code)}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{esc(p["img_alt"])}">
  <meta property="og:locale" content="{OG_LOCALE[code]}">
{og_alt}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(p["title"])}">
  <meta name="twitter:description" content="{esc(p["desc"])}">
  <meta name="twitter:image" content="{og_image(code)}">
  <meta itemprop="name" content="{esc(p["title"])}">
  <meta itemprop="description" content="{esc(p["desc"])}">
  <meta itemprop="image" content="{og_image(code)}">
  <link rel="stylesheet" href="/learn/learn.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body>
  <div class="topbar">
    <details class="lang-menu">
      <summary aria-label="{esc(p["lang_label"])}"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="9.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M2.5 12h19M12 2.5c3 3 3 16 0 19M12 2.5c-3 3-3 16 0 19" fill="none" stroke="currentColor" stroke-width="2"/></svg><span>{esc(LANG_NAME[code])}</span></summary>
      <ul>
{langs}
      </ul>
    </details>
  </div>
  <header class="hero">
    <a class="logo" href="{ORG_URL}{UTM}" title="MyTeachers123.com"><img src="/og/logo-myteachers123.png" alt="MyTeachers123.com" width="160" height="160"></a>
    <p class="brand">{brand_html(t["appName"])}</p>
    <h1>{esc(p["h1"])}</h1>
    <p class="lead">{esc(p["lead"])}</p>
    <p class="cta"><a class="btn" href="{play}">{esc(p["play"])}</a></p>
    <p class="note">{esc(p["play_note"])}</p>
    <img class="shot" src="/og/real-piano-scene.png" width="1600" height="1000" alt="{esc(p["real_alt"])}">
  </header>
  <main>
    <section id="real-piano" class="real">
      <h2>{esc(p["real_h"])}</h2>
      <p>{esc(p["real_p"])}</p>
      <ol>
{li(PAGES[code]["real_steps"])}
      </ol>
      <p class="small">{esc(p["real_note"])}</p>
    </section>
    <section id="why" class="why">
      <h2>{esc(p["why_h"])}</h2>
      <ul>
{li(PAGES[code]["why"])}
      </ul>
    </section>
    <section id="what">
      <h2>{esc(p["what_h"])}</h2>
      <p>{esc(p["what_p"])}</p>
      <img class="shot inner" src="/og/screenshot-1280x720.png" width="1280" height="720" alt="{esc(p["img_alt"])}" loading="lazy">
    </section>
    <section id="facts">
      <h2>{esc(p["facts_h"])}</h2>
      <table>
{rows}
      </table>
    </section>
    <section id="parents">
      <h2>{esc(p["parents_h"])}</h2>
      <ul>
{li(PAGES[code]["parents"])}
      </ul>
    </section>
    <section id="teachers">
      <h2>{esc(p["teachers_h"])}</h2>
      <p>{esc(p["teachers_p"])}</p>
      <ul>
{li(PAGES[code]["teachers"])}
      </ul>
    </section>
    <section id="how">
      <h2>{esc(p["how_h"])}</h2>
      <ol>
{li(PAGES[code]["steps"])}
      </ol>
      <p class="cta"><a class="btn" href="{play}">{esc(p["play"])}</a></p>
    </section>
{video_section(code, p)}    <section id="faq">
      <h2>{esc(p["faq_h"])}</h2>
{faq}
    </section>
    <section id="myteachers123" class="mt">
      <h2>{esc(p["mt_h"])}</h2>
      <p>{esc(p["mt_p"])}</p>
      <p class="cta"><a class="btn alt" href="{ORG_URL}{UTM}">{esc(p["mt_cta"])}</a></p>
      <p>{esc(p["mt_teacher"])}</p>
    </section>
  </main>
  <footer>
    <nav aria-label="{esc(p["lang_label"])}">
      <h2>{esc(p["lang_label"])}</h2>
      <ul class="langs">
{langs}
      </ul>
    </nav>
    <p><a href="{ORG_URL}{UTM}">{esc(p["made"])}</a> &middot; <a href="{GITHUB}">{esc(p["source"])}</a> &middot; {esc(p["updated"])}: <time datetime="{TODAY}">{TODAY}</time></p>
  </footer>
</body>
</html>
"""
    return ascii_html(doc)


def sitemap():
    alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{url(c)}"/>' for c in CODES)
    alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url("en")}"/>'
    items = [f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>"]
    items += [f"  <url>\n    <loc>{url(c)}</loc>\n    <lastmod>{TODAY}</lastmod>{alts}\n  </url>" for c in CODES]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(items) + "\n</urlset>\n")


# Search engines and AI assistants that may read the site. A named group replaces the "*" group
# for that crawler, so every group repeats the same rules.
CRAWLERS = [
    ("Search engines", ["Googlebot", "Bingbot", "Slurp", "DuckDuckBot", "Applebot", "YandexBot", "Baiduspider", "NaverBot", "Yeti"]),
    ("OpenAI (ChatGPT)", ["GPTBot", "OAI-SearchBot", "ChatGPT-User"]),
    ("Anthropic (Claude)", ["ClaudeBot", "Claude-SearchBot", "Claude-User"]),
    ("Google Gemini / AI", ["Google-Extended"]),
    ("Microsoft Copilot uses Bingbot (above)", []),
    ("Meta AI", ["meta-externalagent", "meta-externalfetcher"]),
    ("Perplexity", ["PerplexityBot", "Perplexity-User"]),
    ("Apple Intelligence", ["Applebot-Extended"]),
    ("Others", ["Amazonbot", "DuckAssistBot", "MistralAI-User", "CCBot"]),
]


def robots():
    out = ["# Hear-a-Note for Toddlers - everyone is welcome to read and cite these pages.",
           "# (If Cloudflare adds its own AI-crawler block above this, turn off its managed robots.txt.)", ""]
    for title, bots in CRAWLERS:
        out.append(f"# {title}")
        for b in bots:
            out.append(f"User-agent: {b}")
        if bots:
            out += ["Allow: /", "Disallow: /api/", ""]
        else:
            out.append("")
    out += ["User-agent: *", "Allow: /", "Disallow: /api/", "", f"Sitemap: {SITE}/sitemap.xml", ""]
    return "\n".join(out)


def llms():
    p = PAGES["en"]
    t = i18n.STRINGS["en"]
    L = ["# Hear-a-Note for Toddlers", "",
         f"> {fill('en', p['desc'])}", "",
         fill("en", p["what_p"]), "",
         "## " + p["real_h"], "", fill("en", p["real_p"]), ""] + [f"{i}. {fill('en', x)}" for i, x in enumerate(p["real_steps"], 1)] + ["", p["real_note"], "",
         "## Key facts", ""]
    for a, b in [(p["f_age"], p["f_age_v"]), (p["f_price"], p["f_price_v"]), (p["f_account"], p["f_account_v"]),
                 (p["f_devices"], p["f_devices_v"]), (p["f_offline"], p["f_offline_v"]),
                 (p["f_music"], fill("en", p["f_music_v"])), (p["f_songs"], songs("en")),
                 (p["f_modes"], p["f_modes_v"]),
                 (p["f_langs"], "English, Spanish, Traditional Chinese, Simplified Chinese, Korean, Japanese, "
                                "Vietnamese, French, Italian, Russian, German, Hindi")]:
        L.append(f"- {a}: {b}")
    L += ["", "## " + fill("en", p["why_h"]), ""] + [f"- {fill('en', x)}" for x in p["why"]]
    L += ["", "## " + p["parents_h"], ""] + [f"- {fill('en', x)}" for x in p["parents"]]
    L += ["", "## " + p["teachers_h"], "", fill("en", p["teachers_p"]), ""] + [f"- {fill('en', x)}" for x in p["teachers"]]
    L += ["", "## FAQ", ""]
    for q, a in p["faq"]:
        L += [f"### {fill('en', q)}", "", fill("en", a), ""]
    names = {"en": "English", "es": "Spanish", "zh-Hant": "Traditional Chinese", "zh-Hans": "Simplified Chinese",
             "ko": "Korean", "ja": "Japanese", "vi": "Vietnamese", "fr": "French", "it": "Italian",
             "ru": "Russian", "de": "German", "hi": "Hindi"}
    L += ["## Links", "", f"- [Open the app (free)]({SITE}/)"]
    if YOUTUBE["id"]:
        L.append(f"- [Video: 26-minute piano companion for 18-36 months (YouTube)](https://www.youtube.com/watch?v={YOUTUBE['id']})")
    L += [f"- [Information page in {names[c]}]({url(c)})" for c in CODES]
    L += [f"- [Source code (MIT)]({GITHUB})",
          f"- [Publisher: MyTeachers123.com]({ORG_URL}) - a multilingual platform that helps parents find family daycare for infants and toddlers", ""]
    return "\n".join(L)


def main():
    for code in CODES:
        d = ROOT / "learn" / SLUG[code]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page_html(code), encoding="ascii")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="ascii")
    (ROOT / "robots.txt").write_text(robots(), encoding="ascii")
    text = ascii_text(llms())
    bad = sorted({ch for ch in text if ord(ch) > 127})
    assert not bad, f"llms.txt has non-ASCII characters: {bad}"
    (ROOT / "llms.txt").write_text(text, encoding="ascii")
    (ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="ascii")
    print(f"ok: {len(CODES)} pages, sitemap.xml, robots.txt, llms.txt, IndexNow key")


def ascii_text(s):
    """llms.txt is plain text: replace the few typographic characters with ASCII ones."""
    for a, b in {"–": "-", "—": "-", "→": "->", "“": '"', "”": '"', "’": "'"}.items():
        s = s.replace(a, b)
    return s


if __name__ == "__main__":
    main()
