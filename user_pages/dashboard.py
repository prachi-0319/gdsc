import streamlit as st
import plotly.express as px
from auth_functions import *
from ChatBot.chatbot import *


with open('./user_pages/home.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# ---- User Authentication ----
if 'user_info' not in st.session_state:

# Add custom style targeting the a[data-testid="stPageLink"]
#     st.markdown("""
#     <style>
    
#     </style>
# """, unsafe_allow_html=True)

# Use a wrapper class so our styles apply
    st.markdown('<div class="custom-page-link-wrapper">', unsafe_allow_html=True)
    st.page_link("user_options/login_pg.py", label="🚀 Get Started", icon="➡️")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Hero Section ---
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-heading">Your AI-Powered Finance Companion</h1>
        <p class="hero-subtext">
            Unlock financial confidence with tools that empower you to make smarter, safer, and more informed money decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    # --- Feature Cards ---
    features = [
        ("📊", "Financial Advisor", "Get personalized financial advice."),
        ("📖", "Finance Dictionary", "Easily look up financial terms."),
        ("📰", "Finance News", "Stay updated on financial news."),
        ("🤖", "AI Chatbot", "Chat with our AI financial assistant."),
        ("🛡️", "Fraud Detector", "Check if an investment is fraudulent."),
        ("🏛️", "Govt. Schemes Finder", "Find government schemes for you."),
        ("📝", "Finance Quiz", "Test your financial knowledge."),
        ("📚", "Lessons", "Enhance your financial knowledge."),
    ]
    cols = st.columns(4)
    for i, (icon, title, description) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-description">{description}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("")
    st.warning("Please log in to access the dashboard.")
    st.stop()  # Stops execution if not logged in


# ---- Header Section ----
st.markdown("")
st.markdown("")
st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <p>Discover tools, resources, and advice to make informed financial decisions.</p>
    <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
</div>
""", unsafe_allow_html=True)


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

if "user_info" in st.session_state and "user_id" in st.session_state:
    user_id = st.session_state.user_id  # Get the user ID
    user_profile = get_user_profile(user_id)  # Fetch profile data

    if user_profile:
        user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
    else:
        user_name = "User"
# else:
#     user_name = "User"

# Display the name
st.markdown(f"<h4 style='text-align: center;'>Welcome, {user_name}! 🎉</h4>", unsafe_allow_html=True)

# ---- Search Bar for AI Chatbot ----
st.markdown("") # empty line
st.markdown("") # empty line

user_input = st.text_input("🔍 Ask us anything:", placeholder="What is the best long term investment...")

if st.button("Search"):
    if user_input:  # Ensure input is not empty
        st.session_state.chatbot = FinancialChatBot()
        st.session_state.history = []

        bot_response = st.session_state.chatbot.chat(user_input, None)

        st.session_state.history.append({
            "role": "user",
            "content": user_input,
            "image_path": None
        })
        st.session_state.history.append({
            "role": "assistant",
            "text": bot_response["text"],
            "plot": bot_response["plot"]
        })

        # st.session_state["user_query"] = user_input  # Store in session state
        st.switch_page("user_pages/chatbot.py")  # Navigate to chatbot page


# ---- Features Grid ----
st.markdown("<h2 style='text-align: center;'>Explore Our Features</h2>", unsafe_allow_html=True)
st.markdown("") # empty line
st.markdown("") # empty line

features = [
    ("📊", "Financial Advisor", "Get personalized financial advice.", "advisor"),
    ("📖", "Finance Dictionary", "Easily look up financial terms.", "dictionary"),
    ("📰", "Finance News", "Stay updated on financial news.", "news"),
    ("🤖", "AI Chatbot", "Chat with our AI financial assistant.", "chatbot"),
    # ("💰 Savings Tracker", "Monitor and analyze your savings.", "money_tracker"),
    ("🛡️", "Fraud Detector", "Check if an investment is fraudulent.", "fraud_detector"),
    ("🏛️", "Govt. Schemes Finder", "Find government schemes for you.", "govt_schemes"),
    ("📝", "Finance Quiz", "Test your financial knowledge.", "quiz"),
    ("📚", "Lessons", "Enhance your financial knowledge.", "lessons"),
]

# ---- Custom CSS for Styling ----
st.markdown("""
<style>
    .circle-icon {
        border-radius: 50%;
        width: 125px;
        height: 125px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        background-color: rgba(21, 76, 121, 0.15);
        border: 0.7px solid #76b5c5;
        color: white;
        font-size: 50px;
        margin-bottom: 10px;
    }
    .feature-text {
        text-align: center;
    }
    .floating-box {
        background-color: rgba(21, 76, 121, 0.15);
        border-radius: 15px;
        border: 0.7px solid #76b5c5;
        padding: 20px;
        margin: 20px 0;
    }
    .faq-section {
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

cols = st.columns(4)
for i, (icon, title, description, page) in enumerate(features):
    with cols[i % 4]:

        st.markdown(f"""
        <div style="text-align: center;">
            <div class="circle-icon">{icon}</div>
            <p class="feature-text">{title}</p>
            <p class="feature-text">{description}</p>
        </div>
        """, unsafe_allow_html=True)
        # if st.button(f"Open", key=f"feature_{i}"):
        #     st.switch_page(f"user_pages/{page}.py")
        # Create a small column layout to center the button

        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        with button_col2:  # Center column
            if st.button(f"Open", key=f"feature_{i}"):
                st.switch_page(f"user_pages/{page}.py")

        st.markdown("") # empty line
        st.markdown("") # empty line

# ---- Floating Box with Image and Text ----
st.markdown("") # empty line
st.markdown("") # empty line
st.markdown("") # empty line

st.markdown("""
<div class="floating-box">
    <div style="display: flex; align-items: center;">
        <div style="flex: 1; text-align: center;">
            <img src="assets/dashboard_dialog.png" alt="Financial Education" style="border-radius: 10px; max-width: 80%; height: auto;">
        </div>
        <div style="flex: 1; padding-left: 20px;">
            <h3 style="margin-top: 0;">Financial Freedom Starts Here!</h3>
            <p style="font-size: 15px;">Did you know 76% of Indians struggle with basic financial concepts? That's where we come in! Our app makes money mastery easy and fun with:</p>
            <ul style="padding-left: 20px; font-size: 15px;">
                <li style="margin-bottom: 8px;">Bite-sized lessons that stick</li>
                <li style="margin-bottom: 8px;">AI-powered tools tailored just for you</li>
                <li style="margin-bottom: 8px;">Real-world skills to grow your wealth</li>
            </ul>
            <p style="font-size: 15px;">We're closing the financial literacy gap—one user at a time. Your journey to smart money habits starts now! 💡</p>
            <p style="font-weight: bold; font-size: 15px;">Join <span style="color: #27AE60;">50,000+</span> Indians already taking control of their finances!</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- FAQ Section ----
st.markdown("") # empty line
st.markdown("") # empty line
st.markdown("") # empty line
faq_col1, faq_col2 = st.columns(2)

with faq_col2:
    with st.expander("What is Financial Planning?"):
        st.write("Financial planning involves setting financial goals and creating a roadmap to achieve them.")
    with st.expander("How to start saving money?"):
        st.write("Start by creating a budget, setting savings goals, and automating your savings.")
    with st.expander("What are the basics of investing?"):
        st.write("Understand risk tolerance, diversify investments, and invest for the long term.")
    with st.expander("How to detect a fraud scheme?"):
        st.write("Be skeptical of unrealistic promises, avoid pressure tactics, and verify credentials.")

with faq_col1:
    st.markdown("<h2>Frequently asked questions</h2>", unsafe_allow_html=True)
    st.markdown("Can't find what you're looking for? We are always happy to help you navigate your financial journey!")

# ---- Footer Section ----
st.markdown("<hr>", unsafe_allow_html=True)
footer_col1, footer_col2 = st.columns(2)

with footer_col1:
    st.markdown("<h2>Join the FinFriend club today!</h2>", unsafe_allow_html=True)

with footer_col2:
    # st.markdown("<h4>Connect with us:</h4>", unsafe_allow_html=True)
    st.markdown("") # empty line
    st.markdown("") # empty line
    st.markdown("Discord | Gmail | Twitter", unsafe_allow_html=True)