# import streamlit as st
# # from user_pages.dashboard import dashboard
# # from user_options.forgot_password_pg import show_forgot_password_page
# # from user_options.signup_pg import show_create_account_page
# # from user_options.login_pg import show_login_page
# from auth_functions import *
# from user_options.profile_entry import main_profile


# def rate_us_button():
#     @st.dialog("How do you rate our app?")
#     def rate():
#         sentiment_mapping = ["one", "two", "three", "four", "five"]
#         selected = st.feedback("stars")
#         if selected is not None:
#             st.session_state.rate = {"item": sentiment_mapping[selected]}
#             # st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
#             st.rerun()
#     rate()
#     return


# # Set up the page config
# st.set_page_config(page_title="Financial Agent", page_icon="💰", layout="wide")

# def entry_point():
#     st.title("My main entry point :D")

#     "This is a string written with :violet[***magic***]"


# if 'user_info' in st.session_state:
#     # Define the pages for logged-in users

#     # st.title("Welcome to Financial Agent")
#     # Sidebar with buttons for account selection

#     # nav_login = st.navigation(
#     #     [
#     #         st.Page('account_settings/user_controls.py', title="Profile", default=True),  # Magic works
#     #         st.Page("user_pages/dashboard.py", title="Dashboard"),
#     #         st.Page(sign_out, title="Sign Out"),  # Magic works
#     #         st.Page("user_options/profile_entry.py", title="Set Profile"),
#     #         st.Page("user_pages/money_tracker.py", title="Finanace Tracker"),
#     #         st.Page("user_pages/fraud_detector.py", title="Fraud Alert"),
#     #         st.Page("user_pages/quiz.py", title="Quiz"),
#     #         st.Page("user_pages/news.py", title="News"),
#     #         st.Page("user_pages/govt_schemes.py", title="Govt Schemes"),
#     #     ]
#     # )


#     with st.sidebar:
#         nav_login = st.navigation(
#             [
#                 # st.Page('account_settings/user_controls.py', title="Profile"),  # Magic works
#                 st.Page("user_pages/dashboard.py", title="Dashboard", default=True),
#                 # st.Page(sign_out, title="Sign Out"),  # Magic works
#                 # st.Page("user_options/profile_entry.py", title="Set Profile"),
#                 st.Page("user_pages/money_tracker.py", title="Finanace Tracker"),
#                 st.Page("user_pages/lessons.py", title=" Finance Lessons"),
#                 st.Page("user_pages/advisor.py", title="Finanace Advisor"),
#                 st.Page("user_pages/fraud_detector.py", title="Fraud Alert"),
#                 st.Page("user_pages/quiz.py", title="Quiz"),
#                 st.Page("user_pages/news.py", title="News"),
#                 st.Page("user_pages/govt_schemes.py", title="Govt Schemes"),
#                 st.Page("user_pages/dictionary.py", title="Dictionary"),
#                 st.Page("user_pages/chatbot.py", title="Chatbot"),
#             ]
#         )

#         # # Add empty space to push buttons to the bottom
#         # for _ in range(23):  # Adjust the number of empty lines as needed
#         #     st.write("")

#         # Add buttons at the bottom
#         col1, col2, col3 = st.columns([1, 1, 1])
#         with col1:
#             if st.button("Profile", key="profile_button"):
#                 main_profile()  # Trigger the profile function when the button is pressed
#         with col2:
#             if st.button("Sign Out", key="sign_out_button"):
#                 sign_out()  # Trigger the sign_out function when the button is pressed
#         with col3:
#             if st.button("Rate Us", key="rate_us_button"):
#                 # rate_us_button()
#                 if "rate" not in st.session_state:
#                     rate_us_button()  # Trigger the sign_out function when the button is pressed
#                 else:
#                     f"You gave us {st.session_state.rate['item']} stars!"


        
#         # if st.button("Sign Out", key="sign_out_button"):
#         #     sign_out()  # Trigger the sign_out function when the button is pressed

#         # if st.button("Profile", key="profile_button"):
#         #     main_profile()  # Trigger the sign_out function when the button is pressed

#     nav_login.run()

# else:
#     st.title("Welcome to Financial Agent")
#     # Sidebar with buttons for account selection

