import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timezone

from design.layout import setup_app_layout
from design.components import (
    render_page_header, render_metric_card, render_risk_index_card,
    get_priority_badge_html, get_status_badge_html, get_sla_badge_html, render_empty_state
)
from utils_api import get_complaints, get_analytics_overview, get_clusters, get_risk_index_data

setup_app_layout("Command Center")

render_page_header(
    title="Operations Command Center",
    subtitle=f"Real-time operational dashboard • Last updated {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}"
)

# Fetch database-derived KPIs & Risk Index
kpis = get_analytics_overview()
risk_data = get_risk_index_data()

# KPI Strip
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    render_metric_card("Total Complaints", str(kpis.get("total_complaints", 0)), sublabel="System lifetime count")
with col2:
    render_metric_card("Open Grievances", str(kpis.get("open_complaints", 0)), delta=f"{kpis.get('open_complaints', 0)} active", sublabel="Requires action")
with col3:
    render_metric_card("Critical (P1)", str(kpis.get("critical_complaints", 0)), sublabel="Immediate safety/medical")
with col4:
    render_metric_card("SLA Breaches", str(kpis.get("sla_breaches", 0)), delta="Breached" if kpis.get("sla_breaches", 0) > 0 else "Clean", sublabel="Exceeded target")
with col5:
    render_metric_card("AI Automation", f"{kpis.get('ai_automation_rate', 100.0)}%", sublabel="Routed without human review")

st.markdown("<br>", unsafe_allow_html=True)

# Main Grid Row 1: Charts (Left ~65%) and Operational Risk (Right ~35%)
grid_col1, grid_col2 = st.columns([2, 1])

with grid_col1:
    st.markdown("### 📊 Grievance Category & Priority Distribution")
    data = get_complaints(params={"size": 200})
    items = data.get("items", [])
    df = pd.DataFrame(items)

    if not df.empty:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            cat_counts = df["complaint_type"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig_cat = px.bar(cat_counts, x="Category", y="Count", color="Category", title="Category Counts")
            fig_cat.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10), height=260)
            st.plotly_chart(fig_cat, use_container_width=True)

        with chart_col2:
            pri_counts = df["priority"].value_counts().reset_index()
            pri_counts.columns = ["Priority", "Count"]
            fig_pri = px.pie(pri_counts, names="Priority", values="Count", title="Priority Breakdown", color_discrete_sequence=["#D32F2F", "#E65100", "#F57C00", "#388E3C"])
            fig_pri.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=260)
            st.plotly_chart(fig_pri, use_container_width=True)
    else:
        render_empty_state("No Active Complaints", "The database currently contains no grievance records.")

with grid_col2:
    st.markdown("### ⚡ Operational Risk")
    render_risk_index_card(
        score=risk_data.get("risk_index", 0.0),
        level=risk_data.get("risk_level", "LOW"),
        drivers=["SLA Breach Rate", "Complaint Volume", "Active Clusters"]
    )
    st.info(f"⏱️ **SLA Compliance:** `{kpis.get('sla_compliance_rate', 100.0)}%` of resolved complaints met target.")

st.markdown("---")

# Main Grid Row 2: Active Incidents & Operational Attention Items
st.markdown("### 🚨 Active Incidents & High Priority Attention Items")
clusters = get_clusters()

if clusters:
    df_clusters = pd.DataFrame(clusters)
    st.dataframe(df_clusters[["cluster_id", "cluster_label", "complaint_count", "status"]], use_container_width=True)
else:
    render_empty_state("No Active Incidents Detected", "No recurring DBSCAN complaint clusters require immediate escalation.")
