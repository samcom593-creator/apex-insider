#!/usr/bin/env python3
"""Build the apex-insider static site from content-ideas archive.

Pulls posts from claude-sync's memory/-Users-samjames/content-ideas/
(synced into the working dir via the workflow), renders each as a
permanent SEO-optimized page, plus an index, RSS, and sitemap.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SOURCE = Path(os.environ.get("CONTENT_SOURCE", ROOT / "content-source"))

DOCS.mkdir(exist_ok=True)

BASE_URL = "https://samcom593-creator.github.io/apex-insider"
SITE_TITLE = "APEX Nation — Daily AI Edge for Sales & Insurance Pros"
SITE_DESC = (
    "Daily AI-powered sales & insurance edge by Sam James (King of Sales). "
    "Tactics 95% of agents don't know — recruited 70+ agents at age 20. "
    "Want to do this for real? Apply at apex-financial.org/apply."
)
AUTHOR = "Sam James — @theprincejamez"
APPLY_CTA = "https://apex-financial.org/apply"
IG_CTA = "https://www.instagram.com/theprincejamez/"


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body {
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  max-width: 720px;
  margin: 0 auto;
  padding: 32px 20px 120px;
  background: #fafaf7;
  color: #111;
}
@media (prefers-color-scheme: dark) {
  body { background: #0f0f10; color: #e8e8e6; }
  a { color: #ffd84d; }
  hr { border-color: #333; }
  .card { background: #18181a; border-color: #2a2a2c; }
  .cta { background: #1a1a1b; border-color: #ffd84d; }
}
header { margin-bottom: 32px; }
header h1 { font-size: 26px; margin: 0 0 4px; letter-spacing: -0.02em; }
header p { margin: 0; font-size: 14px; opacity: 0.7; }
a { color: #1a4dcf; text-decoration: none; border-bottom: 1px solid transparent; }
a:hover { border-bottom-color: currentColor; }
.cta {
  display: block;
  margin: 32px 0;
  padding: 20px 22px;
  border: 2px solid #1a4dcf;
  border-radius: 8px;
  background: #fff;
  text-align: center;
  font-weight: 600;
  font-size: 17px;
}
.cta:hover { transform: translateY(-1px); transition: transform 0.1s; border-bottom-color: #1a4dcf; }
.card {
  background: #fff;
  border: 1px solid #ececec;
  border-radius: 8px;
  padding: 18px 22px;
  margin: 12px 0;
}
.card h2 { margin: 0 0 4px; font-size: 18px; }
.card .meta { font-size: 13px; opacity: 0.6; }
article h1 { font-size: 28px; line-height: 1.2; margin-top: 0; }
article h2 { font-size: 22px; margin-top: 32px; }
article h3 { font-size: 18px; }
article p { margin: 12px 0; }
article blockquote { border-left: 3px solid currentColor; padding-left: 16px; margin: 16px 0; opacity: 0.85; }
footer { margin-top: 64px; padding-top: 24px; border-top: 1px solid currentColor; font-size: 13px; opacity: 0.65; }
.signup {
  margin: 32px 0; padding: 24px; border-radius: 10px;
  background: linear-gradient(135deg, #1a4dcf 0%, #4a1acf 100%);
  color: #fff;
}
.signup h3 { margin-top: 0; color: #fff; }
.signup form { display: flex; gap: 8px; flex-wrap: wrap; }
.signup input[type=email] { flex: 1 1 200px; padding: 12px 14px; border: 0; border-radius: 6px; font-size: 15px; }
.signup button { padding: 12px 18px; background: #ffd84d; color: #111; border: 0; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 15px; }
"""


def page_template(title: str, meta_desc: str, body_html: str, *, canonical: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_escape(title)}</title>
<meta name="description" content="{html_escape(meta_desc)}">
<meta name="author" content="{html_escape(AUTHOR)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html_escape(title)}">
<meta property="og:description" content="{html_escape(meta_desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@theprincejamez">
<link rel="alternate" type="application/rss+xml" title="APEX Nation" href="{BASE_URL}/rss.xml">
<style>{CSS}</style>
</head>
<body>
<header>
  <h1><a href="{BASE_URL}/" style="border:0">APEX Nation</a></h1>
  <p>Daily AI edge for sales & insurance pros · by <a href="{IG_CTA}">@theprincejamez</a></p>
</header>
{body_html}
<div class="signup">
  <h3>Want to do this for a living?</h3>
  <p>Sam recruited 70+ agents at age 20. He'll show you how. No fluff, no hype.</p>
  <form action="https://formsubmit.co/ajax/sam.com593@gmail.com" method="POST">
    <input type="hidden" name="_subject" value="APEX Insider signup">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="source" value="apex-insider">
    <input type="email" name="email" placeholder="Your email" required>
    <button type="submit">Get the inside track</button>
  </form>
