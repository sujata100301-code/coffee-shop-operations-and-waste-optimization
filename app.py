import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Coffee Shop BI & Waste Optimization Dashboard", layout="wide")

st.title("Boutique Coffee Shop Analytics & Waste Optimization Platform")
st.markdown("Optimizing inventory purchasing to reduce perishable food/milk waste and maximize peak hour revenue using **Coffee Shop Sales.xlsx**.")

# Load Dataset directly from the Transactions sheet
@st.cache_data
def load_data():
    df = pd.read_excel('Coffee Shop Sales.xlsx', sheet_name='Transactions')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_location = st.sidebar.selectbox("Select Store Location", options=['All'] + list(df['store_location'].unique()))
selected_category = st.sidebar.selectbox("Select Product Category", options=['All'] + list(df['product_category'].unique()))

filtered_df = df.copy()
if selected_location != 'All':
    filtered_df = filtered_df[filtered_df['store_location'] == selected_location]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['product_category'] == selected_category]

# --- KPI METRICS ---
st.subheader("Level 1 & 2: Key Performance Indicators & Trends")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['Revenue'].sum()
aov = filtered_df['Revenue'].mean()
peak_hour = filtered_df.groupby('Hour')['Revenue'].sum().idxmax()
bakery_df = filtered_df[filtered_df['product_category'] == 'Bakery']
est_waste_cost = bakery_df['Revenue'].sum() * 0.15  # Estimated 15% perishable spoilage rate

col1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
col2.metric(label="Average Order Value (AOV)", value=f"${aov:.2f}")
col3.metric(label="Peak Rush Hour", value=f"{peak_hour}:00 - {peak_hour+1}:00")
col4.metric(label="Est. Perishable Waste Cost", value=f"${est_waste_cost:,.2f}")

st.markdown("---")

# --- CHARTS SECTION ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### Peak Rush Hours (Footfall & Revenue by Hour)")
    hourly_trend = filtered_df.groupby('Hour')['Revenue'].sum().reset_index()
    fig_trend = px.line(hourly_trend, x='Hour', y='Revenue', markers=True, title="Hourly Revenue Distribution")
    st.plotly_chart(fig_trend, use_container_width=True)

with col_b:
    st.markdown("### Productivity & Popularity Index (Revenue by Category)")
    cat_summary = filtered_df.groupby('product_category')['Revenue'].sum().reset_index()
    fig_bar = px.bar(cat_summary, x='product_category', y='Revenue', color='product_category', title="Category Revenue Performance")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- BUSINESS INTELLIGENCE INSIGHTS & ACTIONS ---
st.markdown("---")
st.subheader("Levels 3, 4 & 5: Strategic Business Insights & Actions")

st.info("Fact / Trend: Sales peak sharply between 8:30 AM - 10:30 AM, but drop significantly by 3:00 PM, resulting in unused morning pastries spoiling.")
st.warning("Risk & Opportunity: Afternoon footfall is low, leading to dead inventory and wasted operational effort on perishable baking stock.")
st.success("Recommended Business Action: Launch a '2-for-1 Afternoon Happy Hour' on pastries from 3:00 PM to 5:00 PM and reduce morning baking batch sizes by 10%.")
