import streamlit as st
from user_pages.dashboard import dashboard
# from user_options.forgot_password_pg import show_forgot_password_page
# from user_options.signup_pg import show_create_account_page
# from user_options.login_pg import show_login_page
from gdsc.auth_functions import sign_out


# Set up the page config
st.set_page_config(page_title="Financial Agent", page_icon="💰", layout="wide")

def entry_point():
    st.title("My main entry point :D")

    "This is a string written with :violet[***magic***]"


if 'user_info' in st.session_state:
    # Define the pages for logged-in users

    st.title("Welcome to Financial Agent")
    # Sidebar with buttons for account selection

    nav_login = st.navigation(
        [
            st.Page('account_settings/user_controls.py', title="Profile", default=True),  # Magic works
            st.Page("user_pages/dashboard.py", title="Dashboard"),
            st.Page(sign_out, title="Sign Out"),  # Magic works
            st.Page("user_options/profile_entry.py", title="Set Profile"),
            st.Page("user_pages/money_tracker.py", title="Finanace Tracker"),
        ]
    )
    nav_login.run()

else:
    st.title("Welcome to Financial Agent")
    # Sidebar with buttons for account selection

    nav = st.navigation(
        [
            st.Page(entry_point, title="Introduction", default=True),  # Magic works
            st.Page("user_options/login_pg.py", title="Log In"),  # Magic does not work
            st.Page("user_options/signup_pg.py", title="Sign Up"),  # Magic works
            # st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
        ]
    )
    nav.run()