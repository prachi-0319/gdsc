import streamlit as st
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ QUIZ QUESTIONS ~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function to fetch quiz questions
@st.cache_data(show_spinner=True)

def get_quiz_questions(history_json, mode="general"):
    """
    Generates quiz questions using Gemini API based on user's past interactions.

    :param history_json: JSON string of user quiz/chat/dictionary history
    :param mode: "general" for beginner questions, "personalized" for tailored ones
    :return: List of multiple-choice questions
    """

    if mode == "general":
        prompt = (
            "Generate 5 beginner-friendly finance multiple-choice questions."
            " Each question should follow this format:\n"
            "Question: <question_text>\n"
            "A) <option 1>\n"
            "B) <option 2>\n"
            "C) <option 3>\n"
            "D) <option 4>\n"
            "Answer: <Correct option letter>\n"
            "Explanation: <Explanation of the correct answer>\n"
        )
    else:
        prompt = (
            f"Based on the user's history:\n{history_json}\n"
            "Generate 5 personalized multiple-choice finance questions."
            " Each question should follow this format:\n"
            "Question: <question_text>\n"
            "A) <option 1>\n"
            "B) <option 2>\n"
            "C) <option 3>\n"
            "D) <option 4>\n"
            "Answer: <Correct option letter>\n"
            "Explanation: <Explanation of the correct answer>\n"
        )

    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt)

        if not response or not response.candidates:
            return []

        raw_text = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else ""

        # Splitting response into structured questions
        questions_list = raw_text.strip().split("\n\n")
        questions = []

        for idx,q_text in enumerate(questions_list):
            lines = q_text.strip().split("\n")
            if len(lines) < 6:
                continue  # Skip malformed questions

            question_text = lines[0].replace(f"Question {idx}: ", "").strip()
            options = [lines[i].strip() for i in range(1, 5)]
            correct_answer_line = lines[5].strip()
            correct_answer = correct_answer_line.replace("Answer: ", "").strip()[0]  # Extract A, B, C, or D
            explanation = lines[6].replace("Explanation: ", "").strip() if len(lines) > 6 else "No explanation provided."

            questions.append({
                "question": question_text,
                "options": options,
                "answer": correct_answer,
                "explanation": explanation
            })

        return questions

    except Exception as e:
        st.error(f"Error fetching quiz questions: {str(e)}")
        return []






# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ STREAMLIT APP ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


'''
Sample user history JSON:
{
    "quiz_answers": [
        {
            "question": "What is a budget?",
            "selected": "A) A type of bank account",
            "correct": false
        },
        {
            "question": "What does APR stand for?",
            "selected": "A) Annual Percentage Rate",
            "correct": true
        }
    ],
    "finance_gpt_queries": [
        "How does inflation impact my savings?",
        "What are some safe investments for beginners?"
    ],
    "searched_terms": [
        "Compound Interest",
        "Stock Market Index"
    ]
}

'''

st.title("Finance Quiz App")

# Initialize session state for all types of user history
if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = "general"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []  # Stores past quiz answers
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores Finance GPT queries
if "dictionary_searches" not in st.session_state:
    st.session_state.dictionary_searches = []  # Stores searched financial terms

# Select mode
quiz_mode = st.radio("Choose Quiz Type:", ["General", "Personalized"])

# If mode changes, reset questions and history
if quiz_mode.lower() != st.session_state.quiz_mode:
    st.session_state.quiz_mode = quiz_mode.lower()
    st.session_state.questions = []
    st.session_state.current_question = 0
    if quiz_mode.lower() == "general":
        st.session_state.quiz_history = []  # Reset history in general mode

# Consolidate all history into one JSON
user_history = {
    "quiz_answers": st.session_state.quiz_history or [{"question": "Placeholder", "selected": "A) Sample", "correct": False}],
    "finance_gpt_queries": st.session_state.chat_history or ["What is a budget?"],
    "searched_terms": st.session_state.dictionary_searches or ["Investment"]
}
history_json = json.dumps(user_history, indent=4)


# Fetch new questions when quiz starts
if not st.session_state.questions:
    with st.spinner("Fetching new quiz questions..."):
        st.session_state.questions = get_quiz_questions(history_json, mode=st.session_state.quiz_mode)

# Display questions
if st.session_state.questions:
    q_idx = st.session_state.current_question
    question_data = st.session_state.questions[q_idx]

    st.subheader(f"Q{q_idx + 1}: {question_data['question']}")
    selected_option = st.radio("Choose your answer:", question_data["options"], key=q_idx)

    if st.button("Submit Answer"):
        correct = selected_option.startswith(question_data["answer"])
        if correct:
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect! The correct answer is: {question_data['answer']}.\n\nExplanation: {question_data['explanation']}")

        # Store answer in history only for personalized mode
        if st.session_state.quiz_mode == "personalized":
            st.session_state.quiz_history.append({
                "question": question_data["question"],
                "selected": selected_option,
                "correct": correct
            })

    # Next Question button
    if st.button("Next Question"):
        if q_idx + 1 < len(st.session_state.questions):
            st.session_state.current_question += 1
            st.rerun()
        else:
            st.success("Quiz completed! 🎯")