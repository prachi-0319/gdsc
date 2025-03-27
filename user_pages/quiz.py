# import streamlit as st
# import json
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")



# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ QUIZ QUESTIONS ~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # Function to fetch quiz questions
# @st.cache_data(show_spinner=True)

# def get_quiz_questions(history_json, mode="general"):
#     """
#     Generates quiz questions using Gemini API based on user's past interactions.

#     :param history_json: JSON string of user quiz/chat/dictionary history
#     :param mode: "general" for beginner questions, "personalized" for tailored ones
#     :return: List of multiple-choice questions
#     """

#     if mode == "general":
#         prompt = (
#             "Generate 5 beginner-friendly finance multiple-choice questions."
#             " Each question should follow this format:\n"
#             "Question: <question_text>\n"
#             "A) <option 1>\n"
#             "B) <option 2>\n"
#             "C) <option 3>\n"
#             "D) <option 4>\n"
#             "Answer: <Correct option letter>\n"
#             "Explanation: <Explanation of the correct answer>\n"
#         )
#     else:
#         prompt = (
#             f"Based on the user's history:\n{history_json}\n"
#             "Generate 5 personalized multiple-choice finance questions."
#             " Each question should follow this format:\n"
#             "Question: <question_text>\n"
#             "A) <option 1>\n"
#             "B) <option 2>\n"
#             "C) <option 3>\n"
#             "D) <option 4>\n"
#             "Answer: <Correct option letter>\n"
#             "Explanation: <Explanation of the correct answer>\n"
#         )

#     model = genai.GenerativeModel("gemini-1.5-pro-latest")

#     try:
#         response = model.generate_content(prompt)

#         if not response or not response.candidates:
#             return []

#         raw_text = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else ""

#         # Splitting response into structured questions
#         questions_list = raw_text.strip().split("\n\n")
#         questions = []

#         for idx,q_text in enumerate(questions_list):
#             lines = q_text.strip().split("\n")
#             if len(lines) < 6:
#                 continue  # Skip malformed questions

#             question_text = lines[0].replace(f"Question {idx}: ", "").strip()
#             options = [lines[i].strip() for i in range(1, 5)]
#             correct_answer_line = lines[5].strip()
#             correct_answer = correct_answer_line.replace("Answer: ", "").strip()[0]  # Extract A, B, C, or D
#             explanation = lines[6].replace("Explanation: ", "").strip() if len(lines) > 6 else "No explanation provided."

#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "answer": correct_answer,
#                 "explanation": explanation
#             })

#         return questions

#     except Exception as e:
#         st.error(f"Error fetching quiz questions: {str(e)}")
#         return []






# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ STREAMLIT APP ~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# '''
# Sample user history JSON:
# {
#     "quiz_answers": [
#         {
#             "question": "What is a budget?",
#             "selected": "A) A type of bank account",
#             "correct": false
#         },
#         {
#             "question": "What does APR stand for?",
#             "selected": "A) Annual Percentage Rate",
#             "correct": true
#         }
#     ],
#     "finance_gpt_queries": [
#         "How does inflation impact my savings?",
#         "What are some safe investments for beginners?"
#     ],
#     "searched_terms": [
#         "Compound Interest",
#         "Stock Market Index"
#     ]
# }

# '''

# st.title("Finance Quiz App")

# # Initialize session state for all types of user history
# if "quiz_mode" not in st.session_state:
#     st.session_state.quiz_mode = "general"
# if "questions" not in st.session_state:
#     st.session_state.questions = []
# if "current_question" not in st.session_state:
#     st.session_state.current_question = 0
# if "quiz_history" not in st.session_state:
#     st.session_state.quiz_history = []  # Stores past quiz answers
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []  # Stores Finance GPT queries
# if "dictionary_searches" not in st.session_state:
#     st.session_state.dictionary_searches = []  # Stores searched financial terms

# # Select mode
# quiz_mode = st.radio("Choose Quiz Type:", ["General", "Personalized"])

# # If mode changes, reset questions and history
# if quiz_mode.lower() != st.session_state.quiz_mode:
#     st.session_state.quiz_mode = quiz_mode.lower()
#     st.session_state.questions = []
#     st.session_state.current_question = 0
#     if quiz_mode.lower() == "general":
#         st.session_state.quiz_history = []  # Reset history in general mode

# # Consolidate all history into one JSON
# user_history = {
#     "quiz_answers": st.session_state.quiz_history or [{"question": "Placeholder", "selected": "A) Sample", "correct": False}],
#     "finance_gpt_queries": st.session_state.chat_history or ["What is a budget?"],
#     "searched_terms": st.session_state.dictionary_searches or ["Investment"]
# }
# history_json = json.dumps(user_history, indent=4)


