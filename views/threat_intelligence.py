import streamlit as st
from utils.ui import apply_styles, page_header, footer, sidebar_brand, sidebar_status
from utils.session import init_state
from intel.virustotal import lookup

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("Threat Intelligence","Check extracted indicators with VirusTotal.","🌐")
analysis = st.session_state.analysis
if not analysis:
    st.info("Run an email investigation first.")
else:
    api_key = ""
    try:
        api_key = st.secrets.get("VIRUSTOTAL_API_KEY","")
    except Exception:
        pass
    api_key = st.text_input("VirusTotal API key (optional)",value=api_key,type="password")
    kind = st.selectbox("Indicator type",["url","domain","ip"])
    lookup_key = {"url":"urls","domain":"domains","ip":"ips"}[kind]
    options = analysis["iocs"].get(lookup_key,[])
    if not options:
        st.info(f"No {kind} indicators are available.")
    else:
        indicator = st.selectbox("Indicator",options)
        if st.button("Run VirusTotal Lookup"):
            with st.spinner("Querying VirusTotal..."):
                st.json(lookup(indicator,kind,api_key))
    st.caption("Only submit indicators you are authorised to share with an external service.")
footer()
