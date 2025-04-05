# import streamlit as st
# import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore
# import json # Needed for Streamlit Secrets method
# import os # Needed for Environment Variable method

# # --- Page Configuration ---
# # Set page config *first*

# # st.title("📢 Discussion Forum")
# # st.write("Welcome! Share your thoughts or reply to others.")

# st.markdown("""
# <div class="profile-header">
#     <h1 style="font-size:55px; color:white; text-align:center;">📢 Discussion Forum</h1>
#     <p style="text-align:center;">Welcome! Share your thoughts or reply to others.</p>
# </div>
# """, unsafe_allow_html=True)
# st.markdown("")
# st.markdown("")
# st.markdown("")

# # --- Firebase Initialization ---
# # Ensure db is defined globally or passed reliably
# db = None
# posts_ref = None

# # Choose ONE credentials method:

# # Method A: Local JSON file
# #FIREBASE_KEY_PATH = "firebase_key.json"
# #try:
# #    if not firebase_admin._apps:
# #        if os.path.exists(FIREBASE_KEY_PATH):
# #            cred = credentials.Certificate(FIREBASE_KEY_PATH)
# #            firebase_admin.initialize_app(cred)
# #            st.session_state.firebase_initialized = True # Flag success
# #        else:
# #            st.error(f"Firebase key file not found at: {FIREBASE_KEY_PATH}")
# #            st.session_state.firebase_initialized = False
# #            st.stop()
# #    else:
# #         st.session_state.firebase_initialized = True # Already initialized
# #
# #except Exception as e:
# #    if "already exists" not in str(e):
# #      st.error(f"Firebase initialization failed: {e}")
# #       st.session_state.firebase_initialized = False
# #       st.stop()
# #    else:
# #        # If it already exists, assume it's okay
# #        st.session_state.firebase_initialized = True

# # # Method B: Streamlit Secrets (Uncomment and configure secrets.toml)
# try:
#     if not firebase_admin._apps:
#         firebase_secrets = st.secrets.get("GOOGLE_FIREBASE_DISCUSSION")
#         if firebase_secrets:
#             cred = credentials.Certificate(firebase_secrets)
#             firebase_admin.initialize_app(cred)
#             st.session_state.firebase_initialized = True
#         else:
#             st.error("Firebase credentials not found in Streamlit Secrets.")
#             st.session_state.firebase_initialized = False
#             st.stop()
#     else:
#         st.session_state.firebase_initialized = True
# except Exception as e:
#     if "already exists" not in str(e):
#         st.error(f"Firebase initialization failed using Secrets: {e}")
#         st.session_state.firebase_initialized = False
#         st.stop()
#     else:
#         st.session_state.firebase_initialized = True

# # # Method C: Environment Variable (Uncomment and set env var)
# # try:
# #     if not firebase_admin._apps:
# #         if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
# #             firebase_admin.initialize_app()
# #             st.session_state.firebase_initialized = True
# #         else:
# #             st.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
# #             st.session_state.firebase_initialized = False
# #             st.stop()
# #     else:
# #         st.session_state.firebase_initialized = True
# # except Exception as e:
# #     if "already exists" not in str(e):
# #        st.error(f"Firebase initialization failed using Env Var: {e}")
# #        st.session_state.firebase_initialized = False
# #        st.stop()
# #     else:
# #         st.session_state.firebase_initialized = True


# # Get Firestore client only if initialization succeeded
# if st.session_state.get("firebase_initialized", False):
#     try:
#         db = firestore.client()
#         posts_ref = db.collection('forum_posts') # Use a specific collection name
#     except Exception as e:
#         st.error(f"Failed to connect to Firestore: {e}")
#         st.stop()
# else:
#     st.error("Firebase not initialized. Cannot connect to Firestore.")
#     st.stop()

# # --- User Profile Function ---
# def get_user_profile(user_id):
#     """Fetches the user's profile from Firestore using their user ID."""
#     if db is None:
#         # This check is slightly redundant due to checks above, but good practice
#         st.error("Database connection is not available.")
#         return None
#     try:
#         doc_ref = db.collection("UserData").document(user_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             return doc.to_dict()
#     except Exception as e:
#         st.error(f"Error fetching user profile for {user_id}: {e}")
#     return None

# # --- Determine Current User ---
# # Use session state to store fetched user info to avoid repeated DB calls
# if 'current_user_name' not in st.session_state:
#     st.session_state.current_user_name = None

# # Check if user_id exists and if we haven't fetched the name yet OR if user_id changed
# # (Add more sophisticated logic here if user_id can change within the session)
# user_id_from_session = st.session_state.get("user_id")

