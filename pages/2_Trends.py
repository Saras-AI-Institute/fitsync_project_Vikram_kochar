import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="FitSync – Trends")

# ── Global styles ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0e0e0e;
    color: #e8e8e8;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem 3rem; max-width: 1400px; }

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
.divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 2rem 0;
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 1rem;
}

/* ── Stat grid ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin-bottom: 0;
}
.stat-block {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
}
.stat-name {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 0.8rem;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.35rem;
}
.stat-key {
    font-size: 0.72rem;
    color: #555;
}
.stat-val {
    font-size: 0.95rem;
    font-weight: 500;
    color: #d4d4d4;
    letter-spacing: -0.01em;
}

/* ── Chart card ── */
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
</style>
""", unsafe_allow_html=True)

# ── Plotly base theme ────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#888", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor="#1a1a1a", linecolor="#222", tickcolor="#333", showgrid=True, zeroline=False),
    yaxis=dict(gridcolor="#1a1a1a", linecolor="#222", tickcolor="#333", showgrid=True, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#222", font=dict(color="#666", size=10)),
    hoverlabel=dict(bgcolor="#1a1a1a", bordercolor="#333", font=dict(family="DM Sans", color="#e8e8e8", size=12)),
)
GREEN    = "#4ade80"
TEAL     = "#2dd4bf"
LAVENDER = "#a78bfa"
AMBER    = "#fbbf24"
PALETTE  = [GREEN, TEAL, LAVENDER, AMBER]

# ── Data ─────────────────────────────────────────────────────────────────────
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
st.markdown('<div class="page-label">● FitSync — Trends</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Trends &amp; Insights</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-sub">Showing data for <b style="color:#4ade80">{time_range}</b></div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Summary stats ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Summary Statistics</div>', unsafe_allow_html=True)

METRICS = [
    ('Recovery_Score', 'Recovery Score'),
    ('Sleep_Hours',    'Sleep Hours'),
    ('Steps',          'Steps'),
    ('Calories_Burned','Calories Burned'),
]

cols = st.columns(4)
for i, (col_key, label) in enumerate(METRICS):
    mean = filtered_data[col_key].mean()
    mn   = filtered_data[col_key].min()
    mx   = filtered_data[col_key].max()
    with cols[i]:
        st.markdown(f"""
        <div class="stat-block">
            <div class="stat-name">{label}</div>
            <div class="stat-row"><span class="stat-key">Mean</span><span class="stat-val">{mean:.1f}</span></div>
            <div class="stat-row"><span class="stat-key">Min</span><span class="stat-val">{mn:.1f}</span></div>
            <div class="stat-row"><span class="stat-key">Max</span><span class="stat-val">{mx:.1f}</span></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Monthly avg recovery ──────────────────────────────────────────────────────
st.markdown('<div class="section-label">Monthly Average Recovery Score</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card"><div class="chart-title">Recovery Score — Month over Month</div>', unsafe_allow_html=True)

fd = filtered_data.copy()
fd['Month'] = fd['Date'].dt.to_period('M').astype(str)
monthly_avg = fd.groupby('Month')['Recovery_Score'].mean().reset_index()

fig_monthly = go.Figure()
fig_monthly.add_trace(go.Bar(
    x=monthly_avg['Month'],
    y=monthly_avg['Recovery_Score'],
    marker=dict(
        color=monthly_avg['Recovery_Score'],
        colorscale=[[0, "#1a2e1a"], [0.5, "#22c55e"], [1, "#4ade80"]],
        showscale=False,

    ),
    hovertemplate="<b>%{x}</b><br>Avg Recovery: %{y:.1f}<extra></extra>"
))
fig_monthly.update_layout(**PLOT_LAYOUT, height=280)
st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Distributions ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Distributions</div>', unsafe_allow_html=True)

dist_cols = st.columns(2)
dist_metrics = [
    ('Steps',          'Daily Steps',       GREEN),
    ('Calories_Burned','Calories Burned',   AMBER),
    ('Recovery_Score', 'Recovery Score',    TEAL),
    ('Sleep_Hours',    'Sleep Hours',       LAVENDER),
]

for idx, (metric, label, color) in enumerate(dist_metrics):
    with dist_cols[idx % 2]:
        st.markdown(f'<div class="chart-card"><div class="chart-title">Distribution — {label}</div>', unsafe_allow_html=True)
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=filtered_data[metric],
            marker=dict(
                color=color,
                opacity=0.75,
                line=dict(color="rgba(0,0,0,0)", width=0)
            ),
            hovertemplate=f"<b>{label}</b><br>Count: %{{y}}<extra></extra>"
        ))
        fig_hist.update_layout(**PLOT_LAYOUT, height=240,
                               bargap=0.06)
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)