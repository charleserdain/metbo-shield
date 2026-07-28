import streamlit as st
from utils.ui import apply_styles, page_header, footer, sidebar_brand, sidebar_status
from utils.session import init_state

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("IOC Explorer","Review extracted indicators of compromise.","🔎")
analysis = st.session_state.analysis
if not analysis:
    st.info("Run an email investigation first.")
else:
    for key,label in [("urls","URLs"),("domains","Domains"),("ips","IP Addresses"),("emails","Email Addresses")]:
        st.subheader(label)
        values = analysis["iocs"].get(key,[])
        if values:
            st.dataframe({label:values},use_container_width=True,hide_index=True)
        else:
            st.caption("None extracted.")
footer()
