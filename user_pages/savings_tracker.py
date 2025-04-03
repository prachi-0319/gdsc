# import streamlit as st
# import time
# from streamlit_lottie import st_lottie
# import json

# # Load Lottie animations (you can replace these with your own)
# def load_lottie(filepath):
#     with open(filepath, "r") as f:
#         return json.load(f)

# # Initialize session state
# if 'total_saved' not in st.session_state:
#     st.session_state.total_saved = 0
# if 'transactions' not in st.session_state:
#     st.session_state.transactions = []

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .savings-header {
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .savings-header h1 {
#         color: #27AE60;
#         font-size: 2.5rem;
#     }
#     .piggy-container {
#         display: flex;
#         justify-content: center;
#         margin: 2rem 0;
#         height: 250px;
#     }
#     .amount-display {
#         font-size: 3rem;
#         text-align: center;
#         color: #27AE60;
#         margin: 1rem 0;
#         font-weight: bold;
#     }
#     .progress-container {
#         margin: 2rem 0;
#         position: relative;
#     }
#     .milestone-flag {
#         position: absolute;
#         bottom: 20px;
#         transform: translateX(-50%);
#         text-align: center;
#         font-size: 0.8rem;
#     }
#     .coin-animation {
#         position: absolute;
#         animation: fall 1.5s ease-in;
#     }
#     @keyframes fall {
#         0% { transform: translateY(-100px); opacity: 1; }
#         100% { transform: translateY(100px); opacity: 0; }
#     }
# </style>
# """, unsafe_allow_html=True)

# # Page Header
# st.markdown("""
# <div class="savings-header">
#     <h1>💰 Savings Tracker</h1>
#     <p>Watch your savings grow with every deposit!</p>
# </div>
# """, unsafe_allow_html=True)

# # Piggy Bank Animation Container
# with st.empty():
#     st.markdown("""
#     <div class="piggy-container">
#         <div id="animation-container"></div>
#     </div>
#     """, unsafe_allow_html=True)

#     # This would be replaced with your actual Lottie animation
#     # st_lottie(load_lottie("piggy_bank.json"), height=250, key="piggy")

# # Current Savings Display
# st.markdown(f"""
# <div class="amount-display">
#     ₹{st.session_state.total_saved:,.2f}
# </div>
# """, unsafe_allow_html=True)

# # Input Form
# with st.form("savings_form"):
#     amount = st.number_input("Amount to add:", min_value=1, step=100)
#     submit_button = st.form_submit_button("Add to Savings")

# # Handle form submission
# if submit_button and amount:
#     # Animate coin falling
#     st.markdown(f"""
#     <div class="coin-animation" style="left: 50%;">
#         +₹{amount:,.2f}
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Update total
#     st.session_state.total_saved += amount
#     st.session_state.transactions.append(amount)
    
#     # Rerun to show animation
#     st.rerun()

# # Progress Bar with Milestones
# milestones = [500, 1000, 1500, 2000, 2500, 3000]
# current_progress = min(st.session_state.total_saved / max(milestones) * 100, 100)

# st.markdown("""
# <div class="progress-container">
#     <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
#         <span>₹0</span>
#         <span>₹{max_milestone:,.0f}</span>
#     </div>
# """.format(max_milestone=max(milestones)), unsafe_allow_html=True)

# st.progress(int(current_progress))

# # Add milestone flags
# milestone_html = ""
# for milestone in milestones:
#     position = milestone / max(milestones) * 100
#     milestone_html += f"""
#     <div class="milestone-flag" style="left: {position}%;">
#         <div>₹{milestone:,.0f}</div>
#         <div style="font-size: 1.5rem;">{'🏁' if st.session_state.total_saved >= milestone else '🚩'}</div>
#     </div>
#     """

# st.markdown(milestone_html, unsafe_allow_html=True)
# st.markdown("</div>", unsafe_allow_html=True)

# # Transaction History
# if st.session_state.transactions:
#     st.subheader("Recent Transactions")
#     for i, transaction in enumerate(st.session_state.transactions[-5:][::-1], 1):
#         st.write(f"{i}. +₹{transaction:,.2f}")

# # Reset Button
# if st.button("Start Over", type="secondary"):
#     st.session_state.total_saved = 0
#     st.session_state.transactions = []
#     st.rerun()



# import streamlit as st
# import json
# import time
# from streamlit_lottie import st_lottie
# import requests

# # Initialize session state
# if 'total_saved' not in st.session_state:
#     st.session_state.total_saved = 0
# if 'transactions' not in st.session_state:
#     st.session_state.transactions = []
# if 'savings_goal' not in st.session_state:
#     st.session_state.savings_goal = 3000  # Default goal

# # Sample Lottie animation URLs (replace with your own URLs or local files)
# PIGGY_BANK_URL = "https://lottie.host/82fa6b35-399b-4782-8730-f839816f125f/7dqS8Nk6PX.json"
# # COIN_URL = "https://assets1.lottiefiles.com/packages/lf20_pmvvft8n.json"

# @st.cache_data
# def load_lottie_url(url):
#     """Load Lottie animation from URL"""
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Load animations
# piggy_animation = load_lottie_url(PIGGY_BANK_URL)
# # coin_animation = load_lottie_url(COIN_URL)

# # Custom CSS
# st.markdown("""
# <style>
#     .piggy-container {
#         display: flex;
#         justify-content: center;
#         margin: 2rem 0;
#         height: 250px;
#         position: relative;
#     }
#     .amount-display {
#         font-size: 3rem;
#         text-align: center;
#         color: #27AE60;
#         margin: 1rem 0;
#         font-weight: bold;
#     }
#     .goal-display {
#         font-size: 1.2rem;
#         text-align: center;
#         color: #555;
#         margin-bottom: 1rem;
#     }
#     .progress-container {
#         margin: 2rem 0;
#         position: relative;
#     }
#     .milestone-flag {
#         position: absolute;
#         bottom: 20px;
#         transform: translateX(-50%);
#         text-align: center;
#         font-size: 0.8rem;
#     }
#     .goal-form {
#         background-color: #f0f8f0;
#         padding: 1.5rem;
#         border-radius: 10px;
#         margin-bottom: 2rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Page Header
# st.markdown("""
# <div class="savings-header">
#     <h1>💰 Smart Savings Tracker</h1>
#     <p>Set a goal and watch your savings grow!</p>
# </div>
# """, unsafe_allow_html=True)

# # Goal Setting Section

# col1, col2 = st.columns([1, 1])

# with col1:
        
#     with st.expander("🎯 Set Your Savings Goal", expanded=True if st.session_state.savings_goal == 3000 else False):
#         with st.form("goal_form"):
#             new_goal = st.number_input(
#                 "Enter your savings goal amount:",
#                 min_value=100,
#                 value=st.session_state.savings_goal,
#                 step=100
#             )

#             if st.form_submit_button("Set Goal"):
#                 st.session_state.savings_goal = new_goal
#                 st.success(f"Goal set to ₹{new_goal:,.2f}!")
#                 st.rerun()

#     # Display current goal
#     st.markdown(f"""
#     <div class="goal-display">
#         Target: ₹{st.session_state.savings_goal:,.2f} 
#         | Progress: {min(100, st.session_state.total_saved/st.session_state.savings_goal*100):.1f}%
#     </div>
#     """, unsafe_allow_html=True)


# with col2:
#     # Piggy Bank Animation
#     if piggy_animation:
#         st_lottie(
#             piggy_animation,
#             height=250,
#             key="piggy",
#             speed=1,
#             loop=True
#         )
#     else:
#         st.warning("Couldn't load piggy bank animation")

#     # Current Savings Display
#     st.markdown(f"""
#     <div class="amount-display">
#         ₹{st.session_state.total_saved:,.2f}
#     </div>
#     """, unsafe_allow_html=True)

#     # Input Form
#     with st.form("savings_form"):
#         amount = st.number_input("Amount to add:", min_value=1, step=100)
#         submit_button = st.form_submit_button("💰 Add to Savings")

#     # Handle form submission
#     if submit_button and amount:
#         # Show coin animation
#         if coin_animation:
#             with st.empty():
#                 st_lottie(
#                     coin_animation,
#                     height=100,
#                     key=f"coin_{time.time()}",
#                     speed=1,
#                     loop=False
#                 )
        
#         # Update total
#         st.session_state.total_saved += amount
#         st.session_state.transactions.append(amount)
        
#         # Rerun to show animation
#         st.rerun()

#     # Progress Bar with Dynamic Milestones
#     milestone_step = max(500, st.session_state.savings_goal // 6)  # About 6 milestones
#     milestones = list(range(milestone_step, st.session_state.savings_goal + milestone_step, milestone_step))
#     current_progress = min(st.session_state.total_saved / st.session_state.savings_goal * 100, 100)

#     st.markdown(f"""
#     <div class="progress-container">
#         <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
#             <span>₹0</span>
#             <span>₹{st.session_state.savings_goal:,.0f}</span>
#         </div>
#     """, unsafe_allow_html=True)

#     st.progress(int(current_progress))

#     # Add milestone flags
#     milestone_html = ""
#     for milestone in milestones:
#         if milestone > st.session_state.savings_goal:
#             continue
#         position = milestone / st.session_state.savings_goal * 100
#         achieved = st.session_state.total_saved >= milestone
#         milestone_html += f"""
#         <div class="milestone-flag" style="left: {position}%;">
#             <div>₹{milestone:,.0f}</div>
#             <div style="font-size: 1.5rem;">{'🏆' if achieved else '🎯'}</div>
#         </div>
#         """

#     st.markdown(milestone_html, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # Transaction History
#     if st.session_state.transactions:
#         st.subheader("📝 Recent Transactions")
#         for i, transaction in enumerate(st.session_state.transactions[-5:][::-1], 1):
#             st.write(f"{i}. +₹{transaction:,.2f}")

#     # Reset Button
#     if st.button("🔄 Start Over", type="secondary"):
#         st.session_state.total_saved = 0
#         st.session_state.transactions = []
#         st.rerun()


import streamlit as st
import requests
from streamlit_lottie import st_lottie

# Initialize session state
if 'total_saved' not in st.session_state:
    st.session_state.total_saved = 0
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'savings_goal' not in st.session_state:
    st.session_state.savings_goal = 3000

# Lottie animation
PIGGY_BANK_URL = "https://lottie.host/82fa6b35-399b-4782-8730-f839816f125f/7dqS8Nk6PX.json"

@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

piggy_animation = load_lottie_url(PIGGY_BANK_URL)

# Custom CSS
st.markdown("""
<style>
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .header h1 {
        color: #27AE60;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .savings-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .amount-display {
        font-size: 3rem;
        text-align: center;
        color: #27AE60;
        margin: 1rem 0;
        font-weight: bold;
    }
    .progress-container {
        margin: 1.5rem 0;
        position: relative;
    }
    .milestone-flag {
        position: absolute;
        bottom: 20px;
        transform: translateX(-50%);
        text-align: center;
        font-size: 0.8rem;
    }
    .transaction-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .form-input {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>💰 Smart Savings Tracker</h1>
    <p>Reach your financial goals one rupee at a time</p>
</div>
""", unsafe_allow_html=True)

# CENTERED SAVINGS DISPLAY (3-column layout)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="savings-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3>Your Savings Progress</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Piggy Bank Animation
    if piggy_animation:
        st_lottie(piggy_animation, height=180, key="piggy", speed=1, loop=True)
    
    # Current Savings Display
    st.markdown(f"""
    <div class="amount-display">
        ₹{st.session_state.total_saved:,.2f}
    </div>
    <div style="text-align: center; color: #666; margin-bottom: 1rem;">
        of ₹{st.session_state.savings_goal:,.2f} goal
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar
    progress = min(st.session_state.total_saved / st.session_state.savings_goal * 100, 100)
    st.progress(int(progress))
    
    st.markdown("</div>", unsafe_allow_html=True)

# MAIN CONTENT AREA (2-column layout)
left_col, right_col = st.columns([1, 1])

with left_col:
    # Goal Setting
    with st.expander("🎯 Set Savings Goal", expanded=True):
        with st.form("goal_form"):
            new_goal = st.number_input(
                "Target amount:",
                min_value=100,
                value=st.session_state.savings_goal,
                step=100
            )
            if st.form_submit_button("Update Goal"):
                st.session_state.savings_goal = new_goal
                st.success(f"New goal set: ₹{new_goal:,.2f}")
                st.rerun()
    
    # Add Savings Form
    with st.form("savings_form"):
        st.markdown("### 💸 Add Savings")
        amount = st.number_input("Amount:", min_value=1, step=100)
        if st.form_submit_button("Add to Savings"):
            if amount:
                st.session_state.total_saved += amount
                st.session_state.transactions.append(amount)
                st.rerun()

with right_col:
    # Milestones
    st.markdown("""
    <div class="savings-card">
        <h3>🏆 Milestones</h3>
    """, unsafe_allow_html=True)
    
    milestone_step = max(500, st.session_state.savings_goal // 5)
    milestones = list(range(milestone_step, st.session_state.savings_goal + milestone_step, milestone_step))
    
    for milestone in milestones:
        if milestone > st.session_state.savings_goal:
            continue
        achieved = st.session_state.total_saved >= milestone
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 0.5rem 0;">
            <div style="font-size: 1.5rem; margin-right: 0.5rem;">
                {'✅' if achieved else '⚪'}
            </div>
            <div>
                ₹{milestone:,.0f} {'(Achieved!)' if achieved else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Recent Transactions
if st.session_state.transactions:
    st.markdown("""
    <div class="savings-card">
        <h3>📝 Recent Transactions</h3>
    """, unsafe_allow_html=True)
    
    for i, transaction in enumerate(st.session_state.transactions[-5:][::-1], 1):
        st.markdown(f"""
        <div class="transaction-item">
            {i}. +₹{transaction:,.2f}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Reset Button (centered)
st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
if st.button("🔄 Reset Savings Tracker", type="secondary"):
    st.session_state.total_saved = 0
    st.session_state.transactions = []
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)