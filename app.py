import textwrap

import streamlit as st
import plotly.express as px

from agent.civicpulse_agent import process_complaint


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CivicPulse | Grievance Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. DESIGN TOKENS
# ==========================================

COLORS = {
    "primary": "#123B3A",
    "secondary": "#245B57",
    "mint": "#A8DCCB",
    "coral": "#F28C72",
    "background": "#F6F8F5",
    "surface": "#FFFFFF",
    "text": "#203432",
    "muted": "#667A74",
    "placeholder": "#788982",
    "border": "#D5E3DC",
    "success": "#278568"
}


# ==========================================
# 3. HELPERS
# ==========================================

def html(markup: str) -> str:
    """
    Flatten HTML so Streamlit's Markdown never treats indented
    lines as a code block (this was the cause of the raw <div>
    text showing in the sidebar).
    """
    lines = textwrap.dedent(markup).splitlines()
    return "\n".join(line.strip() for line in lines if line.strip())


def render(markup: str):
    st.markdown(html(markup), unsafe_allow_html=True)


def report_card(label, value_html, hint="", extra=""):
    return f"""
    <div class="report-card">
        <div class="report-label">{label}</div>
        <div class="report-value">{value_html}</div>
        {extra}
        <div class="report-hint">{hint}</div>
    </div>
    """


# ==========================================
# 4. CUSTOM SVG BRAND MARK
# ==========================================

LOGO = """
<svg width="42" height="42" viewBox="0 0 48 48"
     xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="3" width="42" height="42"
          rx="13" fill="#245B57"/>
    <path d="M12 31 L24 13 L36 31"
          fill="none" stroke="#A8DCCB"
          stroke-width="3.5" stroke-linecap="round"
          stroke-linejoin="round"/>
    <path d="M17 31 V24 H31 V31"
          fill="none" stroke="#F28C72"
          stroke-width="3" stroke-linecap="round"
          stroke-linejoin="round"/>
    <path d="M24 20 V25"
          stroke="#FFFFFF" stroke-width="2.5"
          stroke-linecap="round"/>
</svg>
"""

# Collapse the SVG into one line
LOGO = " ".join(line.strip() for line in LOGO.splitlines())


# ==========================================
# 5. GLOBAL CSS
# ==========================================

