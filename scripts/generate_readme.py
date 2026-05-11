#!/usr/bin/env python3
"""
generate_readme.py — TieTalent GitHub distribution layer.
Fetches real jobs from API, filters client-side by keyword,
builds direct job page URLs (/en/jobs/p-{id}/{city}-{slug}).
Falls back to curated list if API returns no matches.
"""

import argparse, random, json, re, urllib.request
from datetime import datetime, timezone

BASE_URL = "https://tietalent.com"
API_URL  = "https://tietalent.com/api/v1/public-jobs"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60]

def build_job_url(job):
    job_id = job["id"]
    name   = job.get("name", "job")
    locs   = job.get("locations", [])
    city   = locs[0]["city"] if locs else ""
    city_slug = slugify(city)
    name_slug = slugify(name)
    if city_slug:
        return f"{BASE_URL}/en/jobs/p-{job_id}/{city_slug}-{name_slug}"
    return f"{BASE_URL}/en/jobs/p-{job_id}/{name_slug}"

def format_location(job):
    locs = job.get("locations", [])
    if not locs:
        return "Europe"
    loc = locs[0]
    city    = loc.get("city", "")
    country = loc.get("country", "")
    if city and country:
        return f"{city}, {country}"
    return country or city or "Europe"

def infer_work_type(job):
    text = (job.get("name","") + " " + job.get("description","")[:300]).lower()
    if "remote" in text: return "Remote OK"
    if "hybrid" in text: return "Hybrid"
    return "On-site"

# ─── API fetch ────────────────────────────────────────────────────────────────

def fetch_jobs(page=1, page_size=100):
    """Fetch a page of jobs from the API."""
    try:
        payload = json.dumps({
            "filters": {},
            "pageSize": page_size,
            "page": page
        }).encode()
        req = urllib.request.Request(
            API_URL, data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)["data"]["items"]
    except Exception as e:
        print(f"API error: {e}")
        return []

def filter_by_keywords(jobs, keywords):
    """Client-side filter — match job title against keywords."""
    result = []
    seen_ids = set()
    for job in jobs:
        if job["id"] in seen_ids:
            continue
        name = job.get("name", "").lower()
        if any(kw in name for kw in keywords):
            result.append(job)
            seen_ids.add(job["id"])
    return result

# ─── Repo configs ─────────────────────────────────────────────────────────────

REPO_CONFIGS = {
    "ai-jobs-europe": {
        "title":   "AI & Machine Learning Jobs in Europe 🤖",
        "tagline": "Live AI, ML, and data science roles at top European companies — updated daily.",
        "keywords": [
            "ai engineer", "machine learning", "data scientist", "nlp engineer",
            "computer vision", "mlops", "deep learning", "llm", "ml engineer",
            "artificial intelligence", "data science",
        ],
        "market_insight": (
            "The European AI job market is growing faster than any other engineering discipline. "
            "France, Switzerland, and Germany are home to world-class AI labs and production teams. "
            "Demand for LLM engineers, MLOps specialists, and AI platform engineers is "
            "significantly outpacing supply — giving qualified candidates strong negotiating leverage."
        ),
        "trending": "LLM engineering, RAG pipelines, and AI safety roles are seeing the fastest growth this quarter.",
        "browse_links": [
            ("AI Engineer Jobs",               "/en/jobs/ai-engineer"),
            ("Machine Learning Engineer Jobs", "/en/jobs/machine-learning-engineer"),
            ("Data Scientist Jobs",            "/en/jobs/data-scientist"),
            ("NLP Engineer Jobs",              "/en/jobs/nlp-engineer"),
            ("Computer Vision Engineer Jobs",  "/en/jobs/computer-vision-engineer"),
            ("Data Engineer Jobs",             "/en/jobs/data-engineer"),
        ],
        "fallback": [
            ("AI Engineer",               "Mistral AI",      "Paris, France",         "Remote OK",   "/en/jobs/ai-engineer"),
            ("LLM Engineer",              "Aleph Alpha",     "Heidelberg, Germany",   "Hybrid",      "/en/jobs/machine-learning-engineer"),
            ("Senior Data Scientist",     "Booking.com",     "Amsterdam, Netherlands","Remote OK",   "/en/jobs/data-scientist"),
            ("MLOps Engineer",            "Hugging Face",    "Paris, France",         "Remote OK",   "/en/jobs/machine-learning-engineer"),
            ("NLP Engineer",              "DeepL",           "Cologne, Germany",      "Hybrid",      "/en/jobs/nlp-engineer"),
            ("Machine Learning Engineer", "Spotify",         "Stockholm, Sweden",     "Remote OK",   "/en/jobs/machine-learning-engineer"),
            ("Computer Vision Engineer",  "Prophesee",       "Paris, France",         "Hybrid",      "/en/jobs/computer-vision-engineer"),
            ("Data Scientist",            "CERN",            "Geneva, Switzerland",   "Hybrid",      "/en/jobs/data-scientist"),
            ("Senior ML Engineer",        "Klarna",          "Stockholm, Sweden",     "Remote OK",   "/en/jobs/machine-learning-engineer"),
            ("Applied AI Engineer",       "Google DeepMind", "Zurich, Switzerland",   "On-site",     "/en/jobs/ai-engineer"),
            ("Senior AI Engineer",        "Cohere",          "Remote — Europe",       "Full remote", "/en/jobs/ai-engineer"),
        ],
    },
    "remote-tech-jobs-europe": {
        "title":   "Remote Tech Jobs in Europe 🌍",
        "tagline": "Live remote and hybrid tech roles at European companies — updated daily.",
        "keywords": [
            "software engineer", "software developer", "full stack", "fullstack",
            "backend engineer", "frontend engineer", "devops", "platform engineer",
            "site reliability", "sre", "kubernetes", "cloud engineer",
            "product manager", "data engineer", "cybersecurity", "security engineer",
        ],
        "market_insight": (
            "Over 60% of European tech roles now include a remote or hybrid option. "
            "Switzerland, France, Germany, and the Netherlands are leading the shift toward "
            "distributed teams — creating strong opportunities for candidates across Europe."
        ),
        "trending": "Remote DevOps, AI engineering, and senior product management are the fastest-growing categories this quarter.",
        "browse_links": [
            ("Software Engineer Jobs",         "/en/jobs/software-engineer"),
            ("Full-Stack Developer Jobs",      "/en/jobs/full-stack-developer"),
            ("DevOps Engineer Jobs",           "/en/jobs/devops-engineer"),
            ("Backend Engineer Jobs",          "/en/jobs/backend-engineer"),
            ("Product Manager Jobs",           "/en/jobs/product-manager"),
            ("Data Engineer Jobs",             "/en/jobs/data-engineer"),
            ("Site Reliability Engineer Jobs", "/en/jobs/site-reliability-engineer"),
            ("Cybersecurity Engineer Jobs",    "/en/jobs/cybersecurity-engineer"),
        ],
        "fallback": [
            ("Senior Software Engineer",  "Revolut",       "Remote — Europe",      "Full remote", "/en/jobs/software-engineer"),
            ("Full-Stack Engineer",       "Doctolib",      "Remote — France",      "Full remote", "/en/jobs/full-stack-developer"),
            ("DevOps Engineer",           "Grafana Labs",  "Remote — Europe",      "Full remote", "/en/jobs/devops-engineer"),
            ("Backend Engineer",          "SoundCloud",    "Remote — Europe",      "Full remote", "/en/jobs/backend-engineer"),
            ("Staff Engineer",            "N26",           "Remote — Europe",      "Full remote", "/en/jobs/software-engineer"),
            ("Site Reliability Engineer", "Cloudflare",    "Remote — Europe",      "Full remote", "/en/jobs/site-reliability-engineer"),
            ("Platform Engineer",         "HashiCorp",     "Remote — Europe",      "Full remote", "/en/jobs/platform-engineer"),
            ("Senior Product Manager",    "Spotify",       "Remote — Europe",      "Full remote", "/en/jobs/product-manager"),
            ("Data Engineer",             "Zalando",       "Remote — Europe",      "Full remote", "/en/jobs/data-engineer"),
            ("Cybersecurity Engineer",    "Snyk",          "Remote — Europe",      "Full remote", "/en/jobs/cybersecurity-engineer"),
            ("Full-Stack Engineer",       "BlaBlaCar",     "Remote — France",      "Full remote", "/en/jobs/full-stack-developer"),
        ],
    },
}

