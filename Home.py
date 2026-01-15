import streamlit as st

st.set_page_config(
    page_title="Chitrang's Tools",
    page_icon="👋",
)

st.title("Welcome to My Utility Hub 👋")

st.markdown("""
### 🛠️ About These Tools
This application hosts a collection of utility tools designed to simplify daily tasks.
Select a tool from the sidebar to get started!

- **Work Hours Tracker**: Track your daily work hours, calculate breaks, and view overtime projections.
- **PDF Unlocker**: Easily remove passwords from your PDF files.

---

### 👨‍💻 About Me
I am a passionate developer creating useful tools and applications.

**Contact Details:**
- 📞 **Phone**: +91-9353291003
- 📧 **Email**: chitrang313@gmail.com

**Connect with me:**
<a href="https://github.com/chitrang313" target="_blank" style="text-decoration: none; margin-right: 10px;">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30" height="30" alt="GitHub" style="vertical-align: middle;"> GitHub
</a>
<a href="https://www.linkedin.com/in/chitrang313/" target="_blank" style="text-decoration: none;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30" height="30" alt="LinkedIn" style="vertical-align: middle;"> LinkedIn
</a>

""", unsafe_allow_html=True)

st.sidebar.success("Select a tool above to begin.")