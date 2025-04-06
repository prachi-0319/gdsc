# import streamlit as st
# from auth_functions import *

# initialize_firebase_once()

# def rate_us_button():
#     @st.dialog("How do you rate our app?")
#     def rate():
#         sentiment_mapping = ["one", "two", "three", "four", "five"]
#         selected = st.feedback("stars", key="rating_feedback_stars") # Use a unique key
#         if selected is not None:
#             st.session_state.user_rating = {"stars": sentiment_mapping[selected - 1]}
#             st.success(f"Thank you for rating us {selected} star(s)!")
#             st.rerun()
#         else:
#             st.write("Please select a star rating.")

#     rate()
#     return

# # Set up the page config
# st.set_page_config(
#     page_title="Financial Agent", 
#     page_icon="💰", 
#     layout="wide", 
#     initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed')
# )

# st.logo(
#     image = "assets/logo_finfriend.png",
#     size = "large",
#     icon_image = "assets/logo_finfriend.png",
# )

# # st.markdown("""
# #     <style>
# #         /* Button */
# #         .stButton>button {
# #             background-color: rgba(28, 90, 151, 0.5);
# #             color: white;
# #             border-radius: 8px;
# #             padding: 0.5rem 1rem;
# #             width: 100%;
# #             transition: all 0.3s;
# #         }
# #         .stButton>button:hover {
# #             background-color: #1E5F8B;
# #             transform: translateY(-2px);
# #         }
# #     </style>""", unsafe_allow_html=True)

# st.markdown("""
#     <style>
#         /* Button */
#         .stButton>button {
#             background-color: rgba(131, 158, 101, 0.8);
#             color: white;
#             border: none;
#             border-radius: 10px;
#             padding: 0.5rem 1rem;
#             width: 100%;
#             transition: all 0.3s;
#         }
#         .stButton>button:hover {
#             background-color: #839E65;
#             transform: translateY(-2px);
#         }
#     </style>""", unsafe_allow_html=True)


# def entry_point():
#     st.title("My main entry point :D")

#     "This is a string written with :violet[***magic***]"


# def get_user_profile(user_id):
#     """Fetches the user's profile from Firestore using their user ID."""
#     if db is None:
#         st.error("Database not initialized.")
#         return None

#     doc_ref = db.collection("UserData").document(user_id)
#     doc = doc_ref.get()

#     if doc.exists:
#         user_data = doc.to_dict()
#         return user_data  # Return the full profile dictionary
#     return None  # Return None if the user profile is not found


# if 'user_info' in st.session_state:
#     # initialize_firebase()
#     user_info = st.session_state.user_info
#     user_id = user_info['localId']
#     st.session_state.user_id = user_id
#     # print("USER ID: ",user_id)
#     nav_login = []

#     st.markdown("")
#     st.markdown("")

#     user_id = st.session_state.user_id  # Get the user ID
#     user_profile = get_user_profile(user_id)  # Fetch profile data

#     if user_profile:
#         user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
#     else:
#         user_name = "User"

#     # if "user_info" in st.session_state and "user_id" in st.session_state:
#     #     user_id = st.session_state.user_id  # Get the user ID
#     #     user_profile = get_user_profile(user_id)  # Fetch profile data

#     #     if user_profile:
#     #         user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
#     #     else:
#     #         user_name = "User"
#     # else:
#     #     user_name = "User"

    

#     with st.sidebar:
#         st.markdown(f"<h4 style='text-align: center;'>Welcome, {user_name}! 🎉</h4>", unsafe_allow_html=True)
#         nav_login = st.navigation(
#             [
#                 st.Page("user_pages/dashboard.py", title="Dashboard", default=True),
#                 st.Page("user_pages/advisor.py", title="Finanace Advisor"),
#                 st.Page("user_pages/lessons.py", title=" Finance Lessons"),
#                 st.Page("user_pages/finance_toolkit.py", title="Financial Tools"),
#                 st.Page("user_pages/quiz.py", title="Quiz"),
#                 st.Page("user_pages/news.py", title="News"),
#                 st.Page("user_pages/dictionary.py", title="Dictionary"),
#                 st.Page("user_pages/chatbot.py", title="Chatbot"),
#                 st.Page("user_pages/savings_tracker.py", title="Savings"),
#                 st.Page("user_pages/stock_analysis.py", title="Stock Analysis"),
#                 st.Page("user_pages/discussion_forum.py", title = "Discussion Forum"),
#                 st.Page("user_options/profile_entry.py", title="Profile"),
#                 # st.Page("user_pages/contact.py", title="Contact Us"),
#             ]
#         )

