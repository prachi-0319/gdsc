import streamlit as st
import gdsc.auth_functions as auth_functions


def dashboard():
    if 'user_info' not in st.session_state:
        st.warning("Please log in to access the dashboard.")
        return  # Prevent further execution of the code if the user is not logged in
    
    st.title("User Controls")
    st.write(f"Welcome, {st.session_state.user_info.get('email', 'User')}")

    # logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    # settings = st.Page("account_settings/user_controls.py", title="Settings", icon=":material/settings:")
    # dashboard = st.Page("pages/dashboard.py", title='Dashboard',icon=":material/settings:")
    
# st.title("Financial Agent Dashboard")
# st.write("Welcome to your financial dashboard!")
# Add your financial dashboard components here
# st.header("Your Financial Overview")