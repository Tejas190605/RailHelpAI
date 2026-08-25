import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from design.layout import setup_app_layout
from design.components import (
    render_page_header, render_empty_state, get_priority_badge_html, get_status_badge_html
)
from utils_api import get_complaints, review_complaint

setup_app_layout("Human Review")

render_page_header(
    title="Human AI Review Console",
    subtitle="Review low & moderate confidence automated predictions before operational department routing."
)

data = get_complaints(params={"status": "PENDING_REVIEW", "size": 50})
items = data.get("items", [])
df = pd.DataFrame(items)

if not df.empty:
    st.warning(f"⚠️ **{len(df)}** complaints require human review before operational routing.")

    selected_id = st.selectbox("Select Complaint Reference to Review:", df["complaint_id"].tolist())
    complaint_data = df[df["complaint_id"] == selected_id].iloc[0].to_dict()

    st.markdown(f"### Complaint `{selected_id}`")
    st.info(f"**Grievance Description:** {complaint_data.get('complaint_text')}")

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Predicted Category:** `{complaint_data.get('complaint_type')}`")
    col2.markdown(f"**Predicted Priority:** {get_priority_badge_html(complaint_data.get('priority'))}", unsafe_allow_html=True)
    col3.markdown(f"**Suggested Department:** `{complaint_data.get('department')}`")

    st.markdown("---")

    with st.form("human_review_form"):
        st.markdown("#### Human Operator Review Controls")
        action = st.radio("Action:", ["Approve", "Override"])
        
        final_category = st.text_input("Override Category:", value=complaint_data.get('complaint_type'))
        final_priority = st.selectbox("Override Priority:", ["P1", "P2", "P3", "P4"], index=2)
        final_department = st.text_input("Override Department:", value=complaint_data.get('department'))
        reason = st.text_area("Reason for modification:", placeholder="e.g., Verified coach-wide issue, escalated priority.")

        submitted = st.form_submit_button("Submit Human Review", type="primary")

        if submitted:
            payload = {
                "reviewer": "Operator Supervisor",
                "action": action,
                "final_category": final_category if action == "Override" else None,
                "final_priority": final_priority if action == "Override" else None,
                "final_department": final_department if action == "Override" else None,
                "reason": reason
            }
            res = review_complaint(selected_id, payload)
            if res.get("success"):
                st.success(f"Review recorded for {selected_id}. Complaint assigned and routed.")
                st.rerun()
            else:
                st.error(f"Error submitting review: {res.get('error')}")

else:
    render_empty_state("No Pending AI Reviews", "All predictions have passed confidence thresholds and been automatically routed.")
