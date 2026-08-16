"""
Every word on the site lives here.

Editing content should never mean editing markup. Add a project by appending a
dict to PROJECTS; add a skill by appending a string to STACK. The templates
loop over these, so the page rebuilds around whatever you put in.

Anything with an `accent` key takes one of: black, white, pink, cyan, lime,
violet. Those map to the plate classes in site.css, and each one is a
pre-verified AA-safe text/background pairing — see the colour contract at the
top of site.css before inventing a new one.
"""

# --- identity ---------------------------------------------------------------

SITE = {
    "name": "Aryan Gorde",
    "role": "Backend & full-stack developer",
    "domain": "https://aryangorde.com",
    "email": "aryangorde6@gmail.com",
    "github": "https://github.com/aryangorde8",
    "github_handle": "aryangorde8",
    "linkedin": "https://www.linkedin.com/in/aryan-gorde-6b660a264/",
    "resume": "/Aryan_Gorde_Resume.pdf",
    "title": "Aryan Gorde — Backend & Full-Stack Developer",
    "description": (
        "Aryan Gorde — backend and full-stack developer. Django, FastAPI, and the "
        "infrastructure that keeps them up. Builder of DebtClear and Mnemos."
    ),
    "og_description": (
        "Django, FastAPI, and the infrastructure underneath. Loud portfolio, quiet deploys."
    ),
    "photo": "aryan.jpg",          # source file in build_src/images/
    "photo_alt": "Aryan Gorde",
}

# --- nav --------------------------------------------------------------------
# (id, label) — id must match a section id, and build.py verifies that.

NAV = [
    ("about",      "About"),
    ("stack",      "Stack"),
    ("debtclear",  "DebtClear"),
    ("projects",   "Projects"),
    ("experience", "Experience"),
    ("stats",      "Stats"),
    ("contact",    "Contact"),
]

# --- hero -------------------------------------------------------------------

HERO = {
    "stickers": [
        {"text": "Backend",    "accent": "pink"},
        {"text": "Full-stack", "accent": "cyan"},
        {"text": "Ships it",   "accent": "lime"},
    ],
    "first_name": "Aryan",
    "last_name": "Gorde",
    "blurb": (
        "I build the parts of a product that have to be <strong>right</strong> — money "
        "maths that reconciles to the cent, APIs that fail loudly, and deploys boring "
        "enough to run on a Tuesday night. Django and FastAPI on the server, Postgres "
        "underneath, AWS around it."
    ),
    "photo_badge": "Open to backend &amp; full-stack roles",
}

# --- about ------------------------------------------------------------------

ABOUT = {
    "paragraphs": [
        "I'm a computer engineering student who wandered onto the server side and never "
        "left. The work I like has a correct answer buried in it somewhere — an "
        "amortisation schedule that has to balance, a retrieval pipeline that has to cite "
        "the document it actually used, a deploy that has to be repeatable.",

        "Most of what I ship is Django or FastAPI behind a small, sharp frontend. I'd "
        "rather spend the afternoon on the migration strategy than the hover state. "
        "(This page is what happens when I get to do both.)",
    ],
    "photo_stickers": [
        {"text": "Open to roles",  "accent": "pink"},
        {"text": "Backend focus",  "accent": "lime"},
    ],
    # The first tile is rendered with the borrowed neomorphism treatment.
    "facts": [
        {"label": "Currently", "value": "Computer<br />Engineering", "accent": "neo"},
        {"label": "Building",  "value": "DebtClear",                 "accent": "violet"},
        {"label": "Learning",  "value": "Distributed<br />Systems",  "accent": "lime"},
        {"label": "Status",    "value": "Available",                 "accent": "black"},
    ],
}

# --- stack ------------------------------------------------------------------
# The last group is rendered with the borrowed claymorphism treatment.

STACK = [
    {"title": "Languages", "note": "What I write day to day.",
     "accent": "white",
     "items": ["Python", "JavaScript", "TypeScript", "SQL", "Bash"]},

    {"title": "Backend", "note": "Where most of the time goes.",
     "accent": "black",
     "items": ["Django", "DRF", "FastAPI", "Celery", "Node.js"]},

    {"title": "Data", "note": "Storage, cache, and the queries between.",
     "accent": "cyan",
     "items": ["PostgreSQL", "MongoDB Atlas", "Redis", "SQLite"]},

    {"title": "Infra", "note": "Off the laptop, and staying up.",
     "accent": "lime",
     "items": ["AWS EC2", "Docker", "GitHub Actions", "Nginx", "Gunicorn"]},

    {"title": "AI", "note": "Used where it earns its latency.",
     "accent": "pink",
     "items": ["Llama 3.3 · Groq", "Amazon Bedrock", "Hybrid retrieval", "Citations"]},

    {"title": "Frontend", "note": "Enough to ship the whole thing solo.",
     "accent": "clay",
     "items": ["React", "Tailwind", "Chart.js", "Vanilla JS"]},
]

# --- featured project (rendered in the borrowed minimalism strip) -----------

