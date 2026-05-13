#!/usr/bin/env python3
"""Build the APEX Nation static site from content sources."""
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SOURCE = Path(os.environ.get("CONTENT_SOURCE", ROOT / "content-source"))
CORNER = ROOT / "cornerstone"
DOCS.mkdir(exist_ok=True)

BASE = "https://samcom593-creator.github.io/apex-insider"
TITLE = "APEX Nation — Sam James / King of Sales"
DESC = "Sam James — 20, recruited 70+ life-insurance agents, building APEX Financial. Daily AI + sales edge for people building their own thing."
AUTHOR = "Sam James — @theprincejamez"
APPLY = "https://apex-financial.org/apply"
IG = "https://www.instagram.com/theprincejamez/"
SINK = "https://formsubmit.co/ajax/sam.com593@gmail.com"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


CSS = """
:root { --ink:#0a0a0c; --paper:#faf7ef; --gold:#ffd84d; --gold-deep:#c89c1a;
  --muted:rgba(10,10,12,0.55); --line:rgba(10,10,12,0.10); --card:#fff;
  color-scheme: light dark; }
*{box-sizing:border-box} html,body{margin:0;padding:0}
body{font:17px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--paper);color:var(--ink);-webkit-font-smoothing:antialiased}
@media (prefers-color-scheme: dark){:root{--ink:#f1efe7;--paper:#0a0a0c;--muted:rgba(241,239,231,0.6);--line:rgba(241,239,231,0.12);--card:#15151a}}
.wrap{max-width:760px;margin:0 auto;padding:24px 22px}
.nav{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:10}
.nav .brand{font-weight:800;letter-spacing:-0.02em;text-decoration:none;color:var(--ink);font-size:17px}
.nav .brand .dot{color:var(--gold)}
.nav .links{display:flex;gap:18px;font-size:14px;align-items:center}
.nav a{color:var(--muted);text-decoration:none}
.nav a:hover{color:var(--ink)}
.nav .apply{background:var(--ink);color:var(--paper);padding:8px 14px;border-radius:6px;font-weight:700}
@media (prefers-color-scheme: dark){.nav .apply{background:var(--gold);color:var(--ink)}}
@media (max-width:520px){.nav .links a:not(.apply){display:none}}
.hero{padding:56px 22px 36px;text-align:center;max-width:760px;margin:0 auto}
.kicker{font-size:13px;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold-deep);font-weight:700;margin-bottom:14px}
@media (prefers-color-scheme: dark){.kicker{color:var(--gold)}}
.hero h1{font-size:clamp(34px,6.5vw,56px);line-height:1.05;letter-spacing:-0.03em;margin:0 0 18px;font-weight:900}
.hero h1 .accent{color:var(--gold-deep)}
@media (prefers-color-scheme: dark){.hero h1 .accent{color:var(--gold)}}
.sub{font-size:19px;color:var(--muted);margin:0 auto 28px;max-width:560px}
.row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-block;padding:14px 22px;border-radius:8px;font-weight:700;text-decoration:none;font-size:15px;transition:transform .08s;border:2px solid transparent}
.btn:hover{transform:translateY(-1px)}
.btn-primary{background:var(--ink);color:var(--paper)}
@media (prefers-color-scheme: dark){.btn-primary{background:var(--gold);color:var(--ink)}}
.btn-ghost{background:transparent;color:var(--ink);border-color:var(--ink)}
.btn-gold{background:var(--gold);color:var(--ink);border-color:var(--gold-deep)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;margin:48px 0}
.stat{text-align:center;padding:22px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.stat .n{font-size:32px;font-weight:900;letter-spacing:-0.02em}
.stat .l{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em}
h2.section{font-size:28px;letter-spacing:-0.02em;margin:48px 0 12px}
.sub-section{color:var(--muted);margin:0 0 18px}
.card-grid{display:grid;grid-template-columns:1fr;gap:12px}
@media (min-width:600px){.card-grid.col-2{grid-template-columns:1fr 1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px 22px;text-decoration:none;color:var(--ink);display:block;transition:border-color .15s,transform .08s}
.card:hover{border-color:var(--gold-deep);transform:translateY(-1px)}
.card .date{font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted)}
.card h3{margin:6px 0 8px;font-size:19px}
.card p{margin:0;color:var(--muted);font-size:14px}
.offer{padding:36px 28px;background:var(--card);border:2px solid var(--line);border-radius:14px;margin:32px 0}
.offer.gold{border-color:var(--gold);background:linear-gradient(180deg,transparent 0%,rgba(255,216,77,0.06) 100%)}
.offer .price{font-size:14px;color:var(--gold-deep);letter-spacing:0.1em;text-transform:uppercase;font-weight:700}
@media (prefers-color-scheme: dark){.offer .price{color:var(--gold)}}
.offer h3{font-size:24px;margin:6px 0 12px;letter-spacing:-0.02em}
.offer ul{padding-left:18px;margin:12px 0 20px}
.signup{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.signup input{flex:1 1 220px;padding:13px 14px;border:1px solid var(--line);border-radius:8px;font:inherit;background:var(--paper);color:var(--ink)}
.signup button{padding:13px 22px;background:var(--gold);color:var(--ink);border:0;border-radius:8px;font-weight:800;cursor:pointer;font:inherit}
.signup button:hover{background:var(--gold-deep);color:var(--paper)}
article{max-width:720px;margin:0 auto;padding:24px 22px 80px}
article h1{font-size:clamp(28px,5vw,40px);line-height:1.15;letter-spacing:-0.02em}
article h2{font-size:24px;margin-top:40px;letter-spacing:-0.02em}
article h3{font-size:19px;margin-top:24px}
article p{margin:14px 0}
article blockquote{border-left:3px solid var(--gold);padding-left:18px;margin:22px 0;color:var(--muted);font-style:italic}
article ul,article ol{padding-left:22px}
article li{margin:6px 0}
footer{padding:48px 22px;border-top:1px solid var(--line);margin-top:80px;text-align:center;font-size:14px;color:var(--muted)}
footer a{color:var(--muted)}
.banner-strip{background:var(--ink);color:var(--paper);text-align:center;padding:8px 22px;font-size:13px}
@media (prefers-color-scheme: dark){.banner-strip{background:var(--gold);color:var(--ink)}}
.banner-strip a{color:var(--gold);font-weight:700;text-decoration:none}
@media (prefers-color-scheme: dark){.banner-strip a{color:var(--ink);text-decoration:underline}}
"""

