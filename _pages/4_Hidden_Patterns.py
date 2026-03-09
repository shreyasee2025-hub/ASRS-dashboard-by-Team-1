import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load

st.title("Surprising Patterns")

df = load()
if df is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

st.markdown("#### Clear weather causes more human mistakes than bad weather")
st.markdown("""
This was one of the more surprising things we found in the data.

**VMC (Visual Meteorological Conditions)** means clear and sunny skies where you can see everything outside.
**IMC (Instrument Meteorological Conditions)** means there are clouds, fog, or rain and it is hard to see.

When the sky is clear, pilots sometimes get too comfortable and do not pay as much attention.
When the weather is bad, they are much more careful because they know the risk.
So more mistakes actually happen on clear days than on stormy ones.
""")

hf_map = {
    'Fatigue': 'HF_Fatigue',
    'Distraction': 'HF_Distraction',
    'Workload': 'HF_Workload',
    'Situational Awareness': 'HF_Situational_Awareness'
}

rows = []
for cond in ['VMC', 'IMC']:
    sub = df[df['Flight_Conditions'] == cond]
    for label, col in hf_map.items():
        rows.append({'Condition': cond, 'Factor': label, 'Reports': sub[col].sum()})

vmc_df = pd.DataFrame(rows)
fig1 = px.bar(
    vmc_df, x='Factor', y='Reports', color='Condition', barmode='group',
    color_discrete_map={'VMC': '#1a6faf', 'IMC': '#a8c8e8'}
)
fig1.update_layout(height=380)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("#### Yearly trend by human factor")
st.markdown("This chart shows how reporting of each human mistake changed over time. You will notice all lines are flat near zero before 2009. This is because the ASRS database only started coding these specific human factor fields consistently around that time. The data from 2009 onwards is what tells the real story.")

selected = st.multiselect("Pick factors to compare",
    list(hf_map.keys()), default=['Fatigue', 'Distraction'])

trend_rows = []
for label in selected:
    col = hf_map[label]
    yearly = df.groupby('Year')[col].sum().reset_index()
    yearly.columns = ['Year', 'Reports']
    yearly['Factor'] = label
    trend_rows.append(yearly)

if trend_rows:
    trend_df = pd.concat(trend_rows)
    fig2 = px.line(trend_df, x='Year', y='Reports', color='Factor', markers=True)
    fig2.update_layout(height=370)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("The numbers told us a lot. But we wanted to go one step further and read what pilots actually wrote in their own words when they filed these reports.")
