import streamlit as st
from utils.session import init_state, log_event
from utils.ui import apply_styles, sidebar_brand, sidebar_status, page_header, section_title, footer

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("Settings", "Configure the local analyst experience and demonstration preferences.", "⚙")

section_title("Analyst Profile", "Workspace")
st.session_state.analyst = st.text_input("Analyst display name", value=st.session_state.analyst)
st.session_state.show_sample_data = st.toggle("Show fictional demonstration cases", value=st.session_state.show_sample_data)

section_title("Threat Intelligence", "Integrations")
st.info("VirusTotal is optional. Add VIRUSTOTAL_API_KEY to .streamlit/secrets.toml for local use or to Streamlit Cloud secrets after deployment.")

section_title("Data Handling", "Privacy")
st.warning("METBO Shield stores investigation data only in the active Streamlit session. Do not upload sensitive production email unless you control the environment.")
if st.button("Save preferences", type="primary"):
    log_event("Settings updated", "Analyst profile or demo-data preference changed")
    st.success("Preferences saved for this browser session.")

if st.button("Reset current session", type="secondary"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
footer()
