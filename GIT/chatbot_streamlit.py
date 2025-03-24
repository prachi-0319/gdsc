import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from Financial_Agent_Self_Eval import *  # Assuming this contains necessary imports and tools
import plotly.graph_objects as go
import json
import pandas as pd
import numpy as np
import base64
import re

# Initialize LLM for context processing
llm = update_router()

# Modified FinancialChatBot class to include sources and videos
class FinancialChatBot:
    def __init__(self):
        self.conversation_history = []
        self.model = update_router()
        self.context_messages = []  # Store actual message objects for context
        self.plots = []  # Store generated plots
        self.sources = []  # Store news sources/references
        self.videos = []  # Store YouTube video URLs
        self.raw_plot_data = None  # Store raw plot data

    def _format_bot_message(self, content: str) -> str:
        return f"🤖 Assistant: {content}"

    def _format_user_message(self, content: str) -> str:
        return f"👤 User: {content}"

    def _update_context(self, user_input: str, bot_response: str):
        self.context_messages.append(HumanMessage(content=user_input))
        self.context_messages.append(AIMessage(content=bot_response))
        if len(self.context_messages) > 10:
            self.context_messages = self.context_messages[-10:]

    def _process_with_context(self, user_input: str):
        if not self.context_messages:
            return user_input
        context_system_prompt = """
        You are a financial assistant analyzing a conversation history.
        Given the conversation history and a new user query, generate an enhanced query incorporating context.
        Return ONLY the enhanced query.
        """
        context_prompt = "Conversation history:\n"
        for msg in self.context_messages[-6:]:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            context_prompt += f"{role}: {msg.content}\n\n"
        context_prompt += f"New user query: {user_input}\n\nEnhanced query:"
        try:
            messages = [
                SystemMessage(content=context_system_prompt),
                HumanMessage(content=context_prompt)
            ]
            enhanced_query = llm.invoke(messages).content.strip()
            return enhanced_query
        except Exception as e:
            print(f"Context processing error: {e}")
            return user_input

    def _extract_and_process_plots(self, response):
        self.plots = []
        if isinstance(response, dict) and 'plots' in response:
            plot_data = response['plots']
            if isinstance(plot_data, list):
                for item in plot_data:
                    if isinstance(item, dict):
                        fig = go.Figure(item)
                        self.plots.append(fig)
            elif isinstance(plot_data, dict):
                fig = go.Figure(plot_data)
                self.plots.append(fig)

    def chat(self, user_input: str, image_path: str = None) -> dict:
        self.conversation_history.append(self._format_user_message(user_input))
        contextualized_input = user_input
        if self.context_messages and not image_path:
            contextualized_input = self._process_with_context(user_input)
        image_list = [image_path] if image_path else []
        initial_state = create_initial_state(contextualized_input, image_list)
        if self.context_messages:
            initial_state["messages"] = self.context_messages + [HumanMessage(content=contextualized_input)]
        try:
            response = self.model.invoke(initial_state)
            bot_response = response.get('running_summary', '')
            if not bot_response and isinstance(response, dict) and response.get('messages'):
                bot_response = response['messages'][-1].content
            self._extract_and_process_plots(response)
            # Assuming response includes sources and videos; adapt as needed
            self.sources = response.get('sources_gathered', [])  # From web_research
            self.videos = [video['url'] for video in response.get('youtube_videos', [])] if 'youtube_videos' in response else response.get('videos', [])
            self._update_context(user_input, bot_response)
            formatted_response = self._format_bot_message(bot_response)
            self.conversation_history.append(formatted_response)
            return {
                "text": bot_response,
                "plots": self.plots,
                "sources": self.sources,
                "videos": self.videos
            }
        except Exception as e:
            error_message = f"Error: {str(e)}"
            self.conversation_history.append(self._format_bot_message(error_message))
            return {"text": error_message, "plots": [], "sources": [], "videos": []}

    def clear_history(self):
        self.conversation_history = []
        self.context_messages = []
        self.plots = []
        self.sources = []
        self.videos = []
        self.raw_plot_data = None

def translate_text(text, language='english'):
    try:
        url = 'https://api.two.ai/v2'
        client = OpenAI(base_url=url, api_key=os.environ.get("SUTRA_API_KEY"))
        response = client.chat.completions.create(
            model='sutra-v2',
            messages=[{"role": "user", "content": f"Translate this text in {language}: {text}"}],
            max_tokens=1024,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

# Streamlit UI
def main():
    st.set_page_config(page_title="Financial Assistant", page_icon="💰", layout="wide")
    
    # Initialize session state
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FinancialChatBot()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Sidebar settings
    st.sidebar.title("Settings")
    languages = ["english", "hindi", "spanish", "french", "german", "chinese", "japanese", "arabic"]
    selected_language = st.sidebar.selectbox("Select Response Language", languages)
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    image_path = None
    if uploaded_file is not None:
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = "temp_image.jpg"
        st.sidebar.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    if st.sidebar.button("Clear Chat"):
        st.session_state.chatbot.clear_history()
        st.session_state.messages = []

    # Two-column layout
    chat_col, viz_col = st.columns([0.6, 0.4])

    # Chat column (left)
    with chat_col:
        st.title("Financial Assistant Chatbot")
        st.subheader("Ask me anything about finance!")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        user_input = st.chat_input("Type your message here...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.chat(user_input, image_path)
                    display_text = response["text"]
                    if selected_language.lower() != "english":
                        display_text = translate_text(response["text"], selected_language)
                    st.write(display_text)
                    st.session_state.messages.append({"role": "assistant", "content": display_text})

    # Additional content column (right)
    with viz_col:
        st.title("Additional Content")
        
        # Graphs section
        st.subheader("Graphs")
        if st.session_state.chatbot.plots:
            for plot in st.session_state.chatbot.plots:
                st.plotly_chart(plot, use_container_width=True)
        else:
            st.info("No graphs to display yet.")
        
        # References section
        st.subheader("References")
        if st.session_state.chatbot.sources:
            for source in st.session_state.chatbot.sources:
                st.markdown(f"- [{source}]({source})")
        else:
            st.info("No references available.")
        
        # YouTube Recommendations section
        st.subheader("YouTube Recommendations")
        if st.session_state.chatbot.videos:
            for video_url in st.session_state.chatbot.videos:
                video_id = extract_video_id(video_url)
                if video_id:
                    st.components.v1.html(
                        f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>',
                        height=315,
                    )
                else:
                    st.write(f"Invalid YouTube URL: {video_url}")
        else:
            st.info("No video recommendations available.")

if __name__ == "__main__":
    main()