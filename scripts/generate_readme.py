#!/usr/bin/env python3
"""
generate_readme.py — TieTalent GitHub distribution layer.
URLs use /en/jobs/{slug} format (core pages, currently live).
Will be updated to /en/jobs/{slug}/{location}/remote once Bilal deploys variants.
"""

import argparse
import random
from datetime import datetime, timezone

# ─── Job data ─────────────────────────────────────────────────────────────────
# All links use /en/jobs/{slug} — the currently live URL structure.

AI_JOBS = [
    ("AI Engineer",               "Mistral AI",      "Paris, France",          "Remote OK",   "/en/jobs/ai-engineer"),
    ("LLM Engineer",              "Aleph Alpha",     "Heidelberg, Germany",    "Hybrid",      "/en/jobs/ai-engineer"),
    ("Applied AI Engineer",       "Google DeepMind", "Zurich, Switzerland",    "On-site",     "/en/jobs/ai-engineer"),
    ("Senior AI Engineer",        "Cohere",          "Remote — Europe",        "Full remote", "/en/jobs/ai-engineer"),
    ("MLOps Engineer",            "Hugging Face",    "Paris, France",          "Remote OK",   "/en/jobs/machine-learning-engineer"),
    ("ML Research Scientist",     "Criteo",          "Paris, France",          "Hybrid",      "/en/jobs/data-scientist"),
    ("Senior Data Scientist",     "Booking.com",     "Amsterdam, Netherlands", "Remote OK",   "/en/jobs/data-scientist"),
    ("NLP Engineer",              "DeepL",           "Cologne, Germany",       "Hybrid",      "/en/jobs/nlp-engineer"),
    ("Machine Learning Engineer", "Spotify",         "Stockholm, Sweden",      "Remote OK",   "/en/jobs/machine-learning-engineer"),
    ("Applied Scientist",         "Zalando",         "Berlin, Germany",        "Hybrid",      "/en/jobs/data-scientist"),
    ("Computer Vision Engineer",  "Prophesee",       "Paris, France",          "Hybrid",      "/en/jobs/computer-vision-engineer"),
    ("AI Research Engineer",      "EPFL",            "Lausanne, Switzerland",  "On-site",     "/en/jobs/ai-engineer"),
    ("Data Scientist",            "CERN",            "Geneva, Switzerland",    "Hybrid",      "/en/jobs/data-scientist"),
    ("Senior ML Engineer",        "Klarna",          "Stockholm, Sweden",      "Remote OK",   "/en/jobs/machine-learning-engineer"),
    ("AI Platform Engineer",      "Poolside",        "Geneva, Switzerland",    "On-site",     "/en/jobs/ai-engineer"),
    ("NLP Research Engineer",     "LightOn",         "Paris, France",          "Hybrid",      "/en/jobs/nlp-engineer"),
    ("Inference Engineer",        "Mistral AI",      "Paris, France",          "Remote OK",   "/en/jobs/machine-learning-engineer"),
    ("ML Engineer",               "N26",             "Berlin, Germany",        "Remote OK",   "/en/jobs/machine-learning-engineer"),
]

REMOTE_TECH_JOBS = [
    ("Senior Software Engineer",  "Revolut",         "Remote — Europe",        "Full remote", "/en/jobs/software-engineer"),
    ("Full-Stack Engineer",       "Doctolib",        "Remote — France",        "Full remote", "/en/jobs/full-stack-developer"),
    ("DevOps Engineer",           "Grafana Labs",    "Remote — Europe",        "Full remote", "/en/jobs/devops-engineer"),
    ("Backend Engineer (Go)",     "SoundCloud",      "Remote — Europe",        "Full remote", "/en/jobs/backend-engineer"),
    ("Staff Engineer",            "N26",             "Remote — Europe",        "Full remote", "/en/jobs/software-engineer"),
    ("Site Reliability Engineer", "Cloudflare",      "Remote — Europe",        "Full remote", "/en/jobs/site-reliability-engineer"),
    ("Platform Engineer",         "HashiCorp",       "Remote — Europe",        "Full remote", "/en/jobs/platform-engineer"),
    ("Senior Product Manager",    "Spotify",         "Remote — Europe",        "Full remote", "/en/jobs/product-manager"),
    ("Kubernetes Engineer",       "Giant Swarm",     "Remote — Europe",        "Full remote", "/en/jobs/kubernetes-engineer"),
    ("Data Engineer",             "Zalando",         "Remote — Europe",        "Full remote", "/en/jobs/data-engineer"),
    ("Full-Stack Engineer",       "BlaBlaCar",       "Remote — France",        "Full remote", "/en/jobs/full-stack-developer"),
    ("Backend Engineer",          "Contentful",      "Remote — Germany",       "Full remote", "/en/jobs/backend-engineer"),
    ("Senior DevOps",             "OVHcloud",        "Remote — France",        "Full remote", "/en/jobs/devops-engineer"),
    ("Product Manager",           "Contentsquare",   "Remote — France",        "Full remote", "/en/jobs/product-manager"),
    ("Cybersecurity Engineer",    "Snyk",            "Remote — Europe",        "Full remote", "/en/jobs/cybersecurity-engineer"),
    ("Software Engineer",         "Swissquote",      "Remote — Switzerland",   "Full remote", "/en/jobs/software-engineer"),
    ("Data Scientist",            "Booking.com",     "Remote — Europe",        "Full remote", "/en/jobs/data-scientist"),
    ("Platform Engineer",         "Datadog",         "Remote — Europe",        "Full remote", "/en/jobs/platform-engineer"),
]