# if user_id_from_session and st.session_state.current_user_name is None:
#     user_profile = get_user_profile(user_id_from_session)
#     if user_profile:
#         # Assuming the profile has a 'Name' field
#         st.session_state.current_user_name = user_profile.get("Name", "Unknown User")
#     else:
#         st.session_state.current_user_name = "Unknown User" # Profile not found
# elif not user_id_from_session:
#     st.session_state.current_user_name = "Guest" # No user logged in

# # --- Sidebar: Display User Info ---
# st.sidebar.header("👤 User")
# if st.session_state.current_user_name and st.session_state.current_user_name != "Guest":
#     st.sidebar.write(f"Logged in as: **{st.session_state.current_user_name}**")
#     # Enable posting/replying if user is known
#     can_interact = True
# else:
#     st.sidebar.warning("Please log in to post or reply.")
#     # Disable posting/replying if user is Guest or Unknown
#     can_interact = False
# st.sidebar.divider()

# # --- New Post Section (Moved to Main Area) ---
# st.header("✍️ Create New Post")
# with st.expander("Click here to write a new post", expanded=False): # Collapsed by default
#     if can_interact:
#         with st.form("new_post_form", clear_on_submit=True):
#             new_post_title = st.text_input("Post Title")
#             new_post_content = st.text_area("Post Content", height=150)
#             submitted_post = st.form_submit_button("Create Post")

#             if submitted_post:
#                 # Username comes from the fetched profile now
#                 current_username = st.session_state.current_user_name
#                 if not current_username or current_username in ["Guest", "Unknown User"]:
#                     st.error("Cannot post without being logged in.") # Should not happen if can_interact is False, but good check
#                 elif not new_post_title:
#                     st.warning("Please enter a title for your post.")
#                 elif not new_post_content:
#                     st.warning("Please enter some content for your post.")
#                 else:
#                     # Prepare data for Firestore
#                     new_post_data = {
#                         "author": current_username, # Use fetched name
#                         "title": new_post_title,
#                         "content": new_post_content,
#                         "timestamp": firestore.SERVER_TIMESTAMP,
#                         "replies": []
#                     }
#                     try:
#                         posts_ref.add(new_post_data)
#                         st.success("Post created successfully!")
#                         # Optional: Rerun to see post immediately, though it will show on next interaction too
#                         # st.rerun()
#                     except Exception as e:
#                         st.error(f"Error creating post: {e}")
#     else:
#         st.warning("You must be logged in to create posts.")
# st.divider() # Add a divider after the create post section


# # --- Fetch and Display Posts ---
# st.header("📜 Forum Posts")

# try:
#     # Fetch posts ordered by timestamp descending
#     posts_stream = posts_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
#     posts_list = list(posts_stream) # Convert to list

#     if not posts_list:
#         st.info("No posts yet. Be the first to create one!")
#     else:
#         for doc in posts_list:
#             post = doc.to_dict()
#             post_id = doc.id

#             with st.container(border=True):
#                 st.subheader(f"{post.get('title', 'No Title')}")
#                 timestamp = post.get('timestamp')
#                 ts_string = "Unknown time"
#                 if timestamp and isinstance(timestamp, datetime.datetime):
#                     # Format timestamp nicely
#                     ts_string = timestamp.strftime('%Y-%m-%d %H:%M:%S') # Consider timezone adjustments if needed
#                 elif timestamp:
#                      ts_string = str(timestamp) # Fallback

#                 st.caption(f"Posted by **{post.get('author', 'Unknown')}** on {ts_string}")
#                 st.write(post.get('content', ''))

#                 # --- Replies Section ---
#                 with st.expander("💬 Replies", expanded=False):
#                     replies = post.get('replies', [])
#                     if not replies:
#                         st.write("_No replies yet._")
#                     else:
#                         # Sort replies by timestamp (assuming they are stored with timestamps)
#                         # Note: Firestore server timestamps in arrays might be tricky to sort reliably
#                         # If replies are complex, consider a subcollection in Firestore
#                         sorted_replies = sorted(replies, key=lambda r: r.get('timestamp', datetime.datetime.min))

#                         for reply in sorted_replies:
#                             reply_ts_string = "Unknown time"
#                             reply_ts = reply.get('timestamp')
#                             if reply_ts and isinstance(reply_ts, datetime.datetime):
#                                 reply_ts_string = reply_ts.strftime('%H:%M:%S') # Only time for replies?
#                             elif reply_ts:
#                                 reply_ts_string = str(reply_ts)

#                             #st.markdown(f"**{reply.get('author', 'Unknown')}** ({reply_ts_string}):")
#                             # Use st.markdown with '>' for blockquote style
#                             #st.markdown(f"> {reply.get('content', '').replace('\n', '\n> ')}") # Handle multiline replies
#                             #st.markdown("---")

#                             st.markdown(f"**{reply.get('author', 'Unknown')}** ({reply_ts_string}):")
#                             # Use st.markdown with '>' for blockquote style
#                             # Perform replacement first to avoid f-string backslash error
#                             reply_text = reply.get('content', '')
#                             formatted_reply_text = reply_text.replace('\n', '\n> ')
#                             st.markdown(f"> {formatted_reply_text}") # Use the formatted variable
#                             st.markdown("---")

