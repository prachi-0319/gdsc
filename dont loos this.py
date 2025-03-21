import streamlit as st
import gdsc.auth_functions as auth_functions

# Set page config
st.set_page_config(
    page_title="Financial Agent",
    page_icon="💰",
    layout="wide"
)

# Initialize session state for page navigation if not exists
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    st.session_state.current_page = 'login'
    
    # Main title
    st.title("Welcome to Financial Agent")
    
    col1, col2, col3 = st.columns([1,2,1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
    auth_form = col2.form(key='Authentication form',clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
# Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email,password)
            if 'user_info' in st.session_state:
                st.text(st.session_state.user_info)
                st.session_state.current_page = 'main'
                st.rerun()  # Add this line to refresh the page

    # Create Account
    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email,password)
            if 'user_info' in st.session_state:
                st.session_state.current_page = 'main'
                st.rerun()  # Add this line to refresh the page

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # Sidebar for navigation and user controls
    with st.sidebar:
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

    # Main content area
    if st.session_state.current_page == 'main':
        st.title("Financial Agent Dashboard")
        st.write("Welcome to your financial dashboard!")
        
        # Add your main application content here
        # For example:
        st.header("Your Financial Overview")
        # Add more components and functionality as needed
