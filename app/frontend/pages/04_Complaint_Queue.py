import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from design.layout import setup_app_layout
from design.components import (
    render_page_header, get_priority_badge_html, get_status_badge_html, render_empty_state
)
from utils_api import get_complaints, update_status, assign_complaint

setup_app_layout("Complaint Queue")

render_page_header(
    title="Operator Complaint Triage Queue",
    subtitle="Centralized operational board for monitoring, filtering, and assigning active passenger grievances."
)

# Triage Filter Bar
f1, f2, f3, f4 = st.columns(4)
with f1:
    filter_status = st.selectbox("Status Filter", ["All", "New", "PENDING_REVIEW", "ASSIGNED", "IN_PROGRESS", "Resolved"])
with f2:
    filter_priority = st.selectbox("Priority Filter", ["All", "P1", "P2", "P3", "P4"])
with f3:
    filter_category = st.selectbox("Category Filter", ["All", "Air Conditioning", "Cleanliness", "Water Supply", "Electrical", "Catering", "Security", "Medical", "Other"])
with f4:
    search_term = st.text_input("Search Reference / Train / Station", placeholder="e.g. B4, RAI-1001, Pune")

params = {"size": 100}
if filter_status != "All":
    params["status"] = filter_status
if filter_priority != "All":
    params["priority"] = filter_priority
if filter_category != "All":
    params["category"] = filter_category
if search_term:
    params["search"] = search_term

data = get_complaints(params)
items = data.get("items", [])
df = pd.DataFrame(items)

if not df.empty:
    st.markdown(f"Displaying **{len(df)}** active complaint records:")
    
    # Scannable data table
    display_cols = ["complaint_id", "complaint_type", "priority", "department", "status", "train_number", "coach", "created_at"]
    st.dataframe(df[display_cols], use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚡ Quick Operational Actions")
    selected_ref = st.selectbox("Select Complaint Reference to Action:", df["complaint_id"].tolist())
    
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        new_status = st.selectbox("Update Lifecycle Status:", ["ASSIGNED", "IN_PROGRESS", "WAITING_FOR_INFORMATION", "Resolved"])
        if st.button("Apply Status Change"):
            res = update_status(selected_ref, new_status)
            if res.get("success"):
                st.success(f"Updated status of {selected_ref} to {new_status}")
                st.rerun()
            else:
                st.error(f"Error updating status: {res.get('error')}")

    with act_col2:
        new_dept = st.text_input("Reassign Department:", value="Electrical / Coach Maintenance")
        if st.button("Reassign Department"):
            res = assign_complaint(selected_ref, new_dept)
            if res.get("success"):
                st.success(f"Reassigned {selected_ref} to {new_dept}")
                st.rerun()
            else:
                st.error(f"Error reassigning department: {res.get('error')}")

else:
    render_empty_state("No Complaints Match Selected Filters", "Adjust your search terms or filter selection to view active grievance records.")
