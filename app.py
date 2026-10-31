import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="IBM HR Analytics", page_icon="📊", layout="wide")

st.markdown("""<style>
.block-container {padding-top: 1.5rem; max-width: 1250px;}
h1, h2, h3 {letter-spacing: -0.025em;}
[data-testid="stMetric"] {background: #f4f7fb; border: 1px solid #dce5ef; border-radius: 12px; padding: 16px;}
[data-testid="stMetricLabel"] {font-weight: 600;}
[data-testid="stSidebar"] {background: #f1f5f9;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    files = ["Employees.csv", "Compensation.csv", "Performance.csv", "Experience.csv", "Employment Status.csv"]
    frames = [pd.read_csv(name) for name in files]
    df = frames[0]
    for frame in frames[1:]:
        df = df.merge(frame, on="EmployeeNumber", validate="one_to_one")
    df = df.dropna().copy()
    df["Attrition_Flag"] = df["Attrition"].eq("Yes").astype(int)
    return df

@st.cache_resource
def load_model():
    return joblib.load("attrition_model (1).pkl")

def pct(series):
    return float(series.mean() * 100) if len(series) else 0.0

def grouped_rates(frame, column):
    result = frame.groupby(column, dropna=False).agg(
        Employees=("Attrition_Flag", "size"),
        Departures=("Attrition_Flag", "sum"),
        Attrition_Rate=("Attrition_Flag", "mean")
    )
    result["Attrition_Rate"] *= 100
    return result.sort_values("Attrition_Rate", ascending=False)

def chart_rates(frame, column, title):
    st.subheader(title)
    summary = grouped_rates(frame, column)
    if summary.empty:
        st.info("No data available for this selection.")
        return summary
    st.bar_chart(summary["Attrition_Rate"], horizontal=True, x_label="Attrition rate (%)", y_label=column)
    with st.expander("View underlying figures"):
        table = summary.rename(columns={"Attrition_Rate": "Attrition rate (%)"}).copy()
        st.dataframe(table.style.format({"Attrition rate (%)": "{:.2f}"}), use_container_width=True)
    return summary

def insight(text):
    st.markdown("**Management insight**")
    st.info(text)

df = load_data()
page = st.sidebar.radio("Explore dashboard", [
    "Executive Overview", "General Attrition", "High-Performer Retention", "Attrition Risk Simulator"
])
st.sidebar.caption("IBM HR Analytics | Educational capstone")
st.title("IBM HR Analytics")
st.caption("Workforce Attrition & Strategic Talent Retention | Historical analysis and model demonstration")
st.divider()

if page == "Executive Overview":
    st.header("Executive Overview")
    high = df[df["PerformanceRating"] == 4]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees analysed", f"{len(df):,}")
    c2.metric("Employees who left", f"{int(df['Attrition_Flag'].sum()):,}")
    c3.metric("Overall attrition", f"{pct(df['Attrition_Flag']):.2f}%")
    c4.metric("High-performer attrition", f"{pct(high['Attrition_Flag']):.2f}%" if len(high) else "N/A")
    dept = chart_rates(df, "Department", "Attrition by department")
    if not dept.empty:
        top = dept.iloc[0]
        name = str(dept.index[0])
        insight(f"{name} has the highest observed departmental attrition rate ({top['Attrition_Rate']:.2f}%; {int(top['Departures'])} departures among {int(top['Employees'])} employees). Review team-level exit feedback, workload and career opportunities before deciding on interventions.")
    st.markdown("**Recommended management priorities**")
    st.write("1. Review departments with elevated attrition, considering the number of employees as well as the rate.")
    st.write("2. Investigate overtime and job-satisfaction patterns rather than assuming causation.")
    st.write("3. Monitor the loss of high performers separately from overall attrition.")

elif page == "General Attrition":
    st.header("General Employee Attrition")
    options = ["All Departments"] + sorted(df["Department"].dropna().astype(str).unique().tolist())
    selected = st.selectbox("Department", options)
    filtered = df if selected == "All Departments" else df[df["Department"] == selected]
    c1, c2, c3 = st.columns(3)
    c1.metric("Employees", f"{len(filtered):,}")
    c2.metric("Departures", f"{int(filtered['Attrition_Flag'].sum()):,}")
    c3.metric("Attrition rate", f"{pct(filtered['Attrition_Flag']):.2f}%")
    left, right = st.columns(2)
    with left:
        overtime = chart_rates(filtered, "OverTime", "Attrition by overtime")
    with right:
        satisfaction = chart_rates(filtered, "JobSatisfaction", "Attrition by job satisfaction")
    if "Yes" in overtime.index and "No" in overtime.index:
        yes_rate = overtime.loc["Yes", "Attrition_Rate"]
        no_rate = overtime.loc["No", "Attrition_Rate"]
        insight(f"Employees with overtime have an observed attrition rate of {yes_rate:.2f}%, compared with {no_rate:.2f}% for employees without overtime (difference: {yes_rate-no_rate:+.2f} percentage points). Consider reviewing workload distribution and employee feedback. This is an association, not proof of cause.")
    else:
        insight("Review overtime and satisfaction patterns alongside sample sizes, exit reasons and other factors before selecting HR interventions.")

elif page == "High-Performer Retention":
    st.header("High-Performer Retention")
    st.caption("High performers are defined as employees with PerformanceRating = 4.")
    high = df[df["PerformanceRating"] == 4].copy()
    c1, c2, c3 = st.columns(3)
    c1.metric("High performers", f"{len(high):,}")
    c2.metric("High performers who left", f"{int(high['Attrition_Flag'].sum()):,}")
    c3.metric("High-performer attrition", f"{pct(high['Attrition_Flag']):.2f}%" if len(high) else "N/A")
    if len(high):
        chart_rates(high, "Department", "High-performer attrition by department")
        left, right = st.columns(2)
        with left:
            chart_rates(high, "OverTime", "High performers: overtime")
        with right:
            chart_rates(high, "JobSatisfaction", "High performers: job satisfaction")
        insight(f"{int(high['Attrition_Flag'].sum())} of {len(high)} high performers left ({pct(high['Attrition_Flag']):.2f}%). Prioritise qualitative retention discussions and investigate patterns in workload, satisfaction and career development. Small groups may have unstable percentages.")
    else:
        st.warning("No employees with PerformanceRating = 4 were found.")

elif page == "Attrition Risk Simulator":
    st.header("Attrition Risk Simulator")
    st.caption("Explore how a trained logistic regression model responds to hypothetical employee profiles.")
    try:
        model = load_model()
        st.success("Prediction model loaded successfully")
        with st.form("simulator"):
            left, right = st.columns(2)
            with left:
                age = st.slider("Age", 18, 60, 30)
                income = st.number_input("Monthly income (dataset units)", min_value=1009, max_value=19999, value=5000, step=100)
                stock = st.selectbox("Stock option level", [0, 1, 2, 3])
                overtime = st.selectbox("Overtime", ["No", "Yes"])
                satisfaction = st.slider("Job satisfaction (1 = low, 4 = high)", 1, 4, 4)
            with right:
                balance = st.slider("Work-life balance (1 = low, 4 = high)", 1, 4, 2)
                involvement = st.slider("Job involvement (1 = low, 4 = high)", 1, 4, 3)
                tenure = st.slider("Years at company", 0, 40, 3)
                promotion = st.slider("Years since last promotion", 0, 15, 2)
                performance = st.selectbox("Performance rating", [3, 4], index=1)
            submit = st.form_submit_button("Predict attrition probability", type="primary")
        if submit:
            input_data = pd.DataFrame([{
                "Age": float(age), "MonthlyIncome": int(income),
                "StockOptionLevel": int(stock), "OverTime": overtime,
                "JobSatisfaction": int(satisfaction), "WorkLifeBalance": int(balance),
                "JobInvolvement": int(involvement), "YearsAtCompany": int(tenure),
                "YearsSinceLastPromotion": int(promotion), "PerformanceRating": int(performance)
            }])
            probabilities = model.predict_proba(input_data)[0]
            classes = list(model.classes_)
            leave_prob = float(probabilities[classes.index(1)])
            stay_prob = float(probabilities[classes.index(0)])
            a, b = st.columns(2)
            a.metric("Estimated attrition probability", f"{leave_prob:.2%}")
            b.metric("Estimated staying probability", f"{stay_prob:.2%}")
            st.progress(leave_prob)
            st.info("Compare scenarios by changing one input at a time. Changes in model output do not demonstrate that an intervention would cause the same change in real employee outcomes.")
        st.warning("For learning and demonstration only. Model probabilities are not established as calibrated or reliable for individual HR decisions. Do not use these outputs to make employment decisions.")
    except Exception as error:
        st.error("The model could not be loaded or used for prediction.")
        st.exception(error)
