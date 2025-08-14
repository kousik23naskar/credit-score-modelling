# app.py

import streamlit as st
import requests

st.set_page_config(page_title="Credit Score Predictor", layout="wide")

st.title("📊 Credit Score & Default Probability Predictor")
st.markdown("Enter applicant information below to predict credit score, risk level, and default probability.")

# === Input Layout ===
st.subheader("🧾 Applicant Information")

# Create two columns for input layout
col1, col2 = st.columns(2)

with col1:
    person_age = st.slider("👤 Age", 18, 100, 30)
    person_income = int(st.number_input("💰 Income (Annual)", value=50000, step=1000))
    person_home_ownership = st.selectbox("🏠 Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"])
    person_emp_length = st.slider("💼 Employment Length (years)", 0, 40, 5)
    loan_intent = st.selectbox("📌 Loan Intent", ["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"])

with col2:
    loan_grade = st.selectbox("🏷️ Loan Grade", ["A", "B", "C", "D", "E", "F", "G"])
    loan_amnt = int(st.number_input("🏦 Loan Amount", value=10000, step=500))
    loan_int_rate = st.slider("📉 Interest Rate (%)", 5.0, 30.0, 13.0)
    loan_percent_income = st.slider("📊 Loan % of Income", 0.01, 1.0, 0.2)
    cb_person_default_on_file = st.selectbox("📁 Previous Default", ["Y", "N"])
    cb_person_cred_hist_length = st.slider("📆 Credit History Length (years)", 1, 30, 10)

# Combine inputs
input_data = {
    "person_age": person_age,
    "person_income": person_income,
    "person_home_ownership": person_home_ownership,
    "person_emp_length": person_emp_length,
    "loan_intent": loan_intent,
    "loan_grade": loan_grade,
    "loan_amnt": loan_amnt,
    "loan_int_rate": loan_int_rate,
    "loan_percent_income": loan_percent_income,
    "cb_person_default_on_file": cb_person_default_on_file,
    "cb_person_cred_hist_length": cb_person_cred_hist_length
}

st.markdown("---")

# === Predict Button ===
if st.button("🔍 Predict Credit Score"):
    with st.spinner("Predicting..."):
        try:
            response = requests.post("http://localhost:8000/predict/", json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Prediction Successful!")

                # === Show results in columns ===
                score_col, risk_col, prob_col = st.columns(3)
                score_col.metric("📈 Credit Score", result["credit_score"])
                risk_col.metric("🎯 Risk Level", result["risk_level"])
                prob_col.metric("📉 Default Probability", f'{result["default_probability"]:.2%}')

                st.info(f"📋 Credit Level: {result['credit_level']} — {result['credit_description']}")
            else:
                st.error("❌ Prediction failed. Check input or backend logs.")
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 Could not connect to backend: {e}")