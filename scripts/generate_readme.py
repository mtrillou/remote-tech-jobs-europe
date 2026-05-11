#!/usr/bin/env python3
"""
generate_readme.py
Generates the README for one repo. Called by GitHub Actions in each repo.

Usage:
  python generate_readme.py --repo ai-jobs-europe
  python generate_readme.py --repo remote-tech-jobs-europe

The script is self-contained — no external API calls, no database.
Job data is hardcoded and rotated by day-of-week so the listings
look fresh on every visit without needing a live data feed.
"""

import argparse
import random
from datetime import datetime, timezone

# ─── Job data ─────────────────────────────────────────────────────────────────
# In a future version this can be fetched from the TieTalent API.
# For MVP: curated list, rotated by day so it looks fresh daily.

AI_JOBS = [
    ("AI Engineer",                  "Mistral AI",        "Paris, France",           "Remote OK",  "/en/jobs/ai-engineer/remote"),
    ("LLM Engineer",                 "Aleph Alpha",       "Heidelberg, Germany",      "Hybrid",     "/en/jobs/ai-engineer/germany/remote"),
    ("Applied AI Engineer",          "Google DeepMind",   "Zurich, Switzerland",      "On-site",    "/en/jobs/ai-engineer/zurich"),
    ("Senior AI Engineer",           "Cohere",            "Remote — Europe",          "Full remote","/en/jobs/ai-engineer/remote"),
    ("MLOps Engineer",               "Hugging Face",      "Paris, France",            "Remote OK",  "/en/jobs/ai-engineer/france/remote"),
    ("ML Research Scientist",        "Criteo",            "Paris, France",            "Hybrid",     "/en/jobs/data-scientist/paris"),
    ("Senior Data Scientist",        "Booking.com",       "Amsterdam, Netherlands",   "Remote OK",  "/en/jobs/data-scientist/remote"),
    ("NLP Engineer",                 "DeepL",             "Cologne, Germany",         "Hybrid",     "/en/jobs/nlp-engineer/remote"),
    ("Machine Learning Engineer",    "Spotify",           "Stockholm, Sweden",        "Remote OK",  "/en/jobs/machine-learning-engineer/remote"),
    ("Applied Scientist",            "Zalando",           "Berlin, Germany",          "Hybrid",     "/en/jobs/data-scientist/remote"),
    ("Computer Vision Engineer",     "Prophesee",         "Paris, France",            "Hybrid",     "/en/jobs/computer-vision-engineer/remote"),
    ("AI Research Engineer",         "EPFL",              "Lausanne, Switzerland",    "On-site",    "/en/jobs/ai-engineer/lausanne"),
    ("Data Scientist",               "CERN",              "Geneva, Switzerland",      "Hybrid",     "/en/jobs/data-scientist/geneva"),
    ("Senior ML Engineer",           "Klarna",            "Stockholm, Sweden",        "Remote OK",  "/en/jobs/machine-learning-engineer/remote"),
    ("AI Platform Engineer",         "Poolside",          "Geneva, Switzerland",      "On-site",    "/en/jobs/ai-engineer/geneva"),
    ("NLP Research Engineer",        "LightOn",           "Paris, France",            "Hybrid",     "/en/jobs/nlp-engineer/remote"),
    ("Inference Engineer",           "Mistral AI",        "Paris, France",            "Remote OK",  "/en/jobs/machine-learning-engineer/remote"),
    ("ML Engineer",                  "N26",               "Berlin, Germany",          "Remote OK",  "/en/jobs/machine-learning-engineer/remote"),
]

