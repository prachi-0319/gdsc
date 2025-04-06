import os
import time
import re
import json
import plotly.graph_objs as go
import streamlit as st
from plotly.io import to_json, from_json
from ChatBot.chatbot import *

import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from datetime import datetime
import auth_functions
from auth_functions import *

def create_new_chat(user_email):
    """Create a new chat document in Firestore"""
    chat_id = str(uuid.uuid4()) # This is the issue will need to change this auto generating the chat id
    chat_ref = db.collection('chats').document(chat_id)
    
    chat_ref.set({
        'metadata': {
            'userId': st.session_state.get('user_id', 'anonymous'),
            'userEmail': user_email,
            'createdAt': firestore.SERVER_TIMESTAMP,
            'lastUpdated': firestore.SERVER_TIMESTAMP
        }
    })
    return chat_id

def save_message(chat_id, message, sender):
    """Save a message to the specific chat document"""
    chat_ref = db.collection('Chats').document(chat_id)
    
    # Add message to messages subcollection
    chat_ref.collection('messages').add({
        'content': message,
        'role': sender,
        'sentAt': firestore.SERVER_TIMESTAMP
    })
    
    # Update last updated timestamp
    chat_ref.update({
        'metadata.lastUpdated': firestore.SERVER_TIMESTAMP
    })

def get_chat_history(chat_id):
    """Retrieve chat history for a specific chat"""
    messages_ref = db.collection('Chats').document(chat_id).collection('messages')
    messages = messages_ref.order_by('timestamp').stream()
    
    return [msg.to_dict() for msg in messages]

def select_language():
    """
    Create a language selection dropdown
    Returns the selected language
    """
    languages = {
        "English": "english",  
        "Hindi": "hindi", 
        "Telugu": "telugu",
        "Urdu": "urdu",
        "Tamil":"tamil",
        "Marathi": "marathi",
        "Bengali": "bengali",
        "Gujarati": "gujarati",
        "Punjabi": "punjabi",
        "Kannada": "kannada",
        "Malayalam": "malayalam",
        "Odia": "odia",
        "Assamese": "assamese"
    }
    
    st.sidebar.header("🌐 Language Settings")
    selected_language = st.sidebar.selectbox(
        "Choose Your Language",
        list(languages.keys()),
        index=0  # Default to English
    )
    
    return languages[selected_language]

