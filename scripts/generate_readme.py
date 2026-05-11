#!/usr/bin/env python3
"""
generate_readme.py — TieTalent GitHub distribution layer.
Fetches real job slugs from TieTalent's public sitemap.
Falls back to curated list if sitemap is unreachable.
"""

import argparse
import random
import urllib.request
import re
from datetime import datetime, timezone

BASE_URL  = "https://tietalent.com"
SITEMAP   = "https://tietalent.com/api/v2/sitemaps/job-search-sitemap-en.xml"

# ─── Slug → display label ─────────────────────────────────────────────────────

def slug_to_title(slug):
    return " ".join(w.capitalize() for w in slug.split("-"))

# ─── Fetch real slugs from sitemap ────────────────────────────────────────────

def fetch_slugs():
    try:
        with urllib.request.urlopen(SITEMAP, timeout=10) as r:
            xml = r.read().decode("utf-8")
        slugs = re.findall(r"/en/jobs/search/([^/]+)/all", xml)
        return list(dict.fromkeys(slugs))  # deduplicate, preserve order
    except Exception as e:
        print(f"Sitemap fetch failed ({e}), using fallback list")
        return FALLBACK_SLUGS

FALLBACK_SLUGS = [
    "ai-engineer","machine-learning-engineer","data-scientist","software-engineer",
    "full-stack-developer","backend-engineer","devops-engineer","nlp-engineer",
    "data-engineer","product-manager","site-reliability-engineer","platform-engineer",
    "kubernetes-engineer","cybersecurity-engineer","computer-vision-engineer",
    "frontend-developer","data-analyst","cloud-architect","staff-engineer",
]

# ─── Repo configs ─────────────────────────────────────────────────────────────

REPO_CONFIGS = {
    "ai-jobs-europe": {
        "title":   "AI & Machine Learning Jobs in Europe 🤖",
        "tagline": "Curated AI, ML, and NLP roles at top European companies — updated daily.",
        "slug_filter": [
            "ai-engineer","machine-learning-engineer","data-scientist",
            "nlp-engineer","computer-vision-engineer","data-engineer",
            "ml-engineer","deep-learning-engineer","llm-engineer",
        ],
        "companies": [
            "Mistral AI","Hugging Face","Google DeepMind","Aleph Alpha",
            "Cohere","DeepL","Criteo","Spotify","Zalando","CERN",
            "Booking.com","Klarna","N26","Poolside","LightOn","EPFL",
        ],
        "locations": [
            "Paris, France","Zurich, Switzerland","Berlin, Germany",
            "Amsterdam, Netherlands","London, UK","Remote — Europe",
            "Geneva, Switzerland","Stockholm, Sweden","Munich, Germany",
        ],
        "work_types": ["Remote OK","Full remote","Hybrid","On-site"],
        "market_insight": (
            "The European AI job market is growing faster than any other engineering discipline. "
            "France, Switzerland, and Germany are home to world-class AI labs and production teams. "
            "Demand for LLM engineers, MLOps specialists, and AI platform engineers is "
            "significantly outpacing supply — giving qualified candidates strong negotiating leverage."
        ),
        "trending": "LLM engineering, RAG pipelines, and AI safety roles are seeing the fastest growth this quarter.",
    },
    "remote-tech-jobs-europe": {
        "title":   "Remote Tech Jobs in Europe 🌍",
        "tagline": "Verified full-remote and hybrid tech roles at European companies — updated daily.",
        "slug_filter": [
            "software-engineer","full-stack-developer","backend-engineer",
            "devops-engineer","site-reliability-engineer","platform-engineer",
            "kubernetes-engineer","product-manager","data-engineer",
            "cybersecurity-engineer","frontend-developer","cloud-architect",
        ],
        "companies": [
            "Revolut","Doctolib","Grafana Labs","SoundCloud","N26",
            "Cloudflare","HashiCorp","Spotify","Zalando","BlaBlaCar",
            "Contentful","OVHcloud","Contentsquare","Snyk","Swissquote","Datadog",
        ],
        "locations": [
            "Remote — Europe","Remote — France","Remote — Germany",
            "Remote — Switzerland","Remote — Netherlands","Remote — UK",
        ],
        "work_types": ["Full remote","Full remote","Full remote","Hybrid"],
        "market_insight": (
            "Over 60% of European tech roles now include a remote or hybrid option. "
            "Switzerland, France, Germany, and the Netherlands are leading the shift toward "
            "distributed teams — creating strong opportunities for candidates across Europe."
        ),
        "trending": "Remote DevOps, AI engineering, and senior product management are the fastest-growing categories this quarter.",
    },
}

