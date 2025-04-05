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




# import streamlit as st
# import auth_functions

# # ---- User Authentication ----
# if 'user_info' not in st.session_state:
#     st.warning("Please log in to access the dashboard.")
#     st.stop()  # Stops execution if not logged in

# # ---- Dashboard Header ----

# st.markdown("<h1 style='text-align: center;'>🙌 FinFriend</h1>", unsafe_allow_html=True)
# st.markdown(f"<h3 style='text-align: center;'>Welcome, {st.session_state.user_info.get('email', 'User')}! 🎉</h3>", unsafe_allow_html=True)

# # ---- Search Bar for AI Chatbot ----
# search_query = st.text_input("🔍 Ask us anything:", placeholder="What is the best long term investment...")
# if st.button("Search"):
#     st.switch_page(f"user_pages/chatbot.py")

# # ---- Features Section ----
# st.markdown("### 🌟 Explore Our Features")

# # ---- Full-Width Grid Layout ----
# col1, col2, col3 = st.columns([1, 1, 1])  # Equal column width

# features = [
#     ("📊 Financial Advisor", "Get personalized financial advice.", "advisor"),
#     ("📖 Finance Dictionary", "Easily look up financial terms.", "dictionary"),
#     ("📰 Finance News", "Stay updated on financial news.", "news"),
#     ("🤖 AI Chatbot", "Chat with our AI financial assistant.", "chatbot"),
#     ("💰 Savings Tracker", "Monitor and analyze your savings.", "money_tracker"),
#     ("🛡️ Fraud Detector", "Check if an investment is fraudulent.", "fraud_detector"),
#     ("🏛️ Govt. Schemes Finder", "Find government schemes for you.", "govt_schemes"),
#     ("📝 Finance Quiz", "Test your financial knowledge.", "quiz"),
#     ("📚 Lessons", "Enhance your financial knowledge.", "quiz"),
# ]

# # ---- Display Features in Animated Cards ----
# for i, (title, description, page) in enumerate(features):
#     with (col1 if i % 3 == 0 else (col2 if i % 3 == 1 else col3)):  # Alternating columns
#         with st.container():
#             st.markdown(f"""
#                 <div style="border-radius: 10px; padding: 15px; margin: 10px; 
#                             background: linear-gradient(to right, #2E86C1, #5DADE2);
#                             color: white; text-align: center; font-size: 18px;">
#                     <h3>{title}</h3>
#                     <p>{description}</p>
#                 </div>
#             """, unsafe_allow_html=True)
#             if st.button(f"Open {title}", key=f"feature_{i}"):
#                 st.switch_page(f"user_pages/{page}.py")

# # ---- Quick Actions Section ----
# st.markdown("### ⚡ Quick Actions")
# quick_col1, quick_col2, quick_col3 = st.columns(3)

# with quick_col1:
#     if st.button("📊 Go to Savings Tracker"):
#         st.switch_page(f"user_pages/money_tracker.py")

# with quick_col2:
#     if st.button("📝 Take a Finance Quiz"):
#         st.switch_page(f"user_pages/quiz.py")

# with quick_col3:
#     if st.button("🏛️ Find Govt. Schemes"):
#         st.switch_page(f"user_pages/govt_schemes.py")


import streamlit as st
import plotly.express as px
from auth_functions import *
from ChatBot.chatbot import *
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container


# ---- User Authentication ----
if 'user_info' not in st.session_state:
    st.warning("Please log in to access the dashboard.")
    st.stop()  # Stops execution if not logged in


# ---- Page Configuration ----
# st.set_page_config(page_title="FinFriend", layout="wide")

# ---- Header Section ----

st.markdown("")
st.markdown("")
st.markdown("")

cols = st.columns([2,1])

with cols[0]:
    st.image("assets/homepage_image.png", use_container_width=True, caption="Homepage Image")

