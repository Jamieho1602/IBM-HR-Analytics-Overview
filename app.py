import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="IBM HR Analytics", page_icon="📊", layout="wide")
st.title("IBM HR Analytics")
st.subheader("Workforce Attrition & Strategic Talent Retention")

@st.cache_data
def load_data():
    employees = pd.read_csv("Employees.csv")
    compensation = pd.read_csv("Compensation.csv")
    performance = pd.read_csv("Performance.csv")
    experience = pd.read_csv("Experience.csv")
    employment_status = pd.read_csv("Employment Status.csv")

    hr_data = pd.merge(employees, compensation, on="EmployeeNumber", validate="one_to_one")
    hr_data = pd.merge(hr_data, performance, on="EmployeeNumber", validate="one_to_one")
    hr_data = pd.merge(hr_data, experience, on="EmployeeNumber", validate="one_to_one")
    hr_data = pd.merge(hr_data, employment_status, on="EmployeeNumber", validate="one_to_one")
    hr_data = hr_data.dropna().copy()
    hr_data["Attrition_Flag"] = (hr_data["Attrition"] == "Yes").astype(int)
    return hr_data

@st.cache_resource
def load_model():
    return joblib.load("attrition_model (1).pkl")

df = load_data()
page = st.sidebar.radio("Select a Page", [
    "Executive Overview", "General Attrition", "High-Performer Retention", "Attrition Risk Simulator"
])

if page == "Executive Overview":
    st.header("Executive Overview")
    total = len(df)
    left = int(df["Attrition_Flag"].sum())
    high = df[df["PerformanceRating"] == 4]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", f"{total:,}")
    c2.metric("Employees Left", f"{left:,}")
    c3.metric("Overall Attrition", f"{100 * left / total:.2f}%" if total else "N/A")
    c4.metric("High-Performer Attrition", f"{100 * high['Attrition_Flag'].mean():.2f}%" if len(high) else "N/A")
    st.subheader("Attrition by Department")
    dept = df.groupby("Department")["Attrition_Flag"].mean().mul(100).sort_values(ascending=False)
    st.bar_chart(dept, horizontal=True, x_label="Attrition Rate (%)", y_label="Department")
    st.info("Management focus: Understand overall employee attrition and the potential loss of high-performing talent.")

elif page == "General Attrition":
    st.header("General Employee Attrition")
    departments = sorted(df["Department"].dropna().unique().tolist())
    selected = st.selectbox("Select Department", ["All Departments"] + departments)
    filtered = df if selected == "All Departments" else df[df["Department"] == selected]
    c1, c2 = st.columns(2)
    c1.metric("Total Employees", f"{len(filtered):,}")
    c2.metric("Attrition Rate", f"{100 * filtered['Attrition_Flag'].mean():.2f}%" if len(filtered) else "N/A")
    st.subheader("Attrition by Overtime")
    st.bar_chart(filtered.groupby("OverTime")["Attrition_Flag"].mean().mul(100))
    st.subheader("Attrition by Job Satisfaction")
    st.bar_chart(filtered.groupby("JobSatisfaction")["Attrition_Flag"].mean().mul(100))
    st.caption("Historical associations do not establish causes of attrition.")

elif page == "High-Performer Retention":
    st.header("High-Performer Retention")
    st.write("This dashboard focuses on employees with Performance Rating 4.")
    high = df[df["PerformanceRating"] == 4]
    c1, c2, c3 = st.columns(3)
    c1.metric("High-Performing Employees", f"{len(high):,}")
    c2.metric("High Performers Who Left", f"{int(high['Attrition_Flag'].sum()):,}")
    c3.metric("High-Performer Attrition Rate", f"{100 * high['Attrition_Flag'].mean():.2f}%" if len(high) else "N/A")
    if len(high):
        st.subheader("High-Performer Attrition by Job Satisfaction")
        st.bar_chart(high.groupby("JobSatisfaction")["Attrition_Flag"].mean().mul(100))
        st.subheader("High-Performer Attrition by Overtime")
        st.bar_chart(high.groupby("OverTime")["Attrition_Flag"].mean().mul(100))
        st.subheader("High-Performer Attrition by Department")
        department = high.groupby("Department")["Attrition_Flag"].mean().mul(100).sort_values(ascending=False)
        st.bar_chart(department, horizontal=True, x_label="Attrition Rate (%)", y_label="Department")
        st.info("Investigate retention concerns among high performers, including satisfaction, overtime and career progression.")
        st.caption("These are historical group-level patterns, not individual predictions.")

elif page == "Attrition Risk Simulator":
    st.header("Attrition Risk Simulator")
    st.write("Explore how a trained logistic regression model responds to hypothetical employee characteristics.")
    try:
        model = load_model()
        st.success("Model loaded successfully!")
    except Exception as error:
        st.error("The prediction model could not be loaded.")
        st.exception(error)
        st.stop()

    st.caption("Use hypothetical profiles only. The results are exploratory model estimates, not validated individual resignation risks or employment decision criteria.")
    with st.form("prediction_form"):
        a, b = st.columns(2)
        with a:
            age = st.slider("Age", 18, 60, 35)
            income = st.number_input("Monthly Income (dataset units)", min_value=1009, max_value=19999, value=6500, step=100)
            stock = st.selectbox("Stock Option Level", [0, 1, 2, 3])
            overtime = st.selectbox("Overtime", ["No", "Yes"])
            satisfaction = st.slider("Job Satisfaction (1 = low, 4 = high)", 1, 4, 3)
        with b:
            balance = st.slider("Work-Life Balance (1 = low, 4 = high)", 1, 4, 3)
            involvement = st.slider("Job Involvement (1 = low, 4 = high)", 1, 4, 3)
            tenure = st.slider("Years at Company", 0, 40, 5)
            promotion = st.slider("Years Since Last Promotion", 0, min(15, tenure), min(2, tenure))
            rating = st.selectbox("Performance Rating", [3, 4], index=1)
        submitted = st.form_submit_button("Predict Attrition Probability")

    if submitted:
        input_data = pd.DataFrame([{
            "Age": float(age),
            "MonthlyIncome": int(income),
            "StockOptionLevel": int(stock),
            "OverTime": overtime,
            "JobSatisfaction": int(satisfaction),
            "WorkLifeBalance": int(balance),
            "JobInvolvement": int(involvement),
            "YearsAtCompany": int(tenure),
            "YearsSinceLastPromotion": int(promotion),
            "PerformanceRating": int(rating),
        }])
        try:
            classes = list(model.classes_)
            if 1 not in classes:
                st.error("Model does not contain the expected attrition class (1).")
            else:
                probabilities = model.predict_proba(input_data)[0]
