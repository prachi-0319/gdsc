import streamlit as st
import auth_functions

# Log In form
st.title("Log In")
with st.form(key="login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Log In")
    st.page_link('user_options/forgot_password_pg.py', label='Reset Password')
    if submit_button:
        if email and password:
            with st.spinner('Logging in...'):
                auth_functions.sign_in(email, password)
                if 'user_info' in st.session_state:
                    st.session_state.current_page = 'dashboard'
                    st.success('Logged in successfully!')
                    st.rerun()  # Refresh to load the next page after sign-in
                else:
                    st.error("Failed to log in. Please check your credentials.")
        else:
            st.error("Please provide both email and password.")
