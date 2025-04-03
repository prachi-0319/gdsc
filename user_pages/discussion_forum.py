import streamlit as st
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import json # Needed for Streamlit Secrets method
import os # Needed for Environment Variable method

# --- Page Configuration ---
# Set page config *first*

st.title("📢 Discussion Forum")
st.write("Welcome! Share your thoughts or reply to others.")

# --- Firebase Initialization ---
# Ensure db is defined globally or passed reliably
db = None
posts_ref = None

# Choose ONE credentials method:

# Method A: Local JSON file
#FIREBASE_KEY_PATH = "firebase_key.json"
#try:
#    if not firebase_admin._apps:
#        if os.path.exists(FIREBASE_KEY_PATH):
#            cred = credentials.Certificate(FIREBASE_KEY_PATH)
#            firebase_admin.initialize_app(cred)
#            st.session_state.firebase_initialized = True # Flag success
#        else:
#            st.error(f"Firebase key file not found at: {FIREBASE_KEY_PATH}")
#            st.session_state.firebase_initialized = False
#            st.stop()
#    else:
#         st.session_state.firebase_initialized = True # Already initialized
#
#except Exception as e:
#    if "already exists" not in str(e):
#      st.error(f"Firebase initialization failed: {e}")
#       st.session_state.firebase_initialized = False
#       st.stop()
#    else:
#        # If it already exists, assume it's okay
#        st.session_state.firebase_initialized = True

# # Method B: Streamlit Secrets (Uncomment and configure secrets.toml)
try:
    if not firebase_admin._apps:
        firebase_secrets = st.secrets.get("GOOGLE_FIREBASE_DISCUSSION")
        if firebase_secrets:
            cred = credentials.Certificate(firebase_secrets)
            firebase_admin.initialize_app(cred)
            st.session_state.firebase_initialized = True
        else:
            st.error("Firebase credentials not found in Streamlit Secrets.")
            st.session_state.firebase_initialized = False
            st.stop()
    else:
        st.session_state.firebase_initialized = True
except Exception as e:
    if "already exists" not in str(e):
        st.error(f"Firebase initialization failed using Secrets: {e}")
        st.session_state.firebase_initialized = False
        st.stop()
    else:
        st.session_state.firebase_initialized = True

# # Method C: Environment Variable (Uncomment and set env var)
# try:
#     if not firebase_admin._apps:
#         if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
#             firebase_admin.initialize_app()
#             st.session_state.firebase_initialized = True
#         else:
#             st.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
#             st.session_state.firebase_initialized = False
#             st.stop()
#     else:
#         st.session_state.firebase_initialized = True
# except Exception as e:
#     if "already exists" not in str(e):
#        st.error(f"Firebase initialization failed using Env Var: {e}")
#        st.session_state.firebase_initialized = False
#        st.stop()
#     else:
#         st.session_state.firebase_initialized = True


# Get Firestore client only if initialization succeeded
if st.session_state.get("firebase_initialized", False):
    try:
        db = firestore.client()
        posts_ref = db.collection('forum_posts') # Use a specific collection name
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {e}")
        st.stop()
else:
    st.error("Firebase not initialized. Cannot connect to Firestore.")
    st.stop()

# --- User Profile Function ---
def get_user_profile(user_id):
    """Fetches the user's profile from Firestore using their user ID."""
    if db is None:
        # This check is slightly redundant due to checks above, but good practice
        st.error("Database connection is not available.")
        return None
    try:
        doc_ref = db.collection("UserData").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        st.error(f"Error fetching user profile for {user_id}: {e}")
    return None

# --- Determine Current User ---
# Use session state to store fetched user info to avoid repeated DB calls
if 'current_user_name' not in st.session_state:
    st.session_state.current_user_name = None

# Check if user_id exists and if we haven't fetched the name yet OR if user_id changed
# (Add more sophisticated logic here if user_id can change within the session)
user_id_from_session = st.session_state.get("user_id")

if user_id_from_session and st.session_state.current_user_name is None:
    user_profile = get_user_profile(user_id_from_session)
    if user_profile:
        # Assuming the profile has a 'Name' field
        st.session_state.current_user_name = user_profile.get("Name", "Unknown User")
    else:
        st.session_state.current_user_name = "Unknown User" # Profile not found
elif not user_id_from_session:
    st.session_state.current_user_name = "Guest" # No user logged in

# --- Sidebar: Display User Info ---
st.sidebar.header("👤 User")
if st.session_state.current_user_name and st.session_state.current_user_name != "Guest":
    st.sidebar.write(f"Logged in as: **{st.session_state.current_user_name}**")
    # Enable posting/replying if user is known
    can_interact = True
else:
    st.sidebar.warning("Please log in to post or reply.")
    # Disable posting/replying if user is Guest or Unknown
    can_interact = False
st.sidebar.divider()

# --- New Post Section (Moved to Main Area) ---
st.header("✍️ Create New Post")
with st.expander("Click here to write a new post", expanded=False): # Collapsed by default
    if can_interact:
        with st.form("new_post_form", clear_on_submit=True):
            new_post_title = st.text_input("Post Title")
            new_post_content = st.text_area("Post Content", height=150)
            submitted_post = st.form_submit_button("Create Post")

            if submitted_post:
                # Username comes from the fetched profile now
                current_username = st.session_state.current_user_name
                if not current_username or current_username in ["Guest", "Unknown User"]:
                    st.error("Cannot post without being logged in.") # Should not happen if can_interact is False, but good check
                elif not new_post_title:
                    st.warning("Please enter a title for your post.")
                elif not new_post_content:
                    st.warning("Please enter some content for your post.")
                else:
                    # Prepare data for Firestore
                    new_post_data = {
                        "author": current_username, # Use fetched name
                        "title": new_post_title,
                        "content": new_post_content,
                        "timestamp": firestore.SERVER_TIMESTAMP,
                        "replies": []
                    }
                    try:
                        posts_ref.add(new_post_data)
                        st.success("Post created successfully!")
                        # Optional: Rerun to see post immediately, though it will show on next interaction too
                        # st.rerun()
                    except Exception as e:
                        st.error(f"Error creating post: {e}")
    else:
        st.warning("You must be logged in to create posts.")
