import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mental Health Analytics", layout="wide")

# ----------------------------
# Structured Dataset (Matches Output)
# ----------------------------

data = pd.DataFrame({
    "Age": [22,25,28,30,32,35,38,40,42,45],
    "Gender": ["Female","Male","Female","Male","Female",
               "Male","Female","Male","Female","Male"],
    "StressLevel": [3,4,5,6,7,8,9,6,5,7],
    "SleepHours": [8,7,6,6,5,4,5,7,8,6],
    "AnxietyLevel": [4,5,6,7,8,9,7,6,5,8]
})

# Productivity (Strong Negative with Stress)
data["Productivity"] = 12 - data["StressLevel"]

# Mental Health Score (Based on Sleep + Low Stress + Low Anxiety)
data["MentalHealthScore"] = (
    data["SleepHours"] * 10
    - data["StressLevel"] * 4
    - data["AnxietyLevel"] * 3
)

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Options")

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=data["Gender"].unique(),
    default=data["Gender"].unique()
)

age_filter = st.sidebar.slider(
    "Age Range",
    int(data["Age"].min()),
    int(data["Age"].max()),
    (22, 45)
)

filtered_data = data[
    (data["Gender"].isin(gender_filter)) &
    (data["Age"].between(age_filter[0], age_filter[1]))
]

# ----------------------------
# Title
# ----------------------------
st.title("Mental Health Analytics Dashboard")
st.write("Colorful & Interactive EDA using Streamlit")

# ----------------------------
# Key Indicators (Like Figure 6.1)
# ----------------------------
st.subheader("Key Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Stress", round(filtered_data["StressLevel"].mean(),1))
col2.metric("Avg Sleep (hrs)", round(filtered_data["SleepHours"].mean(),1))
col3.metric("Avg Anxiety", round(filtered_data["AnxietyLevel"].mean(),1))
col4.metric("Mental Score", round(filtered_data["MentalHealthScore"].mean(),1))

# ----------------------------
# Stress vs Productivity (Figure 6.2)
# ----------------------------
st.subheader("Stress vs Productivity")

fig1, ax1 = plt.subplots()
sns.lineplot(data=filtered_data,
             x="StressLevel",
             y="Productivity",
             marker="o",
             ax=ax1)
st.pyplot(fig1)

# ----------------------------
# Sleep vs Mental Health
# ----------------------------
st.subheader("Sleep vs Mental Health")

fig2, ax2 = plt.subplots()
sns.scatterplot(
    data=filtered_data,
    x="SleepHours",
    y="MentalHealthScore",
    hue="Gender",
    s=100,
    ax=ax2
)
st.pyplot(fig2)

# ----------------------------
# Mental Health Distribution (Figure 6.3)
# ----------------------------
st.subheader("Mental Health Score Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(filtered_data["MentalHealthScore"],
             kde=True,
             bins=6,
             ax=ax3)
st.pyplot(fig3)

# ----------------------------
# Gender-wise Mental Health (Boxplot)
# ----------------------------
st.subheader("Gender-wise Mental Health")

fig4, ax4 = plt.subplots()
sns.boxplot(data=filtered_data,
            x="Gender",
            y="MentalHealthScore",
            ax=ax4)
st.pyplot(fig4)

# ----------------------------
# Correlation Heatmap (Figure 6.4)
# ----------------------------
st.subheader("Correlation Heatmap")

fig5, ax5 = plt.subplots()
sns.heatmap(filtered_data.corr(numeric_only=True),
            annot=True,
            cmap="coolwarm",
            ax=ax5)
st.pyplot(fig5)

st.success("Dashboard Generated Successfully!")
