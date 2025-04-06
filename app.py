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
            <p>Discover tools, resources, and advice to make informed financial decisions.</p>
            <p>Explore personalized financial advice, track savings, analyse stocks, and more.</p>
        </div>
        """, unsafe_allow_html=True)

    initialize_firebase()
    # Sidebar with buttons for account selection

    nav = st.navigation(
        [
            st.Page("user_pages/dashboard.py",title="Introduction", default=True),  # Magic works
            st.Page("user_options/login_pg.py", title="Log In"),  # Magic does not work
            st.Page("user_options/signup_pg.py", title="Sign Up"),  # Magic works
            st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
            # st.Page("user_options/forgot_password_pg.py", title="Reset Password"),  # Magic works
        ]
    )
    nav.run()


# --------------------------------------------------------------------------------------------------------------------------