#                     # --- Add Reply Form ---
#                                         # --- Add Reply Form ---
#                     if can_interact: # Check if user is allowed to reply
#                         reply_key_suffix = f"_{post_id}"
#                         with st.form(key=f"reply_form{reply_key_suffix}", clear_on_submit=True):
#                             reply_content = st.text_area("Write your reply:", height=100, key=f"reply_content{reply_key_suffix}")
#                             submitted_reply = st.form_submit_button("Submit Reply")

#                             if submitted_reply:
#                                 current_username = st.session_state.current_user_name
#                                 if not reply_content:
#                                     st.warning("Reply cannot be empty.")
#                                 elif not current_username or current_username in ["Guest", "Unknown User"]:
#                                      st.error("Cannot reply without being logged in.") # Safety check
#                                 else:
#                                     # --- SOLUTION: Generate timestamp on client ---
#                                     # Use UTC for consistency, as Firestore timestamps are typically UTC
#                                     current_utc_time = datetime.datetime.now(datetime.timezone.utc)
#                                     # --- End of Solution ---

#                                     new_reply_data = {
#                                         "author": current_username, # Use fetched name
#                                         "content": reply_content,
#                                         # --- SOLUTION: Use the client-generated timestamp ---
#                                         "timestamp": current_utc_time
#                                         # "timestamp": firestore.SERVER_TIMESTAMP # <-- REMOVE THIS LINE
#                                         # --- End of Solution ---
#                                     }
#                                     try:
#                                         post_doc_ref = posts_ref.document(post_id)
#                                         post_doc_ref.update({
#                                             'replies': firestore.ArrayUnion([new_reply_data])
#                                         })
#                                         st.success("Reply posted!")
#                                         # Rerun is essential here to refresh the display immediately
#                                         st.rerun()
#                                     except Exception as e:
#                                         st.error(f"Error posting reply: {e}")
#                                         # Log the full traceback for easier debugging if needed
#                                         # import traceback
#                                         # st.error(traceback.format_exc())
#                     else:
#                         # Optionally show a message if user can't reply
#                         # st.write("_Log in to reply._")
#                         pass # Or just don't show the form

#             st.divider() # Separator between posts

# except Exception as e:
#     st.error(f"Error fetching or displaying posts from Firestore: {e}")
#     # Optionally log the full traceback for debugging
#     # import traceback
#     # st.error(traceback.format_exc())


# # --- Footer ---
# st.sidebar.divider()
# st.sidebar.caption("Powered by Firebase Firestore")


# -------------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore
# import json
# import os

