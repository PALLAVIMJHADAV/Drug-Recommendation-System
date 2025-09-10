import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("drugs.csv")  # your CSV path

st.set_page_config(page_title="Interactive Drug Dashboard", layout="wide")
st.title("💊 Interactive Drug Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Medical condition filter
conditions = df['medical_condition'].dropna().unique()
selected_conditions = st.sidebar.multiselect("Select Medical Condition", conditions, default=conditions)

# Rating slider filter
min_rating, max_rating = int(df['rating'].min()), int(df['rating'].max())
selected_rating = st.sidebar.slider("Filter by Rating", min_rating, max_rating, (min_rating, max_rating))

# Drug name search
search_term = st.sidebar.text_input("Search Drug by Name").lower()

# Filter the dataframe
df_filtered = df[
    df['medical_condition'].isin(selected_conditions) &
    df['rating'].between(selected_rating[0], selected_rating[1])
]

if search_term:
    df_filtered = df_filtered[df_filtered['drug_name'].str.lower().str.contains(search_term)]

# Ensure numeric columns
df_filtered['rating'] = pd.to_numeric(df_filtered['rating'], errors='coerce').fillna(0)
df_filtered['no_of_reviews'] = pd.to_numeric(df_filtered['no_of_reviews'], errors='coerce').fillna(0)

# Histogram of Ratings
st.subheader("Rating Distribution")
fig_rating = px.histogram(
    df_filtered,
    x='rating',
    nbins=30,
    color='medical_condition',
    title="Distribution of Ratings",
    marginal="box",
    hover_data=['drug_name', 'no_of_reviews']
)
st.plotly_chart(fig_rating, use_container_width=True)

# Top Drugs by Rating
st.subheader("Top Drugs by Rating")
top_n = st.slider("Select Top N Drugs", 5, 50, 15)
top_drugs = df_filtered.nlargest(top_n, 'rating')
fig_top = px.bar(
    top_drugs,
    x='drug_name',
    y='rating',
    color='medical_condition',
    hover_data=['drug_name', 'rating', 'no_of_reviews'],
    title=f"Top {top_n} Drugs by Rating"
)
st.plotly_chart(fig_top, use_container_width=True)

# Popularity vs Rating Scatter
st.subheader("Drug Popularity vs Rating")
fig_scatter = px.scatter(
    df_filtered,
    x='no_of_reviews',
    y='rating',
    size='rating',
    color='medical_condition',
    hover_name='drug_name',
    hover_data=['drug_classes', 'generic_name', 'activity'],
    title="Popularity vs Rating (bubble size = rating)",
    size_max=40
)
st.plotly_chart(fig_scatter, use_container_width=True)




# Dataset Preview
st.markdown("### Dataset Preview")
st.dataframe(df_filtered.reset_index(drop=True))
