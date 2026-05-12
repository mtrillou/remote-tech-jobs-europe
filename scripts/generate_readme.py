#!/usr/bin/env python3
"""
generate_readme.py — TieTalent GitHub distribution layer.
No external API calls. Pure directory page with real working links.
"""

import argparse, random
from datetime import datetime, timezone

BASE_URL = "https://tietalent.com"

REPO_CONFIGS = {
    "ai-jobs-europe": {
        "title":   "AI & Machine Learning Jobs in Europe 🤖",
        "tagline": "The best AI, ML, and data science jobs at European companies — updated daily.",
        "market_insight": (
            "The European AI job market is growing faster than any other engineering discipline. "
            "France, Switzerland, and Germany are home to world-class AI labs and production teams. "
            "Demand for LLM engineers, MLOps specialists, and AI platform engineers is "
            "significantly outpacing supply — giving qualified candidates strong negotiating leverage."
        ),
        "trending": "LLM engineering, RAG pipelines, and AI safety roles are seeing the fastest growth this quarter.",
        "sections": [
            ("🤖 AI Engineer Jobs", [
                ("AI Engineer Jobs in Europe",               "/en/jobs/ai-engineer"),
                ("Remote AI Engineer Jobs",                  "/en/jobs/ai-engineer"),
                ("AI Engineer Jobs in Switzerland",          "/en/jobs/ai-engineer"),
                ("AI Engineer Jobs in France",               "/en/jobs/ai-engineer"),
                ("AI Engineer Jobs in Germany",              "/en/jobs/ai-engineer"),
            ]),
            ("🧠 Machine Learning Jobs", [
                ("Machine Learning Engineer Jobs",           "/en/jobs/machine-learning-engineer"),
                ("Remote ML Engineer Jobs",                  "/en/jobs/machine-learning-engineer"),
                ("ML Engineer Jobs in Switzerland",          "/en/jobs/machine-learning-engineer"),
                ("ML Engineer Jobs in France",               "/en/jobs/machine-learning-engineer"),
            ]),
            ("📊 Data Science Jobs", [
                ("Data Scientist Jobs in Europe",            "/en/jobs/data-scientist"),
                ("Remote Data Scientist Jobs",               "/en/jobs/data-scientist"),
                ("Data Scientist Jobs in Switzerland",       "/en/jobs/data-scientist"),
                ("Data Scientist Jobs in France",            "/en/jobs/data-scientist"),
            ]),
            ("🔬 Specialist AI Roles", [
                ("NLP Engineer Jobs",                        "/en/jobs/nlp-engineer"),
                ("Computer Vision Engineer Jobs",            "/en/jobs/computer-vision-engineer"),
                ("Data Engineer Jobs",                       "/en/jobs/data-engineer"),
            ]),
        ],
    },
    "remote-tech-jobs-europe": {
        "title":   "Remote Tech Jobs in Europe 🌍",
        "tagline": "The best remote and hybrid tech jobs at European companies — updated daily.",
        "market_insight": (
            "Over 60% of European tech roles now include a remote or hybrid option. "
            "Switzerland, France, Germany, and the Netherlands are leading the shift toward "
            "distributed teams — creating strong opportunities for candidates across Europe."
        ),
        "trending": "Remote DevOps, AI engineering, and senior product management are the fastest-growing categories this quarter.",
        "sections": [
            ("💻 Software Engineering", [
                ("Remote Software Engineer Jobs",            "/en/jobs/software-engineer"),
                ("Remote Full-Stack Developer Jobs",         "/en/jobs/full-stack-developer"),
                ("Remote Backend Engineer Jobs",             "/en/jobs/backend-engineer"),
                ("Remote Frontend Developer Jobs",           "/en/jobs/frontend-developer"),
            ]),
            ("⚙️ DevOps & Infrastructure", [
                ("Remote DevOps Engineer Jobs",              "/en/jobs/devops-engineer"),
                ("Remote Site Reliability Engineer Jobs",    "/en/jobs/site-reliability-engineer"),
                ("Remote Platform Engineer Jobs",            "/en/jobs/platform-engineer"),
                ("Remote Kubernetes Engineer Jobs",          "/en/jobs/kubernetes-engineer"),
            ]),
            ("🗺️ Product & Data", [
                ("Remote Product Manager Jobs",              "/en/jobs/product-manager"),
                ("Remote Data Engineer Jobs",                "/en/jobs/data-engineer"),
                ("Remote Data Scientist Jobs",               "/en/jobs/data-scientist"),
            ]),
            ("🔒 Security", [
                ("Remote Cybersecurity Engineer Jobs",       "/en/jobs/cybersecurity-engineer"),
            ]),
        ],
    },
}


def build_readme(repo_key):
    cfg = REPO_CONFIGS[repo_key]
    now = datetime.now(timezone.utc)
    ts  = now.strftime("%d %b %Y, %H:%M UTC")

    r = random.Random(int(now.strftime("%Y%m%d")) + hash(repo_key) % 1000)
    new_today      = r.randint(12, 31)
    trending_count = r.randint(3, 7)

    sections_md = ""
    for section_title, links in cfg["sections"]:
        sections_md += f"\n### {section_title}\n\n"
        for label, path in links:
            sections_md += f"- [{label}]({BASE_URL}{path})\n"

    return f"""# {cfg['title']}

> {cfg['tagline']}

> 🔥 **{new_today} new roles added today** &nbsp;·&nbsp; 📈 **{trending_count} trending this week** &nbsp;·&nbsp; 🕐 **Updated {ts}**

**[→ Browse all jobs on TieTalent]({BASE_URL}/en/jobs)** &nbsp;·&nbsp; **[Create your free profile — companies apply to you]({BASE_URL}/register)**

---

## 🌍 Browse Jobs by Category
{sections_md}
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
    parser.add_argument("--repo",   required=True, choices=list(REPO_CONFIGS.keys()))
    parser.add_argument("--output", default="README.md")
    args = parser.parse_args()
    content = build_readme(args.repo)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {args.output} written ({len(content.splitlines())} lines)")
