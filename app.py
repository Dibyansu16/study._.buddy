from dotenv import load_dotenv
import os
import streamlit as st
import requests
import json
import re
import time
import urllib.parse

st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #13161e;
    --border:  #1e2330;
    --accent:  #7effc0;
    --red:     #ff6b6b;
    --yellow:  #ffd93d;
    --text:    #e8ecf4;
    --muted:   #6b7591;
    --radius:  12px;
}

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1300px; }

/* ===== HAMBURGER NAV ===== */
#ham-toggle { display: none; }

.ham-nav-wrapper {
    position: relative;
    z-index: 9999;
    margin-bottom: 1.5rem;
}

.ham-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.6rem 1rem;
}

.ham-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    background: linear-gradient(135deg, var(--accent) 0%, #4fd9ff 50%, var(--yellow) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}

.ham-btn {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    padding: 4px 6px;
    border-radius: 6px;
    transition: background 0.2s;
    user-select: none;
}
.ham-btn:hover { background: var(--border); }

.ham-btn span {
    display: block;
    width: 22px;
    height: 2px;
    background: var(--accent);
    border-radius: 2px;
    transition: all 0.3s ease;
}

/* Animate to X when open */
#ham-toggle:checked ~ .ham-nav-wrapper .ham-btn span:nth-child(1) {
    transform: translateY(7px) rotate(45deg);
}
#ham-toggle:checked ~ .ham-nav-wrapper .ham-btn span:nth-child(2) {
    opacity: 0;
}
#ham-toggle:checked ~ .ham-nav-wrapper .ham-btn span:nth-child(3) {
    transform: translateY(-7px) rotate(-45deg);
}

.ham-menu {
    display: none;
    position: absolute;
    top: calc(100% + 6px);
    left: 0;
    right: 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}

#ham-toggle:checked ~ .ham-nav-wrapper .ham-menu {
    display: block;
}

.ham-menu a {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.75rem 1.2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--muted) !important;
    text-decoration: none !important;
    border-bottom: 1px solid var(--border);
    transition: all 0.15s ease;
    letter-spacing: 0.02em;
}
.ham-menu a:last-child { border-bottom: none; }
.ham-menu a:hover {
    background: var(--border);
    color: var(--text) !important;
}
.ham-menu a.active {
    background: rgba(126,255,192,0.08);
    color: var(--accent) !important;
    border-left: 3px solid var(--accent);
}

/* ===== MOBILE RESPONSIVE ===== */
@media (max-width: 768px) {
    .block-container {
        padding: 0.75rem 0.75rem !important;
    }

    /* Hide sidebar on mobile */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    .main-title {
        font-size: 1.7rem !important;
        line-height: 1.2 !important;
    }
    .sub-title {
        font-size: 0.72rem !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
    }

    /* Prevent word breaks everywhere */
    * {
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }

    /* Larger tap targets for inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 1rem !important;
        padding: 0.7rem !important;
    }

    .stButton > button {
        font-size: 0.85rem !important;
        padding: 0.65rem 0.9rem !important;
        min-height: 44px !important;
    }

    .response-box {
        font-size: 0.82rem !important;
        padding: 1rem !important;
        max-height: 400px !important;
    }

    .quiz-q { font-size: 0.88rem !important; }
    .quiz-opt { font-size: 0.8rem !important; }
    .fc-q { font-size: 0.88rem !important; }
    .fc-a { font-size: 0.8rem !important; }

    .card { padding: 1rem !important; }

    /* Make 2-col layouts stack on mobile */
    [data-testid="column"] {
        min-width: 100% !important;
    }
}

@media (min-width: 769px) {
    /* On desktop, hide hamburger entirely — sidebar handles nav */
    .ham-nav-wrapper { display: none !important; }
    #ham-toggle { display: none !important; }

    /* Force sidebar to always be visible and open on desktop */
    [data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        width: 260px !important;
        min-width: 260px !important;
        transform: none !important;
        opacity: 1 !important;
    }
    /* Hide the collapse arrow button so user can't close the sidebar */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    button[kind="header"] {
        display: none !important;
    }
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--accent) 0%, #4fd9ff 50%, var(--yellow) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.sub-title {
    font-family: 'DM Mono', monospace;
    color: var(--muted);
    font-size: 0.85rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-accent { border-left: 3px solid var(--accent); }
