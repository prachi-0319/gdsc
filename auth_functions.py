# import json
# import requests
# import streamlit as st

# ## -------------------------------------------------------------------------------------------------
# ## Firebase Auth API -------------------------------------------------------------------------------
# ## -------------------------------------------------------------------------------------------------

# def sign_in_with_email_and_password(email, password):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8"}
#     data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def get_account_info(id_token):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8"}
#     data = json.dumps({"idToken": id_token})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def send_email_verification(id_token):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8"}
#     data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def send_password_reset_email(email):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8"}
#     data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def create_user_with_email_and_password(email, password):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8" }
#     data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def delete_user_account(id_token):
#     request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
#     headers = {"content-type": "application/json; charset=UTF-8"}
#     data = json.dumps({"idToken": id_token})
#     request_object = requests.post(request_ref, headers=headers, data=data)
#     raise_detailed_error(request_object)
#     return request_object.json()

# def raise_detailed_error(request_object):
#     try:
#         request_object.raise_for_status()
#     except requests.exceptions.HTTPError as error:
#         raise requests.exceptions.HTTPError(error, request_object.text)

# ## -------------------------------------------------------------------------------------------------
# ## Authentication functions ------------------------------------------------------------------------
# ## -------------------------------------------------------------------------------------------------

# # def sign_in(email:str, password:str) -> None:
# #     try:
# #         # Attempt to sign in with email and password
# #         id_token = sign_in_with_email_and_password(email,password)['idToken']

# #         # Get account information
# #         user_info = get_account_info(id_token)["users"][0]

# #         # If email is not verified, send verification email and do not sign in
# #         if not user_info["emailVerified"]:
# #             send_email_verification(id_token)
# #             st.session_state.auth_warning = 'Check your email to verify your account'

# #         # Save user info to session state and rerun
# #         else:
# #             st.session_state.user_info = user_info
# #             st.experimental_rerun()

# #     except requests.exceptions.HTTPError as error:
# #         error_message = json.loads(error.args[1])['error']['message']
# #         if error_message in {"INVALID_EMAIL","EMAIL_NOT_FOUND","INVALID_PASSWORD","MISSING_PASSWORD"}:
# #             st.session_state.auth_warning = 'Error: Use a valid email and password'
# #         else:
# #             st.session_state.auth_warning = 'Error: Please try again later'

# #     except Exception as error:
# #         print(error)
# #         st.session_state.auth_warning = 'Error: Please try again later'


# def sign_in(email:str, password:str) -> None:
#     try:
#         # Attempt to sign in with email and password
#         response = sign_in_with_email_and_password(email,password)['idToken']
#         id_token = response['idToken']
#         # Get account information
#         user_info = get_account_info(id_token)["users"][0]

#         # If email is not verified, send verification email and do not sign in
#         if not user_info["emailVerified"]:
#             send_email_verification(id_token)
#             st.session_state.auth_warning = 'Check your email to verify your account'

#         # Save user info to session state and rerun
#         else:
#             st.session_state.user_info = user_info
#             st.experimental_rerun()

#     except requests.exceptions.HTTPError as error:
#         error_message = json.loads(error.args[1])['error']['message']
#         if error_message in {"INVALID_EMAIL","EMAIL_NOT_FOUND","INVALID_PASSWORD","MISSING_PASSWORD"}:
#             st.session_state.auth_warning = 'Error: Use a valid email and password'
#         else:
#             st.session_state.auth_warning = 'Error: Please try again later'

#     except Exception as error:
#         print(error)
#         st.session_state.auth_warning = 'Error: Please try again later'

# def create_account(email:str, password:str) -> None:
#     try:
#         # Create account (and save id_token)
#         id_token = create_user_with_email_and_password(email,password)['idToken']

#         # Create account and send email verification
#         send_email_verification(id_token)
#         st.session_state.auth_success = 'Check your inbox to verify your email'
    
#     except requests.exceptions.HTTPError as error:
#         error_message = json.loads(error.args[1])['error']['message']
#         if error_message == "EMAIL_EXISTS":
#             st.session_state.auth_warning = 'Error: Email belongs to existing account'
#         elif error_message in {"INVALID_EMAIL","INVALID_PASSWORD","MISSING_PASSWORD","MISSING_EMAIL","WEAK_PASSWORD"}:
#             st.session_state.auth_warning = 'Error: Use a valid email and password'
#         else:
#             st.session_state.auth_warning = 'Error: Please try again later'
    
