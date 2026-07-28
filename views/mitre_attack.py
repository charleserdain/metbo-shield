import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.ui import apply_styles, page_header, footer, sidebar_brand, sidebar_status, section_title
from utils.session import init_state
from utils.mitre_mapper import map_mitre

apply_styles(); init_state(); sidebar_brand(); sidebar_status()
page_header("MITRE ATT&CK","Explore mapped phishing behaviours in an interactive ATT&CK view.","🎯")
analysis = st.session_state.analysis
if not analysis:
    st.info("Run an email investigation first.")
    footer(); st.stop()

mappings = map_mitre(analysis["findings"])
if not mappings:
    st.info("No MITRE ATT&CK techniques were mapped.")
    footer(); st.stop()

df = pd.DataFrame(mappings)
section_title("Technique Coverage", "Interactive Matrix")
# Build a compact matrix from whatever fields the mapper returns.
tech_col = next((c for c in df.columns if "technique" in c.lower()), df.columns[0])
id_col = next((c for c in df.columns if c.lower() in {"id","technique id","technique_id"} or "id" == c.lower()), None)
label = df[tech_col].astype(str)
if id_col:
    label = df[id_col].astype(str) + " · " + label
fig = go.Figure(go.Treemap(labels=label, parents=["Phishing"]*len(df), values=[1]*len(df), root_color="#0b1725", marker=dict(colorscale="Blues", line=dict(width=2, color="#07101c")), textfont=dict(color="white")))
fig.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
section_title("Mapped Evidence", "Technique Detail")
st.dataframe(df, use_container_width=True, hide_index=True)
footer()
