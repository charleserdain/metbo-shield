from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.ui import (
    apply_styles, sidebar_brand, sidebar_status, dashboard_header, status_card,
    action_card, stat_card, section_title, footer,
)
from utils.session import init_state
from utils.helpers import threat_level

apply_styles()
init_state()
sidebar_brand()
sidebar_status()
dashboard_header(st.session_state.case_id)

risk = int(st.session_state.hybrid_score or 0)
risk_label = threat_level(risk) if st.session_state.analysis else "Informational"
updated = st.session_state.last_analysis_at or "No analysis yet"

c1, c2, c3 = st.columns(3)
with c1:
    status_card("Case Status", st.session_state.status, f"Case ID: {st.session_state.case_id}", "▣", "green")
with c2:
    status_card("Current Risk Score", f"{risk}/100", f"Risk Level: {risk_label}", "⌁", "blue")
with c3:
    status_card("Last Analysis", updated, "Current browser session", "◷", "amber")

section_title("Quick Actions", "Analyst Workspace")
q1, q2, q3 = st.columns(3, gap="medium")
with q1:
    action_card("New Investigation", "Upload an .eml file or manually enter message content.", "✉", "blue")
    st.page_link("views/email_investigation.py", label="Start investigation  →", use_container_width=True)
with q2:
    action_card("Threat Intelligence", "Enrich URLs, domains, and IP addresses with VirusTotal.", "◎", "purple")
    st.page_link("views/threat_intelligence.py", label="Open intelligence  →", use_container_width=True)
with q3:
    action_card("Reports", "Review evidence and export PDF, JSON, or CSV reports.", "▤", "green")
    st.page_link("views/reports.py", label="View reports  →", use_container_width=True)

history = pd.DataFrame(st.session_state.case_history)
if history.empty:
    history = pd.DataFrame(columns=["Case ID", "Date", "Status", "Priority", "Risk", "Disposition", "Source"])

analysed = len(history)
high_risk = int((history["Risk"] >= 65).sum()) if not history.empty else 0
safe = int((history["Risk"] < 35).sum()) if not history.empty else 0
open_cases = int(history["Status"].isin(["Open", "In Review"]).sum()) if not history.empty else 0

section_title("Dashboard Statistics", "Portfolio Demonstration")
s1, s2, s3, s4 = st.columns(4)
with s1:
    stat_card("Emails Analysed", analysed, "✉", "blue", "All recorded cases")
with s2:
    stat_card("High-Risk Cases", high_risk, "◇", "red", "Score 65 or higher")
with s3:
    stat_card("Safe Emails", safe, "✓", "green", "Score below 35")
with s4:
    stat_card("Open Cases", open_cases, "▱", "amber", "Open or in review")

st.markdown(
    '<div class="demo-notice"><b>Demo data enabled</b><span>Dashboard history includes clearly labelled fictional cases so recruiters can see the full interface before running an analysis.</span></div>',
    unsafe_allow_html=True,
)