#         # # Add empty space to push buttons to the bottom
#         # for _ in range(23):  # Adjust the number of empty lines as needed
#         #     st.write("")

#         # Sidebar Footer Buttons
#         st.markdown("<div class='sidebar-footer'>", unsafe_allow_html=True)
#         col1, col2 = st.columns(2)
#         with col1:
#             # Use type="secondary" for less emphasis
#             if st.button("Sign Out", key="sign_out_button_sidebar", type="secondary"):
#                 sign_out()
#         with col2:
#             if st.button("Rate Us", key="rate_us_button_sidebar", type="secondary"):
#                 if "user_rating" not in st.session_state:
#                     rate_us_dialog()
#                 # If already rated, clicking might reopen or do nothing based on dialog logic
#                 # Displaying message below is cleaner

#         # Show rating message persistently if rated
#         if "user_rating" in st.session_state:
#             st.success(f"Thanks for your {st.session_state.user_rating['stars']} star rating!")
#             # Consider adding a small button/link to "Change rating?" which could clear session state and call dialog again.
#             # if st.button("Change rating?", key="change_rating", type="small"): # Needs custom small button CSS or use link
#             #      del st.session_state.user_rating
#             #      st.rerun() # Rerun to make Rate Us button active again

#         st.markdown("</div>", unsafe_allow_html=True)


#     # Run the selected page function
#     nav_selection_logged_in.run()

# else:
#     st.markdown("")
#     st.markdown("")
#     st.markdown("")

#     cols = st.columns([2,1])

#     with cols[0]:
#         st.image("assets/homepage_image.png", use_container_width=True)

#     with cols[1]:
#         st.markdown("")
#         st.markdown("")
#         st.markdown("")
#         st.markdown("")
#         st.markdown("")
#         st.markdown("")
#         # st.markdown("<h1 style='text-align: right; font-size: 80px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
#         st.markdown("<h1 style='text-align: right; font-size: 70px; font-weight: bold;'>WELCOME TO FINFRIEND</h1>", unsafe_allow_html=True)
#         st.markdown("""
#         <div style="text-align: right; margin-top: 20px;">
#             <p>Discover tools, resources, and advice to make informed financial decisions. Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
#         </div>
#         """, unsafe_allow_html=True)

#     initialize_firebase()
#     # Sidebar with buttons for account selection

#     nav = st.navigation(
#         [
#             st.Page("user_pages/dashboard.py",title="Introduction", default=True),  # Magic works
#             st.Page("user_options/login_pg.py", title="Log In"),  # Magic does not work
#             st.Page("user_options/signup_pg.py", title="Sign Up"),  # Magic works
#             # st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
#         ]
#     )
#     nav.run()


# # --------------------------------------------------------------------------------------------------------------------------


# # import os
# # import streamlit as st
# # from auth_functions import *
# # from streamlit_navigation_bar import st_navbar

# # # Initialize Firebase
# # initialize_firebase_once()

# # # Define the 'Rate Us' button functionality
# # def rate_us_button():
# #     @st.dialog("How do you rate our app?")
# #     def rate():
# #         sentiment_mapping = ["one", "two", "three", "four", "five"]
# #         selected = st.feedback("stars")
# #         if selected is not None:
# #             st.session_state.rate = {"item": sentiment_mapping[selected]}
# #             st.rerun()
# #     rate()
# #     return

# # # Set up the page config
# # st.set_page_config(page_title="Financial Agent", page_icon="💰", layout="wide")

# # # Add a logo
# # st.logo(
# #     image="assets/logo_finfriend.png",
# #     size="large",
# #     icon_image="assets/logo_finfriend.png",
# # )

