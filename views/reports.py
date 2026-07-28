import csv, io, json
import streamlit as st
from utils.ui import apply_styles, page_header, footer, sidebar_brand, sidebar_status
from utils.session import init_state
from utils.helpers import threat_level, classification, recommendation
from utils.mitre_mapper import map_mitre
from reports.pdf_report import build_pdf

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("Reports","Export the current investigation in JSON, CSV, or PDF format.","📄")
analysis = st.session_state.analysis
if not analysis:
    st.info("Run an email investigation first.")
else:
    score = st.session_state.hybrid_score
    case = {
        "product":"METBO Shield v6",
        "case_id":st.session_state.case_id,
        "analyst":st.session_state.analyst,
        "status":st.session_state.status,
        "priority":st.session_state.priority,
        "disposition":st.session_state.disposition,
        "hybrid_score":score,
        "rule_score":analysis["rule_score"],
        "ml_result":st.session_state.ml_result,
        "threat_level":threat_level(score),
        "classification":classification(score),
        "recommendation":recommendation(score),
        "email":st.session_state.email_data,
        "findings":analysis["findings"],
        "iocs":analysis["iocs"],
        "authentication":analysis["authentication"],
        "mitre_attack":map_mitre(analysis["findings"]),
        "notes":st.session_state.notes,
    }
    json_bytes = json.dumps(case,indent=2,default=str).encode()
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer,fieldnames=["category","severity","evidence","points"])
    writer.writeheader(); writer.writerows(analysis["findings"])
    pdf_bytes = build_pdf(case)
    a,b,c = st.columns(3)
    a.download_button("Download JSON",json_bytes,file_name=f"{case['case_id']}.json",mime="application/json",use_container_width=True)
    b.download_button("Download CSV",csv_buffer.getvalue(),file_name=f"{case['case_id']}.csv",mime="text/csv",use_container_width=True)
    c.download_button("Download PDF",pdf_bytes,file_name=f"{case['case_id']}.pdf",mime="application/pdf",use_container_width=True)
    st.subheader("Report Preview")
    st.json(case)
footer()