NAV = f'<div class="banner-strip">Free Wed/Sat seminar → <a href="https://samcom593-creator.github.io/seminar/">save your seat</a></div><nav class="nav"><a class="brand" href="{BASE}/">APEX<span class="dot">.</span>Nation</a><div class="links"><a href="{BASE}/platform.html">Platform</a><a href="{BASE}/course.html">Course</a><a href="{BASE}/leads.html">Leads</a><a class="apply" href="{APPLY}">Apply</a></div></nav>'

FOOTER = f'<footer><div class="row"><a href="{BASE}/">Home</a><a href="{BASE}/platform.html">Platform</a><a href="{BASE}/course.html">Course</a><a href="{BASE}/leads.html">Leads</a><a href="{IG}">Instagram</a><a href="{BASE}/rss.xml">RSS</a></div><p>© {datetime.now().year} APEX Nation · auto-published daily · Built by {AUTHOR}</p></footer>'


def page(title, desc, body, *, canonical):
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:creator" content="@theprincejamez">
<link rel="alternate" type="application/rss+xml" title="APEX Nation" href="{BASE}/rss.xml">
<style>{CSS}</style>
</head><body>{NAV}{body}{FOOTER}</body></html>'''


def teaser_of(html):
    m = re.search(r"<(?:h2|p)[^>]*>(.*?)</(?:h2|p)>", html, re.DOTALL)
    t = re.sub(r"<[^>]+>", " ", m.group(1))[:140].strip() if m else ""
    return t + ("…" if t else "")


def home(posts, corns):
    if posts:
        rec = "".join(
            f'<a class="card" href="{p["slug"]}.html"><div class="date">{p["date"].strftime("%b %d, %Y")}</div><h3>Daily Edge — {p["date"].strftime("%b %d, %Y")}</h3><p>{esc(teaser_of(p["body_html"]))}</p></a>'
            for p in posts[:6]
        )
    else:
        rec = '<div class="card"><div class="date">Tomorrow</div><h3>Daily post drops at 11 AM ET</h3><p>3 IG/TikTok Reel hooks + 1 YouTube Short — AI tactics filming-ready.</p></div>'
    cs = "".join(
        f'<a class="card" href="{c["slug"]}.html"><div class="date">Cornerstone</div><h3>{esc(c["title"])}</h3><p>{esc(c["teaser"])}</p></a>'
        for c in corns[:3]
    )
    body = f'''<section class="hero"><div class="kicker">King of Sales · @theprincejamez</div>
