import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from design.layout import setup_app_layout
from design.components import render_page_header, render_metric_card, render_empty_state
from utils_api import get_train_profile_data

setup_app_layout("Train Intelligence")

render_page_header(
    title="Train Analytical Profile",
    subtitle="Operational health metrics, worst affected coaches, and SLA compliance per train."
)

train_input = st.text_input("Enter Train Number:", value="12951")

if train_input:
    data = get_train_profile_data(train_input.strip())
    
    st.markdown(f"### Train `{data.get('train_number')}` Profile")

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

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Top Category Distribution")
        cats = data.get("top_categories", [])
        if cats:
            df_cats = pd.DataFrame(cats)
            fig1 = px.bar(df_cats, x="category", y="count", color="category", title="Categories Distribution")
            fig1.update_layout(showlegend=False, height=260)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            render_empty_state("No Category Data", f"No category records for train {train_input}.")

    with col_b:
        st.markdown("#### Worst Affected Coaches")
        coaches = data.get("worst_coaches", [])
        if coaches:
            df_coaches = pd.DataFrame(coaches)
            fig2 = px.bar(df_coaches, x="coach", y="count", color="coach", title="Coaches Distribution")
            fig2.update_layout(showlegend=False, height=260)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            render_empty_state("No Coach Data", f"No coach breakdown available for train {train_input}.")
