import pandas as pd
import streamlit as st

from utils.session import init_state
from utils.ui import apply_styles, footer, page_header, sidebar_brand, sidebar_status, section_title

apply_styles()
init_state(); sidebar_brand(); sidebar_status()
page_header("Case Management", "Review, prioritise, and reopen investigation records.", "📂")

history = pd.DataFrame(st.session_state.case_history)
if history.empty:
    st.info("No cases have been recorded yet.")
    footer(); st.stop()

section_title("Case Queue", "Analyst Operations")
f1, f2, f3 = st.columns([1, 1, 1.2])
status_filter = f1.multiselect("Status", sorted(history["Status"].dropna().unique()), default=[])
priority_filter = f2.multiselect("Priority", ["Critical", "High", "Medium", "Low"], default=[])
search = f3.text_input("Search case ID or disposition")

filtered = history.copy()
if status_filter:
    filtered = filtered[filtered["Status"].isin(status_filter)]
if priority_filter:
    filtered = filtered[filtered["Priority"].isin(priority_filter)]
if search:
    mask = filtered.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
    filtered = filtered[mask]

st.dataframe(
    filtered[["Case ID", "Date", "Status", "Priority", "Risk", "Disposition", "Source"]],
    use_container_width=True,
    hide_index=True,
    height=340,
)

section_title("Case Detail", "Selected Record")
case_ids = filtered["Case ID"].tolist()
if not case_ids:
    st.warning("No cases match the current filters.")
else:
    selected_id = st.selectbox("Select a case", case_ids)
    record = filtered[filtered["Case ID"] == selected_id].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk", f"{int(record['Risk'])}/100")
    c2.metric("Priority", record["Priority"])
    c3.metric("Status", record["Status"])
    c4.metric("Source", record["Source"])

    left, right = st.columns([1.4, 1], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="case-detail-card">
              <span>CASE IDENTIFIER</span><strong>{record['Case ID']}</strong>
              <span>CREATED / UPDATED</span><strong>{record['Date']}</strong>
              <span>DISPOSITION</span><strong>{record['Disposition']}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        new_status = st.selectbox("Update status", ["Open", "In Review", "Closed"], index=["Open", "In Review", "Closed"].index(record["Status"]) if record["Status"] in ["Open", "In Review", "Closed"] else 0)
        new_disposition = st.selectbox("Disposition", ["Pending Review", "Benign", "Suspicious", "Confirmed Phishing", "Escalated"], index=0)
        if st.button("Save case update", type="primary", use_container_width=True):
            for item in st.session_state.case_history:
                if item["Case ID"] == selected_id:
                    item["Status"] = new_status
                    item["Disposition"] = new_disposition
                    break
            st.success(f"Updated {selected_id}.")
            st.rerun()

footer()
