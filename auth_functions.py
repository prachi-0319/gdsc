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


import json
import requests
import streamlit as st

## -------------------------------------------------------------------------------------------------
## Firebase Auth API -------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in_with_email_and_password(email, password):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def get_account_info(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_email_verification(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def send_password_reset_email(email):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8"}
    data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def create_user_with_email_and_password(email, password):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
    headers = {"content-type": "application/json; charset=UTF-8" }
    data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
    request_object = requests.post(request_ref, headers=headers, data=data)
    raise_detailed_error(request_object)
    return request_object.json()

def delete_user_account(id_token):
    request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key={0}".format(st.secrets["FIREBASE"]['FIREBASE_WEB_API_KEY'])
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
## Authentication functions ------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------

def sign_in(email:str, password:str) -> None:
    try:
        # Attempt to sign in with email and password
        id_token = sign_in_with_email_and_password(email,password)['idToken']

        # Get account information
        user_info = get_account_info(id_token)["users"][0]

        # If email is not verified, send verification email and do not sign in
        if not user_info["emailVerified"]:
            send_email_verification(id_token)
            st.session_state.auth_warning = 'Check your email to verify your account'

        # Save user info to session state and rerun
        else:
            st.session_state.user_info = user_info
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


def sign_out() -> None:
    st.session_state.clear()
    st.session_state.auth_success = 'You have successfully signed out'


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
import toml

def initialize_firebase():
    """Initialize Firebase only once if not already done"""
    global db
    if not firebase_admin._apps:
        # Load credentials from the TOML file
        toml_config = toml.load(".streamlit/secrets.toml")
        
        # Extract Firebase credentials from the TOML file
        firebase_config = toml_config.get("textkey")  # Assuming the TOML contains "textkey" with the JSON string
        
        if firebase_config:
            # Convert the json string to dictionary
            import json
            firebase_credentials = json.loads(firebase_config)

            # Use the credentials to initialize Firebase
            cred = credentials.Certificate(firebase_credentials)
            #cred = credentials.Certificate('firebase-key.json')
            firebase_admin.initialize_app(cred)
            db = firestore.client()
        else:
            print("No credentials found in TOML file.")
    elif db is None:
        db = firestore.client()

def initialize_firebase_once():
    """Initialize Firebase once per session"""
    if 'firebase_initialized' not in st.session_state or not st.session_state.firebase_initialized:
        initialize_firebase()
        st.session_state.firebase_initialized = True

def create_user_profile_in_firestore(user_id, email):
    # Create a new document for the user in Firestore
    user_prof = db.collection('UserProfiles').document(user_id)
    # user_data = db.collection('UserData').document(user_id)

    # Initialize user profile with basic info
    user_prof.set({
        'email': email,
        'first_login': True,
        'current_login': False,
        'createdAt': firestore.SERVER_TIMESTAMP
    })
    # user_data.set({
    #     'Name': None,
    #     'Investing Experienc': None,
    #     'Income': None,
    #     'Age': None
    # })