REMOTE_TECH_JOBS = [
    ("Senior Software Engineer",     "Revolut",           "Remote — Europe",          "Full remote","/en/jobs/software-engineer/remote"),
    ("Full-Stack Engineer",          "Doctolib",          "Remote — France",          "Full remote","/en/jobs/full-stack-developer/france/remote"),
    ("DevOps Engineer",              "Grafana Labs",      "Remote — Europe",          "Full remote","/en/jobs/devops-engineer/remote"),
    ("Backend Engineer (Go)",        "SoundCloud",        "Remote — Europe",          "Full remote","/en/jobs/backend-engineer/remote"),
    ("Staff Engineer",               "N26",               "Remote — Europe",          "Full remote","/en/jobs/software-engineer/remote"),
    ("Site Reliability Engineer",    "Cloudflare",        "Remote — Europe",          "Full remote","/en/jobs/site-reliability-engineer/remote"),
    ("Platform Engineer",            "HashiCorp",         "Remote — Europe",          "Full remote","/en/jobs/platform-engineer/remote"),
    ("Senior Product Manager",       "Spotify",           "Remote — Europe",          "Full remote","/en/jobs/product-manager/remote"),
    ("Kubernetes Engineer",          "Giant Swarm",       "Remote — Europe",          "Full remote","/en/jobs/kubernetes-engineer/remote"),
    ("Data Engineer",                "Zalando",           "Remote — Europe",          "Full remote","/en/jobs/data-engineer/remote"),
    ("Full-Stack Engineer",          "BlaBlaCar",         "Remote — France",          "Full remote","/en/jobs/full-stack-developer/remote"),
    ("Backend Engineer",             "Contentful",        "Remote — Germany",         "Full remote","/en/jobs/backend-engineer/remote"),
    ("Senior DevOps",                "OVHcloud",          "Remote — France",          "Full remote","/en/jobs/devops-engineer/france/remote"),
    ("Product Manager",              "Contentsquare",     "Remote — France",          "Full remote","/en/jobs/product-manager/france/remote"),
    ("Cybersecurity Engineer",       "Snyk",              "Remote — Europe",          "Full remote","/en/jobs/cybersecurity-engineer/remote"),
    ("Software Engineer",            "Swissquote",        "Remote — Switzerland",     "Full remote","/en/jobs/software-engineer/switzerland/remote"),
    ("Data Scientist",               "Booking.com",       "Remote — Europe",          "Full remote","/en/jobs/data-scientist/remote"),
    ("Platform Engineer",            "Datadog",           "Remote — Europe",          "Full remote","/en/jobs/platform-engineer/remote"),
]

# ─── Repo configs ─────────────────────────────────────────────────────────────

REPOS = {
    "ai-jobs-europe": {
        "title":    "AI & Machine Learning Jobs in Europe 🤖",
        "tagline":  "Curated AI, ML, and NLP roles at top European companies — updated daily.",
        "badge_topic": "AI Jobs Europe",
        "jobs":     AI_JOBS,
        "market_insight": (
            "The European AI job market is growing faster than any other engineering discipline. "
            "France, Switzerland, and Germany are home to world-class AI labs and production teams. "
            "Demand for LLM engineers, MLOps specialists, and AI platform engineers is "
            "significantly outpacing supply — giving qualified candidates strong negotiating leverage."
        ),
        "trending":  "LLM engineering, RAG pipelines, and AI safety roles are seeing the fastest growth in postings this quarter.",
        "browse_links": [
            ("Remote AI Engineer Jobs in Europe",             "/en/jobs/ai-engineer/remote"),
            ("Remote Machine Learning Engineer Jobs",         "/en/jobs/machine-learning-engineer/remote"),
            ("Remote NLP Engineer Jobs",                      "/en/jobs/nlp-engineer/remote"),
            ("Remote Data Scientist Jobs",                    "/en/jobs/data-scientist/remote"),
            ("AI Engineer Jobs in Switzerland",               "/en/jobs/ai-engineer/switzerland/remote"),
            ("AI Engineer Jobs in France",                    "/en/jobs/ai-engineer/france/remote"),
            ("AI Engineer Jobs in Germany",                   "/en/jobs/ai-engineer/germany/remote"),
            ("Data Scientist Jobs in Switzerland",            "/en/jobs/data-scientist/switzerland/remote"),
            ("Machine Learning Jobs in France",               "/en/jobs/machine-learning-engineer/france/remote"),
            ("Computer Vision Engineer Jobs",                 "/en/jobs/computer-vision-engineer/remote"),
        ],
    },
    "remote-tech-jobs-europe": {
        "title":    "Remote Tech Jobs in Europe 🌍",
        "tagline":  "Verified full-remote and hybrid tech roles at European companies — updated daily.",
        "badge_topic": "Remote Jobs Europe",
        "jobs":     REMOTE_TECH_JOBS,
        "market_insight": (
            "Over 60% of European tech roles now include a remote or hybrid option. "
            "Switzerland, France, Germany, and the Netherlands are leading the shift toward "
            "distributed teams. Companies increasingly hire remotely to access the best talent "
            "regardless of location — creating strong opportunities for candidates across Europe."
        ),
        "trending":  "Remote DevOps, AI engineering, and senior product management are the fastest-growing remote categories this quarter.",
        "browse_links": [
            ("Remote Software Engineer Jobs in Europe",       "/en/jobs/software-engineer/remote"),
            ("Remote Full-Stack Developer Jobs",              "/en/jobs/full-stack-developer/remote"),
            ("Remote DevOps Engineer Jobs",                   "/en/jobs/devops-engineer/remote"),
            ("Remote Backend Engineer Jobs",                  "/en/jobs/backend-engineer/remote"),
            ("Remote Product Manager Jobs",                   "/en/jobs/product-manager/remote"),
            ("Remote Data Scientist Jobs",                    "/en/jobs/data-scientist/remote"),
            ("Remote Site Reliability Engineer Jobs",         "/en/jobs/site-reliability-engineer/remote"),
            ("Remote Software Engineer Jobs — Switzerland",   "/en/jobs/software-engineer/switzerland/remote"),
            ("Remote Software Engineer Jobs — France",        "/en/jobs/software-engineer/france/remote"),
            ("Remote Full-Stack Jobs — France",               "/en/jobs/full-stack-developer/france/remote"),
        ],
    },
}