st.divider() # Add a divider after the create post section


# --- Fetch and Display Posts ---
st.header("📜 Forum Posts")

try:
    # Fetch posts ordered by timestamp descending
    posts_stream = posts_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    posts_list = list(posts_stream) # Convert to list

    if not posts_list:
        st.info("No posts yet. Be the first to create one!")
    else:
        for doc in posts_list:
            post = doc.to_dict()
            post_id = doc.id

            with st.container(border=True):
                st.subheader(f"{post.get('title', 'No Title')}")
                timestamp = post.get('timestamp')
                ts_string = "Unknown time"
                if timestamp and isinstance(timestamp, datetime.datetime):
                    # Format timestamp nicely
                    ts_string = timestamp.strftime('%Y-%m-%d %H:%M:%S') # Consider timezone adjustments if needed
                elif timestamp:
                     ts_string = str(timestamp) # Fallback

                st.caption(f"Posted by **{post.get('author', 'Unknown')}** on {ts_string}")
                st.write(post.get('content', ''))

                # --- Replies Section ---
                with st.expander("💬 Replies", expanded=False):
                    replies = post.get('replies', [])
                    if not replies:
                        st.write("_No replies yet._")
                    else:
                        # Sort replies by timestamp (assuming they are stored with timestamps)
                        # Note: Firestore server timestamps in arrays might be tricky to sort reliably
                        # If replies are complex, consider a subcollection in Firestore
                        sorted_replies = sorted(replies, key=lambda r: r.get('timestamp', datetime.datetime.min))

                        for reply in sorted_replies:
                            reply_ts_string = "Unknown time"
                            reply_ts = reply.get('timestamp')
                            if reply_ts and isinstance(reply_ts, datetime.datetime):
                                reply_ts_string = reply_ts.strftime('%H:%M:%S') # Only time for replies?
                            elif reply_ts:
                                reply_ts_string = str(reply_ts)

                            #st.markdown(f"**{reply.get('author', 'Unknown')}** ({reply_ts_string}):")
                            # Use st.markdown with '>' for blockquote style
                            #st.markdown(f"> {reply.get('content', '').replace('\n', '\n> ')}") # Handle multiline replies
                            #st.markdown("---")

                            st.markdown(f"**{reply.get('author', 'Unknown')}** ({reply_ts_string}):")
                            # Use st.markdown with '>' for blockquote style
                            # Perform replacement first to avoid f-string backslash error
                            reply_text = reply.get('content', '')
                            formatted_reply_text = reply_text.replace('\n', '\n> ')
                            st.markdown(f"> {formatted_reply_text}") # Use the formatted variable
                            st.markdown("---")

                    # --- Add Reply Form ---
                                        # --- Add Reply Form ---
                    if can_interact: # Check if user is allowed to reply
                        reply_key_suffix = f"_{post_id}"
                        with st.form(key=f"reply_form{reply_key_suffix}", clear_on_submit=True):
                            reply_content = st.text_area("Write your reply:", height=100, key=f"reply_content{reply_key_suffix}")
                            submitted_reply = st.form_submit_button("Submit Reply")

                            if submitted_reply:
                                current_username = st.session_state.current_user_name
                                if not reply_content:
                                    st.warning("Reply cannot be empty.")
                                elif not current_username or current_username in ["Guest", "Unknown User"]:
                                     st.error("Cannot reply without being logged in.") # Safety check
                                else:
                                    # --- SOLUTION: Generate timestamp on client ---
                                    # Use UTC for consistency, as Firestore timestamps are typically UTC
                                    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
                                    # --- End of Solution ---

                                    new_reply_data = {
                                        "author": current_username, # Use fetched name
                                        "content": reply_content,
                                        # --- SOLUTION: Use the client-generated timestamp ---
                                        "timestamp": current_utc_time
                                        # "timestamp": firestore.SERVER_TIMESTAMP # <-- REMOVE THIS LINE
                                        # --- End of Solution ---
                                    }
                                    try:
                                        post_doc_ref = posts_ref.document(post_id)
                                        post_doc_ref.update({
                                            'replies': firestore.ArrayUnion([new_reply_data])
                                        })
                                        st.success("Reply posted!")
                                        # Rerun is essential here to refresh the display immediately
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error posting reply: {e}")
                                        # Log the full traceback for easier debugging if needed
                                        # import traceback
                                        # st.error(traceback.format_exc())
                    else:
                        # Optionally show a message if user can't reply
                        # st.write("_Log in to reply._")
                        pass # Or just don't show the form

            st.divider() # Separator between posts

except Exception as e:
    st.error(f"Error fetching or displaying posts from Firestore: {e}")
    # Optionally log the full traceback for debugging
    # import traceback
    # st.error(traceback.format_exc())


# --- Footer ---
st.sidebar.divider()
st.sidebar.caption("Powered by Firebase Firestore")