#     except Exception as error:
#         print(error)
#         st.session_state.auth_warning = 'Error: Please try again later'


# def reset_password(email:str) -> None:
#     try:
#         send_password_reset_email(email)
#         st.session_state.auth_success = 'Password reset link sent to your email'
    
#     except requests.exceptions.HTTPError as error:
#         error_message = json.loads(error.args[1])['error']['message']
#         if error_message in {"MISSING_EMAIL","INVALID_EMAIL","EMAIL_NOT_FOUND"}:
#             st.session_state.auth_warning = 'Error: Use a valid email'
#         else:
#             st.session_state.auth_warning = 'Error: Please try again later'    
    
#     except Exception:
#         st.session_state.auth_warning = 'Error: Please try again later'


# def sign_out() -> None:
#     st.session_state.clear()
#     st.session_state.auth_success = 'You have successfully signed out'
#     # st.rerun()


# def delete_account(password:str) -> None:
#     try:
#         # Confirm email and password by signing in (and save id_token)
#         id_token = sign_in_with_email_and_password(st.session_state.user_info['email'],password)['idToken']
        
#         # Attempt to delete account
#         delete_user_account(id_token)
#         st.session_state.clear()
#         st.session_state.auth_success = 'You have successfully deleted your account'

#     except requests.exceptions.HTTPError as error:
#         error_message = json.loads(error.args[1])['error']['message']
#         print(error_message)

#     except Exception as error:
#         print(error)

# def check_user_logged_in():
#     """ Check if the user is logged in """
#     return 'user_info' in st.session_state and st.session_state.user_info


from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
import json
import requests
import streamlit as st
# import streamlit_cookie_manager as cookie_manager


## -------------------------------------------------------------------------------------------------
## Firebase and authentication -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

# Global variable for Firestore client
db = None