<h1>I Make <span class="accent">Leaders</span>.</h1>
<p class="sub">20 years old. 70+ agents recruited. $30–40K/mo personal. Building APEX Financial into the agency that owns the AI era of insurance — and showing the playbook in real time.</p>
<div class="row"><a class="btn btn-primary" href="{APPLY}">Apply to APEX</a><a class="btn btn-ghost" href="{BASE}/course.html">King of Sales Course →</a></div></section>
<div class="wrap">
<div class="stats">
<div class="stat"><div class="n">70+</div><div class="l">Agents recruited</div></div>
<div class="stat"><div class="n">20</div><div class="l">Years old</div></div>
<div class="stat"><div class="n">$30K+</div><div class="l">Monthly personal</div></div>
<div class="stat"><div class="n">163</div><div class="l">APEX edge fns</div></div>
</div>
<h2 class="section">Cornerstone</h2>
<p class="sub-section">The plays you can read once and reuse forever.</p>
<div class="card-grid col-2">{cs}</div>
<h2 class="section">Daily Edge</h2>
<p class="sub-section">Every morning, 3 IG/TikTok Reel ideas + 1 YouTube Short. AI tactics 95% of agents don't know yet.</p>
<div class="card-grid">{rec}</div>
<div class="offer gold" style="margin-top:56px"><div class="price">Free · No spam</div><h3>Get the inside track</h3><p>One email when the daily drop lands. That's it. Unsub anytime.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX Insider signup"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-home"><input type="email" name="email" placeholder="you@yourdomain.com" required><button type="submit">Get the edge</button></form></div>
<div class="offer"><div class="price">Make this your career</div><h3>Become an APEX agent</h3><p>Same playbook. Same tools. Same team that's hit 70+. Apply free, get a 30-min call with Sam, decide together.</p><a class="btn btn-gold" href="{APPLY}" style="margin-top:8px">Apply now →</a></div>
</div>'''
    return page(TITLE, DESC, body, canonical=f"{BASE}/")


def post(p):
    date_str = p["date"].strftime("%B %d, %Y")
    body = f'<article><h1>Daily Edge — {date_str}</h1><p style="color:var(--muted);font-size:14px">{date_str} · 3 min read</p>{p["body_html"]}<hr><p style="font-size:15px"><strong>This is what daily looks like.</strong> 365 days a year of these. Want to build your career on this stack?</p><p><a class="btn btn-gold" href="{APPLY}">Apply to APEX →</a></p></article>'
    return page(f"Daily Edge — {date_str}", f"3 IG/TikTok Reel hooks + 1 YouTube Short for {date_str}.", body, canonical=f"{BASE}/{p['slug']}.html")


def corner(c):
    body = f'<article><p style="color:var(--gold-deep);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;font-weight:700">Cornerstone</p><h1>{esc(c["title"])}</h1><p style="color:var(--muted);font-size:14px">By Sam James · {c.get("updated","2026-05-12")}</p>{c["body_html"]}<hr><p style="font-size:15px"><strong>Building your own thing?</strong> APEX hires for it. The agents we love recruit are people running their own playbook.</p><p><a class="btn btn-gold" href="{APPLY}">Apply to APEX →</a></p></article>'
    return page(c["title"] + " — APEX Nation", c["teaser"], body, canonical=f"{BASE}/{c['slug']}.html")


def platform():
    body = f'''<section class="hero"><div class="kicker">APEX Platform · for agency owners</div>