section_title("Threat Overview", "Case Telemetry")
chart_col, recent_col = st.columns([1, 1.45], gap="large")
with chart_col:
    buckets = pd.cut(
        history["Risk"].astype(int),
        bins=[-1, 34, 64, 84, 100],
        labels=["Low", "Medium", "High", "Critical"],
    ) if not history.empty else pd.Series(dtype="category")
    counts = buckets.value_counts(sort=False).reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
    chart_data = pd.DataFrame({"Severity": counts.index.astype(str), "Cases": counts.values})
    severity_colors = {"Low":"#2bd763","Medium":"#ffd43b","High":"#ff9f1a","Critical":"#ff4757"}
    fig = px.bar(chart_data, x="Severity", y="Cases", color="Severity", color_discrete_map=severity_colors, text="Cases")
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(height=300, showlegend=False, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#dce8f4", yaxis=dict(gridcolor="#243242", title="Cases"), xaxis=dict(title="Severity"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
    st.caption("Severity distribution across live and sample investigations.")
with recent_col:
    st.markdown("#### Recent Investigations")
    display = history[["Case ID", "Status", "Priority", "Risk", "Disposition", "Source"]].head(7).copy()
    display["Risk"] = display["Risk"].astype(str) + "/100"
    st.dataframe(display, use_container_width=True, hide_index=True, height=300)

trend_col, health_col = st.columns([1.45, 1], gap="large")
with trend_col:
    section_title("Risk Trend", "Recent Activity")
    trend = history.head(10).iloc[::-1].copy()
    if not trend.empty:
        trend["Investigation"] = range(1, len(trend) + 1)
        fig = go.Figure(go.Scatter(x=trend["Investigation"], y=trend["Risk"], mode="lines+markers", line=dict(width=3, color="#168fff"), marker=dict(size=8)))
        fig.update_layout(height=235, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#dce8f4", yaxis=dict(range=[0,100], gridcolor="#243242", title="Risk"), xaxis=dict(gridcolor="#1a2735", title="Investigation"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
with health_col:
    section_title("Platform Health", "System Status")
    st.markdown(
        """
        <div class="health-grid">
          <div><span class="health-dot ok"></span><b>Detection Engine</b><small>Operational</small></div>
          <div><span class="health-dot ok"></span><b>ML Classifier</b><small>Ready</small></div>
          <div><span class="health-dot ok"></span><b>IOC Extraction</b><small>Operational</small></div>
          <div><span class="health-dot info"></span><b>VirusTotal</b><small>API key optional</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

section_title("Threat Activity", "Operations Intelligence")
heat_col, feed_col = st.columns([1.35, 1], gap="large")
with heat_col:
    activity = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Investigations": [2, 4, 1, 5, 3, 1, 2],
        "High Risk": [1, 2, 0, 3, 1, 0, 1],
    })
    heat = go.Figure(data=go.Heatmap(
        z=[activity["Investigations"].tolist(), activity["High Risk"].tolist()],
        x=activity["Day"], y=["All investigations", "High risk"],
        colorscale=[[0, "#0b1725"], [0.35, "#124d7c"], [0.7, "#168fff"], [1, "#ff4757"]],
        hovertemplate="%{y}<br>%{x}: %{z}<extra></extra>", showscale=False,
    ))
    heat.update_layout(height=235, margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#dce8f4")
    st.plotly_chart(heat, use_container_width=True, config={"displayModeBar":False})
with feed_col:
    st.markdown("""
    <div class="threat-feed">
      <div><span class="feed-dot critical"></span><b>Credential harvesting</b><small>Microsoft 365 impersonation pattern</small></div>
      <div><span class="feed-dot high"></span><b>Invoice lure</b><small>Urgent payment request with external link</small></div>
      <div><span class="feed-dot medium"></span><b>Delivery notification</b><small>Brand-spoofing campaign indicator</small></div>
      <div><span class="feed-dot low"></span><b>Authentication anomaly</b><small>Reply-To and sender-domain mismatch</small></div>
    </div>
    """, unsafe_allow_html=True)


section_title("SOC Workflow")
steps = [
    ("1", "✉", "Collect", "Upload an email or enter message content"),
    ("2", "⌕", "Analyse", "Run rules and machine-learning scoring"),
    ("3", "⌘", "Enrich", "Review IOCs, authentication, and ATT&CK"),
    ("4", "▣", "Document", "Record analyst notes and disposition"),
    ("5", "▤", "Report", "Export evidence in PDF, JSON, or CSV"),
]
html = '<div class="workflow-shell"><div class="workflow-grid">'
for num, icon, title, body in steps:
    html += f'<div class="workflow-step"><div class="workflow-num">{num}</div><div class="workflow-icon">{icon}</div><b>{title}</b><span>{body}</span></div>'
html += '</div></div>'
st.markdown(html, unsafe_allow_html=True)
footer()
