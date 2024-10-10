import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import re


warnings.filterwarnings("ignore")


data = pd.read_csv(r"C:\\Users\\shubh\\Downloads\\ai_ml_jobs_linkedin.csv")


data['sector'] = data['sector'].fillna('NA')
data = data.dropna(subset=['publishedAt'])


def convert_sector(row):

    data['sector'] = data['sector'].apply(convert_sector)

data['applicationsCount'] = data['applicationsCount'].apply(lambda x: int(re.findall('(\d+) ', x)[0]))

def convert_title(row):

    data['title'] = data['title'].apply(convert_title)

st.sidebar.title("Dashboard Navigation")
selected_visualization = st.sidebar.selectbox(
    "Select a visualization",
    [
        "Top 10 Job Titles by Location Count",
        "Most Available Locations",
        "Latest Job Postings by Applications Count",
        "Distribution of Job Titles by Experience Level",
        "Heatmap of Job Counts by Sector",
        "Top 10 Hiring Companies",
        "Jobs with Most Applicants",
        "Choropleth Map of Popular States",
        "Distribution of Job Titles by Contract Type"
    ]
)


st.title("AI/ML Job Market Dashboard")


if selected_visualization == "Top 10 Job Titles by Location Count":
    top_10_requirements = data.groupby(['title'])['location'].count().reset_index().sort_values(['location'], ascending=False).head(10)
    fig = px.bar(top_10_requirements, x='title', y='location', title='Bar Graph of Location Counts for Top 10 Job Titles', template='plotly_dark')
    st.plotly_chart(fig)

elif selected_visualization == "Most Available Locations":
    most_available_locations = data.groupby(['location'])['title'].count().reset_index().sort_values(['title'], ascending=False).head(10)
    fig = px.bar(most_available_locations, x='location', y='title', title='Most Available Locations', template='plotly_dark')
    st.plotly_chart(fig)

elif selected_visualization == "Latest Job Postings by Applications Count":
    top_10_latest_postings = data[['title', 'publishedAt', 'applicationsCount']].dropna(subset=['publishedAt']).drop_duplicates().sort_values(['publishedAt'], ascending=False).head(10)
    data_radar = top_10_latest_postings.copy()
    data_radar['title'] = data_radar['title'].astype(str)
    fig = px.line_polar(data_radar, r='applicationsCount', theta='title', line_close=True, title='Radar Chart of Applications Count for Latest Job Postings', template='plotly_dark')
    st.plotly_chart(fig)

elif selected_visualization == "Distribution of Job Titles by Experience Level":
    level_based_count = data.groupby('experienceLevel')['title'].count().reset_index().sort_values(['title'])
    fig = px.pie(level_based_count, names='experienceLevel', values='title', title='Distribution of Job Titles by Experience Level', color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

elif selected_visualization == "Heatmap of Job Counts by Sector":
    sectorwise_jobs_top_10 = data.groupby(['sector'])['title'].count().reset_index().sort_values(['title'], ascending=False).head(10)
    fig = px.imshow(sectorwise_jobs_top_10[['title']].T, labels=dict(x='Sector', y='Job Count'), x=sectorwise_jobs_top_10['sector'], y=['Job Count'], color_continuous_scale=px.colors.sequential.Viridis, title='Heatmap of Job Counts by Sector')
    st.plotly_chart(fig)

elif selected_visualization == "Top 10 Hiring Companies":
    top_10_hiring_companies = data.groupby(['companyName'])['title'].count().reset_index().sort_values(['title'], ascending=False).head(10)
    fig = px.pie(top_10_hiring_companies, names='companyName', values='title', title='Donut Chart of Top 10 Hiring Companies', hole=0.4, color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

elif selected_visualization == "Jobs with Most Applicants":
    jobs_with_most_applicants = data.groupby(['title']).sum(['applicationsCount']).reset_index().sort_values(['applicationsCount'], ascending=False).head(10)
    fig = px.funnel(jobs_with_most_applicants, x='applicationsCount', y='title', title='Funnel Chart of Jobs with Most Applicants', color='applicationsCount', color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig)

elif selected_visualization == "Choropleth Map of Popular States":
    data['stateAt'] = data['location'].apply(get_states)
    popular_state_for_applicants = data.groupby(['stateAt']).sum(['applicationsCount']).reset_index().sort_values(['applicationsCount'], ascending=False)
    fig = px.choropleth(popular_state_for_applicants, locations='stateAt', locationmode='USA-states', color='applicationsCount', color_continuous_scale=px.colors.sequential.Plasma, title='Choropleth Map of Popular States for Applicants in the USA', labels={'applicationsCount': 'Number of Applications'}, scope='usa')
    st.plotly_chart(fig)

elif selected_visualization == "Distribution of Job Titles by Contract Type":
    count_per_contract_type = data.groupby(['contractType'])['title'].count().reset_index().sort_values(['title'], ascending=False)
    fig = px.pie(count_per_contract_type, names='contractType', values='title', title='Distribution of Job Titles by Contract Type', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig)


st.sidebar.header("About")
st.sidebar.text("This dashboard provides insights into the AI/ML job market based on LinkedIn job postings.")
