import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import requests
from design.layout import setup_app_layout
from design.components import render_page_header, render_metric_card
from utils_api import BACKEND_API_URL

setup_app_layout("SLA Monitor")

render_page_header(
    title="Real-Time SLA Escalation Monitor",
    subtitle="Operational tracking of response & resolution SLA targets, warning thresholds, and SLA breaches."
)

try:
    sla_res = requests.get(f"{BACKEND_API_URL}/analytics/sla", timeout=5).json()
except Exception:
    sla_res = {"WITHIN_SLA": 0, "APPROACHING_SLA": 0, "ESCALATION_WARNING": 0, "BREACHED": 0}

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_metric_card("Within SLA", str(sla_res.get("WITHIN_SLA", 0)), sublabel="< 50% elapsed")
with c2:
    render_metric_card("Approaching SLA", str(sla_res.get("APPROACHING_SLA", 0)), sublabel=">= 50% elapsed")
with c3:
    render_metric_card("Escalation Warning", str(sla_res.get("ESCALATION_WARNING", 0)), delta="Escalated" if sla_res.get("ESCALATION_WARNING", 0) > 0 else None, sublabel=">= 90% elapsed")
with c4:
    render_metric_card("SLA Breached", str(sla_res.get("BREACHED", 0)), delta="BREACHED" if sla_res.get("BREACHED", 0) > 0 else "Clean", sublabel="Exceeded target")

st.markdown("---")

st.markdown("### 📋 Demonstration SLA Policy Targets")
policy_data = [
    {"Priority Level": "P1 - Critical", "Response Target": "10 minutes", "Resolution Target": "30 minutes", "Escalation Trigger": "Immediate RPF / Medical Emergency Dispatch"},
    {"Priority Level": "P2 - High", "Response Target": "30 minutes", "Resolution Target": "2 hours", "Escalation Trigger": "Depot Supervisor Warning at 90%"},
    {"Priority Level": "P3 - Medium", "Response Target": "2 hours", "Resolution Target": "8 hours", "Escalation Trigger": "Shift Manager Alert at 90%"},
    {"Priority Level": "P4 - Low", "Response Target": "8 hours", "Resolution Target": "24 hours", "Escalation Trigger": "Routine Queue Review"}
]
st.dataframe(pd.DataFrame(policy_data), use_container_width=True)

st.caption("⚠️ **Disclaimer:** These SLA values are prototype parameters for testing and do not represent official Indian Railways SLA commitments.")
