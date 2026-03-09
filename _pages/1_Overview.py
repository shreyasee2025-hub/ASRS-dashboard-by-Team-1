import streamlit as st
import plotly.express as px
from utils.loader import load

st.title("What Causes Aviation Incidents?")

df = load()
if df is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

st.markdown(f"""
We analyzed {len(df):,} incident reports covering 2000 to 2018. Use the slider below to focus on a specific time period. The pie chart shows what was recorded as the starting cause of each incident.
""")

years = st.slider("Year range", int(df['Year'].min()), int(df['Year'].max()),
                  (int(df['Year'].min()), int(df['Year'].max())))
df = df[df['Year'].between(years[0], years[1])]

counts = df['Primary_Problem'].value_counts().reset_index()
counts.columns = ['Cause', 'Reports']

fig = px.pie(
    counts, names='Cause', values='Reports', hole=0.45,
    color_discrete_sequence=px.colors.sequential.Blues_r
)
fig.update_traces(textposition='outside', textinfo='percent+label')
fig.update_layout(height=500, showlegend=False,
                  title="What started the incident?")
st.plotly_chart(fig, use_container_width=True)

hf_pct = round(len(df[df['Primary_Problem'] == 'Human Factors']) / len(df) * 100)
st.info(f"{hf_pct}% of all incidents in this period were caused by a human mistake. It was not the aircraft and it was not the weather.")

st.markdown("Once we knew that human error was the main cause, the next question was obvious. Where exactly are these incidents happening? Is it certain states or a specific part of the flight?")
