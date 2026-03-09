import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load

st.title("When Do Incidents Happen?")

df_all = load()
if df_all is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

df = df_all.copy()
operator = st.selectbox("Operator type", ["All", "Air Carrier", "Personal", "Corporate", "Air Taxi"])
if operator != "All":
    df = df[df['Operator'] == operator]

st.markdown("#### Time of day vs how many incidents")
st.markdown("Afternoon has the most incidents by a clear margin. This makes sense because that is when the most flights are in the air. More flights means more chances for something to go wrong. Late night has the fewest incidents simply because very few flights operate at that hour.")

time_order = ['Late Night', 'Morning', 'Afternoon', 'Evening']
time_counts = df['Time_Of_Day'].value_counts().reindex(time_order).reset_index()
time_counts.columns = ['Time Of Day', 'Reports']

fig1 = px.bar(
    time_counts, x='Time Of Day', y='Reports',
    color='Reports', color_continuous_scale='Blues',
    category_orders={'Time Of Day': time_order}
)
fig1.update_layout(height=350, coloraxis_showscale=False)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("#### Which human mistake comes up most?")
st.markdown("""
Situational awareness is the most reported human mistake by far. It means the pilot lost track of where they were or what was going on around them.
Communication breakdown is second. It means someone said something on the radio and the other person understood it differently.
Fatigue is the least reported, but that does not mean it is rare. Pilots may simply be less likely to admit they were tired when filing a report.
""")

hf_cols = {
    'Situational Awareness': 'HF_Situational_Awareness',
    'Communication Breakdown': 'HF_Communication_Breakdown',
    'Distraction': 'HF_Distraction',
    'Workload': 'HF_Workload',
    'Fatigue': 'HF_Fatigue'
}

hf_df = pd.DataFrame({
    'Factor': list(hf_cols.keys()),
    'Reports': [df[c].sum() for c in hf_cols.values()]
}).sort_values('Reports')

fig2 = px.bar(
    hf_df, x='Reports', y='Factor', orientation='h',
    color='Reports', color_continuous_scale='Blues'
)
fig2.update_layout(height=350, coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### Does operator type change which human mistake comes up most?")
st.markdown("We wanted to know if airline pilots, private pilots, and corporate pilots all make the same kinds of mistakes. The chart below shows the rate of each human factor as a percentage of total incidents for that operator type. This makes it a fair comparison since Air Carriers have far more flights overall.")

top_operators = df_all['Operator'].dropna().value_counts().head(4).index.tolist()
op_rows = []
for op in top_operators:
    sub = df_all[df_all['Operator'] == op]
    total = len(sub)
    if total == 0:
        continue
    for label, col in hf_cols.items():
        op_rows.append({
            'Operator': op,
            'Factor': label,
            'Rate (%)': round(sub[col].sum() / total * 100, 1)
        })

op_df = pd.DataFrame(op_rows)
fig3 = px.bar(
    op_df, x='Factor', y='Rate (%)', color='Operator', barmode='group',
    color_discrete_sequence=['#08306b', '#1a6faf', '#4a9fd4', '#a8c8e8']
)
fig3.update_layout(height=400)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("At this point we had a decent picture of what, where, and when. But then we noticed something in the data that we honestly did not expect. We looked into it more and it became the most interesting part of the whole analysis.")
