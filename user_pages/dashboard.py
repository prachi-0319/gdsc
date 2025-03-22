# import streamlit as st
# import auth_functions 

# def dashboard():
#     if 'user_info' not in st.session_state:
#         st.warning("Please log in to access the dashboard.")
#         return  # Prevent further execution of the code if the user is not logged in
    
#     st.title("User Controls")
#     st.write(f"Welcome, {st.session_state.user_info.get('email', 'User')}")

#     # logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
#     settings = st.Page("account_settings/user_controls.py", title="Settings", icon=":material/settings:")
#     dashboard = st.Page("pages/dashboard.py", title='Dashboard',icon=":material/settings:")
    
# st.title("Financial Agent Dashboard")
# st.write("Welcome to your financial dashboard!")
# # Add your financial dashboard components here
# st.header("Your Financial Overview")




import streamlit as st
import auth_functions

# ---- User Authentication ----
if 'user_info' not in st.session_state:
    st.warning("Please log in to access the dashboard.")
    st.stop()  # Stops execution if not logged in

# ---- Dashboard Header ----

st.markdown("<h1 style='text-align: center;'>🙌 FinFriend</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>Welcome, {st.session_state.user_info.get('email', 'User')}! 🎉</h3>", unsafe_allow_html=True)

# ---- Search Bar for AI Chatbot ----
search_query = st.text_input("🔍 Ask us anything:", placeholder="What is the best long term investment...")
if st.button("Search"):
    st.switch_page(f"user_pages/chatbot.py")

# ---- Features Section ----
st.markdown("### 🌟 Explore Our Features")

# ---- Full-Width Grid Layout ----
col1, col2, col3 = st.columns([1, 1, 1])  # Equal column width

features = [
    ("📊 Financial Advisor", "Get personalized financial advice.", "advisor"),
    ("📖 Finance Dictionary", "Easily look up financial terms.", "dictionary"),
    ("📰 Finance News", "Stay updated on financial news.", "news"),
    ("🤖 AI Chatbot", "Chat with our AI financial assistant.", "chatbot"),
    ("💰 Savings Tracker", "Monitor and analyze your savings.", "money_tracker"),
    ("🛡️ Fraud Detector", "Check if an investment is fraudulent.", "fraud_detector"),
    ("🏛️ Govt. Schemes Finder", "Find government schemes for you.", "govt_schemes"),
    ("📝 Finance Quiz", "Test your financial knowledge.", "quiz"),
    ("📚 Lessons", "Enhance your financial knowledge.", "quiz"),
]

# ---- Display Features in Animated Cards ----
for i, (title, description, page) in enumerate(features):
    with (col1 if i % 3 == 0 else (col2 if i % 3 == 1 else col3)):  # Alternating columns
        with st.container():
            st.markdown(f"""
                <div style="border-radius: 10px; padding: 15px; margin: 10px; 
                            background: linear-gradient(to right, #2E86C1, #5DADE2);
                            color: white; text-align: center; font-size: 18px;">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {title}", key=f"feature_{i}"):
                st.switch_page(f"user_pages/{page}.py")

# ---- Quick Actions Section ----
st.markdown("### ⚡ Quick Actions")
quick_col1, quick_col2, quick_col3 = st.columns(3)

with quick_col1:
    if st.button("📊 Go to Savings Tracker"):
        st.switch_page(f"user_pages/money_tracker.py")

with quick_col2:
    if st.button("📝 Take a Finance Quiz"):
        st.switch_page(f"user_pages/quiz.py")

with quick_col3:
    if st.button("🏛️ Find Govt. Schemes"):
        st.switch_page(f"user_pages/govt_schemes.py")
