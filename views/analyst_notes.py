import streamlit as st
from utils.ui import apply_styles, page_header, footer, sidebar_brand, sidebar_status
from utils.session import init_state

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("Analyst Notes","Document case status, disposition, and investigation decisions.","📝")
st.session_state.analyst = st.text_input("Analyst",value=st.session_state.analyst)
a,b,c = st.columns(3)
status_options = ["Open","Investigating","Escalated","Closed"]
priority_options = ["Low","Medium","High","Critical"]
disposition_options = ["Pending Review","Benign","Spam","Phishing","Malware","Credential Theft"]
st.session_state.status = a.selectbox("Case status",status_options,index=status_options.index(st.session_state.status))
st.session_state.priority = b.selectbox("Priority",priority_options,index=priority_options.index(st.session_state.priority))
st.session_state.disposition = c.selectbox("Disposition",disposition_options,index=disposition_options.index(st.session_state.disposition))
st.session_state.notes = st.text_area("Investigation notes",value=st.session_state.notes,height=260)
st.success("Case fields are retained during this browser session.")
footer()
