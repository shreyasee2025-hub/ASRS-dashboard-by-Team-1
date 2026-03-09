import streamlit as st
import plotly.express as px
from utils.loader import load

st.title("Where Do Incidents Happen?")

df = load()
if df is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

all_phases = df['Flight_Phase'].dropna().unique().tolist()
phases = st.multiselect("Filter by flight phase", all_phases)
if phases:
    df = df[df['Flight_Phase'].isin(phases)]

st.markdown("#### Incident count by US state")
st.markdown("States that have more flights will naturally have more reports. But there are some smaller states that have more incidents than you would expect based on how many flights they have.")

state_df = df[df['State'].str.len() == 2].groupby('State').size().reset_index(name='Reports')

fig1 = px.choropleth(
    state_df, locations='State', locationmode='USA-states',
    color='Reports', scope='usa', color_continuous_scale='Blues'
)
fig1.update_layout(height=430)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("#### Which part of the flight goes wrong most?")
st.markdown("Cruise has the most incidents by a clear margin. This is surprising because cruise is the calm, routine part of a flight. But that routine is exactly the problem. When nothing seems to be happening, attention drifts. Parked is second, which shows that incidents do not only happen in the air. Final approach and landing, which most people expect to be the most dangerous, are actually among the lowest here.")

phase_df = df['Flight_Phase'].value_counts().reset_index()
phase_df.columns = ['Phase', 'Reports']

fig2 = px.bar(
    phase_df, x='Reports', y='Phase', orientation='h',
    color='Reports', color_continuous_scale='Reds'
)
fig2.update_layout(height=420, coloraxis_showscale=False,
                   yaxis=dict(autorange='reversed'))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("Knowing where things go wrong was useful. But we also wanted to know when during the day these incidents happen and what kind of human mistake shows up the most.")