# # --- Page Configuration ---
# # st.set_page_config(layout="wide")

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .post-card {
#         border-radius: 10px;
#         padding: 1.5rem;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         background-color: #1e1e1e;
#         transition: transform 0.2s;
#     }
#     .post-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
#     }
#     .post-title {
#         font-size: 1.4rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#         color: #ffffff;
#     }
#     .post-content {
#         color: #e0e0e0;
#         margin-bottom: 1rem;
#         line-height: 1.6;
#     }
#     .post-meta {
#         font-size: 0.85rem;
#         color: #a0a0a0;
#         margin-bottom: 1rem;
#     }
#     .reply-card {
#         background-color: #2a2a2a;
#         border-radius: 8px;
#         padding: 1rem;
#         margin-bottom: 0.8rem;
#     }
#     .reply-meta {
#         font-size: 0.8rem;
#         color: #888888;
#     }
#     .new-post-container {
#         background-color: #1e1e1e;
#         border-radius: 10px;
#         padding: 1.5rem;
#         margin-bottom: 2rem;
#     }
#     .read-more-btn {
#         color: #4e8cff;
#         cursor: pointer;
#         font-size: 0.9rem;
#     }
#     .forum-header {
#         text-align: center;
#         margin-bottom: 2.5rem;
#     }
#     .forum-title {
#         font-size: 2.5rem;
#         font-weight: 700;
#         color: #ffffff;
#         margin-bottom: 0.5rem;
#     }
#     .forum-subtitle {
#         font-size: 1.1rem;
#         color: #a0a0a0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Forum Header
# st.markdown("""
# <div>
#     <h1 style="font-size:60px; color:white; text-align:center;">📢 Community Forum</h1>
#     <p style="text-align:center;">Join the conversation and share your thoughts</p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("")
# st.markdown("")
# st.markdown("")


# # --- Firebase Initialization ---
# db = None
# posts_ref = None

# try:
#     if not firebase_admin._apps:
#         firebase_secrets = st.secrets.get("GOOGLE_FIREBASE_DISCUSSION")
#         if firebase_secrets:
#             cred = credentials.Certificate(firebase_secrets)
#             firebase_admin.initialize_app(cred)
#             st.session_state.firebase_initialized = True
#         else:
#             st.error("Firebase credentials not found in Streamlit Secrets.")
#             st.session_state.firebase_initialized = False
#             st.stop()
#     else:
#         st.session_state.firebase_initialized = True
# except Exception as e:
#     if "already exists" not in str(e):
#         st.error(f"Firebase initialization failed using Secrets: {e}")
#         st.session_state.firebase_initialized = False
#         st.stop()
#     else:
#         st.session_state.firebase_initialized = True

# if st.session_state.get("firebase_initialized", False):
#     try:
#         db = firestore.client()
#         posts_ref = db.collection('forum_posts')
#     except Exception as e:
#         st.error(f"Failed to connect to Firestore: {e}")
#         st.stop()
# else:
#     st.error("Firebase not initialized. Cannot connect to Firestore.")
#     st.stop()

# # --- User Profile Function ---
# def get_user_profile(user_id):
#     if db is None:
#         st.error("Database connection is not available.")
#         return None
#     try:
#         doc_ref = db.collection("UserData").document(user_id)
#         doc = doc_ref.get()
#         if doc.exists:
#             return doc.to_dict()
#     except Exception as e:
#         st.error(f"Error fetching user profile for {user_id}: {e}")
#     return None

# # --- Determine Current User ---
# if 'current_user_name' not in st.session_state:
#     st.session_state.current_user_name = None

# user_id_from_session = st.session_state.get("user_id")

# if user_id_from_session and st.session_state.current_user_name is None:
#     user_profile = get_user_profile(user_id_from_session)
#     if user_profile:
#         st.session_state.current_user_name = user_profile.get("Name", "Unknown User")
#     else:
#         st.session_state.current_user_name = "Unknown User"
# elif not user_id_from_session:
#     st.session_state.current_user_name = "Guest"

# # --- Sidebar: User Info and Navigation ---
# with st.sidebar:
#     st.header("👤 User Profile")
#     if st.session_state.current_user_name and st.session_state.current_user_name != "Guest":
#         st.success(f"Welcome back, **{st.session_state.current_user_name}**")
#         can_interact = True
#     else:
#         st.warning("Guest User")
#         st.info("Please log in to participate")
#         can_interact = False
    
#     st.divider()
    
#     st.header("🔍 Navigation")
#     if st.button("📜 View All Posts"):
#         st.rerun()
#     if can_interact and st.button("✍️ Create New Post"):
#         st.session_state.show_new_post = True
    
#     st.divider()
#     st.caption("Powered by Firebase Firestore")

# # --- New Post Section ---
# if st.session_state.get('show_new_post', False) or not st.session_state.get('posts_loaded', False):
#     with st.container():
#         st.markdown("""<div class="new-post-container">""", unsafe_allow_html=True)
#         st.header("Create New Post")
        
#         if can_interact:
#             with st.form("new_post_form", clear_on_submit=True):
#                 cols = st.columns([1, 1])
#                 with cols[0]:
#                     new_post_title = st.text_input("Post Title", placeholder="What's your post about?")
#                 with cols[1]:
#                     post_category = st.selectbox("Category", ["General", "Question", "Announcement", "Discussion"])
                
#                 new_post_content = st.text_area("Post Content", height=200, 
#                                               placeholder="Share your thoughts... (Markdown supported)")
                
#                 submitted_post = st.form_submit_button("Publish Post", use_container_width=True)
                
#                 if submitted_post:
#                     current_username = st.session_state.current_user_name
#                     if not current_username or current_username in ["Guest", "Unknown User"]:
#                         st.error("Cannot post without being logged in.")
#                     elif not new_post_title:
#                         st.warning("Please enter a title for your post.")
#                     elif not new_post_content:
#                         st.warning("Please enter some content for your post.")
#                     else:
#                         new_post_data = {
#                             "author": current_username,
#                             "title": new_post_title,
#                             "content": new_post_content,
#                             "category": post_category,
#                             "timestamp": firestore.SERVER_TIMESTAMP,
#                             "replies": []
#                         }
#                         try:
#                             posts_ref.add(new_post_data)
#                             st.success("Post created successfully!")
#                             st.session_state.show_new_post = False
#                             st.session_state.posts_loaded = False
#                             st.rerun()
#                         except Exception as e:
#                             st.error(f"Error creating post: {e}")
#         else:
#             st.warning("You must be logged in to create posts.")
#             if st.button("Back to Forum"):
#                 st.session_state.show_new_post = False
#                 st.rerun()
        
#         st.markdown("""</div>""", unsafe_allow_html=True)

# # --- Fetch and Display Posts ---
# if not st.session_state.get('show_new_post', True):
#     st.header("📜 Community Discussions")
    
#     try:
#         posts_stream = posts_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
#         posts_list = list(posts_stream)
        
#         if not posts_list:
#             st.info("No posts yet. Be the first to create one!")
#         else:
#             # Display filters at the top
#             with st.expander("🔍 Filter Posts", expanded=False):
#                 filter_cols = st.columns([1, 1, 2])
#                 with filter_cols[0]:
#                     category_filter = st.selectbox("Category", ["All"] + sorted(list(set([p.to_dict().get('category', 'General') for p in posts_list]))))
#                 with filter_cols[1]:
#                     sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Most Replies"])
#                 with filter_cols[2]:
#                     search_query = st.text_input("Search posts")
            
#             # Process posts based on filters
#             filtered_posts = []
#             for doc in posts_list:
#                 post = doc.to_dict()
#                 post['id'] = doc.id
                
#                 # Apply filters
#                 if category_filter != "All" and post.get('category') != category_filter:
#                     continue
#                 if search_query and search_query.lower() not in post.get('title', '').lower() + post.get('content', '').lower():
#                     continue
                
#                 filtered_posts.append(post)
            
#             # Sort posts
#             if sort_option == "Oldest First":
#                 filtered_posts.sort(key=lambda x: x.get('timestamp', datetime.datetime.min))
#             elif sort_option == "Most Replies":
#                 filtered_posts.sort(key=lambda x: len(x.get('replies', [])), reverse=True)
#             else:  # Newest First
#                 filtered_posts.sort(key=lambda x: x.get('timestamp', datetime.datetime.max), reverse=True)
            
#             if not filtered_posts:
#                 st.info("No posts match your filters.")
#             else:
#                 # Display in a 3-column grid for larger screens
#                 cols = st.columns(3)
#                 for i, post in enumerate(filtered_posts):
#                     with cols[i % 3]:
#                         with st.container():
#                             # st.markdown(f"""
#                             # <div class="post-card">
#                             #     <div class="post-meta">
#                             #         <span style="color: #4e8cff;">{post.get('category', 'General')}</span> • 
#                             #         {post.get('author', 'Unknown')} • 
#                             #         {post.get('timestamp', datetime.datetime.now()).strftime('%b %d, %Y') if isinstance(post.get('timestamp'), datetime.datetime) else 'Recent'}
#                             #     </div>
#                             #     <div class="post-title">{post.get('title', 'No Title')}</div>
#                             #     <div class="post-content">
#                             #         {post.get('content', '')[:150]}{'...' if len(post.get('content', '')) > 150 else ''}
#                             #     </div>
#                             #     {f'<div class="read-more-btn" onclick="alert(\'Expanded view coming soon!\')">Read more →</div>' if len(post.get('content', '')) > 150 else ''}
                                
#                             #     <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
#                             #         <span style="font-size: 0.85rem; color: #888;">
#                             #             💬 {len(post.get('replies', []))} replies
#                             #         </span>
#                             #         <button onclick="alert('Expanded view coming soon!')" style="background: none; border: none; color: #4e8cff; cursor: pointer;">
#                             #             View Discussion
#                             #         </button>
#                             #     </div>
#                             # </div>
#                             # """, unsafe_allow_html=True)

#                             post_content = post.get('content', '')
#                             truncated_content = post_content[:150] + ('...' if len(post_content) > 150 else '')
#                             read_more = f'<div class="read-more-btn" onclick="alert(\'Expanded view coming soon!\')">Read more →</div>' if len(post_content) > 150 else ''

#                             html_content = f"""
#                             <div class="post-card">
#                                 <div class="post-meta">
#                                     <span style="color: #4e8cff;">{post.get('category', 'General')}</span> • 
#                                     {post.get('author', 'Unknown')} • 
#                                     {post.get('timestamp', datetime.datetime.now()).strftime('%b %d, %Y') if isinstance(post.get('timestamp'), datetime.datetime) else 'Recent'}
#                                 </div>
#                                 <div class="post-title">{post.get('title', 'No Title')}</div>
#                                 <div class="post-content">
#                                     {truncated_content}
#                                 </div>
#                                 {read_more}
                                
#                                 <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
#                                     <span style="font-size: 0.85rem; color: #888;">
#                                         💬 {len(post.get('replies', []))} replies
#                                     </span>
#                                     <button onclick="alert('Expanded view coming soon!')" style="background: none; border: none; color: #4e8cff; cursor: pointer;">
#                                         View Discussion
#                                     </button>
#                                 </div>
#                             </div>
#                             """

#                             st.markdown(html_content, unsafe_allow_html=True)
                
#                 # Detailed view when a post is selected (would need more JS integration for full functionality)
#                 # For now, showing all posts in detail below the grid
#                 st.divider()
#                 st.subheader("Detailed View")
                
#                 for post in filtered_posts:
#                     with st.expander(f"{post.get('title', 'No Title')} - by {post.get('author', 'Unknown')}", expanded=False):
#                         st.markdown(f"""
#                         <div style="margin-bottom: 1.5rem;">
#                             <div style="color: #a0a0a0; font-size: 0.9rem; margin-bottom: 0.5rem;">
#                                 {post.get('timestamp', datetime.datetime.now()).strftime('%B %d, %Y at %H:%M') if isinstance(post.get('timestamp'), datetime.datetime) else 'Recent'} • 
#                                 Category: <span style="color: #4e8cff;">{post.get('category', 'General')}</span>
#                             </div>
#                             <div style="line-height: 1.7; color: #e0e0e0;">
#                                 {post.get('content', '')}
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)
                        