# # Fetch new questions when quiz starts
# if not st.session_state.questions:
#     with st.spinner("Fetching new quiz questions..."):
#         st.session_state.questions = get_quiz_questions(history_json, mode=st.session_state.quiz_mode)

# # Display questions
# if st.session_state.questions:
#     q_idx = st.session_state.current_question
#     question_data = st.session_state.questions[q_idx]

#     st.subheader(f"Q{q_idx + 1}: {question_data['question']}")
#     selected_option = st.radio("Choose your answer:", question_data["options"], key=q_idx)

#     if st.button("Submit Answer"):
#         correct = selected_option.startswith(question_data["answer"])
#         if correct:
#             st.success("Correct! 🎉")
#         else:
#             st.error(f"Incorrect! The correct answer is: {question_data['answer']}.\n\nExplanation: {question_data['explanation']}")

#         # Store answer in history only for personalized mode
#         if st.session_state.quiz_mode == "personalized":
#             st.session_state.quiz_history.append({
#                 "question": question_data["question"],
#                 "selected": selected_option,
#                 "correct": correct
#             })

#     # Next Question button
#     if st.button("Next Question"):
#         if q_idx + 1 < len(st.session_state.questions):
#             st.session_state.current_question += 1
#             st.rerun()
#         else:
#             st.success("Quiz completed! 🎯")



# import streamlit as st
# import json
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ QUIZ QUESTIONS ~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# def get_quiz_questions(history_json, mode="general", difficulty="easy"):
#     """
#     Generates quiz questions using Gemini API based on user's past interactions.

#     :param history_json: JSON string of user quiz/chat/dictionary history
#     :param mode: "general" for beginner questions, "personalized" for tailored ones
#     :param difficulty: "easy", "medium", or "hard"
#     :return: List of questions (multiple-choice, true/false, fill-in-the-blank)
#     """
#     if mode == "general":
#         prompt = (
#             f"Generate 5 {difficulty}-level finance questions. "
#             "Include a mix of multiple-choice, true/false, and fill-in-the-blank questions. "
#             "Each question should follow this format:\n"
#             "Type: <question_type>\n"
#             "Question: <question_text>\n"
#             "Options: <A) option1, B) option2, C) option3, D) option4> (only for multiple-choice)\n"
#             "Answer: <correct_answer>\n"
#             "Explanation: <explanation_of_the_answer>\n"
#         )
#     else:
#         prompt = (
#             f"Based on the user's history:\n{history_json}\n"
#             f"Generate 5 {difficulty}-level personalized finance questions. "
#             "Include a mix of multiple-choice, true/false, and fill-in-the-blank questions. "
#             "Each question should follow this format:\n"
#             "Type: <question_type>\n"
#             "Question: <question_text>\n"
#             "Options: <A) option1, B) option2, C) option3, D) option4> (only for multiple-choice)\n"
#             "Answer: <correct_answer>\n"
#             "Explanation: <explanation_of_the_answer>\n"
#         )

#     model = genai.GenerativeModel("gemini-1.5-pro-latest")

#     try:
#         response = model.generate_content(prompt)

#         if not response or not response.candidates:
#             return []

#         raw_text = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else ""

#         # Splitting response into structured questions
#         questions_list = raw_text.strip().split("\n\n")
#         questions = []

#         for q_text in questions_list:
#             lines = q_text.strip().split("\n")
#             if len(lines) < 4:
#                 continue  # Skip malformed questions

#             question_type = lines[0].replace("Type: ", "").strip()
#             question_text = lines[1].replace("Question: ", "").strip()
#             options = []
#             if question_type == "multiple-choice":
#                 options = [opt.strip() for opt in lines[2].replace("Options: ", "").split(",")]
#             correct_answer = lines[-2].replace("Answer: ", "").strip()
#             explanation = lines[-1].replace("Explanation: ", "").strip()

#             questions.append({
#                 "type": question_type,
#                 "question": question_text,
#                 "options": options,
#                 "answer": correct_answer,
#                 "explanation": explanation
#             })

#         return questions

#     except Exception as e:
#         st.error(f"Error fetching quiz questions: {str(e)}")
#         return []

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ STREAMLIT APP ~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # st.set_page_config(page_title="Finance Quiz App", page_icon="📊", layout="centered")

# # Main Page Layout
# st.title("📊 Finance Quiz App")
# st.markdown("**Improve your financial literacy through fun and engaging quizzes!**")

