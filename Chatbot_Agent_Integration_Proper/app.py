import streamlit as st
import os
import time
import re
import plotly.io as pio
from chatbot_streamlit import *  # Replace with actual module name

# Page configuration
st.set_page_config(page_title="Financial Chatbot", layout="wide")
st.title("Financial Chatbot")

# Create a directory for temporary images
os.makedirs("temp_images", exist_ok=True)

# Initialize chatbot and history in session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = FinancialChatBot()
if "history" not in st.session_state:
    st.session_state.history = []

# Create two columns: 60% left, 40% right
left_column, right_column = st.columns([3, 2])

# Left Column: Chat Interface
with left_column:
    # Display conversation history
    for message in st.session_state.history:
        if message["role"] == "user":
            st.write(f"👤 User: {message['content']}")
            if message.get("image_path"):
                st.write("(Image uploaded)")
        else:
            st.markdown(f"🤖 Assistant: {message['text']}")

    # Input form
    with st.form(key="chat_form"):
        user_input = st.text_input(
            "Your message:", placeholder="e.g., 'Show me a candlestick chart for AAPL'"
        )
        uploaded_file = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])
        submit_button = st.form_submit_button(label="Send")

    # Process input when submitted
    if submit_button and (user_input or uploaded_file):
        image_path = None
        if uploaded_file is not None:
            # Save uploaded image with a unique timestamp
            timestamp = int(time.time())
            image_path = f"temp_images/image_{timestamp}.png"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())
            # If no text input, prompt the bot about the image
            if not user_input:
                user_input = "What do you see in this image?"

        # Get bot response
        bot_response = st.session_state.chatbot.chat(user_input, image_path)

        # Update conversation history
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

        # Refresh the app to update the UI
        st.rerun()

# Right Column: Supplementary Content
with right_column:
    st.write("### All Visual Content and Resources")

    # Collect all plots, images, and resources from history
    all_plots = []
    all_images = []
    all_resources = set()  # Use a set to avoid duplicate resources

    for msg in st.session_state.history:
        if msg["role"] == "user" and msg.get("image_path"):
            all_images.append(msg["image_path"])
        elif msg["role"] == "assistant":
            if msg.get("plot"):
                all_plots.append(msg["plot"])
            bot_text = msg["text"]
            resources = re.findall(r"https?://\S+", bot_text)
            all_resources.update(resources)

    # Display all images
    if all_images:
        st.write("#### Uploaded Images")
        for idx, image_path in enumerate(all_images):
            st.image(image_path, caption=f"Uploaded Image {idx+1}")

    # Display all plots
    if all_plots:
        st.write("#### Plots")
        for idx, plot_json in enumerate(all_plots):
            try:
                fig = pio.from_json(plot_json)
                st.plotly_chart(fig, key=f"plot_{idx}")
            except Exception as e:
                st.error(f"Error rendering plot {idx+1}: {e}")

    # Display all resources
    if all_resources:
        st.write("#### Resources")
        for url in all_resources:
            st.markdown(f"- [{url}]({url})")
    else:
        st.write("No resources available.")