def initialize_firebase():
    """Initialize Firebase only once if not already done"""
    global db
    if not firebase_admin._apps:
        cred = credentials.Certificate('firebase-key.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    elif db is None:
        db = firestore.client()

def initialize_firebase_once():
    """Initialize Firebase once per session"""
    if 'firebase_initialized' not in st.session_state or not st.session_state.firebase_initialized:
        initialize_firebase()
        st.session_state.firebase_initialized = True

## -------------------------------------------------------------------------------------------------
## Firebase Auth API DO NOT CHANGE-------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in_with_email_and_password(email, password):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def get_account_info(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_email_verification(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_password_reset_email(email):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def create_user_with_email_and_password(email, password):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8" }
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def delete_user_account(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(st.secrets['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise requests.exceptions.HTTPError(error, request_object.text)

## -------------------------------------------------------------------------------------------------
## Authentication functions DO NOT CHANGE------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in(email:str, password:str) -> None:
    try:
        id_token = sign_in_with_email_and_password(email,password)['idToken']  # Attempt to sign in with email and password
        user_info = get_account_info(id_token)["users"][0] # Get account information
        user_id = user_info["localId"] #  Get user_id from user info

        # cookie_manager.set("user_id", user_id)

        # Set user_id in session state to check login status on app load
        st.session_state.user_id = user_id
        st.session_state.user_info = user_info # Store user_id and user_info in session_state after login

        if not user_info["emailVerified"]:  # If email is not verified, send verification email and do not sign in
            send_email_verification(id_token)
            # st.session_state.auth_warning = 'Check your email to verify your account'
            st.error('Check your email to verify your account') # Save user info to session state and rerun
        else:
            st.session_state.user_info = user_info #  Store user info in session state
            update_user_login_status(user_info["localId"]) # Update current_login to True in Firestore
            st.success('Logged in successfully!') # Success message
            # st.experimental_rerun()  # Rerun to load the next page (dashboard)
            st.rerun()
            # st.session_state.user_info = user_info
            # st.experimental_rerun()

    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message in {"INVALID_EMAIL","EMAIL_NOT_FOUND","INVALID_PASSWORD","MISSING_PASSWORD"}:
            st.session_state.auth_warning = 'Error: Use a valid email and password'
        else:
            st.session_state.auth_warning = 'Error: Please try again later'

    except Exception as error:
        print(error)
        st.session_state.auth_warning = 'Error: Please try again later'

def update_user_login_status(user_id: str) -> None:
    # Get the Firestore reference for the user
    user_ref = firestore.client().collection('UserProfiles').document(user_id)

    # Update the 'current_login' status
    user_ref.update({
        'current_login': True,  # Set True if logged in, False if logged out
        # 'last_login': firestore.SERVER_TIMESTAMP  # Optionally track the login time
    })

# This function will check Firestore directly to verify the login state
def check_login_status():
    # Check if there is a logged-in user by querying Firestore
    # Assuming you have a way to get the user_id (either stored or from cookies/sessions)
    user_id = st.session_state.get('user_id', None)
    if user_id:
        user_ref = firestore.client().collection('UserProfiles').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            # Check the 'current_login' field to see if the user is logged in
            if user_data.get('current_login', True):
                return True  # User is logged in
            else:
                return False  # User is not logged in
        else:
            return False  # User doesn't exist in the database
    return False  # No user id in session state, treat as logged out

def create_account(email: str, password: str) -> bool:
    try:
        # Create account (and save id_token)
        response = create_user_with_email_and_password(email, password)
        id_token = response['idToken']
        user_id = response['localId']  # Get the user ID (uid)
        create_user_profile_in_firestore(user_id, email) #send verification
        send_email_verification(id_token)
        return True
    
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message == "EMAIL_EXISTS":
            st.session_state.auth_warning = 'Error: Email belongs to existing account'
        elif error_message in {"INVALID_EMAIL","INVALID_PASSWORD","MISSING_PASSWORD","MISSING_EMAIL","WEAK_PASSWORD"}:
            st.session_state.auth_warning = 'Error: Use a valid email and password'
        else:
            st.session_state.auth_warning = 'Error: Please try again later'
    
    except Exception as error:
        print(error)
        st.session_state.auth_warning = 'Error: Please try again later'

def create_user_profile_in_firestore(user_id, email):
    # Create a new document for the user in Firestore
    user_ref = db.collection('UserProfiles').document(user_id)

    # Initialize user profile with basic info
    user_ref.set({
        'email': email,
        'first_login': True,  # New user, needs to set up their profile
        'current_login': False,
        'createdAt': firestore.SERVER_TIMESTAMP
    })

def reset_password(email:str) -> None:
    try:
        send_password_reset_email(email)
        st.session_state.auth_success = 'Password reset link sent to your email'
    
    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        if error_message in {"MISSING_EMAIL","INVALID_EMAIL","EMAIL_NOT_FOUND"}:
            st.session_state.auth_warning = 'Error: Use a valid email'
        else:
            st.session_state.auth_warning = 'Error: Please try again later'    
    
    except Exception:
        st.session_state.auth_warning = 'Error: Please try again later'

# def sign_out() -> None:
#     st.session_state.clear()
#     st.session_state.auth_success = 'You have successfully signed out'

# Changing the sign out so that we change it in the db


def sign_out() -> None:
    # Get user_id from session state (assuming user_id is stored there after login)
    user_id = st.session_state.get('user_id', None)
    
    if user_id:
        # Update Firestore to set 'current_login' to False for the logged-out user
        user_ref = firestore.client().collection('UserProfiles').document(user_id)
        user_ref.update({
            'current_login': False  # Set current_login to False when the user logs out
        })
        # Clear the session state (you can comment this out if you don't want to clear the session)
        st.session_state.clear()

        # Provide feedback to the user
        st.session_state.auth_success = 'You have successfully signed out'
        st.success('You have successfully signed out')

        # Optionally, redirect to a login page or home page after sign-out
        st.experimental_rerun()  # Refresh the app to load the login page again

    else:
        st.error("No user is currently logged in.")

def delete_account(password:str) -> None:
    try:
        # Confirm email and password by signing in (and save id_token)
        id_token = sign_in_with_email_and_password(st.session_state.user_info['email'],password)['idToken']
        
        # Attempt to delete account
        delete_user_account(id_token)
        st.session_state.clear()
        st.session_state.auth_success = 'You have successfully deleted your account'

    except requests.exceptions.HTTPError as error:
        error_message = json.loads(error.args[1])['error']['message']
        print(error_message)

    except Exception as error:
        print(error)