FEATURED = {
    "name_head": "Debt",
    "name_tail": "Clear",
    "summary": (
        "A Django debt-payoff planner. You enter what you owe; it simulates Avalanche and "
        "Snowball strategies side by side, charts the payoff curve, and an AI advisor "
        "explains the trade-off in the plain language a spreadsheet never will."
    ),
    "figures": [
        {"value": "2", "note":
            "payoff strategies simulated in parallel — highest-interest-first and "
            "smallest-balance-first — so the cost of choosing motivation over maths is "
            "visible in rupees, not vibes."},
        {"value": "3.3", "note":
            "Llama 3.3 via Groq powers the advisory layer. Groq's inference speed is what "
            "makes the advice feel like part of the form rather than a job you wait on."},
    ],
    "detail": [
        ("The problem",
         "Payoff calculators give you a number. They don't tell you what happens if you "
         "miss a month, or why the strategy that clears a card fastest can cost more "
         "overall."),
        ("The build",
         "Django and Django REST Framework, with amortisation running server-side so the "
         "numbers are computed once and identically for the chart, the table, and the "
         "advisor prompt. Chart.js renders the curve."),
        ("The AI part",
         "The model is given the computed schedule, never the raw inputs. It explains and "
         "compares; it never does the arithmetic. Money maths belongs in code you can "
         "unit-test."),
        ("Shipping",
         "Deployed on AWS EC2 behind Nginx and Gunicorn. GitHub Actions runs the test "
         "suite on every push and deploys <code>main</code> on green."),
    ],
    "links": [
        {"label": "Open DebtClear", "href": "https://debtclear.aryangorde.com/"},
        {"label": "Read the source", "href": "https://github.com/aryangorde8/debtclear"},
    ],
}

# --- projects ---------------------------------------------------------------
# DebtClear gets its own full-bleed section above; everything else lives here.
# The grid adapts to the length of this list — one card goes full width, two or
# more go side by side — so adding a project is appending a dict, nothing else.
#
# Every claim here has to be traceable to the résumé or the live app. If you
# can't point at where a line came from, don't add it.

PROJECTS = [
    {
        "name": "Mnemos",
        "tag": "AI agent",
        "tag_accent": "lime",
        "accent": "black",
        "blurb": (
            "Memory and retrieval across Gmail, Calendar, and documents. Vector search and "
            "BM25 are fused with Reciprocal Rank Fusion and reranked by Gemini 3 Pro, then "
            "a critic sub-agent audits the answer against the chunks it cited — so a claim "
            "with no source behind it never reaches you."
        ),
        "tech": "TypeScript · Express 5 · MongoDB Atlas · Vertex AI · Cloud Run",
        "links": [
            {"label": "Live",   "href": "https://mnemos.aryangorde.com",
             "aria": "Mnemos live demo", "accent": "cyan"},
            {"label": "Source", "href": "https://github.com/aryangorde8/Mnemos",
             "aria": "Mnemos source on GitHub", "accent": "lime"},
        ],
    },
]

# --- experience (rendered in the borrowed brutalism treatment) --------------
# Sourced from Aryan_Gorde_Resume.pdf. NOTE: the résumé lists no employment —
# it is Education / Projects / Skills / Certifications. So this is a dated
# timeline of real shipped work, not a job history. Do not add invented roles.

EXPERIENCE = [
    {"period": "May 2026", "role": "Mnemos",
     "detail": "Production AI memory agent for retrieval across Gmail, Calendar, and "
               "documents. Hybrid pipeline merging MongoDB Vector Search and BM25 via "
               "Reciprocal Rank Fusion, reranked with Gemini 3 Pro, plus a critic "
               "sub-agent that audits every response against its cited chunks to catch "
               "hallucinations. Deployed on Cloud Run with SSE streaming."},

    {"period": "Mar. 2026", "role": "TicketForge",
     "detail": "Automation pipeline that ingests raw meeting transcripts and generates "
               "structured Linear tickets through a multi-stage Groq prompt chain, "
               "extracting tasks, assignees, deadlines, and priorities from unstructured "
               "text. Devpost hackathon entry."},

    {"period": "Feb. 2026", "role": "DebtClear",
     "detail": "LLM-powered debt resolution platform with a Negotiate Mode that generates "
               "personalised negotiation scripts from a user's debt profile. Django REST "
               "on EC2, Dockerised, GitHub Actions CI/CD, Groq (Llama 3) with SSE "
               "streaming. Sole developer, production-ready in under 72 hours for Hack "
               "the Pulse 2026."},

    {"period": "Jan. 2026", "role": "DevSync",
     "detail": "Full-stack developer portfolio platform — 12+ REST modules, Dockerised "
               "with PostgreSQL 16, Redis 7, Celery and Nginx. Local-LLM assistant on "
               "Ollama with a ChromaDB RAG pipeline and no external API keys. Jenkins "
               "CI/CD with linting, Safety and Trivy scans, and 35+ tests."},
]