#                         # Replies section
#                         st.markdown(f"**💬 Replies ({len(post.get('replies', []))})**")
                        
#                         if not post.get('replies'):
#                             st.info("No replies yet. Be the first to respond!")
#                         else:
#                             for reply in sorted(post.get('replies', []), key=lambda r: r.get('timestamp', datetime.datetime.min)):
#                                 st.markdown(f"""
#                                 <div class="reply-card">
#                                     <div style="font-weight: 600; color: #ffffff; margin-bottom: 0.3rem;">
#                                         {reply.get('author', 'Anonymous')}
#                                     </div>
#                                     <div class="reply-meta">
#                                         {reply.get('timestamp', datetime.datetime.now()).strftime('%b %d %H:%M') if isinstance(reply.get('timestamp'), datetime.datetime) else 'Recently'}
#                                     </div>
#                                     <div style="margin-top: 0.5rem; color: #d0d0d0;">
#                                         {reply.get('content', '')}
#                                     </div>
#                                 </div>
#                                 """, unsafe_allow_html=True)
                        
#                         # Reply form
#                         if can_interact:
#                             with st.form(key=f"reply_form_{post['id']}", clear_on_submit=True):
#                                 reply_content = st.text_area("Your reply", key=f"reply_{post['id']}", 
#                                                            placeholder="Write your response here...")
#                                 if st.form_submit_button("Post Reply"):
#                                     current_username = st.session_state.current_user_name
#                                     if not reply_content:
#                                         st.warning("Reply cannot be empty.")
#                                     else:
#                                         new_reply_data = {
#                                             "author": current_username,
#                                             "content": reply_content,
#                                             "timestamp": datetime.datetime.now(datetime.timezone.utc)
#                                         }
#                                         try:
#                                             post_doc_ref = posts_ref.document(post['id'])
#                                             post_doc_ref.update({
#                                                 'replies': firestore.ArrayUnion([new_reply_data])
#                                             })
#                                             st.success("Reply posted!")
#                                             st.rerun()
#                                         except Exception as e:
#                                             st.error(f"Error posting reply: {e}")
#                         else:
#                             st.info("Log in to reply to this post.")
        