<h1>The operating system <span class="accent">behind</span> 70+ agents.</h1>
<p class="sub">Sam built APEX from scratch — 163 edge functions, 32 cron jobs, real-time audit engine. Now he's licensing it to other agencies. Stop duct-taping Zapier flows.</p>
<div class="row"><a class="btn btn-gold" href="#waitlist">Get on the waitlist</a><a class="btn btn-ghost" href="{APPLY}">Just want to be an agent →</a></div></section>
<div class="wrap">
<h2 class="section">What you get</h2>
<ul style="font-size:17px;line-height:1.7">
<li><strong>Live deal sync</strong> — InsuraCloud / AgentLink / your carrier portal → real-time dashboard</li>
<li><strong>Audit engine</strong> — 5 sub-bots check activation, recruiting, content, seminar, onboarding every 30 min</li>
<li><strong>Real-time alerts</strong> — terminations, sync errors, $2K+ premium celebrations</li>
<li><strong>Recruiting funnel</strong> — apply form → CRM → nudge cadences → onboarding</li>
<li><strong>Quality flags</strong> — fell-off / lapse / declined policies surfaced daily</li>
<li><strong>Manager hierarchy</strong> — admin / manager / agent role isolation built-in</li>
<li><strong>Weekly dialer payment tracking</strong> — who paid for ReadyMode this week, per manager</li>
</ul>
<div class="offer gold" id="waitlist"><div class="price">Charter pricing · $497/mo</div>
<h3>Join the waitlist</h3><p>Limited to 25 agencies for the charter cohort. Onboarding starts Q3 2026.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX Platform waitlist"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-platform"><input type="text" name="agency" placeholder="Your agency name" required><input type="email" name="email" placeholder="you@youragency.com" required><button type="submit">Reserve a seat</button></form>
<p style="font-size:13px;color:var(--muted);margin-top:14px">No payment now. Sam personally vets every applicant.</p></div></div>'''
    return page("APEX Platform — License Sam's CRM", "License the operations stack Sam built. 163 edge fns, real-time audit, automated recruiting. Charter $497/mo.", body, canonical=f"{BASE}/platform.html")


def course():
    body = f'''<section class="hero"><div class="kicker">King of Sales · course</div>
<h1>How I went from <span class="accent">0 to 70+ agents</span> at 20.</h1>
<p class="sub">No theory. No fluff. The exact recruiting playbook Sam ran — DM scripts, application funnels, onboarding cadences, AI stack. Coming soon.</p>
<div class="row"><a class="btn btn-gold" href="#waitlist">Get on the waitlist</a><a class="btn btn-ghost" href="{APPLY}">Or apply to join the team →</a></div></section>
<div class="wrap">
<h2 class="section">What's in it</h2>
<ul style="font-size:17px;line-height:1.7">
<li><strong>The IG DM script</strong> — what to send the first 24h after someone follows you</li>
<li><strong>The "I make leaders" hook</strong> — why this 4-word bio out-converts long-form pitches</li>
<li><strong>The qualification call</strong> — 8 questions that filter tire-kickers in 12 minutes</li>
<li><strong>The onboarding cadence</strong> — day-by-day for the first 30 days</li>
<li><strong>The Discord moat</strong> — how to make your team's group chat the addiction</li>
<li><strong>The AI stack</strong> — exact tools + how Sam wires them</li>
<li><strong>The faith piece</strong> — why young Christian recruits over-index</li>
</ul>
<div class="offer gold" id="waitlist"><div class="price">Founders price · ~$497 one-time</div>
<h3>Get on the waitlist</h3><p>First 100 founders get lifetime access + a 1-on-1 with Sam.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="King of Sales waitlist"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-course"><input type="email" name="email" placeholder="you@yourdomain.com" required><button type="submit">Lock my spot</button></form>
<p style="font-size:13px;color:var(--muted);margin-top:14px">No payment now. You'll get one email when the course goes live.</p></div></div>'''
    return page("King of Sales — Recruiting Playbook", "The exact playbook Sam used to recruit 70+ insurance agents at age 20. Founders price ~$497.", body, canonical=f"{BASE}/course.html")


