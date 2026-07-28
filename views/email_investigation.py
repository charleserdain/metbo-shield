from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from ml.model import predict
from utils.detector import analyze_email
from utils.helpers import classification, recommendation, threat_level
from utils.parser import parse_eml
from utils.session import add_current_case_to_history, init_state, log_event
from utils.ui import apply_styles, footer, page_header, section_title, sidebar_brand, sidebar_status

apply_styles()
init_state(); sidebar_brand(); sidebar_status()
page_header("Email Investigation", "Analyse message content through rules, machine learning, IOC extraction, and authentication checks.", "📧")

section_title("Evidence Intake", "New Investigation")
mode = st.radio("Input method", ["Upload .eml", "Manual entry"], horizontal=True)
email_data = None
if mode == "Upload .eml":
    uploaded = st.file_uploader("Upload an email file", type=["eml"])
    if uploaded:
        email_data = parse_eml(uploaded.getvalue())
else:
    a, b = st.columns(2)
    sender = a.text_input("From")
    reply_to = b.text_input("Reply-To")
    recipient = a.text_input("To")
    subject = b.text_input("Subject")
    body = st.text_area("Message body", height=210)
    attachments = st.text_input("Attachments, separated by commas")
    email_data = {
        "from": sender, "reply_to": reply_to, "to": recipient, "subject": subject, "body": body,
        "attachments": [x.strip() for x in attachments.split(",") if x.strip()], "headers": {},
    }

if email_data and st.button("Run full investigation", type="primary", use_container_width=True):
    with st.spinner("Running rule analysis, ML classification, IOC extraction, and authentication review..."):
        analysis = analyze_email(email_data)
        ml_result = predict(f"{email_data.get('subject', '')}\n{email_data.get('body', '')}")
        hybrid = min(100, round(analysis["rule_score"] * .65 + ml_result["probability"] * .35))
        st.session_state.email_data = email_data
        st.session_state.analysis = analysis
        st.session_state.ml_result = ml_result
        st.session_state.hybrid_score = hybrid
        st.session_state.priority = "Critical" if hybrid >= 85 else ("High" if hybrid >= 65 else ("Medium" if hybrid >= 40 else "Low"))
        st.session_state.status = "In Review"
        st.session_state.investigation_timeline = [
            ("Email collected", "Message content and headers loaded"),
            ("Headers parsed", "Sender, Reply-To, authentication, and routing data reviewed"),
            ("Rule engine completed", f"Rule score: {analysis['rule_score']}/100"),
            ("ML classifier completed", f"Phishing probability: {ml_result['probability']}%"),
            ("IOC extraction completed", f"{len(analysis.get('iocs', [])) if isinstance(analysis.get('iocs'), list) else 0} indicator records identified"),
            ("Case updated", "Investigation placed In Review"),
        ]
        add_current_case_to_history()
        log_event("Investigation completed", f"{st.session_state.case_id} scored {hybrid}/100")
    st.success("Investigation completed successfully.")

analysis = st.session_state.analysis
if analysis:
    hybrid = int(st.session_state.hybrid_score)
    data = st.session_state.email_data
    ml = st.session_state.ml_result

    section_title("Investigation Summary", "Decision Support")
    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="email-summary-card">
              <div><span>FROM</span><strong>{data.get('from','') or 'Unknown'}</strong></div>
              <div><span>TO</span><strong>{data.get('to','') or 'Not supplied'}</strong></div>
              <div><span>SUBJECT</span><strong>{data.get('subject','') or '(No subject)'}</strong></div>
              <div><span>REPLY-TO</span><strong>{data.get('reply_to','') or 'Not present'}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.text_area("Email preview", data.get("body", ""), height=300, disabled=True)
    with right:
        gauge_color = "#ff4757" if hybrid >= 85 else "#ff9f1a" if hybrid >= 65 else "#ffd43b" if hybrid >= 40 else "#2bd763"
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=hybrid,
            number={"suffix": "/100", "font": {"size": 34, "color": "white"}},
            title={"text": f"{threat_level(hybrid).upper()} RISK", "font": {"size": 15, "color": "#9fb2c8"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#6f839b"},
                "bar": {"color": gauge_color},
                "bgcolor": "#0b1420",
                "bordercolor": "#263a50",
                "steps": [
                    {"range": [0, 35], "color": "#10271d"}, {"range": [35, 65], "color": "#2b2811"},
                    {"range": [65, 85], "color": "#302111"}, {"range": [85, 100], "color": "#30151a"},
                ],
            },
        ))
        fig.update_layout(height=270, margin=dict(l=20, r=20, t=55, b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f'<div class="recommendation-card"><b>Recommended action</b><span>{recommendation(hybrid)}</span></div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rule Score", f"{analysis['rule_score']}/100")
    m2.metric("ML Probability", f"{ml['probability']}%")
    m3.metric("Classification", classification(hybrid))
    m4.metric("Indicators", len(analysis["findings"]))

    tabs = st.tabs(["Analysis", "Findings", "Authentication", "Timeline", "Raw Headers"])
    with tabs[0]:
        a, b, c = st.columns(3)
        a.metric("ML Prediction", ml["prediction"])
        b.metric("ML Confidence", f"{ml['confidence']}%")
        c.metric("Priority", st.session_state.priority)
        st.info("The ML component is a portfolio demonstration and should be combined with analyst judgement.")
    with tabs[1]:
        if analysis["findings"]:
            st.dataframe(analysis["findings"], use_container_width=True, hide_index=True)
        else:
            st.success("No rule-based phishing indicators were detected.")
    with tabs[2]:
        cols = st.columns(3)
        for col, (name, result) in zip(cols, analysis["authentication"].items()):
            col.metric(name, str(result).upper())
    with tabs[3]:
        timeline = st.session_state.get("investigation_timeline", [])
        now = datetime.now().strftime("%H:%M:%S")
        html = '<div class="timeline-shell">'
        for idx, (title, detail) in enumerate(timeline, start=1):
            html += f'<div class="timeline-item"><span>{idx}</span><div><b>{title}</b><small>{detail}</small></div><time>{now}</time></div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)
    with tabs[4]:
        headers = data.get("headers", {})
        if headers:
            st.json(headers)
        else:
            st.caption("No raw headers were supplied for this investigation.")

footer()
