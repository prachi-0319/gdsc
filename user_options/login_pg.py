# # pages/login.py
# import streamlit as st
# import auth_functions as auth_functions

# # Log In form
# st.title("Log In")
# with st.form(key="login_form"):
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     submit_button = st.form_submit_button("Log In")
    
#     if submit_button:
#         if email and password:
#             with st.spinner('Logging in...'):
#                 auth_functions.sign_in(email, password)
#                 if 'user_info' in st.session_state:
#                     st.session_state.current_page = 'dashboard'
#                     st.success('Logged in successfully!')
#                     st.rerun()  # Refresh to load the next page after sign-in
#                 else:
#                     st.error("Failed to log in. Please check your credentials.")
#         else:
#             st.error("Please provide both email and password.")


# # def show_login_page(account_selection):
  
# #   # Log In form
# #         st.title("Log In")
# #         with st.form(key="login_form"):
# #             email = st.text_input("Email")
# #             password = st.text_input("Password", type="password")
# #             submit_button = st.form_submit_button("Log In")
        
# #         if submit_button:
# #             if email and password:
# #                 with st.spinner('Logging in...'):
# #                     auth_functions.sign_in(email, password)
# #                     if 'user_info' in st.session_state:
# #                         st.session_state.current_page = 'dashboard'
# #                         st.success('Logged in successfully!')
# #                         st.rerun()  # Refresh to load the next page after sign-in
# #                     else:
# #                         st.error("Failed to log in. Please check your credentials.")
# #             else:
# #                 st.error("Please provide both email and password.")


# # show_login_page('Log In')

#     # st.title("Log In")

#     # # Login Form
#     # email = st.text_input("Email")
#     # password = st.text_input("Password", type="password")
    
#     # if st.form_submit_button("Log In"):
#     #     if email and password:
#     #         with st.spinner('Logging in...'):
#     #             if sign_in(email, password):
#     #                 st.session_state.current_page = 'main'
#     #                 st.success("Logged in successfully!")
#     #                 st.rerun()
#     #             else:
#     #                 st.error("Failed to log in. Please check your credentials.")
#     #     else:
#     #         st.error("Please provide both email and password.")


import streamlit as st
import auth_functions

# Log In form
st.title("Log In")
with st.form(key="login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Log In")
    
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
