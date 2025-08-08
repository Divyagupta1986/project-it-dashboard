import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Project & IT Incident Dashboard", layout="wide")
st.title("📊 Project Progress & IT Incident Tracking Dashboard")

# Mock project data
project_data = pd.DataFrame({
    "Project Name": [f"Project {i}" for i in range(1, 6)],
    "Owner": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Start Date": pd.date_range(start="2023-01-01", periods=5, freq="M"),
    "End Date": pd.date_range(start="2023-06-01", periods=5, freq="M"),
    "Status": ["Completed", "In Progress", "Not Started", "In Progress", "Completed"],
    "Completion %": [100, 60, 0, 45, 100]
})

# Mock incident data
incident_data = pd.DataFrame({
    "Incident ID": [f"INC{i:03d}" for i in range(1, 21)],
    "Type": np.random.choice(["Network", "Hardware", "Software"], size=20),
    "Severity": np.random.choice(["Low", "Medium", "High"], size=20),
    "Date Reported": pd.date_range(end=pd.Timestamp.today(), periods=20),
    "Resolution Time (hrs)": np.random.randint(1, 72, size=20),
    "Status": np.random.choice(["Open", "In Progress", "Resolved"], size=20),
    "Technician": np.random.choice(["Tom", "Jerry", "Anna", "Mike"], size=20),
    "Category": np.random.choice(["Server", "Laptop", "Application", "Network"], size=20)
})

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_status = st.sidebar.multiselect("Project Status", project_data["Status"].unique(), default=project_data["Status"].unique())
selected_category = st.sidebar.multiselect("Incident Category", incident_data["Category"].unique(), default=incident_data["Category"].unique())

filtered_projects = project_data[project_data["Status"].isin(selected_status)]
filtered_incidents = incident_data[incident_data["Category"].isin(selected_category)]

# Project Section
st.subheader("📁 Project Progress Overview")
col1, col2 = st.columns([2, 1])
with col1:
    st.dataframe(filtered_projects)
with col2:
    status_counts = filtered_projects["Status"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# Incident Section
st.subheader("🛠️ IT Incident Overview")
col3, col4 = st.columns([2, 1])
with col3:
    st.dataframe(filtered_incidents)
with col4:
    category_counts = filtered_incidents["Category"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(category_counts.index, category_counts.values, color='skyblue')
    ax2.set_title("Incidents by Category")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# Incident Trends
st.subheader("📈 Incident Trends Over Time")
incident_trend = filtered_incidents.groupby(filtered_incidents["Date Reported"].dt.to_period("M")).size()
incident_trend.index = incident_trend.index.to_timestamp()
fig3, ax3 = plt.subplots()
ax3.plot(incident_trend.index, incident_trend.values, marker='o')
ax3.set_title("Monthly Incident Trend")
ax3.set_xlabel("Month")
ax3.set_ylabel("Number of Incidents")
st.pyplot(fig3)

# KPI Cards
st.subheader("📌 Key Metrics")
col5, col6, col7 = st.columns(3)
col5.metric("Total Projects", len(filtered_projects))
col6.metric("Open Incidents", (filtered_incidents["Status"] == "Open").sum())
col7.metric("Avg Resolution Time (hrs)", round(filtered_incidents["Resolution Time (hrs)"].mean(), 2))
