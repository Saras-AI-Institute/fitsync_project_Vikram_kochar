import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="FitSync – Dashboard")

# ── Global styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #e8e8e8;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem 3rem; max-width: 1400px; }

/* ── Page header ── */
.page-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 0.4rem;
}
.page-title {
    font-size: 2rem;
    font-weight: 600;
    color: #f0f0f0;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.02em;
}
.page-sub {
    font-size: 0.85rem;
    color: #555;
    margin-bottom: 2.2rem;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 2rem 0;
}

/* ── Section label ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 1rem;
}

/* ── Metric cards ── */
.metric-card {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #2a2a2a; }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4ade80, transparent);
}
.metric-label {
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2.1rem;
    font-weight: 600;
    color: #f0f0f0;
    letter-spacing: -0.03em;
    line-height: 1;
}

/* ── Chart wrapper ── */
.chart-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1.2rem 1.4rem 0.8rem 1.4rem;
    margin-bottom: 1rem;
}
.chart-title {
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 0.2rem;
}

/* ── Data table ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Plotly base theme ────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#888", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(
        gridcolor="#1a1a1a", linecolor="#222", tickcolor="#333",
        showgrid=True, zeroline=False
    ),
    yaxis=dict(
        gridcolor="#1a1a1a", linecolor="#222", tickcolor="#333",
        showgrid=True, zeroline=False
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)", bordercolor="#222",
        font=dict(color="#666", size=10)
    ),
    hoverlabel=dict(
        bgcolor="#1a1a1a", bordercolor="#333",
        font=dict(family="DM Sans", color="#e8e8e8", size=12)
    ),
)
GREEN   = "#4ade80"
TEAL    = "#2dd4bf"
LAVENDER = "#a78bfa"
AMBER   = "#fbbf24"

# ── Data ────────────────────────────────────────────────────────────────────
processed_data = process_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.2rem 0 0.5rem 0;'>
        <span style='font-family:DM Mono,monospace;font-size:0.65rem;
                     letter-spacing:0.15em;text-transform:uppercase;color:#444;'>
            Filters
        </span>
    </div>
    """, unsafe_allow_html=True)
    time_range = st.selectbox(
        "Time Range",
        options=["Last 7 Days", "Last 30 Days", "All Time"],
        index=2,
        label_visibility="collapsed"
    )

def filter_data_by_time(data, time_range):
    if 'Date' in data.columns:
        max_date = data['Date'].max()
        if time_range == "Last 7 Days":
            return data[data['Date'] >= max_date - pd.Timedelta(days=7)]
        elif time_range == "Last 30 Days":
            return data[data['Date'] >= max_date - pd.Timedelta(days=30)]
    return data

filtered_data = filter_data_by_time(processed_data, time_range)

# ── Page header ──────────────────────────────────────────────────────────────
st.markdown('<div class="page-label">● FitSync — Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Personal Health Analytics</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-sub">Showing data for <b style="color:#4ade80">{time_range}</b></div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Key Metrics ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Key Metrics</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
metrics = [
    (c1, "Avg Steps",          f"{filtered_data['Steps'].mean():.0f}"),
    (c2, "Avg Sleep Hours",    f"{filtered_data['Sleep_Hours'].mean():.1f} hrs"),
    (c3, "Avg Recovery Score", f"{filtered_data['Recovery_Score'].mean():.1f}"),
]
for col, label, val in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Charts row 1 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Trends &amp; Insights</div>', unsafe_allow_html=True)

lc1, lc2 = st.columns(2)

with lc1:
    st.markdown('<div class="chart-card"><div class="chart-title">Recovery Score &amp; Sleep Trend</div>', unsafe_allow_html=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_data['Date'], y=filtered_data['Recovery_Score'],
        name="Recovery", mode="lines",
        line=dict(color=GREEN, width=1.5, shape="spline"),
        fill="tozeroy", fillcolor="rgba(74,222,128,0.05)"
    ))
    fig1.add_trace(go.Scatter(
        x=filtered_data['Date'], y=filtered_data['Sleep_Hours'],
        name="Sleep hrs", mode="lines",
        line=dict(color=TEAL, width=1.5, shape="spline", dash="dot"),
    ))
    fig1.update_layout(**PLOT_LAYOUT, height=280)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with lc2:
    st.markdown('<div class="chart-card"><div class="chart-title">Recovery Score vs Daily Steps</div>', unsafe_allow_html=True)
    fig2 = px.scatter(
        filtered_data, x='Steps', y='Recovery_Score', color='Sleep_Hours',
        color_continuous_scale=[[0, "#1a2e1a"], [0.5, "#4ade80"], [1, "#a7f3d0"]],
        labels={'Sleep_Hours': 'Sleep hrs'}
    )
    fig2.update_traces(marker=dict(size=6, opacity=0.75))
    fig2.update_layout(**PLOT_LAYOUT, height=280,
                       coloraxis_colorbar=dict(thickness=8, len=0.7, tickfont=dict(size=9, color="#555")))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts row 2 ─────────────────────────────────────────────────────────────
sc1, sc2 = st.columns(2)

with sc1:
    st.markdown('<div class="chart-card"><div class="chart-title">Recovery Score vs Resting Heart Rate</div>', unsafe_allow_html=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=filtered_data['Heart_Rate_bpm'],
        y=filtered_data['Recovery_Score'],
        mode='markers',
        marker=dict(color=LAVENDER, size=6, opacity=0.7),
        hovertemplate="HR: %{x} bpm<br>Recovery: %{y}<extra></extra>"
    ))
    fig3.update_layout(**PLOT_LAYOUT, height=280)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with sc2:
    st.markdown('<div class="chart-card"><div class="chart-title">Daily Calories Burned</div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=filtered_data['Date'], y=filtered_data['Calories_Burned'],
        mode="lines",
        line=dict(color=AMBER, width=1.5, shape="spline"),
        fill="tozeroy", fillcolor="rgba(251,191,36,0.05)"
    ))
    fig4.update_layout(**PLOT_LAYOUT, height=280)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Data table ───────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Raw Data</div>', unsafe_allow_html=True)
st.dataframe(
    processed_data.style.set_properties(**{
        'background-color': '#111',
        'color': '#ccc',
        'border-color': '#1e1e1e'
    }),
    use_container_width=True,
    height=320
)