EDUCATION = {
    "degree": "B.Tech, Computer Engineering",
    "institution": "Sardar Patel Institute of Technology",
    "affiliation": "Mumbai University · Mumbai, India",
    "status": "Aug. 2023 – June 2027",
    "detail": "Computer-science fundamentals with a practical bias: data structures, "
              "operating systems, databases, and machine learning, applied to things "
              "that actually get deployed.",
}

CERTIFICATIONS = [
    ("Meta Back-End Developer Professional Certificate", "Meta · Coursera",   "Dec 2025"),
    ("CI/CD: Continuous Integration and Continuous Delivery", "IBM · Coursera", "Jan 2026"),
    ("AWS Cloud Technical Essentials", "Amazon Web Services · Coursera",       "Jan 2026"),
    ("Docker for Beginners", "KodeKloud",                                       "Jan 2026"),
    ("Kubernetes for Absolute Beginners", "KodeKloud",                          "Jan 2026"),
]

SKILLS = [
    "Languages — Python, JavaScript, TypeScript, SQL, HTML/CSS, C",
    "Frameworks — Django, DRF, Next.js, React, Express.js, Tailwind",
    "DevOps &amp; cloud — Docker, AWS EC2, Cloud Run, Jenkins, Actions, Nginx",
    "Databases — PostgreSQL, MongoDB Atlas (Vector Search, BM25), ChromaDB",
    "AI — Groq, Vertex AI (Gemini), Ollama, sentence-transformers, ReAct agents",
]

# --- stats (rendered in the borrowed bento grid) ----------------------------
# `span` is the desktop column span; build.py keeps the mobile collapse correct
# regardless of what you put here. Every figure has to be checkable against
# something else on the page — the build count matches the experience table
# directly above this section, so don't change one without the other.

STATS_FEATURE = {
    "label": "Featured build",
    "name": "DebtClear",
    "note": "Django · Groq · EC2 · GitHub Actions. Deployed, tested, and live.",
    "href": "https://debtclear.aryangorde.com/",
    "cta": "Open it",
}

STATS = [
    {"value": 4,   "suffix": "",  "label": "Builds shipped in 2026", "accent": "pink",   "span": 1},
    {"value": 3,   "suffix": "+", "label": "Years on Python",        "accent": "lime",   "span": 1},
    {"value": 100, "suffix": "%", "label": "Automated deploys",      "accent": "violet", "span": 2,
     "note": "automated — push to main, tests, ship"},
    {"value": 1,   "suffix": "",  "label": "HTML file, zero requests", "accent": "white", "span": 1},
    {"value": 9,   "suffix": "",  "label": "Design eras borrowed from", "accent": "black", "span": 2,
     "note": "one device each, dropped into a maximalist house style"},
]

# --- contact ----------------------------------------------------------------

CONTACT = {
    "headline": "Let's build something that has to work.",
    "body": (
        "I'm after backend or full-stack work where the hard part is the system design, "
        "the data model, or keeping a deploy boring. If that's what you've got, I'd like "
        "to hear about it. Fastest route is email — I reply to everything that isn't a "
        "recruiter template."
    ),
    "cards": [
        {"title": "GitHub",   "note": "aryangorde8",         "href": SITE["github"],   "accent": "cyan",  "icon": "↗"},
        {"title": "LinkedIn", "note": "the formal version",  "href": SITE["linkedin"], "accent": "white", "icon": "↗"},
        {"title": "Résumé",   "note": "PDF, one page",       "href": SITE["resume"],   "accent": "lime",  "icon": "⤓"},
    ],
}

# --- marquees ---------------------------------------------------------------

MARQUEES = {
    "stack":    ["Django", "FastAPI", "PostgreSQL", "Docker", "AWS EC2",
                 "GitHub Actions", "Redis", "Celery"],
    "shipped":  ["Shipped", "Tested", "Deployed", "Monitored", "Documented", "Still up"],
    "projects": ["2am commits", "no roadmap", "scope creep",
                 "works on my machine", "ship it"],
    "contact":  ["Let's build something", "that has to work"],
}

# --- the borrowed-device credits -------------------------------------------
# Maximalism is the house style; these nine are quoted from the other eras.
# Used both for the on-page credit chips and the colophon list.

BORROWED = [
    ("skeuomorphism", "2007", "hero résumé button", "a real bevel, lit from above"),
    ("neomorphism",   "2019", "about tile",         "soft extrusion in the page's own yellow"),
    ("glassmorphism", "2020", "about bio panel",    "frosted over the pattern"),
    ("claymorphism",  "2021", "frontend card",      "puffy, oversized radii"),
    ("minimalism",    "—",    "DebtClear",          "a full-bleed strip of restraint"),
    ("brutalism",     "2018", "experience",         "materials left exposed"),
    ("liquid glass",  "2025", "hero photo badge",   "refractive rim, travelling sheen"),
    ("bento grid",    "2023", "stats",              "unequal tiles, uniform gutters"),
    ("spatial UI",    "2024", "contact",            "layers at different depths"),
]
