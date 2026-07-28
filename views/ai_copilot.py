import html
import streamlit as st

from utils.helpers import recommendation, threat_level
from utils.mitre_mapper import map_mitre
from utils.session import init_state
from utils.ui import apply_styles, footer, page_header, section_title, sidebar_brand, sidebar_status

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("AI Copilot", "Generate an explainable analyst brief from the current investigation evidence.", "🤖")

analysis = st.session_state.analysis
if not analysis:
    st.info("Run an email investigation first. The copilot uses the active case evidence and does not invent external intelligence.")
    footer(); st.stop()

risk = int(st.session_state.hybrid_score)
email = st.session_state.email_data or {}
ml = st.session_state.ml_result or {}
findings = analysis.get("findings", [])
auth = analysis.get("authentication", {})
mitre = map_mitre(findings)

failed_auth = [name.upper() for name, value in auth.items() if str(value).lower() not in {"pass", "passed", "true", "valid"}]
reasons = []
for finding in findings[:5]:
    if isinstance(finding, dict):
        reasons.append(str(finding.get("Finding") or finding.get("description") or finding.get("Detail") or finding))
    else:
        reasons.append(str(finding))
if failed_auth:
    reasons.append("Authentication concerns: " + ", ".join(failed_auth))
if email.get("reply_to") and email.get("from") and email.get("reply_to") != email.get("from"):
    reasons.append("Reply-To differs from the visible sender")
if not reasons:
    reasons.append("No material phishing indicators were identified by the current rules")

section_title("Executive Brief", "Current Case")
st.markdown(
    f'''<div class="copilot-hero"><div><span>CASE {html.escape(st.session_state.case_id)}</span><h2>{html.escape(threat_level(risk))} risk — {risk}/100</h2><p>{html.escape(recommendation(risk))}</p></div><div class="copilot-score">{risk}</div></div>''',
    unsafe_allow_html=True,
)

left, right = st.columns([1.25, 1], gap="large")
with left:
    section_title("Why the score is elevated", "Evidence Summary")
    items = ''.join(f'<li>{html.escape(r)}</li>' for r in reasons)
    st.markdown(f'<div class="copilot-card"><ul>{items}</ul></div>', unsafe_allow_html=True)
with right:
    section_title("Model Signals", "Decision Support")
    st.metric("Rule score", f"{analysis.get('rule_score', 0)}/100")
    st.metric("ML probability", f"{ml.get('probability', 0)}%")
    st.metric("Recommended priority", st.session_state.priority)

section_title("Analyst Next Steps", "Response Plan")
steps = [
    "Preserve the original message and complete headers as case evidence.",
    "Block or investigate suspicious URLs, domains, IPs, and attachments.",
    "Confirm whether the sender and business request are expected through a trusted channel.",
    "Escalate or quarantine the message when the evidence supports phishing.",
]
cols = st.columns(4)
for idx, (col, step) in enumerate(zip(cols, steps), start=1):
    with col:
        st.markdown(f'<div class="next-step"><span>{idx}</span><p>{html.escape(step)}</p></div>', unsafe_allow_html=True)

section_title("ATT&CK Context", "Mapped Techniques")
if mitre:
    st.dataframe(mitre, use_container_width=True, hide_index=True)
else:
    st.caption("No MITRE ATT&CK technique was mapped from the current findings.")

st.info("This copilot is an explainable portfolio assistant. It summarises local case evidence and does not replace analyst judgement.")
footer()
