import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from design.layout import setup_app_layout
from design.components import render_page_header, render_empty_state
from utils_api import get_clusters, rebuild_clusters

setup_app_layout("Incident Clusters")

render_page_header(
    title="Incident Intelligence Workstation",
    subtitle="Automated DBSCAN grouping of related complaint patterns into correlated operational incidents."
)

if st.button("🔄 Rebuild Incident Clusters", type="primary"):
    res = rebuild_clusters()
    if res.get("status") in ["SUCCESS", "INSUFFICIENT_DATA"]:
        st.success(f"Cluster rebuild complete! Found {res.get('total_clusters_found', 0)} incidents.")
        st.rerun()
    else:
        st.error(f"Error rebuilding clusters: {res.get('reason')}")

clusters = get_clusters()

if clusters:
    st.markdown(f"Displaying **{len(clusters)}** active incident clusters:")
    df_c = pd.DataFrame(clusters)
    st.dataframe(df_c[["cluster_id", "cluster_label", "complaint_count", "status"]], use_container_width=True)
else:
    render_empty_state("No Active Incident Clusters Detected", "Click 'Rebuild Incident Clusters' above to scan open complaints for correlated patterns.")
