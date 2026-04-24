import streamlit as st

st.set_page_config(layout="wide", page_title="FitSync")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

col_spacer, col_toggle = st.columns([11, 1])
with col_toggle:
    label = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

dark = st.session_state.dark_mode

if dark:
    bg          = "#0F1117"
    surface     = "#1A1D27"
    border      = "rgba(255,255,255,0.08)"
    text_pri    = "#F0F2F5"
    text_sec    = "rgba(240,242,245,0.5)"
    text_muted  = "rgba(240,242,245,0.28)"
    accent      = "#4ADE80"
    divider     = "rgba(255,255,255,0.07)"
    sb_bg       = "#0F1117"
    sb_text     = "#F0F2F5"
    sb_text_sec = "rgba(240,242,245,0.5)"
    stroke      = "rgba(255,255,255,0.15)"
else:
    bg          = "#F7F8FA"
    surface     = "#FFFFFF"
    border      = "rgba(0,0,0,0.09)"
    text_pri    = "#111318"
    text_sec    = "rgba(17,19,24,0.55)"
    text_muted  = "rgba(17,19,24,0.35)"
    accent      = "#16A34A"
    divider     = "rgba(0,0,0,0.07)"
    sb_bg       = "#EDEEF2"
    sb_text     = "#111318"
    sb_text_sec = "rgba(17,19,24,0.6)"
    stroke      = "rgba(17,19,24,0.15)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

#MainMenu, footer, header {{ visibility: hidden; }}

.block-container {{
    padding: 1rem 2rem 2rem 2rem !important;
    max-width: 100% !important;
    background: {bg};
    min-height: 100vh;
}}

/* Sidebar full fix */
section[data-testid="stSidebar"] {{
    background: {sb_bg} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {sb_text} !important;
}}
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] li {{
    color: {sb_text} !important;
}}
section[data-testid="stSidebar"] .st-emotion-cache-1cypcdb,
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{
    color: {sb_text} !important;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] p {{
    color: {sb_text} !important;
}}

.fs-wrap {{
    font-family: 'DM Sans', sans-serif;
    color: {text_pri};
    max-width: 680px;
    margin: 40px auto 0 auto;
    padding-bottom: 60px;
}}

.fs-logo {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 40px;
}}

.logo-dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: {accent};
    animation: blink 2.2s ease-in-out infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50%       {{ opacity: 0.35; }}
}}

.logo-name {{
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: {text_pri};
}}

.logo-tag {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: {accent};
    border: 0.5px solid {accent};
    padding: 2px 7px;
    border-radius: 4px;
    opacity: 0.75;
}}

.fs-divider {{
    width: 100%;
    height: 0.5px;
    background: {divider};
    margin: 32px 0;
}}

.eyebrow {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: {text_muted};
    text-transform: uppercase;
    margin-bottom: 12px;
}}

.fs-title {{
    font-family: 'Syne', sans-serif;
    font-size: 38px;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -1.5px;
    color: {text_pri};
    margin-bottom: 14px;
}}

.fs-title .outline {{
    color: transparent;
    -webkit-text-stroke: 1px {stroke};
}}

.fs-sub {{
    font-size: 14px;
    color: {text_sec};
    line-height: 1.75;
    font-weight: 300;
    max-width: 500px;
    margin-bottom: 0;
}}

.section-label {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.8px;
    color: {text_muted};
    text-transform: uppercase;
    margin-bottom: 14px;
}}

.cards-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 32px;
}}

.card {{
    background: {surface};
    border: 0.5px solid {border};
    border-radius: 10px;
    padding: 16px 18px;
}}

.card-title {{
    font-size: 13px;
    font-weight: 500;
    color: {text_pri};
    margin-bottom: 4px;
}}

.card-desc {{
    font-size: 12px;
    color: {text_sec};
    line-height: 1.6;
    font-weight: 300;
}}

.nav-hint {{
    background: {surface};
    border: 0.5px solid {border};
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: {text_sec};
    line-height: 1.6;
}}

.nav-hint strong {{
    color: {text_pri};
    font-weight: 500;
}}

.fs-footer {{
    margin-top: 48px;
    border-top: 0.5px solid {divider};
    padding-top: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.footer-text {{
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: {text_muted};
}}
</style>

<div class="fs-wrap">

  <div class="fs-logo">
    <div class="logo-dot"></div>
    <span class="logo-name">FitSync</span>
    <span class="logo-tag">v1.0</span>
  </div>

  <div class="eyebrow">Personal health analytics</div>
  <h1 class="fs-title">
    Your health,<br><span class="outline">clearly</span> visualised.
  </h1>
  <p class="fs-sub">
    FitSync transforms your raw fitness data into clear, actionable insight —
    recovery, sleep, movement, and calorie trends all in one dashboard.
  </p>

  <div class="fs-divider"></div>

  <div class="section-label">What's inside</div>
  <div class="cards-grid">
    <div class="card">
      <div class="card-title">Recovery score</div>
      <div class="card-desc">Daily scores based on sleep quality and resting heart rate patterns.</div>
    </div>
    <div class="card">
      <div class="card-title">Activity tracking</div>
      <div class="card-desc">Steps and calories burned over time to spot movement habits.</div>
    </div>
    <div class="card">
      <div class="card-title">Sleep analysis</div>
      <div class="card-desc">Sleep hours across weeks and their impact on your recovery.</div>
    </div>
    <div class="card">
      <div class="card-title">Trend insights</div>
      <div class="card-desc">Monthly averages and distributions across every health metric.</div>
    </div>
  </div>

  <div class="nav-hint">
    &#8592; Use the <strong>sidebar</strong> to navigate &mdash;
    <strong>Dashboard</strong> for your full analytics view,
    or <strong>Trends</strong> for deeper pattern analysis.
  </div>

  <div class="fs-footer">
    <span class="footer-text">Built with Streamlit &nbsp;&middot;&nbsp; FitSync &copy; 2025</span>
    <span class="footer-text">{'dark' if dark else 'light'} mode</span>
  </div>

</div>
""", unsafe_allow_html=True)