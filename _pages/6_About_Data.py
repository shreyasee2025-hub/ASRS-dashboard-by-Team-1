import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import load

st.title("About the Data")

df = load()
if df is None:
    st.error("Could not load data. Please run clean_data.py first.")
    st.stop()

st.markdown(f"""
**Source:** NASA Aviation Safety Reporting System (ASRS)
**URL:** https://asrs.arc.nasa.gov/search/database.html
**Date Accessed:** March 2026
**License:** Public domain, NASA curated
**Dataset size:** {len(df):,} incident reports across {df['Year'].nunique()} years

**What is ASRS?**
Pilots, air traffic controllers, and ground crew voluntarily report incidents to NASA.
No one gets punished for reporting. NASA removes all names and identifying details
before releasing the data. It's one of the most honest safety databases in any industry.

**Key columns used**
Date (year and month), time of day, US state, flight conditions, light level,
flight phase, aircraft operator type, aircraft model, human factors involved,
anomaly type, primary problem, and the full narrative written by the reporter.

**What we did to clean it**
Read the raw ASRS data files, kept 15 relevant columns out of 96,
dropped rows with no flight phase or primary problem recorded, mapped time ranges
to readable labels, and created one binary flag per human factor type from the
the semicolon separated values in the original field.

**How to refresh this dashboard**
Go to the ASRS search page, download the data for the new date range, convert it to parquet format and place the files in the data/raw/ folder, then run clean_data.py again. The dashboard will update automatically.
""")

st.markdown("---")

st.markdown("#### Missing values check")
st.markdown("Before we used the data we checked how many values were missing in each column. Columns with high missingness would have needed special handling.")

missing = df.isnull().sum().reset_index()
missing.columns = ['Column', 'Missing Values']
missing = missing.sort_values('Missing Values', ascending=False)

fig_missing = px.bar(
    missing, x='Column', y='Missing Values',
    color='Missing Values', color_continuous_scale='Reds'
)
fig_missing.update_layout(
    height=380, coloraxis_showscale=False,
    xaxis_tickangle=-45,
    title="Missing values per column in the cleaned dataset"
)
st.plotly_chart(fig_missing, use_container_width=True)

cols_with_missing = missing[missing['Missing Values'] > 0]
if len(cols_with_missing) > 0:
    st.caption(f"{len(cols_with_missing)} column(s) still have missing values after cleaning. These are mostly free-text fields like Narrative and Synopsis where pilots sometimes left them blank.")
else:
    st.caption("No missing values remain after cleaning.")

st.markdown("---")

st.markdown("#### How reports are distributed over time")
st.markdown("This helps us understand whether certain years are over or under represented in the data. A big drop or jump in a year could affect how we interpret trends.")

year_counts = df.groupby('Year').size().reset_index(name='Reports')
fig_year = px.bar(
    year_counts, x='Year', y='Reports',
    color='Reports', color_continuous_scale='Blues'
)
fig_year.update_layout(height=350, coloraxis_showscale=False,
                       title="Number of reports per year (2000 to 2018)")
st.plotly_chart(fig_year, use_container_width=True)

st.markdown("#### Are incidents reported evenly across months?")
st.markdown("If certain months have far more reports than others it could point to seasonal patterns in aviation activity or reporting behavior.")

month_labels = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
month_counts = df.groupby('Month').size().reset_index(name='Reports')
month_counts['Month Name'] = month_counts['Month'].map(month_labels)

fig_month = px.bar(
    month_counts, x='Month Name', y='Reports',
    color='Reports', color_continuous_scale='Blues',
    category_orders={'Month Name': list(month_labels.values())}
)
fig_month.update_layout(height=350, coloraxis_showscale=False,
                        title="Number of reports per month")
st.plotly_chart(fig_month, use_container_width=True)