# Custom CSS with reduced box sizes
st.markdown("""
    <style>
    .profile-header h1 {
        color: #556b3b;
        font-size: 60px;
    }
    /* Clean Title */
    .title {
        color: var(--primary);
        text-align: center;
        font-weight: 600;
        margin: 2rem 0;
        font-size: 2.25rem;
        letter-spacing: -0.5px;
    }

    /* Smaller Containers */
    .stContainer {
        background: var(--surface);
        border-radius: 12px;
        padding: 1rem; /* Reduced from 1.5rem */
        margin-bottom: 1rem; /* Reduced from 1.5rem */
        border: 1px solid #30363D;
    }

    /* Smaller Message Cards */
    .user-message {
        background: var(--surface);
        border-left: 4px solid var(--primary);
        border-radius: 8px;
        padding: 0.75rem; /* Reduced from 1rem */
        margin: 0.5rem 0; /* Reduced from 1rem 0 */
    }

    .assistant-message {
        background: var(--surface);
        border-left: 4px solid #30363D;
        border-radius: 8px;
        padding: 0.75rem; /* Reduced from 1rem */
        margin: 0.5rem 0; /* Reduced from 1rem 0 */
    }

    /* Smaller Input Form */
    .stForm {
        background: var(--surface);
        border-radius: 12px;
        padding: 0.75rem; /* Reduced from 1rem */
        margin-top: 2rem;
    }

    .stTextInput>div>div>input {
        background: var(--background);
        color: var(--text-primary);
        border-radius: 8px;
        border: 1px solid #30363D;
        padding: 10px; /* Slightly reduced from 12px */
    }


    /* Minimal Plot Container */
    .plot-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #30363D;
    }

    /* Clean File Uploader */
    .stFileUploader>label {
        border: 1px dashed #30363D;
        border-radius: 8px;
        background: var(--background);
        padding: 0.75rem; /* Reduced to match form */
    }
    /* Add this to your existing CSS */
    .attachment-button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background: rgba(131, 158, 101, 0.8);
        border: 1px solid #30363D;
        color: rgba(131, 158, 101, 0.8);
        cursor: pointer;
        transition: all 0.2s ease;
        margin-right: 8px;
    }
    
    .attachment-button:hover {
        background: #30363D;
        color: var(--text-primary);
    }
    
    .attachment-button svg {
        width: 20px;
        height: 20px;
    }
    
    .hidden-uploader {
        display: none;
    }
    
    /* Adjust the input columns */
    .input-columns {
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Update title to be simpler

# st.markdown("""
# <div class="profile-header">
#     <h1 style="text-align:center;">📈 Financial Insights</h1>
#     <p style="text-align:center;">Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
#     to create a balanced portfolio allocation tailored to your specific needs.</p>
# </div>
# """, unsafe_allow_html=True)

st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">📈 Finance ChatBot</h1>
    <p style="text-align:center;">
        Meet your <span class="highlight">FinFriend</span> — your friendly financial companion!<br>
        It brings together insights from across the web, answers your questions (big or small), suggests helpful YouTube videos, and even creates and explains plots to make finance feel simple and fun.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("")
st.markdown("")
st.markdown("")

# Create a directory for temporary images
os.makedirs("temp_images", exist_ok=True)

selected_language = select_language()
print(selected_language)

# Initialize chatbot and history in session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = FinancialChatBot(language=selected_language)
if "history" not in st.session_state:
    st.session_state.history = []


# Display conversation history
for i in range(0, len(st.session_state.history), 2):
    if i + 1 >= len(st.session_state.history):
        break  # Skip incomplete pairs

    user_msg = st.session_state.history[i]
    assistant_msg = st.session_state.history[i + 1]

    with st.container():
        st.markdown('<div class="stContainer">', unsafe_allow_html=True)
        cols = st.columns([3, 2])

        with cols[0]:
            st.markdown(
                f'<div class="user-message">'
                f'<div style="font-weight: 500; color: var(--primary); margin-bottom: 6px;">👤 Your Query</div>'
                f'{user_msg["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )
                
            st.markdown(
                f'<div class="assistant-message">'
                f'<div style="font-weight: 500; color: var(--text-secondary); margin-bottom: 6px;">🤖 Analysis</div>'
                f'{assistant_msg["text"]}'
                f'</div>',
                unsafe_allow_html=True
            )

        with cols[1]:
            if user_msg.get("image_path"):
                st.image(user_msg["image_path"], caption="Uploaded Chart", use_container_width=True)

            if assistant_msg.get("plot"):
                try:
                    with st.container():
                        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                        plot_dict = json.loads(assistant_msg["plot"])
                        fig = go.Figure(plot_dict)
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font_color='var(--text-primary)',
                            xaxis=dict(showgrid=True, gridcolor='rgba(102, 187, 106, 0.15)', linecolor='rgba(102, 187, 106, 0.4)'),
                            yaxis=dict(showgrid=True, gridcolor='rgba(102, 187, 106, 0.15)', linecolor='rgba(102, 187, 106, 0.4)'),
                            hoverlabel=dict(bgcolor='var(--surface)', font_size=14, font_family="Montserrat"),
                            scene=dict(xaxis=dict(backgroundcolor="rgba(0,0,0,0)"), yaxis=dict(backgroundcolor="rgba(0,0,0,0)"), zaxis=dict(backgroundcolor="rgba(0,0,0,0)")) if fig.data[0].type == 'scatter3d' else {}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error rendering plot: {str(e)}")

            resources = re.findall(r"https?://\S+", assistant_msg["text"])
            if resources:
                with st.expander("Explore Resources", expanded=False):
                    for url in resources:
                        st.markdown(f"- <span style='font-size: 0.9rem;'>🌐</span> [{url}]({url})", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# Input form with loading state
with st.form(key="chat_form", clear_on_submit=True):
    st.markdown('<div class="stForm">', unsafe_allow_html=True)
    input_cols = st.columns([9, 1])

    with input_cols[0]:
        st.markdown("")
        user_input = st.text_input(
            "Your message:",
            placeholder=f"Ask about market trends, stock analysis, or upload a chart...",
            label_visibility="collapsed"
        )

    with input_cols[1]:
        st.markdown(
            '<style>div[data-testid="stFormSubmitButton"] button {width: 100%;}</style>',
            unsafe_allow_html=True
        )
        submit_button = st.form_submit_button(label="🚀 Analyze")

    uploaded_file = st.file_uploader(
        "📤 Drop Financial Charts Here",
        type=["png", "jpg", "jpeg"],
        key="file_uploader",
        help="Upload charts for instant analysis",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Process input with loading spinner
if submit_button and (user_input or uploaded_file):
    with st.spinner("Analyzing..."):
        image_path = None
        if uploaded_file is not None:
            timestamp = int(time.time())
            image_path = f"temp_images/image_{timestamp}.png"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())
            if not user_input:
                user_input = f"Describe what you see in this image. Focus on any charts, financial data, or technical analysis elements if present."

        # Pass language to the chat method
        st.session_state.chatbot.language = selected_language
        bot_response = st.session_state.chatbot.chat(user_input, image_path)

        st.session_state.history.append({
            "role": "user",
            "content": user_input,
            "image_path": image_path
        })
        st.session_state.history.append({
            "role": "assistant",
            "text": bot_response["text"],
            "plot": bot_response["plot"]
        })

        st.rerun()