.card-red    { border-left: 3px solid var(--red); }
.card-yellow { border-left: 3px solid var(--yellow); }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(126,255,192,0.15) !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #5de8a0 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(126,255,192,0.3) !important;
}

.stTextArea label, .stTextInput label, .stSelectbox label, .stSlider label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
}

.response-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius);
    padding: 1.5rem 1.75rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.8;
    white-space: pre-wrap;
    color: var(--text);
    max-height: 500px;
    overflow-y: auto;
}

.quiz-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
}
.quiz-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
}
.quiz-q {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.6rem;
}
.quiz-opt {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: var(--muted);
    padding: 4px 0;
}
.quiz-ans {
    margin-top: 0.6rem;
    padding: 0.4rem 0.8rem;
    background: rgba(126,255,192,0.08);
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: var(--accent);
    border: 1px solid rgba(126,255,192,0.2);
}

.flashcard-front {
    background: linear-gradient(135deg, #1a1d27 0%, #13161e 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--yellow);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.5rem;
}
.flashcard-back {
    background: rgba(126,255,192,0.04);
    border: 1px solid rgba(126,255,192,0.2);
    border-radius: var(--radius);
    padding: 1rem 1.4rem;
    margin-bottom: 1rem;
}
.fc-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.fc-q { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--text); }
.fc-a { font-family: 'DM Mono', monospace; font-size: 0.85rem; color: var(--text); line-height: 1.6; }

.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    margin-right: 6px;
    background: var(--border);
    color: var(--muted);
}

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* suggestion pill buttons in search landing */
.suggest-pill button {
    background: var(--surface) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    padding: 0.45rem 1rem !important;
    text-align: left !important;
    letter-spacing: 0 !important;
}
.suggest-pill button:hover {
    background: var(--border) !important;
    color: var(--text) !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- API config ----------

load_dotenv()
#''' FOR LOCAL EXECUTION
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

#GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
#TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = "llama-3.1-8b-instant"


TAVILY_URL     = "https://api.tavily.com/search"


def ask_groq(prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "messages": messages, "temperature": 0.7, "max_tokens": 2048},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError:
        return f"⚠️ Groq API error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"⚠️ Error: {e}"


def tavily_search(query: str, max_results: int = 6) -> list:
    try:
        resp = requests.post(
            TAVILY_URL,
            headers={"Content-Type": "application/json"},
            json={"api_key": TAVILY_API_KEY, "query": query, "max_results": max_results, "search_depth": "basic"},
            timeout=15,
        )
        resp.raise_for_status()
        return [
            {"title": r.get("title", ""), "snippet": r.get("content", ""), "url": r.get("url", "")}
            for r in resp.json().get("results", [])[:max_results]
        ]
    except Exception:
        return []


def wikipedia_search(query: str, sentences: int = 5) -> dict:
    try:
        search = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": query, "format": "json", "srlimit": 1},
            timeout=8,
        )
        results = search.json().get("query", {}).get("search", [])
        if not results:
            return {}

        title = results[0]["title"]
        extract = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query", "prop": "extracts|info",
                "exsentences": sentences, "exintro": True, "explaintext": True,
                "inprop": "url", "titles": title, "format": "json",
            },
            timeout=8,
        )
        pages = extract.json().get("query", {}).get("pages", {})
        page = next(iter(pages.values()))
        return {
            "title":   page.get("title", ""),
            "extract": page.get("extract", ""),
            "url":     page.get("fullurl", f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}"),
        }
    except Exception:
        return {}


def ai_summarize_search(query: str, sources: list, wiki: dict) -> str:
    parts = []
    if wiki.get("extract"):
        parts.append(f"[Wikipedia — {wiki['title']}]\n{wiki['extract'][:1200]}")
    for i, s in enumerate(sources[:5]):
        if s.get("snippet"):
            parts.append(f"[Source {i+1}: {s['title']}]\n{s['snippet']}")

    system = (
        "You are StudyBuddy AI. Using the search results below, give a clear, study-focused answer. "
        "Cite sources like [Wikipedia] or [Source 1]. Structure: direct answer → key facts → brief summary."
    )
    prompt = f"Query: {query}\n\nSources:\n{chr(10).join(parts)}\n\nGive a comprehensive study answer."
    return ask_groq(prompt, system)


# ---------- session state ----------