def leads():
    body = f'''<section class="hero"><div class="kicker">For FMOs + downline agencies</div>
<h1>Warm life-insurance <span class="accent">recruit leads</span>, vetted by Sam.</h1>
<p class="sub">APEX gets more applications than we can onboard. Instead of letting them sit, we resell vetted overflow to other agencies. Real people, US-licensed or actively studying, ready for the right team.</p>
<div class="row"><a class="btn btn-gold" href="#waitlist">Get on the buyer list</a><a class="btn btn-ghost" href="{BASE}/platform.html">Or license the full platform →</a></div></section>
<div class="wrap">
<h2 class="section">How it works</h2>
<ol style="font-size:17px;line-height:1.7">
<li>APEX collects 200-400 new applications/month from IG, TikTok, referrals.</li>
<li>Our team vets each one — phone screen, license check, motivation check.</li>
<li>The ones we can't onboard right now get offered to buyers like you.</li>
<li>You pay <strong>$50 per warm lead</strong> · contact + vet notes + state + license status.</li>
<li>If 1 of 50 closes, you've paid $2,500 for a producer who'll write $50K+ year 1.</li>
</ol>
<div class="offer gold" id="waitlist"><div class="price">$50/lead · 25 lead minimum</div>
<h3>Get on the buyer list</h3><p>We'll only sell to agencies that pass our vibe-check. Send your agency, team size, what states you write in.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX lead-resale buyer interest"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-leads"><input type="text" name="agency" placeholder="Your agency" required><input type="text" name="states" placeholder="States you write (e.g. TX, FL, CA)" required><input type="email" name="email" placeholder="you@youragency.com" required><button type="submit">Get on the list</button></form></div></div>'''
    return page("Warm Recruit Leads — APEX Lead Marketplace", "Sam's team vets 200-400 applications/month. Buy overflow leads $50/each. Real recruits, not data brokers.", body, canonical=f"{BASE}/leads.html")


STATES = [
    ("texas", "Texas"), ("florida", "Florida"), ("california", "California"),
    ("new-york", "New York"), ("georgia", "Georgia"), ("north-carolina", "North Carolina"),
    ("ohio", "Ohio"), ("illinois", "Illinois"), ("michigan", "Michigan"),
    ("pennsylvania", "Pennsylvania"),
]


def audit():
    body = f'''<section class="hero"><div class="kicker">For agency owners + managers</div>
<h1>Sam audits your <span class="accent">recruiting funnel</span> — $497.</h1>
<p class="sub">90-minute deep-dive on your IG, your DM scripts, your application flow, your onboarding cadence, your CRM. You leave with a 1-page action plan you can ship tomorrow.</p>
<div class="row"><a class="btn btn-gold" href="#book">Book the audit</a><a class="btn btn-ghost" href="{BASE}/platform.html">Or license the platform →</a></div></section>
<div class="wrap">
<h2 class="section">What you get</h2>
<ul style="font-size:17px;line-height:1.7">
<li><strong>Live screenshare</strong> — Sam looks at your IG, your DMs, your funnel, your numbers</li>
<li><strong>The 1-page action plan</strong> — top 5 things to fix this week, ranked by $ impact</li>
<li><strong>Voice memo recap</strong> — 10-min audio you can replay any time</li>
<li><strong>30-day follow-up text</strong> — quick check-in to see what shipped</li>
</ul>
<div class="offer gold" id="book"><div class="price">$497 · one-time · 90 minutes</div>
<h3>Book the audit</h3><p>Drop your agency name + IG handle + the one thing that's costing you sleep. I'll reply with calendar options within 24 hours.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX Audit booking"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-audit"><input type="text" name="agency" placeholder="Your agency" required><input type="text" name="ig_handle" placeholder="Your IG @handle" required><input type="text" name="pain_point" placeholder="What's costing you sleep" required><input type="email" name="email" placeholder="you@youragency.com" required><button type="submit">Request slots</button></form>
<p style="font-size:13px;color:var(--muted);margin-top:14px">No payment now. Pay after we book. Limited to 4 audits per month.</p></div></div>'''
    return page("APEX Audit — Sam looks at your funnel ($497)", "Sam James audits your recruiting funnel in 90 minutes. You leave with a 1-page action plan. $497, 4 slots/month.", body, canonical=f"{BASE}/audit.html")