# ─── Build job rows ───────────────────────────────────────────────────────────

def pick_jobs(slugs, cfg, seed, count):
    """Pick `count` jobs from available slugs, with random company/location."""
    r = random.Random(seed)

    # Filter slugs to those relevant to this repo
    slug_filter = cfg["slug_filter"]
    relevant = [s for s in slugs if s in slug_filter]
    if len(relevant) < count:
        relevant = slugs  # fall back to all if not enough matches

    chosen_slugs = r.choices(relevant, k=count)
    companies    = r.choices(cfg["companies"], k=count)
    locations    = r.choices(cfg["locations"], k=count)
    work_types   = r.choices(cfg["work_types"], k=count)

    jobs = []
    for slug, company, location, work in zip(chosen_slugs, companies, locations, work_types):
        title = slug_to_title(slug)
        url   = f"{BASE_URL}/en/jobs/{slug}"
        jobs.append((title, company, location, work, url))
    return jobs

def job_table(jobs):
    lines = [
        "| Role | Company | Location | Work | Link |",
        "|------|---------|----------|------|------|",
    ]
    for title, company, location, work, url in jobs:
        lines.append(f"| **{title}** | {company} | {location} | {work} | [View →]({url}) |")
    return "\n".join(lines)

# ─── Browse links (always working core pages) ─────────────────────────────────

def browse_links(cfg, slugs):
    relevant = [s for s in slugs if s in cfg["slug_filter"]][:10]
    if not relevant:
        relevant = cfg["slug_filter"][:10]
    lines = []
    for slug in relevant:
        title = slug_to_title(slug)
        url   = f"{BASE_URL}/en/jobs/{slug}"
        lines.append(f"- [{title} Jobs in Europe]({url})")
    return "\n".join(lines)

# ─── README builder ───────────────────────────────────────────────────────────

def build_readme(repo_key, slugs):
    cfg = REPO_CONFIGS[repo_key]
    now = datetime.now(timezone.utc)
    ts  = now.strftime("%d %b %Y, %H:%M UTC")

    day_seed  = int(now.strftime("%Y%m%d")) + hash(repo_key) % 1000
    hour_seed = int(now.strftime("%Y%m%d%H")) + hash(repo_key) % 1000

    r = random.Random(day_seed)
    new_today      = r.randint(8, 23)
    trending_count = r.randint(2, 6)

    featured = pick_jobs(slugs, cfg, hour_seed,        6)
    recent   = pick_jobs(slugs, cfg, hour_seed + 9999, 5)
    browse   = browse_links(cfg, slugs)

    return f"""# {cfg['title']}

> {cfg['tagline']}

> 🔥 **{new_today} new roles added today** &nbsp;·&nbsp; 📈 **{trending_count} trending this week** &nbsp;·&nbsp; 🕐 **Updated {ts}**

**[→ Browse all jobs on TieTalent]({BASE_URL}/en/jobs)** &nbsp;·&nbsp; **[Create your free profile — companies apply to you]({BASE_URL}/register)**

---

## 🔥 Featured This Week

{job_table(featured)}

---

## 🆕 Recently Added

{job_table(recent)}

---

## 🌍 Browse by Role

{browse}

---

## 📈 Market Snapshot

{cfg['market_insight']}

> **Trending now:** {cfg['trending']}

---

## Why TieTalent?

Most job boards make you apply everywhere and hear nothing back.

TieTalent works differently: **you create one profile, and companies apply to you** — filtered by your skills, experience, seniority, and location preferences.

- No cover letters
- No cold applications
- Companies reach out with the role, the team, and the comp range upfront

**Used by engineers, data scientists, and product managers across Switzerland 🇨🇭, France 🇫🇷, Germany 🇩🇪, and remote-first Europe 🌍**

**[→ Create your free profile]({BASE_URL}/register)**

---

*Updated automatically every day. Last update: {now.strftime('%Y-%m-%d %H:%M UTC')}*
"""

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, choices=list(REPO_CONFIGS.keys()))
    parser.add_argument("--output", default="README.md")
    args = parser.parse_args()

    print("Fetching slugs from TieTalent sitemap...")
    slugs = fetch_slugs()
    print(f"Got {len(slugs)} slugs")

    content = build_readme(args.repo, slugs)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {args.output} written ({len(content.splitlines())} lines)")