with cols[1]:
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("<h1 style='text-align: right; font-size: 80px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: right; margin-top: 20px;">
        <p>Discover tools, resources, and advice to make informed financial decisions. Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
    </div>
    """, unsafe_allow_html=True)


# st.markdown("")
# st.markdown("")
# st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold;'>Welcome to FinFriend</h1>", unsafe_allow_html=True)
# st.markdown("""
# <div style="text-align: center; margin-top: 20px;">
#     <p>Discover tools, resources, and advice to make informed financial decisions.</p>
#     <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
# </div>
# """, unsafe_allow_html=True)

# st.image("assets/homepage_image.png", use_container_width=True, caption="Homepage Image")


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

st.markdown("")
st.markdown("")

if "user_info" in st.session_state and "user_id" in st.session_state:
    user_id = st.session_state.user_id  # Get the user ID
    user_profile = get_user_profile(user_id)  # Fetch profile data

    if user_profile:
        user_name = user_profile.get("Name", "User")  # Default to "User" if name is missing
    else:
        user_name = "User"
else:
    user_name = "User"

# Display the name
st.markdown(f"<h4 style='text-align: center;'>Welcome, {user_name}! 🎉</h4>", unsafe_allow_html=True)

# st.markdown("""
# <div style="text-align: center; padding: 20px; background-color: #2E86C1; color: white; border-radius: 10px;">
#     <h1>🙌 Welcome to FinFriend</h1>
#     <h4>Empowering Financial Awareness in India</h4>
#     <button style="background-color: #5DADE2; color: white; padding: 10px 20px; border-radius: 5px; border: none;">Get Started</button>
# </div>
# """, unsafe_allow_html=True)

# ---- Introduction Section ----
# st.markdown("""
# <div style="text-align: center; margin-top: 20px;">
#     <h4>Discover tools, resources, and advice to make informed financial decisions.</h4>
#     <p>Explore personalized financial advice, track savings, detect fraud schemes, and much more.</p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown(f"<h3 style='text-align: center;'>Welcome, {st.session_state.user_info.get('email', 'User')}! 🎉</h3>", unsafe_allow_html=True)

# ---- Search Bar for AI Chatbot ----
st.markdown("") # empty line
st.markdown("") # empty line

user_input = st.text_input("🔍 Ask us anything:", placeholder="What is the best long term investment...")

# if st.button("Search"):
#     st.switch_page(f"user_pages/chatbot.py")

# Store user input in session state
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
# st.markdown("## Explore Our Features")

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


# Apply styling with Streamlit Extras
with stylable_container(
    "card_container",
    css_styles="""
    .card-container {
        gap: 30px;
        justify-items: center;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        padding: 20px;
        max-width: 1200px;
        margin: auto;
    }
    .card{
        background: linear-gradient(135deg, #ffffff, #f5f5f5);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
    }

    .card-icon {
        font-size: 50px;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #333;
    }
    .card-description {
        font-size: 14px;
        color: #666;
        margin-bottom: 20px;
    }
    .card button {
        background: #839E65;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-size: 16px;
        cursor: pointer;
        transition: background 0.3s;
    }
    .card button:hover {
        background: #6F8A50;
    }
    """
):
    cols = st.columns(4)
    for i, (icon, title, description, page) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-description">{description}</div>
                <button onclick="window.location.href='/user_pages/{page}.py'">Open</button>
            </div>
            """, unsafe_allow_html=True)
    
            st.markdown("") # empty line
            st.markdown("") # empty line

# # ---- Custom CSS for Styling ----
# st.markdown("""
# <style>
#     .circle-icon {
#         border-radius: 50%;
#         width: 125px;
#         height: 125px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         margin: 0 auto;
#         background-color: rgba(21, 76, 121, 0.15);
#         border: 0.7px solid #76b5c5;
#         color: white;
#         font-size: 50px;
#         margin-bottom: 10px;
#     }
#     .feature-text {
#         text-align: center;
#     }
#     .floating-box {
#         background-color: rgba(21, 76, 121, 0.15);
#         border-radius: 15px;
#         border: 0.7px solid #76b5c5;
#         padding: 20px;
#         margin: 20px 0;
#     }
#     .faq-section {
#         margin-top: 30px;
#     }
# </style>
# """, unsafe_allow_html=True)

# cols = st.columns(4)
# for i, (icon, title, description, page) in enumerate(features):
#     with cols[i % 4]:

#         st.markdown(f"""
#         <div style="text-align: center;">
#             <div class="circle-icon">{icon}</div>
#             <p class="feature-text">{title}</p>
#             <p class="feature-text">{description}</p>
#         </div>
#         """, unsafe_allow_html=True)
#         # if st.button(f"Open", key=f"feature_{i}"):
#         #     st.switch_page(f"user_pages/{page}.py")
#         # Create a small column layout to center the button

#         button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
#         with button_col2:  # Center column
#             if st.button(f"Open", key=f"feature_{i}"):
#                 st.switch_page(f"user_pages/{page}.py")

#         st.markdown("") # empty line
#         st.markdown("") # empty line

# ---- Floating Box with Image and Text ----
# st.markdown("<h2 style='text-align: center;'>🎉 Did You Know?</h2>", unsafe_allow_html=True)
st.markdown("") # empty line
st.markdown("") # empty line
st.markdown("") # empty line
# st.markdown("""
# <div class="floating-box">
#     <div style="display: flex; align-items: center;">
#         <div style="flex: 1;">
#             <img src="assets/dashboard_dialog.png" alt="Placeholder Image" style="border-radius: 10px; size:80px align:center;">
#         </div>
#         <div style="flex: 1; padding-left: 20px;">
#             <h3>Financial Freedom Starts Here!</h3>
#             <p>Did you know 76% of Indians struggle with basic financial concepts? That's where we come in! 🚀 Our app makes money mastery easy and fun with:</p>
#             <ul>
#             <item>Bite-sized lessons that stick</item>
#             <item>AI-powered tools tailored just for you</item>
#             <item>Real-world skills to grow your wealth</item>
#             </ul>
#             <p>We're closing the financial literacy gap—one user at a time. Your journey to smart money habits starts now! 💡</p>
#             <p>Join <span>50,000+<span> Indians already taking control of their finances!<p>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)
# st.markdown("""
# <div class="floating-box">
#     <div style="display: flex; align-items: center;">
#         <div style="flex: 1; text-align: center;">
#             <img src="assets/dashboard_dialog.png" alt="Financial Education" style="border-radius: 10px; max-width: 80%; height: auto;">
#         </div>
#         <div style="flex: 1; padding-left: 20px;">
#             <h3 style="margin-top: 0;">Financial Freedom Starts Here!</h3>
#             <p style="font-size: 15px;">Did you know 76% of Indians struggle with basic financial concepts? That's where we come in! Our app makes money mastery easy and fun with:</p>
#             <ul style="padding-left: 20px; font-size: 15px;">
#                 <li style="margin-bottom: 8px;">Bite-sized lessons that stick</li>
#                 <li style="margin-bottom: 8px;">AI-powered tools tailored just for you</li>
#                 <li style="margin-bottom: 8px;">Real-world skills to grow your wealth</li>
#             </ul>
#             <p style="font-size: 15px;">We're closing the financial literacy gap—one user at a time. Your journey to smart money habits starts now! 💡</p>
#             <p style="font-weight: bold; font-size: 15px;">Join <span style="color: #27AE60;">50,000+</span> Indians already taking control of their finances!</p>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# Wrap everything inside a stylable container for custom styling
with stylable_container(
    "floating-box-container",
    css_styles="""
    .floating-box-container {
        background-color: #f9f9f9; /* Light gray background for the container */
        border-radius: 20px;      /* Rounded corners */
        padding: 30px;            /* Padding inside the container */
        margin: 40px 0;           /* Margin to separate from other content */
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); /* Soft shadow effect */
    }

    .floating-box {
        position: relative;
        background-color: #ffffff; /* White background for the box */
        border-radius: 15px;       /* Rounded corners */
        padding: 20px;             /* Padding inside the box */
        display: flex;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Box shadow for depth */
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        min-height: 370px
    }

    .floating-box:hover {
        transform: translateY(-10px); /* Hover effect - lift the box */
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
    }

    .floating-box img {
        border-radius: 10px;
        max-width: 100%;  /* Ensure image fits well */
        height: auto;     /* Maintain aspect ratio */
        max-height: 250px; /* Optional: limit image size */
        margin-right: 20px; /* Space between image and content */
    }

    .floating-box .content {
        padding-left: 20px;
        flex: 1;
        min-width: 250px;   /* Minimum width for the content area */
    }

    .floating-box .content h3 {
        margin-top: 0;
        font-size: 24px;
        color: #333;
    }

    .floating-box .content p {
        font-size: 15px;
        color: #555;
    }

    .floating-box .content ul {
        padding-left: 20px;
        font-size: 15px;
        color: #555;
    }

    .floating-box .content p.bold-text {
        font-weight: bold;
        font-size: 16px;
        color: #333;
    }

    @media (max-width: 768px) {
        .floating-box {
            flex-direction: column;
            align-items: center;
        }

        .floating-box img {
            margin-right: 0;
            margin-bottom: 20px; /* Add space between image and content on small screens */
        }

        .floating-box .content {
            padding-left: 0;
            text-align: center;
        }
    }
    """
):
    col1, col2 = st.columns([1, 1])  # Set equal width columns
    with col1:
        st.image("assets/dashboard_dialog.png", use_container_width=True, caption="Financial Education")
    with col2:
    # Create the floating box with both image and content inside it
        st.markdown("""
        <div class="floating-box">
            <div class="content">
                <h3 style="margin-top: 0;">Your Path to Financial Freedom Starts Here!</h3>
                <p style="font-size: 15px;">Did you know that 76% of Indians struggle with understanding basic financial concepts? You're not alone—but there's a solution! Our app is designed to make mastering your finances easy, fun, and empowering with:</p>
                <ul style="padding-left: 20px; font-size: 15px;">
                    <li style="margin-bottom: 8px;">Bite-sized lessons that are easy to grasp and stick with you.</li>
                    <li style="margin-bottom: 8px;">AI-powered tools tailored to your unique financial goals and needs.</li>
                    <li style="margin-bottom: 8px;">Real-world skills to confidently grow your wealth and secure your future.</li>
                </ul>
                <p style="font-size: 15px;">We're closing the financial literacy gap—one user at a time. Your journey to smart money habits starts now! 💡</p>
                <p style="font-weight: bold; font-size: 15px;">Join <span style="color: #27AE60;">50,000+</span> Indians already taking control of their finances!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        
# Floating box with flexbox layout
# Use Streamlit's st.image() for better compatibility
# col1, col2 = st.columns([1, 2])

# with col1:
#     try:
#         st.image("assets/dashboard_dialog.png", use_container_width=True)
#     except FileNotFoundError:
#         st.warning("Image not found. Please check the file path.")

# with col2:
#     st.markdown("""
#     <div class="floating-box-content">
#         <h3>Boost Your Financial Knowledge</h3>
#         <p>Learn the secrets to smart investing and savings. Unlock financial freedom today!</p>
#     </div>
#     """, unsafe_allow_html=True)

# # ---- Interactive Tools Section ----
# st.markdown("## 📈 Interactive Tools")

# # Savings Tracker Chart Example
# st.markdown("### 💰 Savings Tracker Trends")
# data = px.data.gapminder().query("country == 'India'")
# fig = px.line(data, x='year', y='gdpPercap', title='Savings Growth Over Time')
# st.plotly_chart(fig)

# # Finance News Carousel Example (Placeholder)
# st.markdown("### 📰 Trending Finance News")
# news = ["News 1: Stock Market Update", 
#         "News 2: RBI Policy Changes", 
#         "News 3: Top Mutual Funds"]
# carousel_index = st.selectbox("Scroll through news:", range(len(news)))
# st.write(news[carousel_index])

# ---- FAQ Section ----
# st.markdown("<h2 style='text-align: center;'>🤔 Frequently Asked Questions</h2>", unsafe_allow_html=True)
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

# # ---- Footer Section ----
# st.markdown("<hr>", unsafe_allow_html=True)
# footer_col1, footer_col2 = st.columns(2)

# with footer_col1:
#     st.markdown("<h2>Join the FinFriend club today!</h2>", unsafe_allow_html=True)

# with footer_col2:
#     # st.markdown("<h4>Connect with us:</h4>", unsafe_allow_html=True)
#     st.markdown("") # empty line
#     st.markdown("") # empty line
#     st.markdown("Discord | Gmail | Twitter", unsafe_allow_html=True)

# In your dashboard footer section:
from streamlit_modal import Modal
from user_pages.contact import show_contact_form
from user_pages.disclaimer import show_disclaimer

st.markdown("<hr>", unsafe_allow_html=True)
footer_col1, footer_col2 = st.columns(2)

with footer_col1:
    st.markdown("<h2>Join the FinFriend club today!</h2>", unsafe_allow_html=True)

with footer_col2:
    st.markdown("") # empty line
    st.markdown("") # empty line

    sac.segmented(
        items=[
            sac.SegmentedItem(label='discord', icon='discord'),
            sac.SegmentedItem(label='mail', icon='google'),
            sac.SegmentedItem(label='github', icon='github'),
            # sac.SegmentedItem(label='link', icon='share-fill', href='https://mantine.dev/core/segmented-control/'),
            # sac.SegmentedItem(label='disabled', disabled=True),
        ], align='right'
    )

    # sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='discord', size=20))], align='center', variant='text', index=None)
    # sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='facebook', size=20))], align='center', variant='text', index=None)
    # sac.buttons([sac.ButtonsItem(icon=sac.BsIcon(name='youtube', size=20))], align='center', variant='text', index=None)
    # st.markdown("Discord | Gmail | Twitter", unsafe_allow_html=True)
    
    # Contact Us button that opens the modal
    # col1, col2, col3 = st.columns([1,1,1])
    # with col2:
    #     if st.button("Contact Us", key="contact_button"):
    #         st.session_state.open_modal = True

footer_col3, footer_col4 = st.columns(2)
with footer_col3:
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        if st.button("Contact Us", key="contact_button"):
            st.session_state.open_modal = True
    
    with col2:
        if st.button("Disclaimer", key="disclaimer_button"):
            st.session_state.open_disclaimer_modal = True
            # st.session_state.open_modal = True

contact_modal = Modal(
    title="📨 Contact Us",
    key="contact_modal",
    # Optional - makes modal wider
    max_width=800,
    padding=50  
    
)

disclaimer_modal = Modal(
    title="⚠️ Disclaimer",
    key="disclaimer_modal",
    max_width=800,
    padding=50
)

# Modal handling
if st.session_state.get("open_modal", False):
    # contact_modal.open()
    with contact_modal.container():
        show_contact_form()
        
        # Close button - only show if form hasn't been successfully submitted
        if not st.session_state.get("form_submitted", False):
            if st.button("Close", key="modal_close_button"):
                st.session_state.open_modal = False
                st.rerun()
        else:
            # Auto-close after successful submission
            st.session_state.open_modal = False
            st.session_state.form_submitted = False
            st.rerun()

# Render Disclaimer Modal
if st.session_state.get("open_disclaimer_modal", False):
    # disclaimer_modal.open()
    with disclaimer_modal.container():
        show_disclaimer()
