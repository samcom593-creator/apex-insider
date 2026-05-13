# APEX Nation — Daily Insider

Auto-published every day at ~15:30 UTC. Pulls content from Sam's daily AI content engine (in `claude-sync`), renders as a permanent SEO-optimized site, deploys to GitHub Pages.

**Live URL:** https://samcom593-creator.github.io/apex-insider/

**Purpose:** organic SEO + email capture → funnel to apex-financial.org/apply for agent recruiting.

## Architecture
- `scripts/build_site.py` — pure-Python static site generator
- `.github/workflows/build.yml` — daily build + deploy
- Content source: claude-sync's `memory/-Users-samjames/content-ideas/` (pulled in the workflow via GH_SYNC_TOKEN)

## Edit content
Don't edit `docs/` directly — it gets regenerated. Edit the source files in claude-sync's content-ideas archive (or change `scripts/build_site.py` for design changes).
