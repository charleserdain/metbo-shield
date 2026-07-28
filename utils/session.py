from datetime import datetime, timezone
import uuid
import streamlit as st


def _sample_cases() -> list[dict]:
    """Portfolio-safe fictional cases used only to make the dashboard useful before first analysis."""
    return [
        {"Case ID": "DEMO-1048", "Date": "2026-07-28 08:42", "Status": "Open", "Priority": "Critical", "Risk": 92, "Disposition": "Escalated", "Source": "Sample data"},
        {"Case ID": "DEMO-1047", "Date": "2026-07-28 07:15", "Status": "Closed", "Priority": "Low", "Risk": 14, "Disposition": "Benign", "Source": "Sample data"},
        {"Case ID": "DEMO-1046", "Date": "2026-07-27 16:33", "Status": "In Review", "Priority": "High", "Risk": 78, "Disposition": "Pending Review", "Source": "Sample data"},
        {"Case ID": "DEMO-1045", "Date": "2026-07-27 13:09", "Status": "Closed", "Priority": "Medium", "Risk": 46, "Disposition": "Suspicious", "Source": "Sample data"},
        {"Case ID": "DEMO-1044", "Date": "2026-07-27 09:54", "Status": "Closed", "Priority": "Low", "Risk": 8, "Disposition": "Benign", "Source": "Sample data"},
        {"Case ID": "DEMO-1043", "Date": "2026-07-26 18:21", "Status": "Closed", "Priority": "Critical", "Risk": 96, "Disposition": "Confirmed Phishing", "Source": "Sample data"},
    ]


def init_state() -> None:
    defaults = {
        "case_id": f"MS-{datetime.now(timezone.utc):%Y%m%d}-{uuid.uuid4().hex[:6].upper()}",
        "analyst": "Charles Erdain",
        "email_data": None,
        "analysis": None,
        "ml_result": None,
        "hybrid_score": 0,
        "notes": "",
        "status": "Open",
        "priority": "Medium",
        "disposition": "Pending Review",
        "last_analysis_at": None,
        "case_history": _sample_cases(),
        "show_sample_data": True,
        "audit_log": [],
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def add_current_case_to_history() -> None:
    """Insert or replace the current case in the dashboard history."""
    if not st.session_state.get("analysis"):
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    row = {
        "Case ID": st.session_state.case_id,
        "Date": now,
        "Status": st.session_state.status,
        "Priority": st.session_state.priority,
        "Risk": int(st.session_state.hybrid_score),
        "Disposition": st.session_state.disposition,
        "Source": "Live analysis",
    }
    history = [item for item in st.session_state.case_history if item.get("Case ID") != row["Case ID"]]
    st.session_state.case_history = [row, *history][:25]
    st.session_state.last_analysis_at = now


def log_event(action: str, detail: str = "") -> None:
    """Record a lightweight, session-only audit event."""
    event = {
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "Analyst": st.session_state.get("analyst", "Unknown"),
        "Action": action,
        "Detail": detail,
    }
    st.session_state.setdefault("audit_log", []).insert(0, event)
    st.session_state.audit_log = st.session_state.audit_log[:100]
