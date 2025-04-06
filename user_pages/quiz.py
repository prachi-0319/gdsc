import streamlit as st
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ QUIZ QUESTIONS ~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_quiz_questions(history_json, mode="general", difficulty="easy"):
    """
    Generates multiple-choice quiz questions using Gemini API.

    :param history_json: JSON string of user quiz/chat/dictionary history
    :param mode: "general" for beginner questions, "personalized" for tailored ones
    :param difficulty: "easy", "medium", or "hard"
    :return: List of multiple-choice questions
    """
    if mode == "general":
        prompt = (
            f"Generate 20 {difficulty}-level finance multiple-choice questions. "
            "Each question should follow this format:\n"
            "Question: <question_text>\n"
            "A) <option1>\n"
            "B) <option2>\n"
            "C) <option3>\n"
            "D) <option4>\n"
            "Answer: <correct_option_letter>\n"
            "Explanation: <explanation_of_the_answer>\n"
        )
    else:
        prompt = (
            f"Make it related to personalized finances, savings, etc.\n"
            f"Generate 20 {difficulty}-level personalized finance multiple-choice questions. "
            "Each question should follow this format:\n"
            "Question: <question_text>\n"
            "A) <option1>\n"
            "B) <option2>\n"
            "C) <option3>\n"
            "D) <option4>\n"
            "Answer: <correct_option_letter>\n"
            "Explanation: <explanation_of_the_answer>\n"
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

        for q_text in questions_list:
            lines = q_text.strip().split("\n")
            if len(lines) < 6:
                continue  # Skip malformed questions

            question_text = lines[0].replace("Question: ", "").strip()
            options = [lines[i].strip() for i in range(1, 5)]
            correct_answer = lines[5].replace("Answer: ", "").strip()[0]  # Extract A, B, C, or D
            explanation = lines[6].replace("Explanation: ", "").strip() if len(lines) > 6 else "No explanation provided."

            questions.append({
                "question": question_text,
                "options": options,
                "answer": correct_answer,
                "explanation": explanation
            })

        return questions[:20]  # Limit to 20 questions

    except Exception as e:
        st.error(f"Error fetching quiz questions: {str(e)}")
        return []

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~ STREAMLIT APP ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# st.set_page_config(page_title="Finance Quiz App", page_icon="📊", layout="centered")

# Main Page Layout
# st.title("📊 Finance Quiz App")
# st.markdown("Test and expand your money knowledge with interactive quizzes! Choose between general financial concepts or personalized quizzes based on your profile. Adjust the difficulty to match your expertise level - perfect for beginners and experts alike.")
# st.markdown("Each quiz helps you spot knowledge gaps while making finance fun!")




st.markdown("""
    <style>
    .profile-header h1 {
        color: #556b3b;
        font-size: 60px;
    }
    </style>        
""", unsafe_allow_html = True)


st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">📊 Finance Quiz App</h1>
    <p style="text-align:center;">Test and expand your money knowledge with interactive quizzes! Choose between general financial concepts or personalized quizzes based on your profile. 
            Adjust the difficulty to match your expertise level - perfect for beginners and experts alike. Each quiz helps you spot knowledge gaps while making finance fun!</p>
</div>
""", unsafe_allow_html=True)

# st.markdown("""
# <div>
#     <h1 style="font-size:60px; color:white; text-align:center;">📊 Finance Quiz App</h1>
#     <p style="text-align:center;">Test and expand your money knowledge with interactive quizzes! Choose between general financial concepts or personalized quizzes based on your profile.</p>
#     <p style="text-align:center;">Adjust the difficulty to match your expertise level - perfect for beginners and experts alike. Each quiz helps you spot knowledge gaps while making finance fun!</p>
# </div>
# """, unsafe_allow_html=True)


st.markdown("")
st.markdown("")
# Initialize session state
if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = "general"
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "dictionary_searches" not in st.session_state:
    st.session_state.dictionary_searches = []
if "score" not in st.session_state:
    st.session_state.score = 0

# Quiz Settings
st.markdown("### Quiz Settings")
col1, col2 = st.columns(2)
with col1:
    quiz_mode = st.radio("Choose Quiz Type:", ["General", "Personalized"])
with col2:
    difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

# Consolidate all history into one JSON
user_history = {
    "quiz_answers": st.session_state.quiz_history,
    "finance_gpt_queries": st.session_state.chat_history,
    "searched_terms": st.session_state.dictionary_searches
}
history_json = json.dumps(user_history, indent=4)

# Fetch new questions when quiz starts or settings change
if not st.session_state.questions or st.session_state.quiz_mode != quiz_mode.lower():
    with st.spinner("Fetching new quiz questions..."):
        st.session_state.questions = get_quiz_questions(history_json, mode=quiz_mode.lower(), difficulty=difficulty.lower())
        st.session_state.quiz_mode = quiz_mode.lower()
        st.session_state.current_question = 0
        st.session_state.score = 0  # Reset score for new quiz

# Display questions
if st.session_state.questions:
    q_idx = st.session_state.current_question
    question_data = st.session_state.questions[q_idx]

    st.markdown("---")
    st.markdown(f"### Question {q_idx + 1} of 20")
    st.markdown(f"**{question_data['question']}**")

    # Progress bar
    progress = (q_idx + 1) / 20
    st.progress(progress)

    selected_option = st.radio("Choose your answer:", question_data["options"], key=q_idx)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            correct = selected_option.startswith(question_data["answer"])
            #print(correct)
            if correct:
                st.success("Correct! 🎉")
                st.session_state.score += 1
            else:
                correct_option = next(opt for opt in question_data["options"] if opt.startswith(question_data["answer"]))
                st.error(f"Incorrect! The correct answer is: **{correct_option}**.\n\n**Explanation:** {question_data['explanation']}")

            # Store answer in history only for personalized mode
            if st.session_state.quiz_mode == "personalized":
                st.session_state.quiz_history.append({
                    "question": question_data["question"],
                    "selected": selected_option,
                    "correct": correct
                })

    with col2:
        if st.button("Next Question"):
            if q_idx + 1 < len(st.session_state.questions):
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.success(f"Quiz completed! 🎯 Your final score is **{st.session_state.score}/20**.")
                st.session_state.questions = []  # Reset questions for a new quiz
                if st.button("Generate New Quiz"):
                    st.session_state.questions = get_quiz_questions(history_json, mode=quiz_mode.lower(), difficulty=difficulty.lower())
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.rerun()