def mentor():
    body = f'''<section class="hero"><div class="kicker">For 6-figure agency owners only</div>
<h1>1-on-1 with Sam, <span class="accent">monthly</span>.</h1>
<p class="sub">Weekly 60-min calls. Direct access in a private thread. We work the moves that move your number. Capped at 4 mentees.</p>
<div class="row"><a class="btn btn-gold" href="#apply">Apply for a seat</a><a class="btn btn-ghost" href="{BASE}/audit.html">Or try the audit first →</a></div></section>
<div class="wrap">
<h2 class="section">What this is</h2>
<p>Not a course. Not a group call. Me, on your team, every week. You bring the move you're stuck on. We work it. You ship it.</p>
<h2 class="section">Who fits</h2>
<ul style="font-size:17px;line-height:1.7">
<li>You're running $30K+/mo personal income or $100K+/mo team production</li>
<li>You have at least 5 contracted agents</li>
<li>You're willing to commit to 12 months at $5K/mo</li>
<li>You're not chasing the next shiny thing every week</li>
</ul>
<div class="offer gold" id="apply"><div class="price">$5,000/mo · 12 months · 4 seats total</div>
<h3>Apply</h3><p>Tell me about your agency. If you fit, I book a free 30-min fit call. If we both want it, you start the next Monday.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX Mentor application"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-mentor"><input type="text" name="agency" placeholder="Your agency" required><input type="text" name="monthly" placeholder="Current personal monthly $$" required><input type="text" name="team_size" placeholder="Contracted agents on your team" required><input type="text" name="goal" placeholder="12-month goal" required><input type="email" name="email" placeholder="you@youragency.com" required><button type="submit">Apply</button></form>
<p style="font-size:13px;color:var(--muted);margin-top:14px">Honest answers only. I'll know if you fudge the numbers.</p></div></div>'''
    return page("APEX Mentor — 1-on-1 with Sam ($5K/mo)", "Weekly calls + private access. 4 seats. For 6-figure agency owners only.", body, canonical=f"{BASE}/mentor.html")


def pdf():
    body = f'''<section class="hero"><div class="kicker">Free download</div>
<h1>10 lines that made me <span class="accent">$30K last month</span>.</h1>
<p class="sub">The exact DM openers, qualification questions, and close lines I used to recruit 70+ agents and write personal commissions every week. 8 pages. No fluff.</p>
<div class="row"><a class="btn btn-gold" href="#get">Get the PDF</a><a class="btn btn-ghost" href="{APPLY}">Or just apply to APEX →</a></div></section>
<div class="wrap">
<div class="offer gold" id="get"><div class="price">Free · Emailed in 60 seconds</div>
<h3>Get the PDF</h3><p>Drop your email. PDF hits your inbox. After that, one email a week if I have something worth sending. Unsub any time.</p>
<form class="signup" action="{SINK}" method="POST"><input type="hidden" name="_subject" value="APEX 10-Lines PDF"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="source" value="apex-insider-pdf"><input type="email" name="email" placeholder="you@yourdomain.com" required><button type="submit">Send it</button></form>
</div>
<h2 class="section">What's inside</h2>
<ul style="font-size:17px;line-height:1.7">
<li><strong>Lines 1-3:</strong> The first IG DM after someone follows you (3 variants)</li>
<li><strong>Lines 4-5:</strong> The qualification question that filters tire-kickers in 2 messages</li>
<li><strong>Line 6:</strong> The text I send 24h after the call if they ghost</li>
<li><strong>Line 7:</strong> The carrier-anchored close (works for FE + term + IUL)</li>
<li><strong>Lines 8-9:</strong> The "first week win" template — day-7 message for a new agent</li>
<li><strong>Line 10:</strong> The win-back I use for agents who go quiet at month 2</li>
</ul></div>'''
    return page("10 Lines That Made $30K — Sam James", "Free PDF: the DM, qualification, and close lines Sam used to recruit 70+ agents.", body, canonical=f"{BASE}/pdf.html")


