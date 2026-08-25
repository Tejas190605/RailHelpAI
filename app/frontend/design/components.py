import streamlit as st
from design.theme import PRIORITY_COLORS, STATUS_COLORS, SLA_COLORS


def render_page_header(title: str, subtitle: str, badge_status: str = "SYSTEM OPERATIONAL"):
    """Render consistent executive operational header banner."""
    html = f"""
    <div class="operational-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div style="text-align: right;">
                <span class="rail-badge" style="background-color: #111827; color: #10B981; border-color: #059669;">● {badge_status}</span>
                <div style="font-size: 0.7rem; color: #9CA3AF; margin-top: 0.2rem;">RAILHELPAI PROTOTYPE v1.0</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = None, sublabel: str = None):
    """Render structured operational KPI card."""
    delta_html = f'<div style="font-size: 0.75rem; color: #C8102E; margin-top: 0.25rem;">{delta}</div>' if delta else ''
    sublabel_html = f'<div class="rail-card-sublabel">{sublabel}</div>' if sublabel else ''
    
    html = f"""
    <div class="rail-card">
        <div class="rail-card-title">{label}</div>
        <div class="rail-card-value">{value}</div>
        {delta_html}
        {sublabel_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def get_priority_badge_html(priority: str) -> str:
    """Return priority badge HTML snippet."""
    cfg = PRIORITY_COLORS.get(priority, PRIORITY_COLORS["P3"])
    return f'<span class="rail-badge" style="background-color: {cfg["bg"]}; color: {cfg["text"]}; border-color: {cfg["border"]};">{cfg["label"]}</span>'


def get_status_badge_html(status_text: str) -> str:
    """Return status badge HTML snippet."""
    st_upper = status_text.upper().replace(" ", "_")
    cfg = STATUS_COLORS.get(st_upper, {"bg": "#F3F4F6", "text": "#374151", "border": "#D1D5DB"})
    return f'<span class="rail-badge" style="background-color: {cfg["bg"]}; color: {cfg["text"]}; border-color: {cfg["border"]};">{status_text}</span>'


def get_sla_badge_html(sla_status: str) -> str:
    """Return SLA status badge HTML snippet."""
    cfg = SLA_COLORS.get(sla_status, SLA_COLORS["WITHIN_SLA"])
    return f'<span class="rail-badge" style="background-color: {cfg["bg"]}; color: {cfg["text"]}; border-color: {cfg["border"]};">{cfg["label"]}</span>'


def render_risk_index_card(score: float, level: str, drivers: list = None):
    """Render Operational Risk Index summary widget."""
    level_color = "#D32F2F" if level in ["CRITICAL", "HIGH"] else "#F57C00" if level == "MEDIUM" else "#388E3C"
    drivers_list = "".join([f"<li>• {d}</li>" for d in (drivers or ["Complaint Volume", "SLA Breach Rate"])])
    
    html = f"""
    <div class="rail-card" style="border-left: 4px solid {level_color};">
        <div class="rail-card-title">RAILHELPAI OPERATIONAL RISK INDEX</div>
        <div style="display: flex; align-items: baseline; gap: 0.75rem;">
            <div class="rail-card-value" style="color: {level_color};">{score} <span style="font-size: 1rem; color: #6B7280;">/ 100</span></div>
            <span class="rail-badge" style="background-color: {level_color}20; color: {level_color}; border-color: {level_color}; font-size: 0.8rem;">{level}</span>
        </div>
        <div style="font-size: 0.75rem; color: #4B5563; margin-top: 0.5rem; font-weight: 600;">Key Contributing Drivers:</div>
        <ul style="font-size: 0.75rem; color: #6B7280; padding-left: 0.5rem; margin: 0.25rem 0 0 0; list-style: none;">
            {drivers_list}
        </ul>
        <div style="font-size: 0.65rem; color: #9CA3AF; margin-top: 0.5rem; font-style: italic;">* Prototype analytical score — not an official railway risk metric.</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_empty_state(title: str, message: str):
    """Render clean operational empty state."""
    html = f"""
    <div class="rail-card" style="text-align: center; padding: 2rem 1rem; color: #6B7280;">
        <div style="font-size: 1.1rem; font-weight: 600; color: #374151; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 0.85rem;">{message}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
