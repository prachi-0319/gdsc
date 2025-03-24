import streamlit as st
import auth_functions
from auth_functions import *

def get_user_profile(user_id):
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
            "Investment Preferences": "Conservative"
        }
        doc_ref.set(default_profile)
        return default_profile
    
# Function to update user profile in Firestore
def update_user_profile(user_id, profile_data):
    """Update the user's profile information in Firestore."""
    if db is None:
        st.error("Database not initialized.")
        return
    try:
        doc_ref = db.collection("UserData").document(user_id)
        doc_ref.update(profile_data)  # 🔹 Ensure this updates the correct fields
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



st.title("User Profile & Risk Analysis")

if "user_info" in st.session_state:
    user_id = st.session_state.user_id
    user_profile = get_user_profile(user_id)

    if user_profile:
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False
        
        # Display Profile
        st.write("### Profile Details")
        st.write(f"**Name:** {user_profile.get('Name', 'N/A')}")
        st.write(f"**Age:** {user_profile.get('Age', 'N/A')}")
        st.write(f"**Income:** ${user_profile.get('Income', 0):,.2f}")
        st.write(f"**Investing Experience:** {user_profile.get('Investing Experience', 0)} years")
        st.write(f"**Savings:** ${user_profile.get('Savings', 0):,.2f}")
        st.write(f"**Investment Preferences:** {user_profile.get('Investment Preferences', 'N/A')}")

        # Calculate and Show Risk Profile
        risk_category = calculate_risk_profile(
            user_profile["Income"], user_profile["Investing Experience"],
            user_profile["Savings"], user_profile["Investment Preferences"]
        )
        st.subheader(f"📊 Risk Category: **{risk_category}**")

        # Financial Advice
        if risk_category == "Low Risk":
            st.info("💡 You prefer safety. Consider diversified mutual funds and bonds.")
        elif risk_category == "Medium Risk":
            st.info("📈 You have a balanced approach. ETFs, blue-chip stocks, and REITs are good options.")
        else:
            st.warning("⚠️ High risk! Look into growth stocks, crypto, or real estate carefully.")

        # Edit Profile Button
        if not st.session_state.edit_mode:
            if st.button("Edit Profile"):
                st.session_state.edit_mode = True
                st.rerun()
        else:
            with st.form("profile_form"):
                name = st.text_input("Name", user_profile.get("Name", ""))
                age = st.number_input("Age", value=user_profile.get("Age", 18), step=1)
                income = st.number_input("Income", value=user_profile.get("Income", 0), step=100)
                investing_experience = st.number_input("Investing Experience (Years)", value=user_profile.get("Investing Experience", 0), step=1)
                savings = st.number_input("Savings", value=user_profile.get("Savings", 0), step=100)
                investment_pref = st.selectbox("Investment Preferences", ["Conservative", "Moderate", "Aggressive"], 
                                            index=["Conservative", "Moderate", "Aggressive"].index(user_profile.get("Investment Preferences", "Conservative")))

                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Save Changes")
                with col2:
                    cancel = st.form_submit_button("Cancel")

                if submitted:
                    updated_profile = {
                        "Name": name,
                        "Age": age,
                        "Income": income,
                        "Investing Experience": investing_experience,
                        "Savings": savings,
                        "Investment Preferences": investment_pref
                    }
                    update_user_profile(user_id, updated_profile)
                    st.session_state.edit_mode = False
                    st.rerun()

                if cancel:
                    st.session_state.edit_mode = False
                    st.rerun()
    else:
        st.error("User profile not found. Please sign in.")
else:
    st.warning("You need to log in first.")