render("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
""")

st.markdown("""
<style>

:root {
    --teal: #123B3A;
    --teal-light: #245B57;
    --mint: #A8DCCB;
    --coral: #F28C72;
    --background: #F6F8F5;
    --border: #D5E3DC;
    --text: #203432;
    --muted: #667A74;
}

/* APP BACKGROUND + FONT */

.stApp {
    background: var(--background);
    color: var(--text);
}

.stApp,
.stMarkdown,
.stTextArea textarea,
.stButton button,
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stMetric"],
[data-testid="stSidebar"] label {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* breathing room at the top now that the header is hidden */
.block-container {
    padding-top: 3rem;
}

/* HIDE STREAMLIT DEFAULT CHROME */

[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer {
    visibility: hidden;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: var(--teal);
    border-right: 1px solid var(--teal-light);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #F0FAF5;
}

[data-testid="stSidebar"] .stCaption {
    color: #D3EDE3 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(168, 220, 203, 0.25);
}

.brand-name {
    color: #FFFFFF;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
}

.brand-tagline {
    color: var(--mint);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.7px;
    margin-top: 4px;
}

.sidebar-label {
    color: var(--mint);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-top: 24px;
    margin-bottom: 8px;
}

.sidebar-note {
    color: #D3EDE3;
    font-size: 12px;
    line-height: 1.7;
}

/* SIDEBAR RADIO NAVIGATION */

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #FFFFFF !important;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    color: #A8DCCB !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 10px;
}

/* unselected radio circle: mint outline instead of black
   (selected dot colour comes from primaryColor in config.toml) */
[data-testid="stSidebar"] [data-testid="stRadio"] label:not(:has(input:checked)) > div:first-child {
    background-color: transparent !important;
    border: 2px solid #A8DCCB !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) > div:first-child {
    background-color: #F28C72 !important;
    border-color: #F28C72 !important;
}

/* ===== SIDEBAR REDESIGN ===== */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123B3A 0%, #0E2F2E 100%) !important;
}

/* animated heartbeat line under the brand */
.pulse-line {
    display: block;
    margin: 14px 0 4px 0;
    overflow: visible;
}

.pulse-line .pulse-run {
    stroke-dasharray: 70 330;
    stroke-dashoffset: 70;
    animation: pulse-run 3s linear infinite;
    filter: drop-shadow(0 0 4px rgba(168, 220, 203, 0.8));
}

@keyframes pulse-run {
    to { stroke-dashoffset: -400; }
}

/* navigation buttons */
[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 12px 14px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div.stButton > button > div {
    justify-content: flex-start !important;
    width: 100%;
}

[data-testid="stSidebar"] div.stButton > button [data-testid="stMarkdownContainer"] p {
    color: #C9E6DC !important;
    font-weight: 600;
    font-size: 15px;
    text-align: left;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background: rgba(168, 220, 203, 0.10);
    border-color: rgba(168, 220, 203, 0.28);
}

[data-testid="stSidebar"] div.stButton > button:hover p {
    color: #FFFFFF !important;
}

/* live status card */
.live-card {
    background: rgba(36, 91, 87, 0.55);
    border: 1px solid #3F7B72;
    border-radius: 14px;
    padding: 14px 15px;
}

.live-row {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #CFF3E4;
    font-weight: 700;
    font-size: 15px;
}

.live-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #7FE3B5;
    animation: live-ping 2s infinite;
}

@keyframes live-ping {
    0%   { box-shadow: 0 0 0 0 rgba(127, 227, 181, 0.55); }
    70%  { box-shadow: 0 0 0 9px rgba(127, 227, 181, 0); }
    100% { box-shadow: 0 0 0 0 rgba(127, 227, 181, 0); }
}

.live-sub {
    color: #FFFFFF;
    font-size: 12px;
    margin: 6px 0 10px 18px;
}

.chip {
    display: inline-block;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.4px;
    color: #A8DCCB;
    border: 1px solid rgba(168, 220, 203, 0.35);
    border-radius: 20px;
    padding: 3px 9px;
    margin: 0 5px 5px 0;
}

/* how-it-works flow */
.flow-step {
    position: relative;
    display: flex;
    gap: 12px;
    padding-bottom: 16px;
}

.flow-step:not(:last-child)::after {
    content: "";
    position: absolute;
    left: 11px;
    top: 26px;
    bottom: 2px;
    width: 1px;
    background: rgba(168, 220, 203, 0.3);
}

.flow-num {
    flex: 0 0 24px;
    height: 24px;
    border-radius: 50%;
    background: #245B57;
    border: 1px solid #5D9386;
    color: #A8DCCB;
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
}

.flow-num.out {
    border-color: #F28C72;
    color: #F28C72;
}

.flow-title {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 700;
}

.flow-desc {
    color: #B9D9CE;
    font-size: 12px;
    line-height: 1.5;
}

.side-foot {
    color: #9CC4B7;
    font-size: 11px;
    margin-top: 6px;
}

/* HEADINGS */

.main-heading {
    color: var(--teal);
    font-size: 35px;
    font-weight: 800;
    letter-spacing: -1px;
}

.main-subtitle {
    color: var(--muted);
    font-size: 15px;
}

.section-heading {
    color: var(--teal);
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 8px;
}

/* HERO */

.hero-card {
    background: linear-gradient(115deg, #123B3A, #245B57);
    padding: 32px;
    border-radius: 18px;
    margin: 22px 0 28px 0;
    border: 1px solid #3B716A;
    border-bottom: 3px solid #A8DCCB;
}

.hero-title {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
}

.hero-description {
    color: #E1F1EA;
    font-size: 14px;
    line-height: 1.8;
    max-width: 680px;
    margin-top: 9px;
}

.hero-accent {
    color: #F28C72;
}

/* FORM CARD */

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 4px 16px rgba(18, 59, 58, 0.035);
}

/* TEXT AREA */

.stTextArea label {
    color: var(--teal) !important;
    font-weight: 700;
}

/* the border lives on the wrapper, not the textarea itself */
div[data-baseweb="textarea"] {
    background: #FCFDFC !important;
    border: 1px solid #C8DAD1 !important;
    border-radius: 11px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-baseweb="base-input"] {
    border: none !important;
    background: transparent !important;
}

/* whichever inner layer carries the dark border, recolour it */
[data-testid="stTextArea"] div,
[data-testid="stTextArea"] textarea {
    border-color: #C8DAD1 !important;
}

[data-testid="stTextArea"]:focus-within div,
[data-testid="stTextArea"]:focus-within textarea {
    border-color: #245B57 !important;
}

div[data-baseweb="textarea"]:focus-within {
    border: 1px solid #245B57 !important;
    box-shadow: 0 0 0 2px rgba(36, 91, 87, 0.12) !important;
}

.stTextArea textarea {
    background: #FCFDFC !important;
    color: var(--text) !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* VISIBLE PLACEHOLDER */

.stTextArea textarea::placeholder {
    color: #788982 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #788982 !important;
}

/* "Press Ctrl+Enter to submit form" hint */

[data-testid="InputInstructions"] {
    color: #667A74 !important;
}

/* PRIMARY CALL TO ACTION */

div[data-testid="stFormSubmitButton"] button {
    background: #F28C72 !important;
    color: #263A36 !important;
    border: 1px solid #F28C72 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 800 !important;
    transition: all 0.2s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #123B3A !important;
    color: #FFFFFF !important;
    border-color: #123B3A !important;
}

/* OTHER BUTTONS */

div.stButton > button {
    background: #245B57;
    color: #FFFFFF;
    border: 1px solid #245B57;
    border-radius: 10px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #123B3A;
    color: #FFFFFF;
    border-color: #123B3A;
}

/* METRIC CARDS (Intelligence Report) */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #D5E3DC;
    border-top: 3px solid #A8DCCB;
    box-shadow: 0 4px 14px rgba(18, 59, 58, 0.04);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #4F645E !important;
    opacity: 1 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    color: #123B3A !important;
    font-weight: 800;
    font-size: 26px;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* AI STATUS PANEL */

.ai-status {
    background: #E8F5EF;
    border: 1px solid #A8DCCB;
    border-left: 4px solid #245B57;
    border-radius: 12px;
    padding: 15px 18px;
    color: #123B3A;
    font-weight: 600;
    margin: 15px 0;
}

/* EXPANDER */

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #D5E3DC;
    border-radius: 12px;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    background: #E8F5EF !important;
}

div[data-testid="stExpander"] summary * {
    color: #123B3A !important;
    font-weight: 600;
}

div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
    background: #FFFFFF;
    color: #203432;
}

