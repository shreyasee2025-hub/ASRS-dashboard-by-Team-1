import streamlit as st
import plotly.express as px
import pandas as pd
from collections import Counter
from utils.loader import load

STOPWORDS = {
    'the','a','an','and','of','to','in','was','were','had','have','i',
    'we','my','our','at','on','for','with','that','this','it','from',
    'not','but','as','by','into','after','when','during','then','would',
    'could','did','been','is','are','be','or','also','while','about',
    'which','so','its','their','they','he','she','up','out','off','no',
    'us','has','one','two','aircraft','flight','also','just','said',
    'told','called','began','went','then','upon','back','over','there',
    'been','very','more','some','were','have','than','who','they','what',
    'will','me','if','do','re'
}

def top_words(series, n=15):
    words = ' '.join(series.dropna()).lower().split()
    clean = [w.strip('.,;:\'"()') for w in words
             if w.isalpha() and len(w) > 3 and w not in STOPWORDS]
    return pd.DataFrame(Counter(clean).most_common(n), columns=['Word', 'Count'])

st.title("What Do Pilots Actually Write?")
st.markdown("""
The previous pages showed numbers and patterns. This page goes one step further.
Pick a human factor below to see the words pilots actually used when describing that type of incident. Then read a few real reports to see what those numbers look like up close.
""")

df = load()
if df is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

hf_map = {
    'Fatigue': 'HF_Fatigue',
    'Distraction': 'HF_Distraction',
    'Workload': 'HF_Workload',
    'Situational Awareness': 'HF_Situational_Awareness',
    'Communication Breakdown': 'HF_Communication_Breakdown'
}

factor = st.selectbox("Pick a human factor", list(hf_map.keys()), key="hf_select")
narratives = df[df[hf_map[factor]] == 1]['Narrative'].dropna()

word_df = top_words(narratives)
fig = px.bar(
    word_df, x='Count', y='Word', orientation='h',
    color='Count', color_continuous_scale='Blues'
)
fig.update_layout(
    height=430, coloraxis_showscale=False,
    yaxis=dict(autorange='reversed'),
    title=f"Most common words pilots use when reporting {factor}"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Read actual reports")
st.caption("Names, dates, and locations removed by NASA before publishing.")

# Clear saved reports when the factor changes
if st.session_state.get("reports_factor") != factor:
    st.session_state.pop("saved_reports", None)
    st.session_state["reports_factor"] = factor

if st.button("Show 3 random reports"):
    st.session_state["saved_reports"] = narratives.sample(min(3, len(narratives))).tolist()

if "saved_reports" in st.session_state:
    for i, text in enumerate(st.session_state["saved_reports"], 1):
        st.markdown(f"**Report {i}**")
        st.info(text[:500] + "..." if len(str(text)) > 500 else text)

st.divider()

st.markdown("#### What we learned from 97,076 reports")

st.markdown("""
Remember the story we started with. A plane crashed in Kentucky on a clear morning
because the crew lined up on the wrong runway. No storm. No broken engine. Just a
human mistake on a day that looked perfectly safe.

That one story turned out to describe almost everything in this dataset.

Three things stood out across 19 years of reports:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Clear weather is not always safe.** More human mistakes happen on sunny days than stormy ones. Comfort creates complacency.")

with col2:
    st.info("**The routine moments are risky.** Cruise phase and afternoon hours have the most incidents. Not takeoff. Not bad weather.")

with col3:
    st.info("**Situational awareness is the biggest gap.** It is the number one human mistake across all years, all operators, all conditions.")

st.markdown("""
These are not just numbers. Behind each of these reports is a person who sat down
and honestly wrote about the moment something went wrong. They did it so others
could learn.

The sky being clear is not always a good sign.
""")
