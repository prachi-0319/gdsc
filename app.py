import streamlit as st
from auth_functions import *

initialize_firebase_once()

def rate_us_button():
    @st.dialog("How do you rate our app?")
    def rate():
        sentiment_mapping = ["one", "two", "three", "four", "five"]
        selected = st.feedback("stars")
        if selected is not None:
            st.session_state.rate = {"item": sentiment_mapping[selected]}
            # st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
            st.rerun()
    rate()
    return


# Set up the page config
st.set_page_config(page_title="FinFriend", page_icon="💰", layout="wide")

if 'user_info' in st.session_state:
    initialize_firebase()
    user_info = st.session_state.user_info
    user_id = user_info['localId']  # Get the user ID from session state
    st.session_state.user_id = user_id
    nav_login = []

    with st.sidebar:
        nav_login = st.navigation(
            [
                st.Page("user_pages/dashboard.py", title="Dashboard", default=True),
                st.Page("user_pages/lessons.py", title=" Finance Lessons"),
                # st.Page("user_pages/advisor.py", title="Finanace Advisor"),
                st.Page("user_pages/fraud_detector.py", title="Fraud Alert & Gov"),
                st.Page("user_pages/quiz.py", title="Quiz"),
                st.Page("user_pages/news.py", title="News"),
                st.Page("user_pages/dictionary.py", title="Dictionary"),
                st.Page("user_pages/chatbot.py", title="Chatbot"),
                st.Page("user_pages/stock_analysis_pg.py", title="Analysis & Advice"),
                st.Page("user_pages/discussion_forum.py", title = "Discussion_Forum"),
                st.Page("user_options/profile_entry.py", title="Profile"),
            ]
        )

        # Add buttons at the bottom
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("Sign Out", key="sign_out_button"):
                sign_out()  # Trigger the sign_out function when the button is pressed
        with col2:
            if st.button("Rate Us", key="rate_us_button"):
                # rate_us_button()
                if "rate" not in st.session_state:
                    rate_us_button()  # Trigger the sign_out function when the button is pressed
                else:
                    f"You gave us {st.session_state.rate['item']} stars!"
    nav_login.run()

else:
    st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p>Discover tools, resources, and advice to make informed financial decisions.</p>
        <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    initialize_firebase()
    # Sidebar with buttons for account selection

    nav = st.navigation(
        [
            st.Page("user_pages/dashboard.py",title="Introduction", default=True),  # Magic works
            st.Page("user_options/login_pg.py", title="Log In"),  # Magic does not work
            st.Page("user_options/signup_pg.py", title="Sign Up"),  # Magic works
            # st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
        ]
    )
    nav.run()