def state_page(slug, name):
    body = f'''<section class="hero"><div class="kicker">How to start in {name}</div>
<h1>Become a life insurance agent in <span class="accent">{name}</span>.</h1>
<p class="sub">The 4-week path from zero to your first commission check in {name} — license, contracts, leads, and the parts no one tells you.</p>
<div class="row"><a class="btn btn-gold" href="{APPLY}">Apply to APEX</a><a class="btn btn-ghost" href="{BASE}/how-to-become-a-life-insurance-agent.html">Full national guide →</a></div></section>
<div class="wrap"><article>
<h2>The {name} license in 30 days</h2>
<p>The {name} Department of Insurance issues a Life & Health line that runs about 4-6 weeks from study to test to walking-around-with-your-license. Cost: typically $150-$250 all in (fingerprints + exam + license issuance). Anyone telling you you need to pay $5,000 to "join" their team is lying — you do not.</p>
<h2>Why {name} is a good place to start</h2>
<ul>
<li><strong>Reciprocity:</strong> {name} reciprocates with most other states; adding states later is paperwork-only.</li>
<li><strong>Carrier appetite:</strong> Most major carriers (Mutual of Omaha, AIG, Americo, AHL, Royal Neighbors) write in {name} aggressively.</li>
<li><strong>Final-expense demand:</strong> Senior-market final-expense is strong in {name} — easiest entry-level product.</li>
</ul>
<h2>The 30-day path</h2>
<ol>
<li><strong>Week 1:</strong> Buy a study course. ExamFX, Kaplan, or A.D. Banker. 1-2 hours/day.</li>
<li><strong>Week 2:</strong> Take the exam. Pass with 70-85%. Schedule your fingerprint appointment.</li>
<li><strong>Week 3:</strong> Apply for the license. Most {name} agents get their number within 5-7 business days.</li>
<li><strong>Week 4:</strong> Contract with carriers through your FMO. Make your first 20 dials. Close your first deal.</li>
</ol>
<h2>What NOT to do</h2>
<ul>
<li>Pay an FMO $200+ upfront before you've sold a single policy.</li>
<li>Sign a captive contract that says you can't keep your book if you leave.</li>
<li>Buy leads in your first 30 days. Get the license + your team first.</li>
<li>Pick a state you don't live in as your first license. Pick {name}, then expand.</li>
</ul>
<h2>What APEX does for {name} agents</h2>
<p>APEX is the FMO + team Sam runs. We pay 80%+ splits, train you free, give you carrier-vetted leads in {name}, and never charge upfront fees. Onboarding takes a week. If it's not a fit after 90 days, you keep your book and we part friends.</p>
<p><a class="btn btn-gold" href="{APPLY}">Apply to APEX from {name} →</a></p>
</article></div>'''
    return page(f"Become a Life Insurance Agent in {name} — APEX", f"4-week path to your {name} life insurance license + first commission. APEX recruits agents free.", body, canonical=f"{BASE}/states/{slug}.html")


