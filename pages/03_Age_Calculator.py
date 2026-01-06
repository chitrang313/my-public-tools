import streamlit as st
from datetime import date

st.set_page_config(page_title="Age Calculator", page_icon="🎂")
st.title("🎂 Age Calculator")

dob = st.date_input("Select your Date of Birth", min_value=date(1900, 1, 1))

if st.button("Calculate Age"):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.success(f"You are {age} years old!")