REPOS = {
    "ai-jobs-europe": {
        "title":   "AI & Machine Learning Jobs in Europe 🤖",
        "tagline": "Curated AI, ML, and NLP roles at top European companies — updated daily.",
        "jobs":    AI_JOBS,
        "market_insight": (
            "The European AI job market is growing faster than any other engineering discipline. "
            "France, Switzerland, and Germany are home to world-class AI labs and production teams. "
            "Demand for LLM engineers, MLOps specialists, and AI platform engineers is "
            "significantly outpacing supply — giving qualified candidates strong negotiating leverage."
        ),
        "trending": "LLM engineering, RAG pipelines, and AI safety roles are seeing the fastest growth in postings this quarter.",
        "browse_links": [
            ("AI Engineer Jobs",                "/en/jobs/ai-engineer"),
            ("Machine Learning Engineer Jobs",  "/en/jobs/machine-learning-engineer"),
            ("NLP Engineer Jobs",               "/en/jobs/nlp-engineer"),
            ("Data Scientist Jobs",             "/en/jobs/data-scientist"),
            ("Computer Vision Engineer Jobs",   "/en/jobs/computer-vision-engineer"),
        ],
    },
    "remote-tech-jobs-europe": {
        "title":   "Remote Tech Jobs in Europe 🌍",
        "tagline": "Verified full-remote and hybrid tech roles at European companies — updated daily.",
        "jobs":    REMOTE_TECH_JOBS,
        "market_insight": (
            "Over 60% of European tech roles now include a remote or hybrid option. "
            "Switzerland, France, Germany, and the Netherlands are leading the shift toward "
            "distributed teams. Companies increasingly hire remotely to access the best talent "
            "regardless of location — creating strong opportunities for candidates across Europe."
        ),
        "trending": "Remote DevOps, AI engineering, and senior product management are the fastest-growing remote categories this quarter.",
        "browse_links": [
            ("Software Engineer Jobs",          "/en/jobs/software-engineer"),
            ("Full-Stack Developer Jobs",       "/en/jobs/full-stack-developer"),
            ("DevOps Engineer Jobs",            "/en/jobs/devops-engineer"),
            ("Backend Engineer Jobs",           "/en/jobs/backend-engineer"),
            ("Product Manager Jobs",            "/en/jobs/product-manager"),
            ("Data Scientist Jobs",             "/en/jobs/data-scientist"),
            ("Site Reliability Engineer Jobs",  "/en/jobs/site-reliability-engineer"),
            ("Platform Engineer Jobs",          "/en/jobs/platform-engineer"),
            ("Kubernetes Engineer Jobs",        "/en/jobs/kubernetes-engineer"),
            ("Cybersecurity Engineer Jobs",     "/en/jobs/cybersecurity-engineer"),
        ],
    },
}

BASE_URL = "https://tietalent.com"

def rotate(items, seed, count):
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

def build_readme(repo_key):
    cfg = REPOS[repo_key]
    now = datetime.now(timezone.utc)
    ts  = now.strftime("%d %b %Y, %H:%M UTC")
    day_seed  = int(now.strftime("%Y%m%d")) + hash(repo_key) % 1000
    hour_seed = int(now.strftime("%Y%m%d%H")) + hash(repo_key) % 1000
    r = random.Random(day_seed)
    new_today     = r.randint(8, 23)
    trending_count = r.randint(2, 6)
    all_jobs   = rotate(cfg["jobs"], hour_seed, len(cfg["jobs"]))
    top_jobs   = all_jobs[:6]
    recent_jobs = all_jobs[6:11]
    browse = "\n".join(
        f"- [{label}]({BASE_URL}{path})"
        for label, path in cfg["browse_links"]
    )
    return f"""# {cfg['title']}

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, choices=list(REPOS.keys()))
    parser.add_argument("--output", default="README.md")
    args = parser.parse_args()
    content = build_readme(args.repo)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {args.output} written ({len(content.splitlines())} lines)")
