# pages/forgot_password.py
import streamlit as st
import auth_functions as auth_functions

st.title("Password Recovery")
with st.form(key="forgot_password_form"):
    email = st.text_input("Email")
    submit_button = st.form_submit_button("Send Password Reset Link")
    
    if submit_button:
        if email:
            with st.spinner('Sending password reset link...'):
                auth_functions.reset_password(email)
                st.success(f"Password reset instructions have been sent to {email}.")
                account_selection = 'login'
        else:
            st.error("Please provide your email for password recovery.")

