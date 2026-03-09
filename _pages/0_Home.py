import streamlit as st
from utils.loader import load

df = load()

st.markdown("""
<style>
.hero-text {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.sub-text {
    font-size: 1.15rem;
    opacity: 0.75;
    margin-bottom: 2rem;
    line-height: 1.7;
}
.hook-box {
    border-left: 4px solid #1a6faf;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0;
    font-size: 1.05rem;
    line-height: 1.8;
    opacity: 0.9;
}
.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1a6faf;
}
.stat-label {
    font-size: 0.85rem;
    opacity: 0.65;
    margin-top: -8px;
}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown('<p class="hero-text">Why Do Planes Have<br>Incidents?</p>',
            unsafe_allow_html=True)

st.markdown("""
<p class="sub-text">
Every year, thousands of pilots and air traffic controllers write down exactly
what went wrong. We read nearly 100,000 of those reports to find out.
The answer was not what we expected.
</p>
""", unsafe_allow_html=True)

# Hook story
st.markdown("""
<div class="hook-box">
On August 27, 2006, a plane crashed on takeoff in Lexington, Kentucky.
49 of the 50 people on board did not survive. The weather was clear.
The aircraft had no mechanical problems. The crew simply lined up on
the wrong runway. A human mistake on a perfect morning.
</div>
""", unsafe_allow_html=True)

# Key stats
if df is not None:
    total_reports = f"{len(df):,}"
    year_range    = f"{int(df['Year'].min())} to {int(df['Year'].max())}"
    total_years   = str(df['Year'].nunique())
else:
    total_reports = "97,076"
    year_range    = "2000 to 2018"
    total_years   = "19"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<p class="stat-number">{total_reports}</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Real incident reports</p>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<p class="stat-number">{total_years}</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Years of data</p>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<p class="stat-number">{year_range}</p>', unsafe_allow_html=True)
    st.markdown('<p class="stat-label">Time period covered</p>', unsafe_allow_html=True)

st.divider()

# Central question
st.markdown("#### The question we started with")
st.markdown("""
Most people assume aviation incidents happen because something breaks. A bad engine,
a storm, a technical failure. We assumed the same thing.

We were wrong.

Use the pages in the sidebar to follow the story from the beginning.
Each page answers one question and leads to the next.
""")

# Page guide
st.markdown("#### What is in each page")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Overview:** What actually causes incidents?")
    st.markdown("**Where It Happens:** Which states and flight phases?")
    st.markdown("**When and Who:** Time of day and human mistakes")

with col_b:
    st.markdown("**Hidden Patterns:** The finding that surprised us")
    st.markdown("**What Pilots Say:** Real words from real reports")
    st.markdown("**About the Data:** Source, method, and how to refresh")

st.caption("Use the sidebar on the left to navigate through the story.")