# # # Define page functions
# # def show_dashboard():
# #     st.title("Dashboard")
# #     st.write("Welcome to the Dashboard!")

# # def show_lessons():
# #     st.title("Finance Lessons")
# #     st.write("Learn about financial topics here.")

# # def show_advisor():
# #     st.title("Finance Advisor")
# #     st.write("Get personalized financial advice.")

# # def show_finance_toolkit():
# #     st.title("Financial Tools")
# #     st.write("Detect fraud and manage your finances.")

# # def show_quiz():
# #     st.title("Quiz")
# #     st.write("Test your financial knowledge!")

# # def show_news():
# #     st.title("News")
# #     st.write("Stay updated with financial news.")

# # def show_dictionary():
# #     st.title("Dictionary")
# #     st.write("Look up financial terms.")

# # def show_chatbot():
# #     st.title("Chatbot")
# #     st.write("Ask our AI chatbot financial questions.")

# # def show_discussion_forum():
# #     st.title("Discussion Forum")
# #     st.write("Engage in financial discussions.")

# # def show_profile():
# #     st.title("Profile")
# #     st.write("Manage your user profile.")

# # def show_contact():
# #     st.title("Contact Us")
# #     st.write("Reach out to us for support.")

# # def show_savings():
# #     st.title("Savings Tracker")
# #     st.write("Track and optimize your savings.")

# # def show_stock_analysis():
# #     st.title("Stock Analysis")
# #     st.write("Analyze stock market trends.")

# # # Define pages for top navigation
# # pages = ["Dashboard", "Finance Lessons", "Finance Advisor", "Financial Tools", 
# #          "Quiz", "News", "Dictionary", "Chatbot", "Discussion Forum", "Profile",
# #          "Contact Us", "Savings", "Stock Analysis"]

# # # Define page functions mapping
# # functions = {
# #     "Dashboard": show_dashboard,
# #     "Finance Lessons": show_lessons,
# #     "Finance Advisor": show_advisor,
# #     "Financial Tools": show_finance_toolkit,
# #     "Quiz": show_quiz,
# #     "News": show_news,
# #     "Dictionary": show_dictionary,
# #     "Chatbot": show_chatbot,
# #     "Discussion Forum": show_discussion_forum,
# #     "Profile": show_profile,
# #     "Contact Us": show_contact,
# #     "Savings": show_savings,
# #     "Stock Analysis": show_stock_analysis,
# # }

# # # Navigation bar
# # logo_path = "assets/logo_finfriend.svg"
# # urls = {}  # Add external links if needed
# # styles = {
# #     "nav": {"background-color": "royalblue", "justify-content": "left"},
# #     "span": {"color": "white", "padding": "14px"},
# #     "active": {"background-color": "white", "color": "black", "padding": "14px"}
# # }
# # options = {"show_menu": False, "show_sidebar": False}

# # # Get the selected page
# # page = st_navbar(pages, logo_path=logo_path, urls=urls, styles=styles, options=options)

# # # Run the selected page function
# # if page in functions:
# #     functions[page]()

# # # If user is logged in, add buttons
# # if 'user_info' in st.session_state:
# #     initialize_firebase()
# #     user_info = st.session_state.user_info
# #     user_id = user_info['localId']
# #     st.session_state.user_id = user_id

# #     # Sign Out & Rate Us Buttons
# #     col1, col2 = st.columns([1, 1])
# #     with col1:
# #         if st.button("Sign Out", key="sign_out_button"):
# #             sign_out()

# #     with col2:
# #         if st.button("Rate Us", key="rate_us_button"):
# #             if "rate" not in st.session_state:
# #                 rate_us_button()
# #             else:
# #                 f"You gave us {st.session_state.rate['item']} stars!"

# # # If user is not logged in, show the welcome page
# # else:
# #     st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
# #     st.markdown("""
# #     <div style="text-align: center; margin-top: 20px;">
# #         <p>Discover tools, resources, and advice to make informed financial decisions.</p>
# #         <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
# #     </div>
# #     """, unsafe_allow_html=True)



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
st.set_page_config(
    page_title="Financial Agent", 
    page_icon="💰", 
    layout="wide", 
    initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed')
)