# # Initialize session state
# if "quiz_mode" not in st.session_state:
#     st.session_state.quiz_mode = "general"
# if "questions" not in st.session_state:
#     st.session_state.questions = []
# if "current_question" not in st.session_state:
#     st.session_state.current_question = 0
# if "quiz_history" not in st.session_state:
#     st.session_state.quiz_history = []
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "dictionary_searches" not in st.session_state:
#     st.session_state.dictionary_searches = []

# # Quiz Settings
# st.markdown("### Quiz Settings")
# col1, col2 = st.columns(2)
# with col1:
#     quiz_mode = st.radio("Choose Quiz Type:", ["General", "Personalized"])
# with col2:
#     difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

# # Consolidate all history into one JSON
# user_history = {
#     "quiz_answers": st.session_state.quiz_history,
#     "finance_gpt_queries": st.session_state.chat_history,
#     "searched_terms": st.session_state.dictionary_searches
# }
# history_json = json.dumps(user_history, indent=4)

# # Fetch new questions when quiz starts or settings change
# if not st.session_state.questions or st.session_state.quiz_mode != quiz_mode.lower():
#     with st.spinner("Fetching new quiz questions..."):
#         st.session_state.questions = get_quiz_questions(history_json, mode=quiz_mode.lower(), difficulty=difficulty.lower())
#         st.session_state.quiz_mode = quiz_mode.lower()
#         st.session_state.current_question = 0

# # Display questions
# if st.session_state.questions:
#     q_idx = st.session_state.current_question
#     question_data = st.session_state.questions[q_idx]

#     st.markdown("---")
#     st.markdown(f"### Question {q_idx + 1}")
#     st.markdown(f"**{question_data['question']}**")

#     if question_data["type"] == "multiple-choice":
#         selected_option = st.radio("Choose your answer:", question_data["options"], key=q_idx)
#     elif question_data["type"] == "true/false":
#         selected_option = st.radio("Choose your answer:", ["True", "False"], key=q_idx)
#     else:  # fill-in-the-blank
#         selected_option = st.text_input("Your answer:", key=q_idx)

#     if st.button("Submit Answer"):
#         correct = selected_option.lower() == question_data["answer"].lower()
#         if correct:
#             st.success("Correct! 🎉")
#         else:
#             st.error(f"Incorrect! The correct answer is: {question_data['answer']}.\n\n**Explanation:** {question_data['explanation']}")

#         # Store answer in history only for personalized mode
#         if st.session_state.quiz_mode == "personalized":
#             st.session_state.quiz_history.append({
#                 "question": question_data["question"],
#                 "selected": selected_option,
#                 "correct": correct
#             })

#     # Next Question button
#     if st.button("Next Question"):
#         if q_idx + 1 < len(st.session_state.questions):
#             st.session_state.current_question += 1
#             st.rerun()
#         else:
#             st.success("Quiz completed! 🎯")
#             st.session_state.questions = []  # Reset questions for a new quiz


# import streamlit as st
# import json
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ QUIZ QUESTIONS ~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# def get_quiz_questions(history_json, mode="general", difficulty="easy"):
#     """
#     Generates multiple-choice quiz questions using Gemini API.

#     :param history_json: JSON string of user quiz/chat/dictionary history
#     :param mode: "general" for beginner questions, "personalized" for tailored ones
#     :param difficulty: "easy", "medium", or "hard"
#     :return: List of multiple-choice questions
#     """
#     if mode == "general":
#         prompt = (
#             f"Generate 20 {difficulty}-level finance multiple-choice questions. "
#             "Each question should follow this format:\n"
#             "Question: <question_text>\n"
#             "A) <option1>\n"
#             "B) <option2>\n"
#             "C) <option3>\n"
#             "D) <option4>\n"
#             "Answer: <correct_option_letter>\n"
#             "Explanation: <explanation_of_the_answer>\n"
#         )
#     else:
#         prompt = (
#             f"Based on the user's history:\n{history_json}\n"
#             f"Generate 20 {difficulty}-level personalized finance multiple-choice questions. "
#             "Each question should follow this format:\n"
#             "Question: <question_text>\n"
#             "A) <option1>\n"
#             "B) <option2>\n"
#             "C) <option3>\n"
#             "D) <option4>\n"
#             "Answer: <correct_option_letter>\n"
#             "Explanation: <explanation_of_the_answer>\n"
#         )

#     model = genai.GenerativeModel("gemini-1.5-pro-latest")

#     try:
#         response = model.generate_content(prompt)

#         if not response or not response.candidates:
#             return []

#         raw_text = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else ""

#         # Splitting response into structured questions
#         questions_list = raw_text.strip().split("\n\n")
#         questions = []

#         for q_text in questions_list:
#             lines = q_text.strip().split("\n")
#             if len(lines) < 6:
#                 continue  # Skip malformed questions

