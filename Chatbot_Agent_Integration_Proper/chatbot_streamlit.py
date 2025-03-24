import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from Financial_Agent_Self_Eval import *
import os
from openai import OpenAI

# Initialize LLM for context processing
llm = update_router()

class FinancialChatBot:
    def __init__(self):
        self.conversation_history = []
        self.model = update_router()
        self.context_messages = []  # Store actual message objects for context
        
    def _format_bot_message(self, content: str) -> str:
        """Format the bot's message for display"""
        return f"🤖 Assistant: {content}"
    
    def _format_user_message(self, content: str) -> str:
        """Format the user's message for display"""
        return f"👤 User: {content}"
    
    def _update_context(self, user_input: str, bot_response: str):
        """Update the context messages for the next interaction"""
        # Add to context messages (for model processing)
        self.context_messages.append(HumanMessage(content=user_input))
        self.context_messages.append(AIMessage(content=bot_response))
        
        # Keep context within a reasonable size (last 5 interactions = 10 messages)
        if len(self.context_messages) > 10:
            self.context_messages = self.context_messages[-10:]
    
    def _process_with_context(self, user_input: str):
        """Generate a contextualized query based on conversation history"""
        if not self.context_messages:
            return user_input
        
        # Create a prompt to contextualize the query
        context_system_prompt = """
        You are a financial assistant analyzing a conversation history.
        Given the conversation history and a new user query, your task is to:
        1. Understand the context of the ongoing conversation
        2. Generate an enhanced version of the user's query that incorporates relevant context
        3. Return ONLY the enhanced query without any explanations
        """
        
        # Create a formatted context
        context_prompt = "Conversation history:\n"
        for msg in self.context_messages[-6:]:  # Use last 3 interactions max
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            context_prompt += f"{role}: {msg.content}\n\n"
        
        context_prompt += f"New user query: {user_input}\n\nGenerate an enhanced query that incorporates context:"
        
        # Use LLM to generate contextualized query
        try:
            messages = [
                SystemMessage(content=context_system_prompt),
                HumanMessage(content=context_prompt)
            ]
            enhanced_query = llm.invoke(messages).content.strip()
            return enhanced_query
        except Exception as e:
            print(f"Context processing error: {e}")
            return user_input  # Fallback to original query
    
    def chat(self, user_input: str, image_path: str = None) -> str:
        """
        Process a single chat interaction with context awareness
        
        Args:
            user_input (str): The user's message
            image_path (str, optional): Path to an image if one is provided
            
        Returns:
            str: The bot's response
        """
        # Add user message to display history
        self.conversation_history.append(self._format_user_message(user_input))
        
        # Skip contextualizing if this is the first message or providing an image
        contextualized_input = user_input
        if self.context_messages and not image_path:
            contextualized_input = self._process_with_context(user_input)
        
        # Create initial state with image if provided
        image_list = [image_path] if image_path else []
        initial_state = create_initial_state(contextualized_input, image_list)
        
        # Add all previous messages to the state
        if self.context_messages:
            initial_state["messages"] = self.context_messages + [HumanMessage(content=contextualized_input)]
        
        try:
            # Process through the model
            response = self.model.invoke(initial_state)
            
            # Extract the response from running_summary
            bot_response = response.get('running_summary', '')
            if not bot_response and response.get('messages'):
                # Fallback to last message content if running_summary is empty
                bot_response = response['messages'][-1].content
                
            # Update context with this interaction
            self._update_context(user_input, bot_response)
                
            # Format and store bot's response for display
            formatted_response = self._format_bot_message(bot_response)
            self.conversation_history.append(formatted_response)
            
            return bot_response
            
        except Exception as e:
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            self.conversation_history.append(self._format_bot_message(error_message))
            return error_message
    
    def get_conversation_history(self) -> str:
        """Return the full conversation history"""
        return "\n\n".join(self.conversation_history)
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.context_messages = []

def translate_text(text, language='english'):
    """Translate text using Two.AI API"""
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
        return text  # Return original text if translation fails

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Financial Assistant",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("Financial Assistant Chatbot")
    st.subheader("Ask me anything about finance!")
    
    # Initialize session state for chat history and chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FinancialChatBot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Language selection
    languages = ["english", "hindi", "spanish", "french", "german", "chinese", "japanese", "arabic"]
    selected_language = st.sidebar.selectbox("Select Response Language", languages)
    
    # Upload image option
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    image_path = None
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = "temp_image.jpg"
        st.sidebar.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.chatbot.clear_history()
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # User input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.chat(user_input, image_path)
                
                # Translate if not in English
                if selected_language.lower() != "english":
                    with st.spinner(f"Translating to {selected_language}..."):
                        translated_response = translate_text(response, selected_language)
                        st.write(translated_response)
                        # Store the translated response
                        st.session_state.messages.append({"role": "assistant", "content": translated_response})
                else:
                    st.write(response)
                    # Store the original response
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()