import streamlit as st

st.set_page_config(
    page_title="My Utility Hub",
    page_icon="👋",
)

st.title("Welcome to My Utility Hub 👋")
st.write("I have created a collection of useful tools. Select one from the **sidebar** on the left to get started!")

st.sidebar.success("Select a tool above.")