/* SUCCESS BANNER */

.success-banner {
    background: #E8F5EF;
    border: 1px solid #A8DCCB;
    border-left: 4px solid #278568;
    border-radius: 12px;
    padding: 14px 18px;
    color: #123B3A;
    font-weight: 600;
    margin: 16px 0 8px 0;
}

/* ALERTS */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* DIVIDERS */

hr {
    border-color: #D5E3DC;
}

/* FONT FIX: Streamlit's markdown container overrides DM Sans */

.main-heading, .main-subtitle, .section-heading,
.hero-card, .hero-card *,
.brand-name, .brand-tagline, .sidebar-label, .sidebar-note,
.live-card, .live-card *, .flow, .flow *, .side-foot,
.ai-status, .ai-status *, .footer,
.report-head, .report-head *, .report-card, .report-card *,
[data-testid="stMarkdownContainer"] p {
    font-family: 'DM Sans', sans-serif !important;
}

/* BIGGER PRIMARY BUTTON */

div[data-testid="stFormSubmitButton"] button {
    min-height: 54px;
}

div[data-testid="stFormSubmitButton"] button p {
    font-size: 17px !important;
    font-weight: 800 !important;
    color: #263A36 !important;
}

div[data-testid="stFormSubmitButton"] button:hover p {
    color: #FFFFFF !important;
}

/* INTELLIGENCE REPORT */

.report-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin: 34px 0 14px 0;
}

.ticket-chip {
    background: #123B3A;
    color: #A8DCCB;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
    border-radius: 20px;
    padding: 6px 14px;
}

.ticket-chip span {
    color: #D3EDE3;
    font-weight: 500;
    letter-spacing: 0;
    margin-left: 10px;
    padding-left: 10px;
    border-left: 1px solid rgba(168, 220, 203, 0.4);
}

.report-card {
    background: #FFFFFF;
    border: 1px solid #D5E3DC;
    border-top: 3px solid #A8DCCB;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(18, 59, 58, 0.04);
}

.report-label {
    color: #4F645E;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.report-value {
    color: #123B3A;
    font-size: 26px;
    font-weight: 800;
    line-height: 1.25;
}

.report-hint {
    color: #667A74;
    font-size: 12px;
    margin-top: 8px;
}