#         st.session_state.posts_loaded = True
        
#     except Exception as e:
#         st.error(f"Error fetching or displaying posts from Firestore: {e}")


# -------------------------------------------------------------------------------------------------------------------------


import streamlit as st
import datetime
import time
import firebase_admin
from firebase_admin import credentials, firestore

# --- Page Configuration ---
# st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
    .post-card {
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #1e1e1e;
        transition: transform 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .post-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .post-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white;
    }
    .post-content {
        color: #e0e0e0;
        margin-bottom: 1rem;
        flex-grow: 1;
    }
    .post-meta {
        font-size: 0.85rem;
        color: #a0a0a0;
        margin-bottom: 1rem;
    }
    .category-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        background-color: #4e8cff;
        color: white;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
    .forum-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .forum-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }
    .forum-subtitle {
        font-size: 1.1rem;
        color: #a0a0a0;
    }
    .category-tag {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        background-color: #4e8cff;
        color: white;
        font-size: 0.8rem;
    }
    [data-testid="stExpander"] {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stExpander"] .st-emotion-cache-1q7spjk {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Firebase Initialization ---
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["GOOGLE_FIREBASE_DISCUSSION"])
    firebase_admin.initialize_app(cred)

db = firestore.client()
posts_ref = db.collection('forum_posts')

# --- Session State Management ---
if 'show_new_post' not in st.session_state:
    st.session_state.show_new_post = False
if 'force_refresh' not in st.session_state:
    st.session_state.force_refresh = False

# --- User Management ---
def get_current_user():
    # Replace with your actual user authentication logic
    return "Test User"  # Example - should return "Guest" if not logged in

current_user = get_current_user()
can_interact = current_user != "Guest"

# --- Post Management ---
@st.cache_data(ttl=10, show_spinner="Loading posts...")
def load_posts():
    try:
        posts = list(posts_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream())
        return [(doc.id, doc.to_dict()) for doc in posts]
    except Exception as e:
        st.error(f"Error loading posts: {e}")
        return []

