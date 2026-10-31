
import streamlit as st
import joblib

st.set_page_config(
    page_title="IBM HR Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("IBM HR Analytics")
st.subheader("Workforce Attrition & Strategic Talent Retention")

page = st.sidebar.radio(
    "Select a Page",
    [
        "Executive Overview",
        "General Attrition",
        "High-Performer Retention",
        "Attrition Risk Simulator"
    ]
)

if page == "Executive Overview":
    st.header("Executive Overview")
    st.write("Explore workforce attrition and retention.")

elif page == "General Attrition":
    st.header("General Employee Attrition")
    st.write("Interactive HR analysis will appear here.")

elif page == "High-Performer Retention":
    st.header("High-Performer Retention")
    st.write("Focus on employees with Performance Rating 4.")

elif page == "Attrition Risk Simulator":
    st.header("Attrition Risk Simulator")
    st.write("Experimental logistic regression demonstration.")

    @st.cache_resource
    def load_model():
        return joblib.load("attrition_model (1).pkl")

    model = load_model()
    st.success("Model loaded successfully!")