def og_svg():
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0a0a0c"/><stop offset="100%" stop-color="#1a1a22"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/>
<text x="80" y="170" font-family="-apple-system,system-ui,sans-serif" font-size="32" font-weight="700" fill="#ffd84d" letter-spacing="4">APEX NATION</text>
<text x="80" y="320" font-family="-apple-system,system-ui,sans-serif" font-size="100" font-weight="900" fill="#faf7ef" letter-spacing="-2">I Make</text>
<text x="80" y="430" font-family="-apple-system,system-ui,sans-serif" font-size="100" font-weight="900" fill="#ffd84d" letter-spacing="-2">Leaders.</text>
<text x="80" y="540" font-family="-apple-system,system-ui,sans-serif" font-size="22" fill="#faf7ef" opacity="0.7">Sam James · 20 · 70+ agents recruited · @theprincejamez</text>
</svg>'''


FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_post(p):
    t = p.read_text(); m = FM.match(t); body = t[m.end():] if m else t
    try: d = datetime.strptime(p.stem, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except: return None
    body = re.sub(r"^#\s*Content ideas.*?\n+", "", body, count=1)
    return {"date": d, "slug": p.stem, "body_html": body.strip()}


def parse_corner(p):
    t = p.read_text(); m = FM.match(t); fm = m.group(1) if m else ""; body = t[m.end():] if m else t
    g = lambda k: (re.search(rf"^{k}:\s*(.+)$", fm, re.M).group(1).strip().strip('"') if re.search(rf"^{k}:\s*(.+)$", fm, re.M) else "")
    return {"slug": p.stem, "title": g("title") or p.stem, "teaser": g("teaser"), "updated": g("updated"), "body_html": md(body.strip())}


def md(s):
    s = re.sub(r"^### (.+)$", r"<h3>\1</h3>", s, flags=re.M)
    s = re.sub(r"^## (.+)$", r"<h2>\1</h2>", s, flags=re.M)
    s = re.sub(r"^# (.+)$", r"<h2>\1</h2>", s, flags=re.M)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"<em>\1</em>", s)
    out, in_ul = [], False
    for ln in s.split("\n"):
        if re.match(r"^- ", ln):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{ln[2:]}</li>")
        elif re.match(r"^\d+\. ", ln):
            if not in_ul: out.append("<ol>"); in_ul = "ol"
            out.append(f"<li>{re.sub(r'^[0-9]+\\. ', '', ln)}</li>")
        else:
            if in_ul: out.append("</ul>" if in_ul is True else "</ol>"); in_ul = False
            out.append(ln)
    if in_ul: out.append("</ul>" if in_ul is True else "</ol>")
    s = "\n".join(out)
    par = []
    for c in re.split(r"\n\n+", s):
        if c.strip().startswith("<"): par.append(c)
        elif c.strip(): par.append(f"<p>{c.strip()}</p>")
    return "\n\n".join(par)


def rss(posts):
    items = []
    for p in posts[:30]:
        url = f"{BASE}/{p['slug']}.html"; d = p["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")
        items.append(f"<item><title>Daily Edge — {p['date'].strftime('%B %d, %Y')}</title><link>{url}</link><guid>{url}</guid><pubDate>{d}</pubDate></item>")
    return f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(TITLE)}</title><link>{BASE}/</link><description>{esc(DESC)}</description>{"".join(items)}</channel></rss>'


def sitemap(posts, corns):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"<url><loc>{BASE}/</loc><lastmod>{today}</lastmod></url>"]
    for u in ["platform.html", "course.html", "leads.html", "audit.html", "mentor.html", "pdf.html"]:
        urls.append(f"<url><loc>{BASE}/{u}</loc><lastmod>{today}</lastmod></url>")
    for slug, _ in STATES:
        urls.append(f"<url><loc>{BASE}/states/{slug}.html</loc><lastmod>{today}</lastmod></url>")
    for c in corns:
        urls.append(f"<url><loc>{BASE}/{c['slug']}.html</loc><lastmod>{today}</lastmod></url>")
    for p in posts:
        urls.append(f"<url><loc>{BASE}/{p['slug']}.html</loc><lastmod>{p['date'].strftime('%Y-%m-%d')}</lastmod></url>")
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(urls)}</urlset>'


def main():
    posts = []
    if SOURCE.exists():
        for p in sorted(SOURCE.glob("*.md"), reverse=True):
            x = parse_post(p)
            if x: posts.append(x); (DOCS / f"{x['slug']}.html").write_text(post(x))
    corns = []
    if CORNER.exists():
        for p in sorted(CORNER.glob("*.md")):
            c = parse_corner(p); corns.append(c); (DOCS / f"{c['slug']}.html").write_text(corner(c))
    (DOCS / "index.html").write_text(home(posts, corns))
    (DOCS / "platform.html").write_text(platform())
    (DOCS / "course.html").write_text(course())
    (DOCS / "leads.html").write_text(leads())
    (DOCS / "audit.html").write_text(audit())
    (DOCS / "mentor.html").write_text(mentor())
    (DOCS / "pdf.html").write_text(pdf())
    states_dir = DOCS / "states"
    states_dir.mkdir(exist_ok=True)
    for slug, name in STATES:
        (states_dir / f"{slug}.html").write_text(state_page(slug, name))
    (DOCS / "og-image.svg").write_text(og_svg())
    (DOCS / "rss.xml").write_text(rss(posts))
    (DOCS / "sitemap.xml").write_text(sitemap(posts, corns))
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {BASE}/sitemap.xml\n")
    (DOCS / "CNAME").touch()
    # Copy static/ (admin pages, anything verbatim) into docs/
    STATIC = ROOT / "static"
    if STATIC.exists():
        import shutil
        for src in STATIC.rglob("*"):
            if src.is_file():
                rel = src.relative_to(STATIC)
                dst = DOCS / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    print(f"built {len(posts)} posts + {len(corns)} cornerstones")


if __name__ == "__main__":
    main()