def create_post(title, content, category):
    try:
        posts_ref.add({
            "author": current_user,
            "title": title,
            "content": content,
            "category": category,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "replies": []
        })
        st.session_state.force_refresh = True
        st.success("Post created successfully!")
        time.sleep(1)
        st.cache_data.clear()
        st.session_state.show_new_post = False
        st.rerun()

    except Exception as e:
        st.error(f"Error creating post: {e}")

# --- UI Components ---
def show_new_post_form():
    with st.form("new_post_form", clear_on_submit=True):
        cols = st.columns([1, 1])
        with cols[0]:
            title = st.text_input("Title", key="post_title")
        with cols[1]:
            category = st.selectbox("Category", ["General", "Question", "Announcement", "Discussion"])
        
        content = st.text_area("Content", height=200, key="post_content")
        
        col1, col2, col3 = st.columns([0.5, 0.5, 6])
        with col1:
            if st.form_submit_button("Submit"):
                if title and content:
                    create_post(title, content, category)
        with col2:
            if st.form_submit_button("Cancel"):
                st.session_state.show_new_post = False
                st.rerun()


def render_post_card(post_id, post):
    timestamp = post.get('timestamp')
    if isinstance(timestamp, datetime.datetime):
        timestamp_str = timestamp.strftime('%b %d, %Y')
    else:
        timestamp_str = "Recently"
    
    content = post.get('content', '')
    show_full = st.session_state.get(f"show_full_{post_id}", False)
    max_length = 150
    needs_truncation = len(content) > max_length
    
    with st.container():
        # Main post container with border
        with st.container(border=True):
            # Post header with category and metadata
            col1, col2 = st.columns([4, 1.5])
            with col1:
                st.markdown(f"**{post.get('title', 'No Title')}**")
            with col2:
                st.markdown(f"<div style='text-align: center;'><span class='category-tag'>{post.get('category', 'General')}</span></div>", 
                           unsafe_allow_html=True)
            
            st.caption(f"Posted by {post.get('author', 'Unknown')} on {timestamp_str}")
            
            # Post content with inline Read More
            if needs_truncation and not show_full:
                displayed_content = content[:max_length]
                read_more = f"<span style='color: #4e8cff; text-decoration: underline; cursor: pointer;' onclick='alert(\"Toggling content\")'>... Read More</span>"
                st.markdown(f"{displayed_content}{read_more}", unsafe_allow_html=True)
            else:
                st.markdown(content)
                if needs_truncation:
                    st.markdown(f"<span style='color: #4e8cff; text-decoration: underline; cursor: pointer;' onclick='alert(\"Toggling content\")'>Read Less</span>", 
                               unsafe_allow_html=True)
            
            # Reply count and button
            st.markdown(f"💬 {len(post.get('replies', []))} replies", help="Click to view replies")
            
            # Reply section in expander
            with st.expander("View Replies", expanded=False):
                # Existing replies
                if post.get('replies'):
                    for reply in post.get('replies', []):
                        reply_time = reply.get('timestamp', datetime.datetime.now())
                        if isinstance(reply_time, datetime.datetime):
                            reply_time_str = reply_time.strftime('%b %d %H:%M')
                        else:
                            reply_time_str = "Recently"
                        
                        with st.container(border=True):
                            st.markdown(f"**{reply.get('author', 'Anonymous')}**")
                            st.caption(reply_time_str)
                            st.markdown(reply.get('content', ''))
                
                # Reply form
                if can_interact:
                    with st.form(key=f"reply_form_{post_id}", clear_on_submit=True):
                        reply_content = st.text_area("Your reply:", key=f"reply_{post_id}")
                        if st.form_submit_button("Post Reply"):
                            if reply_content:
                                try:
                                    posts_ref.document(post_id).update({
                                        'replies': firestore.ArrayUnion([{
                                            'author': current_user,
                                            'content': reply_content,
                                            'timestamp': datetime.datetime.now(datetime.timezone.utc)
                                        }])
                                    })
                                    st.success("Reply added!")
                                    st.cache_data.clear()
                                    time.sleep(0.5)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error adding reply: {e}")
                            else:
                                st.warning("Reply cannot be empty")
                else:
                    st.info("Log in to reply to this post")


# def render_post_card(post_id, post):
#     timestamp = post.get('timestamp')
#     if isinstance(timestamp, datetime.datetime):
#         timestamp_str = timestamp.strftime('%b %d, %Y')
#     else:
#         timestamp_str = "Recently"
    
#     content = post.get('content', '')
#     truncated = content[:150] + ('...' if len(content) > 150 else '')
    