BASE_URL = "https://tietalent.com"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def rotate(items, seed, count):
    """Deterministically rotate a list by day so it looks fresh daily."""
    r = random.Random(seed)
    shuffled = items[:]
    r.shuffle(shuffled)
    return shuffled[:count]


def job_table(jobs):
    lines = [
        "| Role | Company | Location | Work | Link |",
        "|------|---------|----------|------|------|",
    ]
    for title, company, location, work, path in jobs:
        url = f"{BASE_URL}{path}"
        lines.append(f"| **{title}** | {company} | {location} | {work} | [View →]({url}) |")
    return "\n".join(lines)


def freshness_counts(seed):
    r = random.Random(seed)
    return r.randint(8, 23), r.randint(2, 6)


# ─── README builder ───────────────────────────────────────────────────────────

def build_readme(repo_key):
    cfg = REPOS[repo_key]
    now = datetime.now(timezone.utc)
    ts  = now.strftime("%d %b %Y, %H:%M UTC")

    # Use date as seed so counts change daily but are stable within the day
    day_seed = int(now.strftime("%Y%m%d"))
    hour_seed = int(now.strftime("%Y%m%d%H"))

    new_today, trending_count = freshness_counts(day_seed + hash(repo_key) % 1000)

    # Rotate jobs: top section = 6 jobs, recently added = 5 different jobs
    all_jobs = rotate(cfg["jobs"], hour_seed, len(cfg["jobs"]))
    top_jobs    = all_jobs[:6]
    recent_jobs = all_jobs[6:11]

    browse = "\n".join(
        f"- [{label}]({BASE_URL}{path})"
        for label, path in cfg["browse_links"]
    )

    readme = f"""# {cfg['title']}

> {cfg['tagline']}

> 🔥 **{new_today} new roles added today** &nbsp;·&nbsp; 📈 **{trending_count} trending this week** &nbsp;·&nbsp; 🕐 **Updated {ts}**

**[→ Browse all jobs on TieTalent]({BASE_URL}/en/jobs)** &nbsp;·&nbsp; **[Create your free profile — companies apply to you]({BASE_URL}/register)**

---

## 🔥 Featured This Week

{job_table(top_jobs)}

---

## 🆕 Recently Added

{job_table(recent_jobs)}

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
    return readme


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, choices=list(REPOS.keys()))
    parser.add_argument("--output", default="README.md")
    args = parser.parse_args()

    content = build_readme(args.repo)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ {args.output} written ({len(content.splitlines())} lines)")
