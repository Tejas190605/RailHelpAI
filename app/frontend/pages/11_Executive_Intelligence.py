import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from design.layout import setup_app_layout
from design.components import (
    render_page_header, render_metric_card, render_risk_index_card, render_empty_state
)
from utils_api import get_trends_data, get_recommendations_data, get_risk_index_data

setup_app_layout("Executive Intelligence")

render_page_header(
    title="Executive Multimodal & Prescriptive Intelligence Dashboard",
    subtitle="System-wide operational health, temporal trend detection, prescriptive recommendations, and risk index."
)

# 1. Operational Risk Index Header Widget
risk_data = get_risk_index_data()
risk_col1, risk_col2 = st.columns([1, 2])

with risk_col1:
    render_risk_index_card(
        score=risk_data.get("risk_index", 0.0),
        level=risk_data.get("risk_level", "LOW"),
        drivers=["Volume Surge", "Severity Ratio", "SLA Breaches", "Active Clusters"]
    )

with risk_col2:
    st.markdown("#### 💡 Prescriptive Operational Action Items")
    recs = get_recommendations_data()
    if recs:
        for rec in recs:
            with st.expander(f"📌 [{rec.get('severity')}] {rec.get('title')}", expanded=True):
                st.write(f"**Action Plan:** {rec.get('recommendation_text')}")
                st.info(f"**Supporting Evidence:** {rec.get('supporting_metrics')}")
                st.caption(f"**Algorithmic Rationale:** {rec.get('reasoning')} (Confidence: {round(rec.get('confidence', 0.85)*100, 1)}%)")
    else:
        render_empty_state("No Urgent Prescriptive Actions", "System metrics indicate stable operational status across all departments.")

st.markdown("---")

# 2. Temporal Category Trend Direction
st.markdown("### 📊 7-Day Temporal Trend Direction")
trends_data = get_trends_data()
cat_trends = trends_data.get("category_trends", [])

if cat_trends:
    df_t = pd.DataFrame(cat_trends)
    fig_t = px.bar(
        df_t,
        x="category",
        y="recent_7d_count",
        color="trend",
        title="7-Day Volume & Trend Direction",
        color_discrete_map={"INCREASING": "#D32F2F", "STABLE": "#1976D2", "DECREASING": "#388E3C"}
    )
    fig_t.update_layout(height=280)
    st.plotly_chart(fig_t, use_container_width=True)
else:
    render_empty_state("No Trend Data Available", "Insufficient time-series data to calculate 7-day category trend directions.")
