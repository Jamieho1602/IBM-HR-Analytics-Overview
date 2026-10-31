
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="IBM HR Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("IBM HR Analytics")
st.subheader("Workforce Attrition & Strategic Talent Retention")

# Load and merge the five datasets
@st.cache_data
def load_data():
    employees = pd.read_csv("Employees.csv")
    compensation = pd.read_csv("Compensation.csv")
    performance = pd.read_csv("Performance.csv")
    experience = pd.read_csv("Experience.csv")
    employment_status = pd.read_csv("Employment Status.csv")

    hr_data = pd.merge(
        employees, compensation, on="EmployeeNumber",
        validate="one_to_one"
    )
    hr_data = pd.merge(
        hr_data, performance, on="EmployeeNumber",
        validate="one_to_one"
    )
    hr_data = pd.merge(
        hr_data, experience, on="EmployeeNumber",
        validate="one_to_one"
    )
    hr_data = pd.merge(
        hr_data, employment_status, on="EmployeeNumber",
        validate="one_to_one"
    )

    # Remove records with missing values, as done in Colab
hr_data = hr_data.dropna().copy()

hr_data["Attrition_Flag"] = (
    hr_data["Attrition"] == "Yes"
).astype(int)

return hr_data


df = load_data()

# Navigation
page = st.sidebar.radio(
    "Select a Page",
    [
        "Executive Overview",
        "General Attrition",
        "High-Performer Retention",
        "Attrition Risk Simulator"
    ]
)

# Executive Overview
if page == "Executive Overview":
    st.header("Executive Overview")

    total = len(df)
    left = int(df["Attrition_Flag"].sum())
    rate = df["Attrition_Flag"].mean() * 100

    high = df[df["PerformanceRating"] == 4]
    high_rate = high["Attrition_Flag"].mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", f"{total:,}")
    c2.metric("Employees Left", f"{left:,}")
    c3.metric("Overall Attrition", f"{rate:.2f}%")
    c4.metric(
        "High-Performer Attrition",
        f"{high_rate:.2f}%" if len(high) else "N/A"
    )

    st.subheader("Attrition by Department")
    dept = (
        df.groupby("Department")["Attrition_Flag"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )
    st.bar_chart(dept)

    st.info(
        "Management focus: Understand overall turnover "
        "and the potential loss of high-performing talent."
    )

# General Attrition
elif page == "General Attrition":
    st.header("General Employee Attrition")

    departments = sorted(df["Department"].dropna().unique())
    selected = st.selectbox(
        "Select Department",
        ["All Departments"] + departments
    )

    filtered = df if selected == "All Departments" else (
        df[df["Department"] == selected]
    )

    st.metric(
        "Attrition Rate",
        f"{filtered['Attrition_Flag'].mean() * 100:.2f}%"
    )

    st.subheader("Attrition by Overtime")
    overtime = (
        filtered.groupby("OverTime")["Attrition_Flag"]
        .mean()
        .mul(100)
    )
    st.bar_chart(overtime)

    st.subheader("Attrition by Job Satisfaction")
    satisfaction = (
        filtered.groupby("JobSatisfaction")["Attrition_Flag"]
        .mean()
        .mul(100)
    )
    st.bar_chart(satisfaction)

# High-Performer Retention
elif page == "High-Performer Retention":
    st.header("High-Performer Retention")

    high = df[df["PerformanceRating"] == 4].copy()

    st.metric("High-Performing Employees", len(high))

    if len(high):
        st.metric(
            "High-Performer Attrition Rate",
            f"{high['Attrition_Flag'].mean() * 100:.2f}%"
        )

        st.subheader("Attrition by Job Satisfaction")
        chart = (
            high.groupby("JobSatisfaction")["Attrition_Flag"]
            .mean()
            .mul(100)
        )
        st.bar_chart(chart)

        st.subheader("Attrition by Overtime")
        overtime = (
            high.groupby("OverTime")["Attrition_Flag"]
            .mean()
            .mul(100)
        )
        st.bar_chart(overtime)

        st.caption(
            "Historical attrition patterns among employees "
            "with Performance Rating 4. These are not "
            "individual flight-risk predictions."
        )
    else:
        st.warning("No employees with Performance Rating 4 found.")

# Prediction Simulator
elif page == "Attrition Risk Simulator":
    st.header("Attrition Risk Simulator")

    @st.cache_resource
    def load_model():
        return joblib.load("attrition_model (1).pkl")

    model = load_model()
    st.success("Model loaded successfully!")

    st.info(
        "The logistic regression model is loaded. "
        "We will add employee input fields after confirming "
        "the exact model features."
    )

