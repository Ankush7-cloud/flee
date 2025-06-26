import streamlit as st

st.set_page_config(page_title="Device Management", layout="wide")

# Sidebar Menu
page = st.sidebar.radio("Navigation", ["Home", "Login", "Signup", "Admin"])

# Page Router
if page == "Home":
    import Home as p
elif page == "Login":
    import Login as p
elif page == "Signup":
    import Signup as p
elif page == "Admin":
    import Admin as p

p.app()