defaults = {
    "page": "Explain",
    "history": [],
    "quiz_data": [],
    "flash_data": [],
    "show_answers": {},
    "show_flash": {},
    "quiz_score": {},
    "search_results": None,
    "search_wiki": None,
    "search_summary": None,
    "search_query": "",
    "chat_messages": [
        {"role": "assistant", "content": "Hey! 👋 I'm your Study Buddy. Ask me anything — a concept you're stuck on, help with homework, or just something you want to understand better. What are we studying today?"}
    ],
    # pending_search is set when a suggestion pill is clicked, then consumed on rerun
    "pending_search": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- query-param page routing (used by hamburger nav links) ----------
_valid_pages = {"Explain", "Summarize", "Quiz", "Flashcards", "Chat", "Search"}
_qp = st.query_params.get("page", "")
if _qp in _valid_pages and st.session_state.page != _qp:
    st.session_state.page = _qp

# ---------- hamburger nav (always visible, works on all screen sizes) ----------
_cur = st.session_state.page
_nav_items = [
    ("🔍", "Explain",    "Explain"),
    ("📝", "Summarize",  "Summarize"),
    ("❓", "Quiz",       "Quiz"),
    ("🃏", "Flashcards", "Flashcards"),
    ("💬", "Chat",       "Chat"),
    ("🌐", "Search",     "Web Search"),
]

_links_html = "\n".join(
    f'<a href="?page={key}" target="_self" class="{"active" if key == _cur else ""}">{icon}&nbsp;&nbsp;{label}</a>'
    for icon, key, label in _nav_items
)

st.markdown(f"""
<input type="checkbox" id="ham-toggle">
<div class="ham-nav-wrapper">
  <div class="ham-bar">
    <span class="ham-brand">🧠 StudyBuddy AI</span>
    <label for="ham-toggle" class="ham-btn" title="Menu">
      <span></span><span></span><span></span>
    </label>
  </div>
  <nav class="ham-menu">
    {_links_html}
  </nav>
</div>
""", unsafe_allow_html=True)

# ---------- sidebar ----------

with st.sidebar:
    st.markdown('<div class="main-title" style="font-size:1.6rem;">Study<br>Buddy AI</div>', unsafe_allow_html=True)
    #st.markdown('<div class="sub-title" style="font-size:0.7rem;">Groq · Llama 3.1 · Tavily</div>', unsafe_allow_html=True)
    st.markdown("---")

    pages = [
        ("🔍", "Explain",    "Explain Concepts"),
        ("📝", "Summarize",  "Summarize Notes"),
        ("❓", "Quiz",       "Generate Quiz"),
        ("🃏", "Flashcards", "Flashcards"),
        ("💬", "Chat",       "Study Chat"),
        ("🌐", "Search",     "Web Search"),
    ]

    for icon, key, label in pages:
        active = st.session_state.page == key
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")

    total = len(st.session_state.history)
    quizzes = len(st.session_state.quiz_data)
    cards = len(st.session_state.flash_data)

    st.markdown(f"""
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <div style="flex:1; background:#13161e; border:1px solid #1e2330; border-radius:10px; padding:10px; text-align:center;">
            <div style="font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#7effc0;">{total}</div>
            <div style="font-family:DM Mono,monospace; font-size:0.65rem; color:#6b7591; text-transform:uppercase;">Sessions</div>
        </div>
        <div style="flex:1; background:#13161e; border:1px solid #1e2330; border-radius:10px; padding:10px; text-align:center;">
            <div style="font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#ffd93d;">{quizzes}</div>
            <div style="font-family:DM Mono,monospace; font-size:0.65rem; color:#6b7591; text-transform:uppercase;">Questions</div>
        </div>
        <div style="flex:1; background:#13161e; border:1px solid #1e2330; border-radius:10px; padding:10px; text-align:center;">
            <div style="font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#ff6b6b;">{cards}</div>
            <div style="font-family:DM Mono,monospace; font-size:0.65rem; color:#6b7591; text-transform:uppercase;">Cards</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    #st.markdown('<div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#6b7591; text-align:center;">☁️ Groq Cloud · llama-3.1-8b</div>', unsafe_allow_html=True)


# ===== EXPLAIN =====

if st.session_state.page == "Explain":
    st.markdown('<div class="main-title">Explain Concepts</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Break down any topic into clear, simple language</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Topic or Concept", placeholder="e.g. Quantum Entanglement, Recursion, The French Revolution…")
    with col2:
        level = st.selectbox("Explain as if I'm a…", ["5-year-old 👶", "Middle Schooler 📚", "High Schooler 🎒", "Undergrad 🎓", "Expert 🔬"])

    analogy = st.checkbox("Include a real-world analogy", value=True)
    example = st.checkbox("Include a worked example", value=True)

    if st.button("✨  Explain This", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            extras = []
            if analogy: extras.append("Include a creative real-world analogy.")
            if example: extras.append("Include a concrete worked example.")

            system = (
                f"You are StudyBuddy AI, an expert tutor. Explain concepts clearly and engagingly. "
                f"Tailor your explanation for a {level} audience. {' '.join(extras)} "
                f"Use clear sections: a short intro, the core idea, and a summary. Avoid jargon unless you explain it."
            )

            with st.spinner("Thinking…"):
                result = ask_groq(f"Please explain: {topic}", system)

            st.markdown(f'<div class="response-box">{result}</div>', unsafe_allow_html=True)
            st.session_state.history.append({"type": "explain", "topic": topic, "level": level, "response": result})

    recents = [h for h in st.session_state.history if h["type"] == "explain"][-3:]
    if recents:
        st.markdown("---")
        st.markdown('<div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem; color:#6b7591; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;">Recent Explanations</div>', unsafe_allow_html=True)
        for h in reversed(recents):
            st.markdown(f'<div class="card card-accent"><span class="tag">{h["level"]}</span> <strong style="font-family:Syne,sans-serif;">{h["topic"]}</strong></div>', unsafe_allow_html=True)


# ===== SUMMARIZE =====

elif st.session_state.page == "Summarize":
    st.markdown('<div class="main-title">Summarize Notes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Paste your study material — get crisp, structured summaries</div>', unsafe_allow_html=True)

    notes = st.text_area("Paste your notes or text here", height=220,
                         placeholder="Paste lecture notes, textbook pages, articles…")

    col1, col2, col3 = st.columns(3)
    with col1:
        style = st.selectbox("Summary Style", ["Bullet Points", "Paragraph", "Mind Map Text", "Key Terms Only"])
    with col2:
        length = st.selectbox("Length", ["Short (3-5 pts)", "Medium (5-10 pts)", "Detailed"])
    with col3:
        focus = st.text_input("Focus Area (optional)", placeholder="e.g. formulas, dates, people")

    if st.button("📋  Summarize", use_container_width=True):
        if not notes.strip():
            st.warning("Please paste some notes first.")
        else:
            focus_str = f" Focus especially on: {focus}." if focus.strip() else ""
            system = (
                f"You are StudyBuddy AI, an expert at creating study summaries. "
                f"Summarize using {style} format. Aim for a {length} summary.{focus_str} "
                f"Highlight the most important concepts, key terms, and takeaways. "
                f"If 'Key Terms Only', output a glossary with brief definitions."
            )

            with st.spinner("Summarizing…"):
                result = ask_groq(f"Summarize the following study notes:\n\n{notes}", system)

            st.markdown("### 📄 Summary")
            st.markdown(f'<div class="response-box">{result}</div>', unsafe_allow_html=True)

            word_count = len(notes.split())
            sum_count  = len(result.split())
            reduction  = round((1 - sum_count / max(word_count, 1)) * 100)

            st.markdown(f"""
            <div style="display:flex; gap:12px; margin-top:1rem;">
                <div class="card" style="flex:1; text-align:center; padding:0.8rem;">
                    <div style="font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:#7effc0;">{word_count}</div>
                    <div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#6b7591;">Original Words</div>
                </div>
                <div class="card" style="flex:1; text-align:center; padding:0.8rem;">
                    <div style="font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:#ffd93d;">{sum_count}</div>
                    <div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#6b7591;">Summary Words</div>
                </div>
                <div class="card" style="flex:1; text-align:center; padding:0.8rem;">
                    <div style="font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:#ff6b6b;">{max(reduction,0)}%</div>
                    <div style="font-family:DM Mono,monospace; font-size:0.7rem; color:#6b7591;">Reduction</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.session_state.history.append({"type": "summarize"})


# ===== QUIZ =====

elif st.session_state.page == "Quiz":
    st.markdown('<div class="main-title">Generate Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Test your knowledge with AI-generated questions</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        quiz_topic = st.text_input("Topic", placeholder="e.g. Photosynthesis, World War II")
    with col2:
        q_type = st.selectbox("Question Type", ["Multiple Choice", "True / False", "Short Answer", "Mixed"])
    with col3:
        num_qs = st.slider("Number of Questions", 3, 15, 5)

    difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard", "Expert"], value="Medium")

    if st.button("🎯  Generate Quiz", use_container_width=True):
        if not quiz_topic.strip():
            st.warning("Enter a topic first.")
        else:
            system = (
                "You are StudyBuddy AI quiz generator. Generate quiz questions in STRICT JSON format. "
                "Return ONLY a JSON array, no markdown fences, no extra text. Each element: "
                '{"q": "question text", "type": "mcq|tf|short", '
                '"options": ["A) ...", "B) ...", "C) ...", "D) ..."] (only for mcq), '
                '"answer": "correct answer", "explanation": "brief explanation"}'
            )
            prompt = (
                f"Generate {num_qs} {q_type} questions about '{quiz_topic}' at {difficulty} difficulty. "
                "Return ONLY the JSON array."
            )

            with st.spinner("Generating quiz…"):
                raw = ask_groq(prompt, system)

            try:
                clean = re.sub(r"```(?:json)?|```", "", raw).strip()
                st.session_state.quiz_data    = json.loads(clean)
                st.session_state.show_answers = {}
                st.session_state.quiz_score   = {}
                st.success(f"✅ {len(st.session_state.quiz_data)} questions generated!")
                st.session_state.history.append({"type": "quiz"})
            except Exception:
                st.error("Couldn't parse the quiz. Try again.")
                with st.expander("Raw response"):
                    st.code(raw)

    if st.session_state.quiz_data:
        st.markdown("---")
        st.markdown(f'<div style="font-family:Syne,sans-serif; font-weight:800; font-size:1.1rem; margin-bottom:1rem;">📋 Your Quiz <span style="color:#6b7591; font-size:0.8rem; font-weight:400;">({len(st.session_state.quiz_data)} questions)</span></div>', unsafe_allow_html=True)

        correct = sum(1 for v in st.session_state.quiz_score.values() if v)
        answered = len(st.session_state.quiz_score)
        if answered:
            pct = round(correct / answered * 100)
            color = "#7effc0" if pct >= 70 else "#ffd93d" if pct >= 40 else "#ff6b6b"
            st.markdown(f'<div style="font-family:DM Mono,monospace; font-size:0.82rem; color:{color}; margin-bottom:1rem;">Score so far: {correct}/{answered} ({pct}%)</div>', unsafe_allow_html=True)

        for i, q in enumerate(st.session_state.quiz_data):
            qtype_label = {"mcq": "MCQ", "tf": "True/False", "short": "Short Answer"}.get(q.get("type", ""), "Q")

            st.markdown(f"""
            <div class="quiz-card">
                <div class="quiz-num">Question {i+1} · {qtype_label}</div>
                <div class="quiz-q">{q.get("q","")}</div>
            """, unsafe_allow_html=True)

            if q.get("options"):
                for opt in q["options"]:
                    st.markdown(f'<div class="quiz-opt">{opt}</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            show_key = f"show_{i}"
            btn_label = "Hide Answer" if st.session_state.show_answers.get(show_key) else "Reveal Answer"
            if st.button(btn_label, key=f"ans_btn_{i}"):
                st.session_state.show_answers[show_key] = not st.session_state.show_answers.get(show_key, False)
                st.rerun()

            if st.session_state.show_answers.get(show_key):
                st.markdown(f'<div class="quiz-ans">✓ {q.get("answer","")} &nbsp;|&nbsp; {q.get("explanation","")}</div>', unsafe_allow_html=True)

        if st.button("🔄  New Quiz", use_container_width=True):
            st.session_state.quiz_data    = []
            st.session_state.show_answers = {}
            st.rerun()


# ===== FLASHCARDS =====

elif st.session_state.page == "Flashcards":
    st.markdown('<div class="main-title">Flashcards</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Generate and study term-definition flashcard decks</div>', unsafe_allow_html=True)

    tab_gen, tab_study = st.tabs(["✨  Generate Deck", "📖  Study Deck"])

    with tab_gen:
        col1, col2 = st.columns([3, 1])
        with col1:
            fc_topic = st.text_input("Topic or paste notes", placeholder="e.g. Cell Biology, Python Data Structures…")
        with col2:
            fc_count = st.slider("# Cards", 5, 20, 8)

        fc_style = st.radio("Card Style", ["Term → Definition", "Question → Answer", "Concept → Example"], horizontal=True)

        if st.button("🃏  Generate Flashcards", use_container_width=True):
            if not fc_topic.strip():
                st.warning("Enter a topic first.")
            else:
                system = (
                    "You are StudyBuddy AI flashcard creator. Generate flashcards in STRICT JSON format. "
                    "Return ONLY a JSON array, no markdown, no extra text. "
                    f"Style: {fc_style}. Each element: "
                    '{"front": "term or question", "back": "definition, answer, or example"}'
                )

                with st.spinner("Creating flashcards…"):
                    raw = ask_groq(f"Generate {fc_count} flashcards about: {fc_topic}. Return ONLY the JSON array.", system)

                try:
                    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
                    st.session_state.flash_data = json.loads(clean)
                    st.session_state.show_flash = {}
                    st.success(f"✅ {len(st.session_state.flash_data)} flashcards created! Switch to 'Study Deck' tab.")
                    st.session_state.history.append({"type": "flashcard"})
                except Exception:
                    st.error("Couldn't parse flashcards. Try again.")
                    with st.expander("Raw"):
                        st.code(raw)

    with tab_study:
        if not st.session_state.flash_data:
            st.markdown('<div class="card" style="text-align:center; padding:2.5rem;"><div style="font-size:2rem;">🃏</div><div style="font-family:Syne,sans-serif; font-weight:700; margin:0.5rem 0;">No flashcards yet</div><div style="font-family:DM Mono,monospace; font-size:0.8rem; color:#6b7591;">Generate a deck from the previous tab</div></div>', unsafe_allow_html=True)
        else:
            revealed = sum(1 for v in st.session_state.show_flash.values() if v)
            st.markdown(f'<div style="font-family:DM Mono,monospace; font-size:0.8rem; color:#6b7591; margin-bottom:1rem;">{len(st.session_state.flash_data)} cards · {revealed} revealed</div>', unsafe_allow_html=True)

            cols = st.columns(2)
            for i, card in enumerate(st.session_state.flash_data):
                with cols[i % 2]:
                    flipped = st.session_state.show_flash.get(i, False)

                    st.markdown(f"""
                    <div class="flashcard-front">
                        <div class="fc-label" style="color:#ffd93d;">▲ Front</div>
                        <div class="fc-q">{card.get("front","")}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if flipped:
                        st.markdown(f"""
                        <div class="flashcard-back">
                            <div class="fc-label" style="color:#7effc0;">▼ Back</div>
                            <div class="fc-a">{card.get("back","")}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button("🙈 Hide" if flipped else "👁 Flip", key=f"flip_{i}", use_container_width=True):
                        st.session_state.show_flash[i] = not flipped
                        st.rerun()

            st.markdown("---")
            cola, colb = st.columns(2)
            with cola:
                if st.button("👁  Reveal All", use_container_width=True):
                    st.session_state.show_flash = {i: True for i in range(len(st.session_state.flash_data))}
                    st.rerun()
            with colb:
                if st.button("🔒  Hide All", use_container_width=True):
                    st.session_state.show_flash = {}
                    st.rerun()


# ===== CHAT =====

elif st.session_state.page == "Chat":
    st.markdown('<div class="main-title">Study Chat</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Ask anything — your AI tutor is here 24/7</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        is_user = msg["role"] == "user"
        bg     = "#1e2330" if is_user else "#13161e"
        border = "#ffd93d" if is_user else "#7effc0"
        align  = "flex-end" if is_user else "flex-start"
        label  = "You" if is_user else "StudyBuddy AI"
        lcolor = "#ffd93d" if is_user else "#7effc0"

        st.markdown(f"""
        <div style="display:flex; justify-content:{align}; margin-bottom:0.75rem;">
            <div style="max-width:80%; background:{bg}; border:1px solid {border}22;
                        border-left:3px solid {border}; border-radius:12px; padding:0.9rem 1.1rem;">
                <div style="font-family:Syne,sans-serif; font-size:0.68rem; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.1em; color:{lcolor};
                            margin-bottom:0.35rem;">{label}</div>
                <div style="font-family:DM Mono,monospace; font-size:0.85rem; line-height:1.7;
                            white-space:pre-wrap;">{msg["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Using a form here so pressing Enter or clicking Send clears the input automatically.
    # Without the form, Streamlit keeps the previous message in the box after submit.
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input("", placeholder="Type your question…", label_visibility="collapsed")
        with col_btn:
            send = st.form_submit_button("Send ↗", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        # pass the last 8 messages as context so the AI remembers the conversation
        history_ctx = ""
        for m in st.session_state.chat_messages[-8:]:
            prefix = "Student" if m["role"] == "user" else "StudyBuddy"
            history_ctx += f"{prefix}: {m['content']}\n"

        system = (
            "You are StudyBuddy AI, a friendly, knowledgeable tutor. "
            "Answer clearly and concisely. Use examples when helpful. "
            "If a student seems confused, try a different angle or analogy."
        )

        with st.spinner(""):
            reply = ask_groq(f"Conversation so far:\n{history_ctx}\nStudyBuddy:", system)

        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.session_state.history.append({"type": "chat"})
        st.rerun()

    if len(st.session_state.chat_messages) > 1:
        if st.button("🗑  Clear Chat", use_container_width=False):
            st.session_state.chat_messages = [st.session_state.chat_messages[0]]
            st.rerun()


# ===== WEB SEARCH =====

elif st.session_state.page == "Search":
    st.markdown('<div class="main-title">Web Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">// Search the internet + get an AI-powered study summary</div>', unsafe_allow_html=True)

    # If a suggestion pill was clicked on the previous run, pre-fill and trigger search
    prefill = st.session_state.pop("pending_search", "") if st.session_state.get("pending_search") else ""

    col_q, col_btn = st.columns([5, 1])
    with col_q:
        query = st.text_input(
            "", placeholder="Search anything… e.g. 'How does CRISPR work?', 'French Revolution causes'",
            label_visibility="collapsed", key="search_input",
            value=prefill or st.session_state.search_query,
        )
    with col_btn:
        do_search = st.button("🔍  Search", use_container_width=True)

    # auto-trigger if a suggestion was clicked
    if prefill:
        do_search = True

    col_o1, col_o2, col_o3 = st.columns(3)
    with col_o1:
        use_wiki   = st.checkbox("Include Wikipedia", value=True)
    with col_o2:
        use_web    = st.checkbox("Include Web Results", value=True)
    with col_o3:
        ai_summary = st.checkbox("AI Study Summary", value=True)

    if do_search and query.strip():
        st.session_state.search_query   = query
        st.session_state.search_results = None
        st.session_state.search_wiki    = None
        st.session_state.search_summary = None

        progress = st.progress(0, text="Searching…")
        wiki_data, web_data = {}, []

        if use_wiki:
            progress.progress(20, text="📖 Fetching Wikipedia…")
            wiki_data = wikipedia_search(query, sentences=8)
            st.session_state.search_wiki = wiki_data

        if use_web:
            progress.progress(50, text="🌐 Fetching web results…")
            web_data = tavily_search(query, max_results=6)
            st.session_state.search_results = web_data

        if ai_summary and (wiki_data or web_data):
            progress.progress(75, text="🧠 AI is summarizing…")
            summary = ai_summarize_search(query, web_data, wiki_data)
            st.session_state.search_summary = summary
            st.session_state.history.append({"type": "search", "query": query})

        progress.progress(100, text="Done!")
        time.sleep(0.3)
        progress.empty()
        st.rerun()

    if st.session_state.search_query:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin:1.2rem 0 0.5rem 0;">
            <div style="font-family:Syne,sans-serif; font-weight:800; font-size:1rem; color:#e8ecf4;">Results for:</div>
            <div style="background:#1e2330; padding:4px 14px; border-radius:100px;
                        font-family:DM Mono,monospace; font-size:0.82rem; color:#7effc0;
                        border:1px solid rgba(126,255,192,0.25);">
                {st.session_state.search_query}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.search_summary:
        st.markdown("### 🧠 AI Study Summary")
        st.markdown(f'<div class="response-box">{st.session_state.search_summary}</div>', unsafe_allow_html=True)
        st.markdown("")

    left, right = st.columns(2)

    with left:
        wiki = st.session_state.search_wiki
        if wiki:
            st.markdown(f"""
            <div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;
                        color:#6b7591; text-transform:uppercase; letter-spacing:0.1em;
                        margin-bottom:0.75rem;">📖 Wikipedia</div>
            <div class="card card-yellow">
                <div style="font-family:Syne,sans-serif; font-weight:800; font-size:1rem;
                            color:#ffd93d; margin-bottom:0.5rem;">{wiki.get("title","")}</div>
                <div style="font-family:DM Mono,monospace; font-size:0.82rem; line-height:1.8;
                            color:#c8cfe0; white-space:pre-wrap;">{wiki.get("extract","")[:1000]}{"…" if len(wiki.get("extract",""))>1000 else ""}</div>
                <a href="{wiki.get("url","")}" target="_blank"
                   style="display:inline-block; margin-top:0.75rem; font-family:DM Mono,monospace;
                          font-size:0.75rem; color:#ffd93d; text-decoration:none;
                          border:1px solid rgba(255,217,61,0.3); padding:4px 12px; border-radius:100px;">
                    Read full article →
                </a>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.search_query and st.session_state.search_wiki is not None:
            st.markdown('<div class="card"><div style="color:#6b7591; font-family:DM Mono,monospace; font-size:0.82rem;">No Wikipedia article found.</div></div>', unsafe_allow_html=True)

    with right:
        web = st.session_state.search_results
        if web:
            st.markdown(f"""
            <div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.85rem;
                        color:#6b7591; text-transform:uppercase; letter-spacing:0.1em;
                        margin-bottom:0.75rem;">🌐 Web Results ({len(web)})</div>
            """, unsafe_allow_html=True)
            for r in web:
                domain = re.sub(r"https?://(www\.)?", "", r["url"]).split("/")[0]
                snippet = r.get("snippet", "")[:200]
                st.markdown(f"""
                <div class="card" style="margin-bottom:0.6rem; padding:1rem 1.25rem;">
                    <div style="font-family:DM Mono,monospace; font-size:0.65rem; color:#6b7591; margin-bottom:0.25rem;">🔗 {domain}</div>
                    <div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.88rem;
                                color:#4fd9ff; margin-bottom:0.35rem;">{r.get("title","")}</div>
                    <div style="font-family:DM Mono,monospace; font-size:0.78rem; color:#9aa3b8;
                                line-height:1.6;">{snippet}{"…" if len(r.get("snippet",""))>200 else ""}</div>
                    <a href="{r["url"]}" target="_blank"
                       style="display:inline-block; margin-top:0.5rem; font-family:DM Mono,monospace;
                              font-size:0.72rem; color:#4fd9ff; text-decoration:none;
                              border:1px solid rgba(79,217,255,0.25); padding:3px 10px; border-radius:100px;">
                        Visit →
                    </a>
                </div>
                """, unsafe_allow_html=True)
        elif st.session_state.search_query and st.session_state.search_results is not None and not web:
            st.markdown('<div class="card card-red"><div style="font-family:DM Mono,monospace; font-size:0.82rem; color:#ff6b6b;">⚠️ No web results found. Check your Tavily API key or try again.</div></div>', unsafe_allow_html=True)

    # after a search: let them do more with the topic
    if st.session_state.search_summary:
        st.markdown("---")
        st.markdown('<div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.8rem; color:#6b7591; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;">Do more with this topic</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📝  Summarize this topic", use_container_width=True):
                st.session_state.page = "Summarize"
                st.rerun()
        with c2:
            if st.button("❓  Quiz me on this", use_container_width=True):
                st.session_state.page = "Quiz"
                st.rerun()
        with c3:
            if st.button("🔍  Explain in depth", use_container_width=True):
                st.session_state.page = "Explain"
                st.rerun()

    # landing state: clickable suggestion pills that actually trigger a search
    elif not st.session_state.search_query:
        st.markdown("---")
        #st.markdown('<div style="font-family:Syne,sans-serif; font-weight:700; font-size:0.8rem; color:#6b7591; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;">💡 Try searching for</div>', unsafe_allow_html=True)

        suggestions = []
            

        cols = st.columns(3)
        for i, s in enumerate(suggestions):
            with cols[i % 3]:
                # wrap each button in the suggest-pill div so CSS can de-style it
                st.markdown('<div class="suggest-pill">', unsafe_allow_html=True)
                if st.button(f"🔎 {s}", key=f"suggest_{i}", use_container_width=True):
                    # store the query and let the next rerun pick it up at the top of this page
                    st.session_state.pending_search = s
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)