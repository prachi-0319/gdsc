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
    .profile-header h1 {
            color: #556b3b;
            font-size: 60px;
        }
    .savings-card {
        background: rgba(131, 158, 101, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .amount-display {
        font-size: 3rem;
        text-align: center;
        color: rgba(131, 158, 101, 0.8);
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
<div class="profile-header">
    <h1 style="text-align:center;">💰 Smart Savings Tracker</h1>
    <p style="text-align:center;">Reach your financial goals one rupee at a time</p>
</div>
""", unsafe_allow_html=True)

# st.markdown("""
# <div class="header">
#     <h1>💰 Smart Savings Tracker</h1>
#     <p>Reach your financial goals one rupee at a time</p>
# </div>
# """, unsafe_allow_html=True)

# CENTERED SAVINGS DISPLAY (3-column layout)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("")
    st.markdown("")
    # st.markdown("""
    # <div class="savings-card">
    #     <div style="text-align: center; margin-bottom: 1rem;">
    #         <h3>Your Savings Progress</h3>
    #     </div>
    # """, unsafe_allow_html=True)
    
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

st.markdown("")
st.markdown("")

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


st.markdown("")
st.markdown("")
# Recent Transactions
if st.session_state.transactions:
    st.markdown("""
    <div>
        <h3>📝 Recent Transactions</h3>
    """, unsafe_allow_html=True)
    # st.markdown("""
    # <div class="savings-card">
    #     <h3>📝 Recent Transactions</h3>
    # """, unsafe_allow_html=True)
    
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