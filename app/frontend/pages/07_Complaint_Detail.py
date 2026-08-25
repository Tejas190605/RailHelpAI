import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from design.layout import setup_app_layout
from design.components import (
    render_page_header, get_priority_badge_html, get_status_badge_html, get_sla_badge_html, render_empty_state
)
from utils_api import get_complaint_detail, resolve_complaint

setup_app_layout("Complaint Detail")

render_page_header(
    title="Incident Investigation Console",
    subtitle="Deep complaint investigation, horizontal timeline, multimodal evidence, and resolution workstation."
)

search_ref = st.text_input("Enter Complaint Reference or DB ID:", placeholder="e.g. RAI-1001 or 1")

if search_ref:
    data = get_complaint_detail(search_ref.strip())
    if data:
        st.markdown(f"### Complaint `{data.get('complaint_id')}`")
        
        # Horizontal Incident Lifecycle Timeline
        curr_status = data.get("status", "NEW").upper()
        t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)
        
        t_col1.markdown(f"**1. CREATED**<br>{'✅' if curr_status in ['NEW', 'AI_ANALYZED', 'PENDING_REVIEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'] else '⚪'}", unsafe_allow_html=True)
        t_col2.markdown(f"**2. AI ANALYZED**<br>{'✅' if curr_status in ['AI_ANALYZED', 'PENDING_REVIEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'] else '⚪'}", unsafe_allow_html=True)
        t_col3.markdown(f"**3. ASSIGNED**<br>{'✅' if curr_status in ['ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'] else '⚪'}", unsafe_allow_html=True)
        t_col4.markdown(f"**4. IN PROGRESS**<br>{'✅' if curr_status in ['IN_PROGRESS', 'RESOLVED', 'CLOSED'] else '⚪'}", unsafe_allow_html=True)
        t_col5.markdown(f"**5. RESOLVED**<br>{'✅' if curr_status in ['RESOLVED', 'CLOSED'] else '⚪'}", unsafe_allow_html=True)

        st.markdown("---")

        left_col, right_col = st.columns([3, 2])

        with left_col:
            st.markdown("#### 📄 Grievance & Context")
            st.info(f"**Text:** {data.get('complaint_text')}")

            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**Category:** `{data.get('complaint_type')}`")
            c2.markdown(f"**Priority:** {get_priority_badge_html(data.get('priority'))}", unsafe_allow_html=True)
            c3.markdown(f"**Status:** {get_status_badge_html(data.get('status'))}", unsafe_allow_html=True)

            c4, c5, c6 = st.columns(3)
            c4.markdown(f"**Train:** `{data.get('train_number') or 'N/A'}`")
            c5.markdown(f"**Coach:** `{data.get('coach') or 'N/A'}`")
            c6.markdown(f"**Seat:** `{data.get('seat') or 'N/A'}`")

        with right_col:
            st.markdown("#### 🛠️ Resolution Workstation")
            if data.get("status") not in ["Resolved", "Closed"]:
                with st.form("investigation_resolve_form"):
                    res_text = st.text_area("Resolution Action Notes *", placeholder="Describe operational repair / action taken...", height=100)
                    res_type = st.selectbox("Resolution Type:", ["FIXED", "INFORMATION_PROVIDED", "ESCALATED", "DUPLICATE", "INVALID", "NO_ACTION_REQUIRED", "OTHER"])

                    res_submitted = st.form_submit_button("Mark as RESOLVED", type="primary")

                    if res_submitted:
                        if not res_text or len(res_text.strip()) < 5:
                            st.error("Please provide valid resolution action notes (at least 5 characters).")
                        else:
                            res = resolve_complaint(data.get("complaint_id"), res_text.strip(), res_type)
                            if res.get("success"):
                                st.success(f"Complaint {data.get('complaint_id')} marked as RESOLVED!")
                                st.rerun()
                            else:
                                st.error(f"Error resolving complaint: {res.get('error')}")
            else:
                st.success("✅ This grievance has been RESOLVED!")
    else:
        render_empty_state("Complaint Not Found", f"No grievance record found matching reference '{search_ref}'.")