</div>
<a class="cta" href="{APPLY_CTA}">→ Apply to APEX Financial</a>
<footer>
  <p>APEX Nation · auto-published daily · <a href="{BASE_URL}/rss.xml">RSS</a> · <a href="{IG_CTA}">@theprincejamez</a></p>
  <p>Want to be in the room where this happens? <a href="https://samcom593-creator.github.io/seminar/">Free Wed/Sat seminar</a>.</p>
</footer>
</body>
</html>
"""


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_post(path: Path):
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    # Extract date from filename like 2026-05-13.md
    name = path.stem
    try:
        date_obj = datetime.strptime(name, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    # Strip leading markdown header `# Content ideas — date` if present, since
    # the original body already contains the structured HTML.
    body = re.sub(r"^#\s*Content ideas.*?\n+", "", body, count=1)
    return {
        "date": date_obj,
        "slug": name,
        "body_html": body.strip(),
    }


def render_post(post: dict) -> str:
    date_str = post["date"].strftime("%B %d, %Y")
    title = f"Daily AI Edge — {date_str}"
    desc = f"3 IG/TikTok Reel hooks + 1 YouTube Short ideas for {date_str} — AI tactics agents can film today."
    canonical = f"{BASE_URL}/{post['slug']}.html"
    article_html = (
        f"<article>\n"
        f"<h1>{html_escape(title)}</h1>\n"
        f"<p class=\"meta\">{date_str} · ~3 min read</p>\n"
        f"{post['body_html']}\n"
        f"<p><em>This post is auto-curated from Sam's daily content engine. "
        f"If one of these ideas works, film it and tag @theprincejamez.</em></p>\n"
        f"</article>"
    )
    return page_template(title, desc, article_html, canonical=canonical)


def render_index(posts: list) -> str:
    cards = []
    for p in posts:
        date_str = p["date"].strftime("%b %d, %Y")
        # Pull first <h2> or <p> as a teaser
        m = re.search(r"<(?:h2|p)[^>]*>(.*?)</(?:h2|p)>", p["body_html"], re.DOTALL)
        teaser = re.sub(r"<[^>]+>", " ", m.group(1))[:160].strip() if m else ""
        cards.append(
            f"<a class=\"card\" href=\"{p['slug']}.html\">"
            f"<h2>{date_str}</h2>"
            f"<div class=\"meta\">{html_escape(teaser)}…</div>"
            f"</a>"
        )
    body = (
        "<p style=\"font-size:17px;margin-bottom:32px\">Every day, 3 short-form video ideas + 1 YouTube Short on AI tactics that give sales/insurance agents an edge. "
        "Built for people who want to grow — pick one, film it, post it.</p>"
        + "\n".join(cards)
    )
    return page_template(SITE_TITLE, SITE_DESC, body, canonical=f"{BASE_URL}/")


def render_rss(posts: list) -> str:
    items = []
    for p in posts[:30]:
        url = f"{BASE_URL}/{p['slug']}.html"
        date_str = p["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")
        title = f"Daily AI Edge — {p['date'].strftime('%B %d, %Y')}"
        items.append(
            f"<item>"
            f"<title>{html_escape(title)}</title>"
            f"<link>{url}</link>"
            f"<guid>{url}</guid>"
            f"<pubDate>{date_str}</pubDate>"
            f"<description>{html_escape(p['body_html'][:500])}</description>"
            f"</item>"
        )
    return (
        f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        f"<rss version=\"2.0\"><channel>"
        f"<title>{html_escape(SITE_TITLE)}</title>"
        f"<link>{BASE_URL}/</link>"
        f"<description>{html_escape(SITE_DESC)}</description>"
        f"{''.join(items)}"
        f"</channel></rss>"
    )


def render_sitemap(posts: list) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"<url><loc>{BASE_URL}/</loc><lastmod>{today}</lastmod></url>"]
    for p in posts:
        urls.append(
            f"<url><loc>{BASE_URL}/{p['slug']}.html</loc>"
            f"<lastmod>{p['date'].strftime('%Y-%m-%d')}</lastmod></url>"
        )
    return (
        f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        f"<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{''.join(urls)}"
        f"</urlset>"
    )


def main():
    if not SOURCE.exists():
        print(f"no content source at {SOURCE} — building empty placeholder")
        empty = page_template(
            SITE_TITLE,
            SITE_DESC,
            "<p>Content is being generated. Check back tomorrow morning.</p>",
            canonical=f"{BASE_URL}/",
        )
        (DOCS / "index.html").write_text(empty)
        return

    posts = []
    for path in sorted(SOURCE.glob("*.md"), reverse=True):
        post = parse_post(path)
        if post:
            posts.append(post)
            (DOCS / f"{post['slug']}.html").write_text(render_post(post))
    (DOCS / "index.html").write_text(render_index(posts))
    (DOCS / "rss.xml").write_text(render_rss(posts))
    (DOCS / "sitemap.xml").write_text(render_sitemap(posts))
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    (DOCS / "CNAME").touch()  # placeholder for future custom domain
    print(f"built {len(posts)} posts → {DOCS}")


if __name__ == "__main__":
    main()
