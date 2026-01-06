import streamlit as st

st.set_page_config(page_title="EMI Calculator", page_icon="💰")
st.title("💰 Loan EMI Calculator")

p = st.number_input("Principal Amount (Loan Value)", min_value=0, value=100000)
r = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=8.5)
n = st.number_input("Loan Tenure (in Years)", min_value=1, value=5)

if st.button("Calculate EMI"):
    if p > 0 and r > 0 and n > 0:
        r_monthly = r / (12 * 100)
        n_months = n * 12
        emi = (p * r_monthly * ((1 + r_monthly) ** n_months)) / (((1 + r_monthly) ** n_months) - 1)
        st.success(f"Your Monthly EMI is: {emi:,.2f}")