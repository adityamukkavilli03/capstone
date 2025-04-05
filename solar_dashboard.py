import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Solar Efficiency Dashboard", layout="wide")

# Title
st.title("🔆 Solar Energy Efficiency Dashboard")
st.markdown("Track efficiency, feature impact, and improvement suggestions using SHAP analysis.")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/merged_solar_data.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    return df

data = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filters")
start_date = st.sidebar.date_input("Start Date", value=data['Date'].min())
end_date = st.sidebar.date_input("End Date", value=data['Date'].max())

filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

# Efficiency Line Chart
st.subheader("📉 Efficiency Over Time")
fig = px.line(filtered_data, x='Date', y='Efficiency (%)', title='Efficiency (%) vs Date',
              labels={'Efficiency (%)': 'Efficiency (%)'}, markers=True)
st.plotly_chart(fig, use_container_width=True)

# SHAP Impactful Features Bar Chart
st.subheader("🔥 Most Impactful Features (SHAP)")

top_features = (
    filtered_data['Most Impactful Feature']
    .value_counts()
    .reset_index()
)

top_features.columns = ['Feature', 'Count']  # Rename columns explicitly

fig2 = px.bar(top_features, x='Feature', y='Count', title='Most Frequently Impactful Features')
st.plotly_chart(fig2, use_container_width=True)


# Show rows with low efficiency and recommendations
st.subheader("⚠️ Days with Low Efficiency (< 50%) and Recommendations")
low_eff_df = filtered_data[filtered_data['Efficiency (%)'] < 50]

if not low_eff_df.empty:
    st.dataframe(low_eff_df[['Date', 'Efficiency (%)', 'Most Impactful Feature', 'Recommendation']])
else:
    st.success("No days with efficiency < 50% in selected range.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for Capstone Project")
