
import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# 1. PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="IBM HR Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("IBM HR Analytics")
st.subheader(
    "Workforce Attrition & Strategic Talent Retention"
)


# --------------------------------------------------
# 2. LOAD AND CLEAN DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    employees = pd.read_csv("Employees.csv")
    compensation = pd.read_csv("Compensation.csv")
    performance = pd.read_csv("Performance.csv")
    experience = pd.read_csv("Experience.csv")
    employment_status = pd.read_csv(
        "Employment Status.csv"
    )

    hr_data = pd.merge(
        employees,
        compensation,
        on="EmployeeNumber",
        validate="one_to_one"
    )

    hr_data = pd.merge(
        hr_data,
        performance,
        on="EmployeeNumber",
        validate="one_to_one"
    )

    hr_data = pd.merge(
        hr_data,
        experience,
        on="EmployeeNumber",
        validate="one_to_one"
    )

    hr_data = pd.merge(
        hr_data,
        employment_status,
        on="EmployeeNumber",
        validate="one_to_one"
    )

    # Remove records with missing values
    hr_data = hr_data.dropna().copy()

    # Create attrition indicator
    hr_data["Attrition_Flag"] = (
        hr_data["Attrition"] == "Yes"
    ).astype(int)

    return hr_data


# Load final dataset
df = load_data()


# --------------------------------------------------
# 3. NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Select a Page",
    [
        "Executive Overview",
        "General Attrition",
        "High-Performer Retention",
        "Attrition Risk Simulator"
    ]
)


# --------------------------------------------------
# 4. EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    st.header("Executive Overview")

    total = len(df)
    left = int(df["Attrition_Flag"].sum())

    rate = (
        df["Attrition_Flag"].mean() * 100
        if total > 0 else 0
    )

    high = df[
        df["PerformanceRating"] == 4
    ].copy()

    high_rate = (
        high["Attrition_Flag"].mean() * 100
        if len(high) > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Employees",
        f"{total:,}"
    )

    c2.metric(
        "Employees Left",
        f"{left:,}"
    )

    c3.metric(
        "Overall Attrition",
        f"{rate:.2f}%"
    )

    c4.metric(
        "High-Performer Attrition",
        f"{high_rate:.2f}%"
        if len(high) > 0 else "N/A"
    )

    st.subheader("Attrition by Department")

    dept = (
        df.groupby("Department")["Attrition_Flag"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    st.bar_chart(
        dept,
        horizontal=True,
        x_label="Attrition Rate (%)",
        y_label="Department"
    )

    st.info(
        "Management focus: Understand overall "
        "employee attrition and the potential "
        "loss of high-performing talent."
    )


# --------------------------------------------------
# 5. GENERAL ATTRITION
# --------------------------------------------------

elif page == "General Attrition":

    st.header("General Employee Attrition")

    departments = sorted(
        df["Department"].dropna().unique()
    )

    selected = st.selectbox(
        "Select Department",
        ["All Departments"] + departments
    )

    if selected == "All Departments":
        filtered = df.copy()
    else:
        filtered = df[
            df["Department"] == selected
        ].copy()

    st.metric(
        "Total Employees",
        f"{len(filtered):,}"
    )

    attrition_rate = (
        filtered["Attrition_Flag"].mean() * 100
        if len(filtered) > 0 else 0
    )

    st.metric(
        "Attrition Rate",
        f"{attrition_rate:.2f}%"
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
        filtered.groupby("JobSatisfaction")[
            "Attrition_Flag"
        ]
        .mean()
        .mul(100)
    )

    st.bar_chart(satisfaction)

    st.caption(
        "Charts show historical attrition rates. "
        "They do not establish the causes of attrition."
    )


# --------------------------------------------------
# 6. HIGH-PERFORMER RETENTION
# --------------------------------------------------

elif page == "High-Performer Retention":

    st.header("High-Performer Retention")

    st.write(
        "This dashboard focuses on employees "
        "with Performance Rating 4."
    )

    high = df[
        df["PerformanceRating"] == 4
    ].copy()

    total_high = len(high)

    st.metric(
        "High-Performing Employees",
        f"{total_high:,}"
    )

    if total_high > 0:

        high_left = int(
            high["Attrition_Flag"].sum()
        )

        high_rate = (
            high["Attrition_Flag"].mean() * 100
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "High Performers Who Left",
            f"{high_left:,}"
        )

        c2.metric(
            "High-Performer Attrition Rate",
            f"{high_rate:.2f}%"
        )

        st.subheader(
            "High-Performer Attrition by Job Satisfaction"
        )

        satisfaction = (
            high.groupby("JobSatisfaction")[
                "Attrition_Flag"
            ]
            .mean()
            .mul(100)
        )

        st.bar_chart(satisfaction)

        st.subheader(
            "High-Performer Attrition by Overtime"
        )

        overtime = (
            high.groupby("OverTime")[
                "Attrition_Flag"
            ]
            .mean()
            .mul(100)
        )

        st.bar_chart(overtime)

        st.subheader(
            "High-Performer Attrition by Department"
        )

        department = (
            high.groupby("Department")[
                "Attrition_Flag"
            ]
            .mean()
            .mul(100)
            .sort_values(ascending=False)
        )

        st.bar_chart(
            department,
            horizontal=True,
            x_label="Attrition Rate (%)",
            y_label="Department"
        )

        st.info(
            "Management should investigate "
            "retention concerns among high performers, "
            "particularly job satisfaction, "
            "overtime and career progression."
        )

        st.caption(
            "These are historical group-level patterns, "
            "not predictions of which individual "
            "high performers will resign."
        )

    else:

        st.warning(
            "No employees with Performance Rating 4 found."
        )


# --------------------------------------------------
# 7. ATTRITION RISK SIMULATOR
# --------------------------------------------------

elif page == "Attrition Risk Simulator":

    st.header("Attrition Risk Simulator")

    st.write(
        "Experimental logistic regression demonstration."
    )

    @st.cache_resource
    def load_model():

        return joblib.load(
            "attrition_model (1).pkl"
        )

    try:

        model = load_model()

        st.success(
            "Model loaded successfully!"
        )

        st.info(
            "The trained model is ready. "
            "Employee input fields and prediction "
            "results will be added after we confirm "
            "the model's exact input features."
        )

    except Exception as error:

        st.error(
            "The prediction model could not be loaded."
        )

        st.exception(error)
