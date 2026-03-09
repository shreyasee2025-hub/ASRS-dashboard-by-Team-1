import streamlit as st
import importlib.util
import os

st.set_page_config(page_title="ASRS Incident Analysis", layout="wide")

pages = {
    "Home":             "_pages/0_Home.py",
    "Overview":         "_pages/1_Overview.py",
    "Where It Happens": "_pages/2_Where_It_Happens.py",
    "When & Who":       "_pages/3_When_And_Who.py",
    "Hidden Patterns":  "_pages/4_Hidden_Patterns.py",
    "What Pilots Say":  "_pages/5_What_Pilots_Say.py",
    "About the Data":   "_pages/6_About_Data.py",
}

with st.sidebar:
    st.markdown("## ASRS Dashboard")
    selection = st.radio("Navigate", list(pages.keys()), label_visibility="collapsed")

# Load and run the selected page dynamically
page_path = pages[selection]
spec = importlib.util.spec_from_file_location("page", page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
