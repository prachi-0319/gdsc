# pages/create_account.py
import streamlit as st
import gdsc.auth_functions as auth_functions

# Create Account form
st.title("Create Account")
with st.form(key="create_account_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

if submit_button:
    if email and password:
        with st.spinner('Creating account...'):
            auth_functions.create_account(email, password)
            if 'user_info' in st.session_state:
                st.session_state.current_page = 'login'
                st.success('Account created successfully!')
                account_selection == "Log In"
                st.rerun()  # Refresh to load the next page after account creation
            else:
                st.error("Failed to create account.")
    else:
        st.error("Please provide both email and password.")
    


# def show_create_account_page(account_selection):
#     # Create Account form
#         st.title("Create Account")
#         with st.form(key="create_account_form"):
#             email = st.text_input("Email")
#             password = st.text_input("Password", type="password")
#             submit_button = st.form_submit_button("Sign Up")
        
#         if submit_button:
#             if email and password:
#                 with st.spinner('Creating account...'):
#                     auth_functions.create_account(email, password)
#                     if 'user_info' in st.session_state:
#                         st.session_state.current_page = 'login'
#                         st.success('Account created successfully!')
#                         account_selection == "Log In"
#                         st.rerun()  # Refresh to load the next page after account creation
#                     else:
#                         st.error("Failed to create account.")
#             else:
#                 st.error("Please provide both email and password.")
    
    
    
    # st.title("Create Account")

    # # Account Creation Form
    # email = st.text_input("Email")
    # password = st.text_input("Password", type="password")
    
    # if st.form_submit_button("Create Account"):
    #     if email and password:
    #         with st.spinner('Creating account...'):
    #             if create_account(email, password):
    #                 st.session_state.current_page = 'main'
    #                 st.success("Account created successfully!")
    #                 st.rerun()
    #             else:
    #                 st.error("Failed to create account.")
    #     else:
    #         st.error("Please provide both email and password.")
