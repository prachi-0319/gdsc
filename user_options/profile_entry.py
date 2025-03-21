import streamlit as st
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
# from models import Schema
import json
from datetime import datetime


def initialize_firebase():
    cred = credentials.Certificate('firebase-key.json')
    firebase_admin.initialize_app(cred)

# initialize_firebase()

# Get Firestore client
def get_db():
    db = firestore.client()
    return db

def update_user_profile(user_id, input_name, input_age, input_amt):
    db = get_db()
    # Store the profile data under the user ID document
    user_ref = db.collection("UserProfiles").document(user_id)
    
    # If the user exists, update their profile. If not, create a new one.
    user_ref.set({
        "name": input_name,
        "age": input_age,
        "amount": input_amt,
        "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }, merge=True)  # merge=True allows for partial updates


def main():
     if 'user_info' not in st.session_state:
        st.warning('You need to be signed in to submit your profile!')
        return
    
     user_id = st.session_state.user_info["localId"]  # Using the user's Firebase ID as the document ID
    
     db = get_db()
     # with st.expander("Get all messages"):
     #      ref = db.collection("UserProfiles")
     #      for doc in ref.stream():
     #           st.write("the id is: ", doc.id)
     #           st.write("the contents are: ",doc.to_dict())
     
     with st.form(key="form"):
        input_age = st.text_input("Your age (optional)", help="Can be anonymous")
        input_amt = st.text_area("Your amt")
        input_name = st.text_area("Your Name")

        if st.form_submit_button("Submit form", type="primary"):
            if not input_amt:
                st.error("Please provide a message :balloon:")
                        
            else:
                update_user_profile(user_id, input_name, input_age, input_amt)
                st.success("Your message was posted!")
                st.balloons()



main()











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