#     with st.container():
#         st.markdown(f"""
#         <div class="post-card">
#             <div class="post-meta">
#                 <span class="category-tag">{post.get('category', 'General')}</span>
#                 {post.get('author', 'Unknown')} • {timestamp_str}
#             </div>
#             <div class="post-title">{post.get('title', 'No Title')}</div>
#             <div class="post-content">{truncated}</div>
#             <div style="margin-top: auto; display: flex; justify-content: space-between; align-items: center;">
#                 <span style="font-size: 0.85rem; color: #888;">
#                     💬 {len(post.get('replies', []))} replies
#                 </span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Add reply functionality in an expander
#         with st.expander("💬 Reply to this post"):
#             if can_interact:
#                 with st.form(key=f"reply_form_{post_id}"):
#                     reply_content = st.text_area("Your reply", key=f"reply_{post_id}")
#                     if st.form_submit_button("Submit Reply"):
#                         if reply_content:
#                             try:
#                                 posts_ref.document(post_id).update({
#                                     'replies': firestore.ArrayUnion([{
#                                         'author': current_user,
#                                         'content': reply_content,
#                                         'timestamp': datetime.datetime.now(datetime.timezone.utc)
#                                     }])
#                                 })
#                                 st.success("Reply added!")
#                                 st.cache_data.clear()
#                                 time.sleep(1)
#                                 st.rerun()
#                             except Exception as e:
#                                 st.error(f"Error adding reply: {e}")
#                         else:
#                             st.warning("Reply cannot be empty")
#             else:
#                 st.info("Please log in to reply")
            
#             # Display existing replies
#             st.markdown("**Replies:**")
#             for reply in post.get('replies', []):
#                 reply_time = reply.get('timestamp', datetime.datetime.now())
#                 if isinstance(reply_time, datetime.datetime):
#                     reply_time_str = reply_time.strftime('%b %d %H:%M')
#                 else:
#                     reply_time_str = "Recently"
                
#                 st.markdown(f"""
#                 <div style="margin: 0.5rem 0; padding: 0.5rem; background: #2a2a2a; border-radius: 5px;">
#                     <div style="font-weight: bold; color: #4e8cff;">{reply.get('author', 'Anonymous')}</div>
#                     <div style="font-size: 0.8rem; color: #888;">{reply_time_str}</div>
#                     <div style="margin-top: 0.3rem;">{reply.get('content', '')}</div>
#                 </div>
#                 """, unsafe_allow_html=True)

# --- Main App ---
# Forum Header
st.markdown("""
<div>
    <h1 style="font-size:60px; color:white; text-align:center;">📢 Community Forum</h1>
    <p style="text-align:center;">Join the conversation and share your thoughts</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("")
st.markdown("")

# Always show the "New Post" button
if can_interact and st.button("✍️ Create New Post", use_container_width=True):
    st.session_state.show_new_post = True
    st.session_state.force_refresh = True
    st.rerun()

# New Post Form
if st.session_state.show_new_post:
    show_new_post_form()
    # st.divider()

# Force refresh if needed
if st.session_state.force_refresh:
    st.cache_data.clear()
    st.session_state.force_refresh = False
    time.sleep(1)
    st.rerun()

# Load and display posts
posts = load_posts()

st.markdown("")
st.markdown("")

st.title("Past Discussions")
st.markdown("")

if not posts:
    st.info("No posts yet. Be the first to create one!")
else:
    # Filters
    with st.expander("🔍 Filter Posts", expanded=True):
        filter_cols = st.columns([1, 1, 2])
        with filter_cols[0]:
            # category_filter = st.selectbox("Category", ["All"] + sorted(list(set(p.to_dict().get('category', 'General') for _, p in posts)))
            category_filter = st.selectbox(
                "Category", 
                ["All"] + sorted(list(set(p[1].get('category', 'General') for p in posts)))
            )
        with filter_cols[1]:
            sort_option = st.selectbox("Sort by", ["Newest First", "Oldest First", "Most Replies"])
        with filter_cols[2]:
            search_query = st.text_input("Search posts")

    # Process filtering
    filtered_posts = []
    for post_id, post in posts:
        if category_filter != "All" and post.get('category') != category_filter:
            continue
        if search_query and search_query.lower() not in (post.get('title', '') + post.get('content', '')).lower():
            continue
        filtered_posts.append((post_id, post))

    # Sort posts
    if sort_option == "Oldest First":
        filtered_posts.sort(key=lambda x: x[1].get('timestamp', datetime.datetime.min))
    elif sort_option == "Most Replies":
        filtered_posts.sort(key=lambda x: len(x[1].get('replies', [])), reverse=True)
    else:  # Newest First
        filtered_posts.sort(key=lambda x: x[1].get('timestamp', datetime.datetime.max), reverse=True)

    # Display in 3-column grid
    cols = st.columns(3)
    for i, (post_id, post) in enumerate(filtered_posts):
        with cols[i % 3]:
            render_post_card(post_id, post)

    # Detailed view when clicking "View Discussion" would go here
    # (Would need JavaScript integration for full functionality)