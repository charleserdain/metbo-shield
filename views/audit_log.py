import pandas as pd
import streamlit as st
from utils.session import init_state
from utils.ui import apply_styles, sidebar_brand, sidebar_status, page_header, footer

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("Audit Log", "Review analyst actions recorded during this browser session.", "☷")
logs = st.session_state.get("audit_log", [])
if logs:
    st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)
else:
    st.info("No audit events have been recorded in this session yet.")
footer()