.bar {
    height: 8px;
    background: #E6EEE9;
    border-radius: 8px;
    margin-top: 10px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #245B57, #A8DCCB);
    border-radius: 8px;
}

.badge {
    display: inline-block;
    font-size: 15px;
    font-weight: 800;
    border-radius: 20px;
    padding: 4px 16px;
}

.badge-high   { background: #FDE7E1; color: #B5442A; }
.badge-medium { background: #FBF0DC; color: #8A5E12; }
.badge-low    { background: #E8F5EF; color: #1E6B52; }

/* FOOTER */

.footer {
    color: #667A74;
    text-align: center;
    font-size: 12px;
    padding: 28px 0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 6. CHART THEME
# ==========================================

def apply_civicpulse_chart_theme(fig):

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#F6F8F5",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="DM Sans",
            color="#203432"
        ),
        colorway=[
            "#123B3A",
            "#245B57",
            "#A8DCCB",
            "#F28C72",
            "#D69B49"
        ],
        margin=dict(l=20, r=20, t=45, b=20),
        title_font=dict(size=18, color="#123B3A")
    )

    fig.update_xaxes(gridcolor="#E6EEE9", zerolinecolor="#D5E3DC")
    fig.update_yaxes(gridcolor="#E6EEE9", zerolinecolor="#D5E3DC")

    return fig


# ==========================================
# 7. SIDEBAR BRANDING AND NAVIGATION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "Citizen Portal"

PULSE_PATH = "M0 18 H70 L82 18 L92 5 L104 31 L114 12 L120 18 H260"

# highlight the active nav button (mint glow + coral edge)
active_key = "nav_portal" if st.session_state.page == "Citizen Portal" else "nav_about"
st.markdown(
    f"""<style>
    .st-key-{active_key} button {{
        background: linear-gradient(90deg, rgba(168,220,203,0.20), rgba(168,220,203,0.04)) !important;
        border: 1px solid rgba(168,220,203,0.40) !important;
        box-shadow: inset 4px 0 0 #F28C72;
    }}
    .st-key-{active_key} button p {{ color: #FFFFFF !important; }}
    </style>""",
    unsafe_allow_html=True
)

with st.sidebar:

    # --- brand + heartbeat line ---
    render(f"""
    <div style="display:flex;align-items:center;gap:12px;">
        {LOGO}
        <div>
            <div class="brand-name">CivicPulse</div>
            <div class="brand-tagline">GRIEVANCE INTELLIGENCE</div>
        </div>
    </div>
    <svg class="pulse-line" viewBox="0 0 260 36" preserveAspectRatio="none"
         width="100%" height="30" xmlns="http://www.w3.org/2000/svg">
        <path d="{PULSE_PATH}" fill="none" stroke="rgba(168,220,203,0.22)"
              stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
              vector-effect="non-scaling-stroke"/>
        <path class="pulse-run" pathLength="400" d="{PULSE_PATH}" fill="none"
              stroke="#A8DCCB" stroke-width="2.2" stroke-linecap="round"
              stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
    </svg>
    """)

    # --- navigation ---
    render('<div class="sidebar-label">WORKSPACE</div>')

    if st.button("Citizen Portal", key="nav_portal", icon=":material/edit_note:", use_container_width=True):
        st.session_state.page = "Citizen Portal"
        st.rerun()

    if st.button("About CivicPulse", key="nav_about", icon=":material/info:", use_container_width=True):
        st.session_state.page = "About CivicPulse"
        st.rerun()

    # --- live system card ---
    render('<div class="sidebar-label">AI SYSTEM STATUS</div>')

    render("""
    <div class="live-card">
        <div class="live-row"><span class="live-dot"></span>Model loaded</div>
        <div class="live-sub">Linear SVM classifier</div>
        <span class="chip">DECISION SUPPORT</span><span class="chip">HUMAN REVIEW</span>
    </div>
    """)

    # --- how it works ---
    render('<div class="sidebar-label">HOW IT WORKS</div>')

    render("""
    <div class="flow">
        <div class="flow-step">
            <div class="flow-num">1</div>
            <div><div class="flow-title">Report</div>
            <div class="flow-desc">Citizen describes the issue in plain words</div></div>
        </div>
        <div class="flow-step">
            <div class="flow-num">2</div>
            <div><div class="flow-title">Classify</div>
            <div class="flow-desc">ML model identifies the problem category</div></div>
        </div>
        <div class="flow-step">
            <div class="flow-num out">3</div>
            <div><div class="flow-title">Route</div>
            <div class="flow-desc">Responsible department is recommended</div></div>
        </div>
    </div>
    """)

    render('<div class="side-foot">CivicPulse Prototype v1.0</div>')

page = st.session_state.page


# ==========================================
# 8. CITIZEN PORTAL
# ==========================================

if page == "Citizen Portal":

    render('<div class="main-heading">Citizen Portal</div>')

    render(
        '<div class="main-subtitle">'
        'Report public issues. Let intelligence guide action.'
        '</div>'
    )

    render("""
    <div class="hero-card">
        <div class="hero-title">
            Better communities begin with a voice.
            <span class="hero-accent">●</span>
        </div>
        <div class="hero-description">
            Submit a public grievance and let CivicPulse's
            intelligence engine identify the issue and
            recommend the responsible department for review.
        </div>
    </div>
    """)

    render('<div class="section-heading">Submit a complaint</div>')

    with st.form("complaint_form"):

        complaint = st.text_area(
            "Describe your public issue",
            placeholder=(
                "Example: A huge pothole has formed "
                "near our residential street..."
            ),
            height=145
        )

        submitted = st.form_submit_button(
            "Analyse Complaint  →",
            use_container_width=True
        )

    if submitted:

        if not complaint.strip():

            st.warning("Please enter a complaint first.")

        else:

            with st.spinner(
                "CivicPulse intelligence engine is analysing..."
            ):

                try:

                    result = process_complaint(complaint)

                    ticket_id = result.get("ticket_id", "-")
                    submitted_at = result.get("submitted_at", "")
                    confidence = result.get("confidence")
                    priority = result.get("priority", "Low")
                    reason = result.get("priority_reason", "")

                    render(f"""
                    <div class="report-head">
                        <div class="section-heading" style="margin:0;">
                            Intelligence Report
                        </div>
                        <div class="ticket-chip">
                            {ticket_id}<span>{submitted_at}</span>
                        </div>
                    </div>
                    """)

                    col1, col2 = st.columns(2)

                    with col1:
                        render(report_card(
                            "Predicted Category",
                            result["category"]
                        ))

                    with col2:
                        render(report_card(
                            "Recommended Department",
                            result["recommended_department"]
                        ))

                    col3, col4 = st.columns(2)

                    with col3:
                        if confidence is None:
                            render(report_card(
                                "Model Confidence", "N/A",
                                "Confidence is not available for this model"
                            ))
                        else:
                            render(report_card(
                                "Model Confidence",
                                f"{confidence:.0f}%",
                                "Relative score from the classifier",
                                extra=(
                                    '<div class="bar"><div class="bar-fill" '
                                    f'style="width:{confidence:.0f}%"></div></div>'
                                )
                            ))

                    with col4:
                        hint = (
                            f"Triggered by: &ldquo;{reason}&rdquo;"
                            if reason else
                            "No urgency indicators detected"
                        )
                        render(report_card(
                            "Priority Level",
                            f'<span class="badge badge-{priority.lower()}">'
                            f'{priority}</span>',
                            hint
                        ))

                    render(f"""
                    <div class="ai-status">
                        ✓ Analysis complete
                        <br>
                        <span style="font-weight:400;">
                            Status: {result["status"]}
                            · Recommended for human review
                            before any action is taken
                        </span>
                    </div>
                    """)

                    with st.expander("View submitted complaint"):
                        st.write(complaint)

                except Exception as error:

                    st.error(f"Analysis failed: {error}")


# ==========================================
# 9. ABOUT CIVICPULSE
# ==========================================

elif page == "About CivicPulse":

    render('<div class="main-heading">About CivicPulse</div>')

    render(
        '<div class="main-subtitle">'
        'Making public grievance management more intelligent.'
        '</div>'
    )

    st.divider()

    st.subheader("Our Mission")

    st.write(
        "CivicPulse is an ML-powered public grievance "
        "intelligence and decision-support platform. "
        "It analyses citizen complaints and recommends "
        "appropriate departments for human review."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("ML Algorithm", "Linear SVM")
    col2.metric("Complaint Categories", "8")
    col3.metric("Platform", "AI + ML")


# ==========================================
# 10. FOOTER
# ==========================================

render(
    '<div class="footer">'
    'CivicPulse | Intelligent Grievance Management '
    '&amp; Decision Support'
    '</div>'
)