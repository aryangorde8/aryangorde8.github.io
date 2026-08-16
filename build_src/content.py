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
    "email": "aryangorde8@gmail.com",
    "github": "https://github.com/aryangorde8",
    "github_handle": "aryangorde8",
    "linkedin": "https://www.linkedin.com/in/aryan-gorde-6b660a264/",
    "resume": "/Aryan_Gorde_Resume.pdf",
    "title": "Aryan Gorde — Backend & Full-Stack Developer",
    "description": (
        "Aryan Gorde — backend and full-stack developer. Django, FastAPI, and the "
        "infrastructure that keeps them up. Builder of DebtClear, Mnemos, and MittiGuard."
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
    ("labs",       "Labs"),
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

PROJECTS = [
    {
        "name": "Mnemos",
        "tag": "AI agent",
        "tag_accent": "lime",
        "accent": "black",
        "blurb": (
            "An approval-gated assistant that pairs hybrid retrieval with a graph of prior "
            "context, cites every claim back to a source, and won't touch Gmail or "
            "Calendar until a human clicks approve."
        ),
        "tech": "Python · FastAPI · MongoDB Atlas · Bedrock",
        "links": [
            {"label": "Live",   "href": "https://mnemos.aryangorde.com",
             "aria": "Mnemos live demo", "accent": "cyan"},
            {"label": "Source", "href": "https://github.com/aryangorde8/Mnemos",
             "aria": "Mnemos source on GitHub", "accent": "lime"},
        ],
    },
    {
        "name": "MittiGuard",
        "tag": "Safety workflow",
        "tag_accent": "violet",
        "accent": "white",
        "blurb": (
            "Holds ambiguous farm-input sales pending until evidence is captured, "
            "reviewed, and written to an auditable trail. The real problem was making "
            "\"wait\" the cheap default and \"approve\" the deliberate act."
        ),
        "tech": "Node.js · JavaScript · Bedrock · Docker",
        "links": [
            {"label": "Live",   "href": "https://mittiguard.aryangorde.com/",
             "aria": "MittiGuard live demo", "accent": "pink"},
            {"label": "Source", "href": "https://github.com/aryangorde8/mittiguard",
             "aria": "MittiGuard source on GitHub", "accent": "black"},
        ],
    },
    {
        "name": "Fintrack",
        "tag": "Personal finance",
        "tag_accent": "cyan",
        "accent": "pink",
        "blurb": (
            "Expense tracking with category rules, recurring-transaction detection, and "
            "monthly rollups. Built to stop me rewriting the same spreadsheet formula "
            "every January."
        ),
        "tech": "Python · Django · PostgreSQL · Chart.js",
        "links": [
            {"label": "Source", "href": "https://github.com/aryangorde8",
             "aria": "Fintrack source on GitHub", "accent": "cyan"},
        ],
    },
]

# --- labs -------------------------------------------------------------------

LABS = [
    {"name": "DevSync", "tag": "CLI", "tag_accent": "cyan", "accent": "white",
     "blurb": "One command to pull every repo I have open, stash what's dirty, and print "
              "a single table of what's behind. Replaced a shell alias that had grown to "
              "nine lines.",
     "tech": "Python · Click · GitPython"},

    {"name": "pg-slowlog", "tag": "Tooling", "tag_accent": "lime", "accent": "black",
     "blurb": "Tails Postgres slow-query logs and groups them by normalised shape, so you "
              "find the query fired 4,000 times instead of the one that took 4 seconds "
              "once.",
     "tech": "Python · psycopg · Rich"},

    {"name": "Hotel Ledger", "tag": "Coursework", "tag_accent": "pink", "accent": "lime",
     "blurb": "A hotel management system from a systems module that I kept refactoring "
              "long after it was graded. Room allocation is a bin-packing problem and I "
              "refuse to let it go.",
     "tech": "Django · PostgreSQL"},

    {"name": "NLP Scratchpad", "tag": "Notebooks", "tag_accent": "cyan", "accent": "violet",
     "blurb": "Tokenisers, TF-IDF baselines, and a classifier that beat a fine-tuned model "
              "on a small dataset — the useful reminder that lives in every ML assignment.",
     "tech": "Python · scikit-learn · pandas"},
]

# --- experience (rendered in the borrowed brutalism treatment) --------------
# EDIT: replace with real dates and employers.

EXPERIENCE = [
    {"period": "2025 — now", "role": "Independent Backend Developer",
     "detail": "Designed, built, and deployed DebtClear end to end — data model, "
               "amortisation engine, REST API, AI advisory layer, and the EC2 + GitHub "
               "Actions pipeline that ships it."},
    {"period": "2025", "role": "Hackathon Builds",
     "detail": "Mnemos and MittiGuard — both agentic systems where the interesting "
               "constraint was refusing to act without evidence or human approval."},
    {"period": "2024 — 2025", "role": "Academic Projects",
     "detail": "Hotel management systems, machine-learning experiments, and NLP "
               "assignments, documented as if someone else would have to maintain them."},
]

EDUCATION = {
    "degree": "B.E. Computer Engineering",
    "status": "In progress",
    "detail": "Computer-science fundamentals with a practical bias: data structures, "
              "operating systems, databases, and machine learning, applied to things that "
              "get deployed.",
}

SKILLS = [
    "Backend architecture — Django, DRF, FastAPI",
    "Relational data modelling and query tuning",
    "CI/CD and deployment — Actions, Docker, EC2",
    "LLM integration with hard correctness boundaries",
    "Writing docs a stranger can follow",
]

# --- stats (rendered in the borrowed bento grid) ----------------------------
# EDIT: placeholders. `span` is the desktop column span; build.py keeps the
# mobile collapse correct regardless of what you put here.

STATS_FEATURE = {
    "label": "Featured build",
    "name": "DebtClear",
    "note": "Django · Groq · EC2 · GitHub Actions. Deployed, tested, and live.",
    "href": "https://debtclear.aryangorde.com/",
    "cta": "Open it",
}

STATS = [
    {"value": 3,   "suffix": "",  "label": "Deployed projects",      "accent": "pink",   "span": 1},
    {"value": 4,   "suffix": "+", "label": "Years on Python",        "accent": "lime",   "span": 1},
    {"value": 100, "suffix": "%", "label": "Automated deploys",      "accent": "violet", "span": 2,
     "note": "automated — push to main, tests, ship"},
    {"value": 1,   "suffix": "",  "label": "HTML file, zero builds", "accent": "white",  "span": 1},
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
    "labs":     ["2am commits", "no roadmap", "scope creep",
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
