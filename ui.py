"""Visual style: light and airy, with soft pastel gradients, rounded outlined
cards, an elegant serif for headings and lime pill buttons.

All the CSS lives here so app.py stays about logic.
"""
import html

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

:root {
  --ink: #111111;
  --soft: rgba(17, 17, 17, 0.62);
  --line: #111111;
  --hair: rgba(17, 17, 17, 0.14);
  --lime: #E3FE78;
  --lime-deep: #C9EB4A;
  --pastel: linear-gradient(120deg, #E9E4FF 0%, #DDF4FF 35%, #F3FBEA 65%, #FFE6F1 100%);
}

html, body, .stApp, [class*="st-"], button, input, textarea, select {
  font-family: 'DM Sans', ui-sans-serif, system-ui, -apple-system, sans-serif !important;
}
[data-testid="stIconMaterial"], .material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }

.stApp { background: #FFFFFF; color: var(--ink); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.5rem; max-width: 1180px; }

/* Serif headings */
h1, h2, h3, .serif {
  font-family: 'Instrument Serif', Georgia, serif !important;
  font-weight: 400 !important; letter-spacing: -0.02em; color: var(--ink) !important;
}
h2 { font-size: 2.2rem !important; }
h3 { font-size: 1.7rem !important; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
  color: var(--soft); font-weight: 300; font-size: 1.02rem;
}
[data-testid="stWidgetLabel"] p { color: var(--ink) !important; font-weight: 500 !important; }
button p { color: inherit !important; }

/* Sidebar: soft pastel wash */
[data-testid="stSidebar"] { background: var(--pastel); border-right: 1px solid var(--hair); }

/* Hero: rounded pastel panel */
.hero {
  background: var(--pastel); border-radius: 56px; padding: 3.2rem 3.4rem; margin-bottom: 2rem;
  position: relative; overflow: hidden;
}
.hero::after {
  content: ""; position: absolute; right: -80px; top: -80px; width: 340px; height: 340px;
  background: radial-gradient(circle, rgba(255,255,255,0.9), rgba(255,255,255,0) 70%);
}
.hero h1 { font-size: clamp(2.8rem, 6vw, 4.6rem); line-height: 1; margin: 0 0 0.9rem; padding: 0; }
.hero p { color: var(--soft); font-size: 1.15rem; font-weight: 300; max-width: 560px; margin: 0; }
.hero .tags { margin-top: 1.4rem; }

/* Outlined pill tags */
.chip {
  display: inline-block; padding: 0.22rem 0.8rem; margin: 0.18rem 0.25rem 0.18rem 0;
  border: 1px solid var(--line); border-radius: 999px; font-size: 0.85rem; color: var(--ink);
  background: rgba(255, 255, 255, 0.7);
}

/* Bordered containers become rounded outlined cards */
[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid var(--line) !important; border-radius: 32px !important;
  background: #FFFFFF; padding: 0.6rem 0.8rem;
}

/* Inputs */
[data-testid="stTextAreaRootElement"], [data-testid="stTextInputRootElement"],
[data-testid="stSelectbox"] [class*="ComboBox"] > div {
  border-radius: 20px !important; border: 1px solid var(--hair) !important; background: #FAFAFC !important;
}
[data-testid="stFileUploaderDropzone"] {
  border-radius: 24px !important; border: 1px dashed rgba(17,17,17,0.35) !important;
  background: rgba(255, 255, 255, 0.65) !important;
}

/* Buttons: lime pills */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  border-radius: 999px !important; text-transform: uppercase; letter-spacing: 0.06em;
  font-size: 0.82rem !important; font-weight: 500; padding: 0.55rem 1.4rem;
  border: 1px solid var(--line) !important; background: #FFFFFF; color: var(--ink);
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"],
.stFormSubmitButton > button[kind="primary"] {
  background: var(--lime) !important; border-color: var(--lime) !important; color: var(--ink) !important;
}
.stButton > button:hover { background: var(--lime-deep) !important; border-color: var(--lime-deep) !important; color: var(--ink) !important; }

/* Tabs as outlined pills, lime when selected */
[data-testid="stTabs"] [role="tablist"] { gap: 10px; border-bottom: none !important; box-shadow: none !important; }
[data-testid="stTabs"] [role="tab"] {
  border: 1px solid var(--line) !important; border-radius: 999px !important;
  padding: 6px 20px !important; background: #FFFFFF !important; color: var(--ink) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { background: var(--lime) !important; border-color: var(--lime) !important; }
[data-testid="stTabs"] [role="tab"] p { color: inherit !important; font-weight: 500 !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none !important; }

/* Metrics */
[data-testid="stMetricValue"] { font-family: 'Instrument Serif', Georgia, serif !important; font-size: 2.4rem !important; }
[data-testid="stExpander"] details { border-radius: 24px; border: 1px solid var(--hair); }

/* Score with a tiered progress track */
.score-wrap { margin: 0.4rem 0 1.6rem; }
.score-label { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.78rem; color: var(--soft); }
.score-num { font-family: 'Instrument Serif', Georgia, serif; font-size: 4.6rem; line-height: 1; color: var(--ink); }
.score-num span { font-size: 1.6rem; color: var(--soft); }
.track { position: relative; height: 8px; border-radius: 99px; background: #EEF0F5; margin: 1.6rem 6px 2.6rem; }
.track .fill { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 99px; background: var(--lime-deep); }
.track .tier { position: absolute; top: 50%; transform: translate(-50%, -50%); text-align: center; }
.track .dot {
  width: 22px; height: 22px; border-radius: 50%; background: #FFFFFF; border: 1px solid rgba(17,17,17,0.3);
  margin: 0 auto;
}
.track .tier.reached .dot { background: var(--lime); border-color: var(--ink); }
.track .tier small {
  position: absolute; top: 28px; left: 50%; transform: translateX(-50%); white-space: nowrap;
  font-size: 0.75rem; color: var(--soft);
}

/* Tailoring before/after */
.before { color: rgba(17,17,17,0.45); text-decoration: line-through; font-weight: 300; }
.after { color: var(--ink); font-weight: 500; background: linear-gradient(transparent 60%, rgba(227,254,120,0.8) 60%); }
</style>
"""

TIERS = [(0, "Stretch"), (50, "Possible"), (75, "Strong"), (90, "Standout")]


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)


def hero():
    st.markdown(
        """
        <div class="hero">
          <h1>Find your fit.</h1>
          <p>See how well you match a job, tailor your resume honestly, and keep every
          application in one place.</p>
          <div class="tags">
            <span class="chip">Match score</span><span class="chip">Job summary</span>
            <span class="chip">Honest tailoring</span><span class="chip">Tracker</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def score(label, value):
    value = max(0, min(int(value), 100))
    tiers = "".join(
        f"<div class='tier {'reached' if value >= at else ''}' style='left:{at}%'>"
        f"<div class='dot'></div><small>{name}</small></div>"
        for at, name in TIERS
    )
    st.markdown(
        f"<div class='score-wrap'><div class='score-label'>{html.escape(label)}</div>"
        f"<div class='score-num'>{value}<span>/100</span></div>"
        f"<div class='track'><div class='fill' style='width:{value}%'></div>{tiers}</div></div>",
        unsafe_allow_html=True,
    )


def chips(items):
    if items:
        st.markdown("".join(f"<span class='chip'>{html.escape(str(i))}</span>" for i in items),
                    unsafe_allow_html=True)
