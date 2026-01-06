import streamlit as st

# 1. Setup the page
st.set_page_config(page_title="My Python Tools", page_icon="🛠️")

# 2. Sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ["Home", "Tool A: Text Reverser", "Tool B: Number Squarer"])

# 3. Define the "Home" page
if choice == "Home":
    st.title("Welcome to My Tool Hub! 🚀")
    st.write("I built this using Python. Select a tool from the sidebar to try it out.")

# 4. Define "Tool A"
elif choice == "Tool A: Text Reverser":
    st.header("Tool A: Text Reverser")
    user_input = st.text_input("Enter some text here:")
    if user_input:
        st.success(f"Reversed: {user_input[::-1]}")

# 5. Define "Tool B"
elif choice == "Tool B: Number Squarer":
    st.header("Tool B: Number Squarer")
    number = st.number_input("Enter a number", value=0)
    if st.button("Calculate"):
        st.write(f"The square of {number} is {number ** 2}")