import pandas as pd
import streamlit as st
from datetime import datetime

# Load data
df = pd.read_csv("student_activity.csv")

# Convert last_login to datetime
df["last_login"] = pd.to_datetime(df["last_login"])
days_inactive = (pd.Timestamp.today() - df["last_login"]).dt.days
df["days_inactive"] = days_inactive

# KPI calculations
df["engaged"] = df["completion_percentage"] >= 50
engagement_rate = round((df["engaged"].sum() / len(df)) * 100, 2)
drop_off_rate = round((df[df["completion_percentage"] < 30].shape[0] / len(df)) * 100, 2)

# Streamlit dashboard
st.title("Learning Outcomes Dashboard")
st.metric("Engagement Rate", f"{engagement_rate}%", delta="-4%")
st.metric("Drop-off Rate", f"{drop_off_rate}%", delta="+2%")

st.subheader("Completion % by Module")
st.bar_chart(df.groupby("module_id")["completion_percentage"].mean())

# AI Insight Section
st.subheader("AI Insight")
low_engaged = df[(df["completion_percentage"] < 30) & (df["days_inactive"] > 5)]
if not low_engaged.empty:
    for _, row in low_engaged.iterrows():
        st.write(f"Student {row['student_id']} is at risk. Last active {row['days_inactive']} days ago. Recommend: Assign Module {row['module_id']} Quiz.")
        st.button("Send Reminder", key=row["student_id"])
else:
    st.success("No students at risk right now.")