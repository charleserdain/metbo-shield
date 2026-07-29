import streamlit as st
from utils.session import init_state

st.set_page_config(
    page_title="METBO Shield | Enterprise SOC",
    page_icon="assets/metbo_shield_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
init_state()

pages = {
    "SECURITY OPERATIONS": [
        st.Page("views/dashboard.py", title="Dashboard", icon="🏠", default=True),
        st.Page("views/email_investigation.py", title="Email Investigation", icon="✉️"),
        st.Page("views/case_management.py", title="Case Management", icon="📂"),
        st.Page("views/ioc_explorer.py", title="IOC Explorer", icon="🔎"),
        st.Page("views/mitre_attack.py", title="MITRE ATT&CK", icon="🎯"),
        st.Page("views/analyst_notes.py", title="Analyst Notes", icon="📝"),
        st.Page("views/ai_copilot.py", title="AI Copilot", icon="🤖"),
        st.Page("views/threat_intelligence.py", title="Threat Intelligence", icon="🌐"),
        st.Page("views/reports.py", title="Reports", icon="📄"),
       st.Page("views/audit_log.py", title="Audit Log", icon="📋"),
        st.Page("views/settings.py", title="Settings", icon="⚙️"),
    ]
}
st.navigation(pages).run()
