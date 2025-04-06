import streamlit as st
import auth_functions
from auth_functions import *
from datetime import datetime
from firebase_admin import credentials, firestore

# Custom CSS for styling
st.markdown("""
<style>
    .profile-header h1 {
        color: #556b3b;
        font-size: 60px;
    }
    .profile-card {
        background-color: rgba(165, 199, 127, 0.4);
        border-radius: 10px;
        border: 0.7px solid #76b5c5;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #f5f3eb;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid rgba(131, 158, 101, 0.8);
    }
    .risk-high {
        color: #E74C3C;
        font-weight: bold;
    }
    .risk-medium {
        color: #F39C12;
        font-weight: bold;
    }
    .risk-low {
        color: #27AE60;
        font-weight: bold;
    }
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

def get_user_profile(user_id):
    db = firestore.client()
    doc_ref = db.collection("UserData").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        default_profile = {
            "Name": "New User",
            "Age": 18,
            "Income": 0,
            "Investing Experience": 0,
            "Savings": 0,
            "Investment Preferences": "Conservative",
            "Financial Goal": "",
            "Risk Tolerance": "Medium",
            "Investment Types": [],
        }
        doc_ref.set(default_profile)
        return default_profile
    
def update_user_profile(user_id, profile_data):
    """Update the user's profile information in Firestore."""
    if db is None:
        st.error("Database not initialized.")
        return
    try:
        doc_ref = db.collection("UserData").document(user_id)
        doc_ref.update(profile_data)
        st.success("Profile updated successfully!")
    except Exception as e:
        st.error(f"Error updating profile: {e}")

def calculate_risk_profile(income, investing_experience, savings, investment_pref):
    savings_ratio = savings / income if income > 0 else 0
    risk_score = (investing_experience * 2) + (savings_ratio * 5)

    if investment_pref == "Aggressive":
        risk_score += 5
    elif investment_pref == "Moderate":
        risk_score += 2

    if risk_score > 12:
        return "High Risk"
    elif risk_score > 6:
        return "Medium Risk"
    else:
        return "Low Risk"



# Main Profile Page

# st.title("👤 Your Profile")
# st.write("Manage your personal and financial information")
st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">👤 Your Profile</h1>
    <p style="text-align:center;">Manage your personal and financial information</p>
</div>
""", unsafe_allow_html=True)
st.markdown("")
st.markdown("")

if "user_info" in st.session_state:
    user_id = st.session_state.user_id
    user_profile = get_user_profile(user_id)

    if user_profile:
        # Display Profile Information
        st.markdown("### 📋 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Name</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(user_profile.get("Name", "N/A")), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Age</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(user_profile.get("Age", "N/A")), unsafe_allow_html=True)

            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Investing Experience</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(user_profile.get("Investing Experience", 0)), unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Income</div>
                <div class="metric-value">${:,.2f}</div>
            </div>
            """.format(user_profile.get("Income", 0)), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Savings</div>
                <div class="metric-value">${:,.2f}</div>
            </div>
            """.format(user_profile.get("Savings", 0)), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Investment Preferences</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(user_profile.get("Investment Preferences", "N/A")), unsafe_allow_html=True)
        
        # Risk Profile Section
        risk_category = calculate_risk_profile(
            user_profile["Income"], user_profile["Investing Experience"],
            user_profile["Savings"], user_profile["Investment Preferences"]
        )
        
        risk_class = "risk-high" if risk_category == "High Risk" else \
                    "risk-medium" if risk_category == "Medium Risk" else "risk-low"
        
        st.markdown(f"""
        <div class="profile-card">
            <h3>📊 Your Risk Profile</h3>
            <p>Based on your financial information, your risk tolerance is:</p>
            <div style="font-size: 1.5rem; margin: 1rem 0;" class="{risk_class}">
                {risk_category}
            </div>
        """, unsafe_allow_html=True)
        
        if risk_category == "Low Risk":
            st.info("💡 You prefer safety. Consider diversified mutual funds and bonds.")
        elif risk_category == "Medium Risk":
            st.info("📈 You have a balanced approach. ETFs, blue-chip stocks, and REITs are good options.")
        else:
            st.warning("⚠️ High risk! Look into growth stocks, crypto, or real estate carefully.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("")
        # Edit Profile Section
        st.markdown("### ✏️ Update Profile")
        with st.expander("Edit Profile Information", expanded=False):
            with st.form("profile_form"):
                name = st.text_input("Name", user_profile.get("Name", ""))
                age = st.number_input("Age", value=user_profile.get("Age", 18), step=1)
                income = st.number_input("Income", value=user_profile.get("Income", 0), step=100)
                investing_experience = st.number_input("Investing Experience (Years)", 
                                                     value=user_profile.get("Investing Experience", 0), step=1)
                savings = st.number_input("Savings", value=user_profile.get("Savings", 0), step=100)
                investment_pref = st.selectbox("Investment Preferences", 
                                             ["Conservative", "Moderate", "Aggressive"], 
                                             index=["Conservative", "Moderate", "Aggressive"].index(
                                                 user_profile.get("Investment Preferences", "Conservative")))
                financial_goal = st.text_input("Your Financial Goal (e.g., Save $10,000)")
                risk_tolerance = st.selectbox("Your Risk Tolerance", ["Low", "Medium", "High"])
                investment_types = st.multiselect("Your Investment Preferences", 
                                                     ["Stocks", "Bonds", "Real Estate", "Cryptocurrency"])

                cols = st.columns([1.5,1,10])
                with cols[0]:
                    submitted = st.form_submit_button("Save Changes")
                with cols[1]:
                    if st.form_submit_button("Cancel"):
                        pass

                if submitted:
                    updated_profile = {
                        "Name": name,
                        "Age": age,
                        "Income": income,
                        "Investing Experience": investing_experience,
                        "Savings": savings,
                        "Investment Preferences": investment_pref,
                        "Financial Goal": financial_goal,
                        "Risk Tolerance": risk_tolerance,
                        "Investment Types": investment_types
                        }
                    update_user_profile(user_id, updated_profile)
                    st.rerun()
        
        st.markdown("")
        st.markdown("")
        # Delete Account Section
        st.markdown("### ❌ Account Actions")
        with st.expander("Delete Account", expanded=False):
            st.warning("This action cannot be undone. All your data will be permanently deleted.")
            password = st.text_input(label='Confirm your password',type='password')
            st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')
    else:
        st.error("User profile not found. Please sign in.")
else:
    st.warning("You need to log in first.")