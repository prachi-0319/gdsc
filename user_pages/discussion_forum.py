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
    .profile-header h1 {
        color: rgba(131, 158, 101, 0.8);
        font-size: 60px;
    }
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
        background-color: rgba(131, 158, 101, 0.8);
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
<div class="profile-header">
    <h1 style="text-align:center;">📢 Community Forum</h1>
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