from __future__ import annotations

from datetime import datetime
from pathlib import Path
import base64
import html
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def apply_styles() -> None:
    css_path = ROOT / "assets" / "styles.css"
    st.markdown(css_path.read_text(encoding="utf-8"), unsafe_allow_html=True)


def _image_data(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def sidebar_brand() -> None:
    logo = _image_data(ROOT / "assets" / "metbo_shield_logo.png")
    image = f'<img class="metbo-logo" src="{logo}" alt="METBO Shield logo">' if logo else '<div class="metbo-logo-fallback">M</div>'
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            {image}
            <div class="sidebar-product"><strong>METBO</strong><span>SHIELD</span></div>
        </div>
        <div class="sidebar-tagline">AI-Assisted Phishing Investigation Platform</div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_status() -> None:
    st.sidebar.markdown(
        f"""
        <div class="sidebar-divider"></div>
        <div class="system-label">SYSTEM</div>
        <div class="system-card">
            <div class="system-dot">✓</div>
            <div><strong>System Status</strong><span>All systems operational</span></div>
        </div>
        <div class="sidebar-meta"><span>Version {VERSION}</span><span class="edition-pill">Enterprise Edition</span></div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, icon: str = "") -> None:
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    icon_html = f'<span class="page-icon">{html.escape(icon)}</span>' if icon else ""
    st.markdown(
        f"""
        <div class="page-heading">
            <div>{icon_html}<h1>{safe_title}</h1><p>{safe_subtitle}</p></div>
            <span class="metbo-version">Enterprise Edition&nbsp;&nbsp;•&nbsp;&nbsp;Version {VERSION}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_header(case_id: str) -> None:
    now = datetime.now().strftime("%b %d, %Y • %I:%M %p")
    st.markdown(
        f"""
        <div class="utility-bar"><div class="utility-search">⌕&nbsp;&nbsp;Search investigations, IOCs, or cases</div><div class="utility-actions"><span>◉ Live</span><span>🔔</span><span class="analyst-avatar">CE</span><b>Charles Erdain</b></div></div>
        <div class="dashboard-topbar">
            <div><h1>Welcome back, Analyst</h1><p>Here’s your security operations overview.</p></div>
            <div class="case-chip"><span>Current Case</span><strong>{html.escape(case_id)}</strong></div>
        </div>
        <div class="last-sync">Last updated {now}</div>
        """,
        unsafe_allow_html=True,
    )


def status_card(label: str, value: str, detail: str, icon: str, accent: str = "blue") -> None:
    st.markdown(
        f"""
        <div class="status-card {accent}">
          <div class="status-copy"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong><small>{html.escape(detail)}</small></div>
          <div class="status-icon">{icon}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def action_card(title: str, text: str, icon: str, accent: str) -> None:
    st.markdown(
        f"""
        <div class="action-card {accent}">
          <div class="action-icon">{icon}</div>
          <strong>{html.escape(title)}</strong>
          <span>{html.escape(text)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label: str, value: int | str, icon: str, accent: str, detail: str = "") -> None:
    st.markdown(
        f"""
        <div class="stat-card {accent}">
          <div class="stat-icon">{icon}</div><div><strong>{html.escape(str(value))}</strong><span>{html.escape(label)}</span><small>{html.escape(detail)}</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, eyebrow: str | None = None) -> None:
    eyebrow_html = f"<span>{html.escape(eyebrow)}</span>" if eyebrow else ""
    st.markdown(f'<div class="section-title">{eyebrow_html}<h2>{html.escape(title)}</h2></div>', unsafe_allow_html=True)


def footer() -> None:
    st.markdown(
        f'<div class="metbo-footer"><span>Built with <b>♥</b> by Charles Erdain</span><span>METBO Shield Enterprise Edition v{VERSION}</span></div>',
        unsafe_allow_html=True,
    )
