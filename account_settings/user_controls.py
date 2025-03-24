import streamlit as st
import auth_functions as auth_functions


st.title("User Controls")
st.write(f"Welcome, {st.session_state.user_info.get('email', 'User')}")

# Sign out button
if st.button("Sign Out", type="primary"):
    auth_functions.sign_out()
    st.session_state.current_page = 'login'
    st.rerun()

# Delete account section
st.header("Delete Account")
delete_password = st.text_input("Confirm your password", type="password")
if st.button("Delete Account", type="primary"):
    auth_functions.delete_account(delete_password)
    if 'user_info' not in st.session_state:
        st.session_state.current_page = 'login'
        st.rerun()