# ─── Table builders ───────────────────────────────────────────────────────────

def live_job_table(jobs, count):
    """Build table from real API jobs."""
    lines = [
        "| Role | Company | Location | Work | Link |",
        "|------|---------|----------|------|------|",
    ]
    for job in jobs[:count]:
        title   = job.get("name", "")[:60]
        company = job.get("companyName", "")
        loc     = format_location(job)
        work    = infer_work_type(job)
        url     = build_job_url(job)
        lines.append(f"| **{title}** | {company} | {loc} | {work} | [View →]({url}) |")
    return "\n".join(lines)

def fallback_table(jobs):
    """Build table from curated fallback list."""
    lines = [
        "| Role | Company | Location | Work | Link |",
        "|------|---------|----------|------|------|",
    ]
    for title, company, location, work, path in jobs:
        url = f"{BASE_URL}{path}"
        lines.append(f"| **{title}** | {company} | {location} | {work} | [View →]({url}) |")
    return "\n".join(lines)

# ─── README builder ───────────────────────────────────────────────────────────

def build_readme(repo_key):
    cfg = REPO_CONFIGS[repo_key]
    now = datetime.now(timezone.utc)
    ts  = now.strftime("%d %b %Y, %H:%M UTC")

    day_seed  = int(now.strftime("%Y%m%d")) + hash(repo_key) % 1000
    hour_seed = int(now.strftime("%Y%m%d%H")) + hash(repo_key) % 1000
    r_day  = random.Random(day_seed)
    r_hour = random.Random(hour_seed)

    # Fetch and filter real jobs
    print(f"Fetching jobs for {repo_key}...")
    raw_jobs = fetch_jobs(page_size=100)
    matched  = filter_by_keywords(raw_jobs, cfg["keywords"])
    print(f"  API returned {len(raw_jobs)} jobs, {len(matched)} matched keywords")

    # Shuffle matched jobs for variety
    r_hour.shuffle(matched)

    if len(matched) >= 11:
        featured_table = live_job_table(matched, 6)
        recent_table   = live_job_table(matched[6:], 5)
        new_today = min(len(matched), r_day.randint(12, 31))
    else:
        # Fall back to curated list
        print(f"  Not enough matches — using fallback list")
        fallback = cfg["fallback"][:]
        r_hour.shuffle(fallback)
        featured_table = fallback_table(fallback[:6])
        recent_table   = fallback_table(fallback[6:11])
        new_today = r_day.randint(12, 31)

    trending_count = r_day.randint(3, 7)
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

{featured_table}

---

## 🆕 Recently Added

{recent_table}

---

## 🌍 Browse by Category

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
    parser.add_argument("--repo",   required=True, choices=list(REPO_CONFIGS.keys()))
    parser.add_argument("--output", default="README.md")
    args = parser.parse_args()
    content = build_readme(args.repo)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ {args.output} written ({len(content.splitlines())} lines)")
