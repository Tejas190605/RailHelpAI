import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from design.layout import setup_app_layout
from design.components import render_page_header, get_priority_badge_html, get_status_badge_html
from utils_api import analyze_text, detect_duplicates

setup_app_layout("AI Analysis")

render_page_header(
    title="AI Incident Assessment Engine",
    subtitle="Stateless deep complaint intelligence, entity extraction, priority scoring, and duplicate detection."
)

input_col, report_col = st.columns([1, 1])

with input_col:
    st.markdown("### 📥 Input Complaint Text")
    sample_preset = st.selectbox(
        "Load Sample Scenario:",
        [
            "Custom Text Input",
            "Medical emergency in coach A1 seat 14. Passenger having chest pain.",
            "AC is not cooling in coach B4 seat 21 and we have been waiting for 30 minutes since Pune on train 12951.",
            "Toilet washbasin is clogged and dirty in coach S3 seat 45."
        ]
    )

    if sample_preset != "Custom Text Input":
        text_input = st.text_area("Complaint Text:", value=sample_preset, height=140)
    else:
        text_input = st.text_area("Complaint Text:", value="AC is not working in coach B4 seat 21.", height=140)

    c1, c2 = st.columns(2)
    with c1:
        train_no = st.text_input("Train No (Optional)", value="12951")
    with c2:
        station_name = st.text_input("Station (Optional)", value="Pune")

    run_ai = st.button("🤖 Run Full AI Assessment", type="primary")

with report_col:
    st.markdown("### 📊 Visual Intelligence Assessment Report")
    if run_ai or sample_preset != "Custom Text Input":
        metadata = {"train_number": train_no, "station": station_name}
        res = analyze_text(text_input, metadata)
        
        if res.get("success"):
            data = res.get("data", {})
            cat = data.get("category", {})
            pri = data.get("priority", {})
            dept = data.get("department", {})
            sent = data.get("sentiment", {})
            entities = data.get("entities", {})

            # Executive Summary Cards
            m1, m2, m3 = st.columns(3)
            m1.markdown(f"**Predicted Category:**<br>`{cat.get('value')}` ({round(cat.get('confidence', 0)*100, 1)}%)", unsafe_allow_html=True)
            m2.markdown(f"**Evaluated Priority:**<br>{get_priority_badge_html(pri.get('level'))}", unsafe_allow_html=True)
            m3.markdown(f"**Routed Department:**<br>`{dept.get('name')}`", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🧠 Algorithmic Rationale & Extracted Evidence")
            reasons = pri.get("reasons", [])
            for r in reasons:
                st.write(f"• {r}")

            st.markdown("---")
            st.markdown("#### 📌 Extracted Entities")
            st.json(entities)
        else:
            st.error(f"Error running AI analysis: {res.get('error')}")
    else:
        st.info("Click **Run Full AI Assessment** to generate an intelligence evaluation report.")