st.logo(
    image = "assets/logo_finfriend.png",
    size = "large",
    icon_image = "assets/logo_finfriend.png",
)

# st.markdown("""
#     <style>
#         /* Button */
#         .stButton>button {
#             background-color: rgba(28, 90, 151, 0.5);
#             color: white;
#             border-radius: 8px;
#             padding: 0.5rem 1rem;
#             width: 100%;
#             transition: all 0.3s;
#         }
#         .stButton>button:hover {
#             background-color: #1E5F8B;
#             transform: translateY(-2px);
#         }
#     </style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Button */
        .stButton>button {
            background-color: rgba(131, 158, 101, 0.8);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #839E65;
            transform: translateY(-2px);
        }
    </style>""", unsafe_allow_html=True)


def entry_point():
    st.title("My main entry point :D")

    "This is a string written with :violet[***magic***]"


def get_user_profile(user_id):
    """Fetches the user's profile from Firestore using their user ID."""
    if db is None:
        st.error("Database not initialized.")
        return None

    doc_ref = db.collection("UserData").document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        return user_data  # Return the full profile dictionary
    return None  # Return None if the user profile is not found


if 'user_info' in st.session_state:
    # initialize_firebase()
    user_info = st.session_state.user_info
    user_id = user_info['localId']  # Get the user ID from session state
    st.session_state.user_id = user_id
    # print("USER ID: ",user_id)
    nav_login = []

    st.markdown("")
    st.markdown("")

    user_id = st.session_state.user_id  # Get the user ID
    user_profile = get_user_profile(user_id)  # Fetch profile data

    if user_profile:
        user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
    else:
        user_name = "User"

    # if "user_info" in st.session_state and "user_id" in st.session_state:
    #     user_id = st.session_state.user_id  # Get the user ID
    #     user_profile = get_user_profile(user_id)  # Fetch profile data

    #     if user_profile:
    #         user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
    #     else:
    #         user_name = "User"
    # else:
    #     user_name = "User"

    

    with st.sidebar:
        st.markdown(f"<h4 style='text-align: center;'>Welcome, {user_name}! 🎉</h4>", unsafe_allow_html=True)
        nav_login = st.navigation(
            [
                st.Page("user_pages/dashboard.py", title="Dashboard", default=True),
                st.Page("user_pages/advisor.py", title="Finanace Advisor"),
                st.Page("user_pages/lessons.py", title=" Finance Lessons"),
                st.Page("user_pages/finance_toolkit.py", title="Financial Tools"),
                st.Page("user_pages/quiz.py", title="Quiz"),
                st.Page("user_pages/news.py", title="News"),
                st.Page("user_pages/dictionary.py", title="Dictionary"),
                st.Page("user_pages/chatbot.py", title="Chatbot"),
                st.Page("user_pages/savings_tracker.py", title="Savings"),
                st.Page("user_pages/stock_analysis.py", title="Stock Analysis"),
                st.Page("user_pages/discussion_forum.py", title = "Discussion Forum"),
                st.Page("user_options/profile_entry.py", title="Profile"),
                # st.Page("user_pages/contact.py", title="Contact Us"),
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
    st.markdown("")
    st.markdown("")
    st.markdown("")

    cols = st.columns([2,1])

    with cols[0]:
        st.image("assets/homepage_image.png", use_container_width=True)

    with cols[1]:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        # st.markdown("<h1 style='text-align: right; font-size: 80px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: right; font-size: 70px; font-weight: bold;'>WELCOME TO FINFRIEND</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: right; margin-top: 20px;">
            <p>Discover tools, resources, and advice to make informed financial decisions. Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
        </div>
        """, unsafe_allow_html=True)

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


# --------------------------------------------------------------------------------------------------------------------------


# import os
# import streamlit as st
# from auth_functions import *
# from streamlit_navigation_bar import st_navbar

# # Initialize Firebase
# initialize_firebase_once()

# # Define the 'Rate Us' button functionality
# def rate_us_button():
#     @st.dialog("How do you rate our app?")
#     def rate():
#         sentiment_mapping = ["one", "two", "three", "four", "five"]
#         selected = st.feedback("stars")
#         if selected is not None:
#             st.session_state.rate = {"item": sentiment_mapping[selected]}
#             st.rerun()
#     rate()
#     return

# # Set up the page config
# st.set_page_config(page_title="Financial Agent", page_icon="💰", layout="wide")

# # Add a logo
# st.logo(
#     image="assets/logo_finfriend.png",
#     size="large",
#     icon_image="assets/logo_finfriend.png",
# )

# # Define page functions
# def show_dashboard():
#     st.title("Dashboard")
#     st.write("Welcome to the Dashboard!")

# def show_lessons():
#     st.title("Finance Lessons")
#     st.write("Learn about financial topics here.")

# def show_advisor():
#     st.title("Finance Advisor")
#     st.write("Get personalized financial advice.")

# def show_finance_toolkit():
#     st.title("Financial Tools")
#     st.write("Detect fraud and manage your finances.")

# def show_quiz():
#     st.title("Quiz")
#     st.write("Test your financial knowledge!")

# def show_news():
#     st.title("News")
#     st.write("Stay updated with financial news.")

# def show_dictionary():
#     st.title("Dictionary")
#     st.write("Look up financial terms.")

# def show_chatbot():
#     st.title("Chatbot")
#     st.write("Ask our AI chatbot financial questions.")

# def show_discussion_forum():
#     st.title("Discussion Forum")
#     st.write("Engage in financial discussions.")

# def show_profile():
#     st.title("Profile")
#     st.write("Manage your user profile.")

# def show_contact():
#     st.title("Contact Us")
#     st.write("Reach out to us for support.")

# def show_savings():
#     st.title("Savings Tracker")
#     st.write("Track and optimize your savings.")

# def show_stock_analysis():
#     st.title("Stock Analysis")
#     st.write("Analyze stock market trends.")

# # Define pages for top navigation
# pages = ["Dashboard", "Finance Lessons", "Finance Advisor", "Financial Tools", 
#          "Quiz", "News", "Dictionary", "Chatbot", "Discussion Forum", "Profile",
#          "Contact Us", "Savings", "Stock Analysis"]

# # Define page functions mapping
# functions = {
#     "Dashboard": show_dashboard,
#     "Finance Lessons": show_lessons,
#     "Finance Advisor": show_advisor,
#     "Financial Tools": show_finance_toolkit,
#     "Quiz": show_quiz,
#     "News": show_news,
#     "Dictionary": show_dictionary,
#     "Chatbot": show_chatbot,
#     "Discussion Forum": show_discussion_forum,
#     "Profile": show_profile,
#     "Contact Us": show_contact,
#     "Savings": show_savings,
#     "Stock Analysis": show_stock_analysis,
# }

# # Navigation bar
# logo_path = "assets/logo_finfriend.svg"
# urls = {}  # Add external links if needed
# styles = {
#     "nav": {"background-color": "royalblue", "justify-content": "left"},
#     "span": {"color": "white", "padding": "14px"},
#     "active": {"background-color": "white", "color": "black", "padding": "14px"}
# }
# options = {"show_menu": False, "show_sidebar": False}

# # Get the selected page
# page = st_navbar(pages, logo_path=logo_path, urls=urls, styles=styles, options=options)

# # Run the selected page function
# if page in functions:
#     functions[page]()

# # If user is logged in, add buttons
# if 'user_info' in st.session_state:
#     initialize_firebase()
#     user_info = st.session_state.user_info
#     user_id = user_info['localId']
#     st.session_state.user_id = user_id

#     # Sign Out & Rate Us Buttons
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         if st.button("Sign Out", key="sign_out_button"):
#             sign_out()

#     with col2:
#         if st.button("Rate Us", key="rate_us_button"):
#             if "rate" not in st.session_state:
#                 rate_us_button()
#             else:
#                 f"You gave us {st.session_state.rate['item']} stars!"

# # If user is not logged in, show the welcome page
# else:
#     st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
#     st.markdown("""
#     <div style="text-align: center; margin-top: 20px;">
#         <p>Discover tools, resources, and advice to make informed financial decisions.</p>
#         <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
#     </div>
#     """, unsafe_allow_html=True)