#     nav = st.navigation(
#         [
#             st.Page(entry_point, title="Introduction", default=True),  # Magic works
#             st.Page("user_options/login_pg.py", title="Log In"),  # Magic does not work
#             st.Page("user_options/signup_pg.py", title="Sign Up"),  # Magic works
#             # st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
#         ]
#     )
#     nav.run()



import streamlit as st
# from user_pages.dashboard import dashboard
# from user_options.forgot_password_pg import show_forgot_password_page
# from user_options.signup_pg import show_create_account_page
# from user_options.login_pg import show_login_page
from auth_functions import *
# from account_settings.user_controls import main_profile


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
st.set_page_config(page_title="Financial Agent", page_icon="💰", layout="wide")

st.markdown("""
    <style>
        /* Button */
        .stButton>button {
            background-color: rgba(28, 90, 151, 0.5);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #1E5F8B;
            transform: translateY(-2px);
        }
    </style>""", unsafe_allow_html=True)


def entry_point():
    st.title("My main entry point :D")

    "This is a string written with :violet[***magic***]"


if 'user_info' in st.session_state:
    initialize_firebase()
    user_info = st.session_state.user_info
    user_id = user_info['localId']  # Get the user ID from session state
    st.session_state.user_id = user_id
    # print("USER ID: ",user_id)
    nav_login = []
    # Define the pages for logged-in users

    # st.title("Welcome to Financial Agent")
    # Sidebar with buttons for account selection

    # nav_login = st.navigation(
    #     [
    #         st.Page('account_settings/user_controls.py', title="Profile", default=True),  # Magic works
    #         st.Page("user_pages/dashboard.py", title="Dashboard"),
    #         st.Page(sign_out, title="Sign Out"),  # Magic works
    #         st.Page("user_options/profile_entry.py", title="Set Profile"),
    #         st.Page("user_pages/money_tracker.py", title="Finanace Tracker"),
    #         st.Page("user_pages/fraud_detector.py", title="Fraud Alert"),
    #         st.Page("user_pages/quiz.py", title="Quiz"),
    #         st.Page("user_pages/news.py", title="News"),
    #         st.Page("user_pages/govt_schemes.py", title="Govt Schemes"),
    #     ]
    # )


    with st.sidebar:
        nav_login = st.navigation(
            [
                # st.Page('account_settings/user_controls.py', title="Profile"),  # Magic works
                st.Page("user_pages/dashboard.py", title="Dashboard", default=True),
                # st.Page(sign_out, title="Sign Out"),  # Magic works
                # st.Page("user_options/profile_entry.py", title="Set Profile"),
                # st.Page("user_pages/money_tracker.py", title="Finanace Tracker"),
                st.Page("user_pages/lessons.py", title=" Finance Lessons"),
                st.Page("user_pages/advisor.py", title="Finanace Advisor"),
                st.Page("user_pages/fraud_detector.py", title="Fraud Alert"),
                st.Page("user_pages/quiz.py", title="Quiz"),
                st.Page("user_pages/news.py", title="News"),
                st.Page("user_pages/govt_schemes.py", title="Govt Schemes"),
                st.Page("user_pages/dictionary.py", title="Dictionary"),
                st.Page("user_pages/chatbot.py", title="Chatbot"),
                # st.Page("account_settings/user_controls.py", title="Profile"),
                st.Page("user_pages/discussion_forum.py", title = "Discussion_Forum"),
                st.Page("user_options/profile_entry.py", title="Profile"),
                st.Page("user_pages/contact.py", title="Contact Us"),
                st.Page("user_pages/savings_tracker.py", title="Savings"),
                st.Page("user_pages/budget_helper.py", title="Budget Tracker"),
            ]
        )

        # # Add empty space to push buttons to the bottom
        # for _ in range(23):  # Adjust the number of empty lines as needed
        #     st.write("")

        # Add buttons at the bottom
        col1, col2 = st.columns([1, 1])
        # with col1:
        #     if st.button("Profile", key="profile_button"):
        #         main_profile()  # Trigger the profile function when the button is pressed
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


        
        # if st.button("Sign Out", key="sign_out_button"):
        #     sign_out()  # Trigger the sign_out function when the button is pressed

        # if st.button("Profile", key="profile_button"):
        #     main_profile()  # Trigger the sign_out function when the button is pressed

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



