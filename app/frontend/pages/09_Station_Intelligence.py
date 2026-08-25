import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from design.layout import setup_app_layout
from design.components import render_page_header, render_metric_card, render_empty_state
from utils_api import get_station_profile_data

setup_app_layout("Station Intelligence")

render_page_header(
    title="Station Analytical Profile",
    subtitle="Operational profile, category breakdown, and SLA compliance per station."
)

station_input = st.text_input("Enter Station Name:", value="Pune")

if station_input:
    data = get_station_profile_data(station_input.strip())
    
    st.markdown(f"### Station `{data.get('station_name')}` Profile")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Complaints", str(data.get("total_complaints", 0)))
    with c2:
        render_metric_card("Open Grievances", str(data.get("open_complaints", 0)))
    with c3:
        render_metric_card("Resolved", str(data.get("resolved_complaints", 0)))
    with c4:
        render_metric_card("SLA Compliance", f"{data.get('sla_compliance_rate', 100.0)}%")

    st.markdown("---")

    cats = data.get("top_categories", [])
    if cats:
        st.markdown("#### Top Station Complaint Categories")
        df_cats = pd.DataFrame(cats)
        fig = px.pie(df_cats, names="category", values="count", title="Category Breakdown", color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=280)
        st.plotly_chart(fig, use_container_width=True)
    else:
        render_empty_state("No Station Category Data", f"No records available for station '{station_input}'.")
