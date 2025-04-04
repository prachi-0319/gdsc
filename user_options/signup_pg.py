import streamlit as st
from auth_functions import *

# Create Account form
st.title("Create Account")
with st.form(key="create_account_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

if submit_button:
    if email and password:
        with st.spinner('Creating account...'):
            if create_account(email, password):                
                # Display the success message
                st.success('Account Created Successfully!')
                st.success('Check your inbox to verify your email')
                st.page_link('user_options/login_pg.py', label='Go to Login')
            else:
                st.warning(st.session_state.auth_warning)
    else:
        st.error("Please provide both email and password.")