#             question_text = lines[0].replace("Question: ", "").strip()
#             options = [lines[i].strip() for i in range(1, 5)]
#             correct_answer = lines[5].replace("Answer: ", "").strip()[0]  # Extract A, B, C, or D
#             explanation = lines[6].replace("Explanation: ", "").strip() if len(lines) > 6 else "No explanation provided."

#             questions.append({
#                 "question": question_text,
#                 "options": options,
#                 "answer": correct_answer,
#                 "explanation": explanation
#             })

#         return questions[:20]  # Limit to 20 questions

#     except Exception as e:
#         st.error(f"Error fetching quiz questions: {str(e)}")
#         return []

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~ STREAMLIT APP ~~~~~~~~~~~~~~~~~~~~
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# # st.set_page_config(page_title="Finance Quiz App", page_icon="📊", layout="centered")

# # Main Page Layout
# st.title("📊 Finance Quiz App")
# st.markdown("**Improve your financial literacy through fun and engaging quizzes!**")

# # Initialize session state
# if "quiz_mode" not in st.session_state:
#     st.session_state.quiz_mode = "general"
# if "questions" not in st.session_state:
#     st.session_state.questions = []
# if "current_question" not in st.session_state:
#     st.session_state.current_question = 0
# if "quiz_history" not in st.session_state:
#     st.session_state.quiz_history = []
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "dictionary_searches" not in st.session_state:
#     st.session_state.dictionary_searches = []
# if "score" not in st.session_state:
#     st.session_state.score = 0

# # Quiz Settings
# st.markdown("### Quiz Settings")
# col1, col2 = st.columns(2)
# with col1:
#     quiz_mode = st.radio("Choose Quiz Type:", ["General", "Personalized"])
# with col2:
#     difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])

# # Consolidate all history into one JSON
# user_history = {
#     "quiz_answers": st.session_state.quiz_history,
#     "finance_gpt_queries": st.session_state.chat_history,
#     "searched_terms": st.session_state.dictionary_searches
# }
# history_json = json.dumps(user_history, indent=4)

# # Fetch new questions when quiz starts or settings change
# if not st.session_state.questions or st.session_state.quiz_mode != quiz_mode.lower():
#     with st.spinner("Fetching new quiz questions..."):
#         st.session_state.questions = get_quiz_questions(history_json, mode=quiz_mode.lower(), difficulty=difficulty.lower())
#         st.session_state.quiz_mode = quiz_mode.lower()
#         st.session_state.current_question = 0
#         st.session_state.score = 0  # Reset score for new quiz

# # Display questions
# if st.session_state.questions:
#     q_idx = st.session_state.current_question
#     question_data = st.session_state.questions[q_idx]

#     st.markdown("---")
#     st.markdown(f"### Question {q_idx + 1} of 20")
#     st.markdown(f"**{question_data['question']}**")

#     selected_option = st.radio("Choose your answer:", question_data["options"], key=q_idx)

#     if st.button("Submit Answer"):
#         correct = selected_option.startswith(question_data["answer"])
#         if correct:
#             st.success("Correct! 🎉")
#             st.session_state.score += 1
#         else:
#             st.error(f"Incorrect! The correct answer is: {question_data['answer']}.\n\n**Explanation:** {question_data['explanation']}")

#         # Store answer in history only for personalized mode
#         if st.session_state.quiz_mode == "personalized":
#             st.session_state.quiz_history.append({
#                 "question": question_data["question"],
#                 "selected": selected_option,
#                 "correct": correct
#             })

#     # Next Question button
#     if st.button("Next Question"):
#         if q_idx + 1 < len(st.session_state.questions):
#             st.session_state.current_question += 1
#             st.rerun()
#         else:
#             st.success(f"Quiz completed! 🎯 Your final score is {st.session_state.score}/20.")
#             st.session_state.questions = []  # Reset questions for a new quiz
#             if st.button("Generate New Quiz"):
#                 st.session_state.questions = get_quiz_questions(history_json, mode=quiz_mode.lower(), difficulty=difficulty.lower())
#                 st.session_state.current_question = 0
#                 st.session_state.score = 0
#                 st.rerun()


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
            f"Based on the user's history:\n{history_json}\n"
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
<div>
    <h1 style="font-size:60px; color:white; text-align:center;">📊 Finance Quiz App</h1>
    <p style="text-align:center;">Test and expand your money knowledge with interactive quizzes! Choose between general financial concepts or personalized quizzes based on your profile.</p>
    <p style="text-align:center;">Adjust the difficulty to match your expertise level - perfect for beginners and experts alike. Each quiz helps you spot knowledge gaps while making finance fun!</p>
</div>
""", unsafe_allow_html=True)


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
