# import streamlit as st
# # from google.cloud import firestore
# # import firebase_admin
# # from firebase_admin import credentials, firestore
# # from models import Schema
# import json
# from datetime import datetime


# def initialize_firebase():
#     cred = credentials.Certificate('firebase-key.json')
#     firebase_admin.initialize_app(cred)

# # initialize_firebase()

# # Get Firestore client
# def get_db():
#     db = firestore.client()
#     return db

# def update_user_profile(user_id, input_name, input_age, input_amt):
#     db = get_db()
#     # Store the profile data under the user ID document
#     user_ref = db.collection("UserProfiles").document(user_id)
    
#     # If the user exists, update their profile. If not, create a new one.
#     user_ref.set({
#         "name": input_name,
#         "age": input_age,
#         "amount": input_amt,
#         "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
#     }, merge=True)  # merge=True allows for partial updates


# def main_profile():
#      if 'user_info' not in st.session_state:
#         st.warning('You need to be signed in to view your profile!')
#         return
    
#      user_id = st.session_state.user_info["localId"]  # Using the user's Firebase ID as the document ID
    
#      db = get_db()
#      # with st.expander("Get all messages"):
#      #      ref = db.collection("UserProfiles")
#      #      for doc in ref.stream():
#      #           st.write("the id is: ", doc.id)
#      #           st.write("the contents are: ",doc.to_dict())
     
#      with st.form(key="form"):
#         input_age = st.text_input("Your age (optional)", help="Can be anonymous")
#         input_amt = st.text_area("Your amt")
#         input_name = st.text_area("Your Name")

#         if st.form_submit_button("Submit form", type="primary"):
#             if not input_amt:
#                 st.error("Please provide a message :balloon:")
                        
#             else:
#                 update_user_profile(user_id, input_name, input_age, input_amt)
#                 st.success("Your message was posted!")
#                 st.balloons()

# main()

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# @st.cache_resource
# def get_db():
#       db = firestore.Client.from_service_account_json('firebase-key.json')
#       return db

# def post_message(db, input_age, input_amt, input_name):
#     payload = {
#         Schema.age.value: input_age,
#         Schema.amount.value: input_amt,
#         Schema.name.value: input_name,
#         Schema.date.value: datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
#     }
#     doc_ref = db.collection("messages").document()
#     doc_ref.set(payload)
#     return


import streamlit as st
from datetime import datetime

# Mock session state
# if 'user_info' not in st.session_state:
#     st.session_state.user_info = {"localId": "mock_user_id"}


# Main Profile Page
def main_profile():
    if 'user_info' not in st.session_state:
        st.warning('You need to be signed in to view your profile!')
        return

    user_id = st.session_state.user_info["localId"]  # Using the user's mock ID
    user_data = {
        "name": "John Doe",
        "age": "30",
        "amount": "$5000",
        "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }  # Mock user data

    # Main Page Layout
    st.title("👤 Your Profile")
    st.markdown("---")

    # View Profile Section
    st.header("📋 View Your Profile")
    if user_data:
        # Use columns for name and age
        col1, col2 = st.columns([1, 3])  # Columns for name and age
        with col1:
            st.markdown("### Name")
            st.markdown(f"**{user_data.get('name', 'Not provided')}**")
        with col2:
            st.markdown("### Age")
            st.markdown(f"**{user_data.get('age', 'Not provided')}**")

        st.markdown("### Amount")
        st.markdown(f"**{user_data.get('amount', 'Not provided')}**")

        st.markdown("### Last Updated")
        st.markdown(f"**{user_data.get('date', 'Not available')}**")
    else:
        st.info("No profile data found. Please update your profile.")

    st.markdown("---")

    # Update Profile Section
    st.header("✏️ Update Your Profile")
    with st.form(key="update_profile_form"):
        input_name = st.text_input("Your Name", value=user_data.get("name", "") if user_data else "")
        input_age = st.text_input("Your Age", value=user_data.get("age", "") if user_data else "")
        input_amt = st.text_input("Your Amount", value=user_data.get("amount", "") if user_data else "")

        if st.form_submit_button("Update Profile", type="primary"):
            if not input_name or not input_amt:
                st.error("Please provide your name and amount.")
            else:
                # update_user_profile(user_id, input_name, input_age, input_amt)  # Commented out for mock
                st.success("Your profile has been updated! (mock)")
                st.rerun()

    st.markdown("---")

    # Build Finance Profile Section
    st.header("💰 Build Your Finance Profile")
    with st.form(key="finance_profile_form"):
        financial_goal = st.text_input("Your Financial Goal (e.g., Save $10,000)")
        risk_tolerance = st.selectbox("Your Risk Tolerance", ["Low", "Medium", "High"])
        investment_preference = st.multiselect("Your Investment Preferences", ["Stocks", "Bonds", "Real Estate", "Cryptocurrency"])

        if st.form_submit_button("Save Finance Profile", type="primary"):
            st.success("Your finance profile has been saved! (mock)")

    st.markdown("---")

    # Delete Account Section
    st.header("❌ Delete Your Account")
    if st.button("Delete Account", type="primary"):
        if st.checkbox("Are you sure you want to delete your account? This action cannot be undone."):
            # delete_user_profile(user_id)  # Commented out for mock
            st.session_state.clear()  # Clear session state
            st.success("Account deleted (mock).")
            st.rerun()

# # Run the profile page
# if __name__ == "__main__":
#     main_profile()