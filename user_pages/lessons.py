# # %%
# # %%
# import fitz  
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.tools import Tool
# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq
# from langchain.agents import initialize_agent, Tool, AgentType
# from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain.memory import ConversationBufferMemory
# from langchain_community.embeddings import HuggingFaceEmbeddings
# import os

# # %%
# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = "\n".join([page.get_text() for page in doc])
#     return text

# text = extract_text_from_pdf("assets/the_total_money_makeover.pdf")

# # %%
# text

# # %%
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# docs = text_splitter.create_documents([text])

# # %%
# embeddings_model = HuggingFaceEmbeddings(
#     model_name="jinaai/jina-embeddings-v2-base-en",
#     model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
# )

# # %%
# vectorstore = FAISS.from_documents(docs, embeddings_model)
# vectorstore.save_local("faiss_index")

# # %%
# vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
# retriever = vectorstore.as_retriever()

# # %%
# llm = ChatGroq(model="llama3-8b-8192")

# # %%
# retrieval_qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     return_source_documents=True
# )

# # %%
# def self_evaluate(input_text):
#     parts = input_text.split("|||")
#     query = parts[0]
#     response = parts[1]
#     sources = parts[2] if len(parts) > 2 else ""
    
#     evaluation_prompt = f"""
#     Evaluate the following response to the query:
    
#     QUERY: {query}
#     RESPONSE: {response}
#     SOURCES: {sources}
    
#     Assess based on:
#     1. Factual accuracy (Does it match the sources?)
#     2. Completeness (Does it address all aspects of the query?)
#     3. Relevance (Is the information relevant to the query?)
#     4. Hallucination (Does it contain information not supported by sources?)
    
#     Return a confidence score from 0-10 and explanation.
#     """
    
#     evaluation = llm.predict(evaluation_prompt)
#     return evaluation

# # %%
# tools = [
#     Tool(
#         name="Article Retrieval",
#         func=lambda q: retrieval_qa_chain({"query": q})["result"],
#         description="Retrieve knowledge from the article database."
#     ),
# ]

# # %%
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# # %%
# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     memory=memory
# )

# # %%
# def get_evaluated_response(query):
#     response = agent.run(query)
    
#     try:
#         result = retrieval_qa_chain({"query": query})
#         sources = [doc.page_content for doc in result.get("source_documents", [])]
#         sources_text = "\n".join(sources)
#     except Exception as e:
#         sources_text = "No sources available"
    
#     evaluation = self_evaluate(f"{query}|||{response}|||{sources_text}")
    
#     return {
#         "query": query,
#         "response": response,
#         "evaluation": evaluation,
#         "sources": sources_text
#     }

# # %%
# def transparent_response(query):
#     result = get_evaluated_response(query)
    
#     return f"""
#     Response: {result['response']}
    
#     Confidence assessment: {result['evaluation']}
#     """

# # %%
# print(transparent_response("What are the myths about debt?"))

# # %%
# # %% Install dependencies
# #pip install PyMuPDF langchain langchain_groq langchain_community faiss-cpu

# # %% Import required libraries
# import fitz  
# import re
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq
# from langchain.memory import ConversationBufferMemory
# from langchain.agents import initialize_agent, AgentType, Tool

# # %% Load LLM model
# llm = ChatGroq(model="llama3-8b-8192")

# # %% Function to extract structured text from PDF
# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     current_chapter = None

#     for page in doc:
#         page_text = page.get_text()
        
#         # Detecting chapters using regex (adjust as per formatting)
#         chapter_match = re.search(r'CHAPTER\s+\d+', page_text, re.IGNORECASE)
#         if chapter_match:
#             current_chapter = chapter_match.group(0)
        
#         # Tagging text with chapter information
#         if current_chapter:
#             text += f"\n\n## {current_chapter}\n\n" + page_text

#     return text

# # %% Extract and preprocess text
# pdf_path = "assets/how_finance_works.pdf"
# text = extract_text_from_pdf(pdf_path)

# # %% Chunk the extracted text for vector storage
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=100, separators=["\n\n##", "\n\n"]
# )
# docs = text_splitter.create_documents([text])

# # %% Load embedding model
# embeddings_model = HuggingFaceEmbeddings(
#     model_name="jinaai/jina-embeddings-v2-base-en",
#     model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
# )

# # %% Store chunks in FAISS vector database
# vectorstore = FAISS.from_documents(docs, embeddings_model)
# vectorstore.save_local("faiss_index")

# # %% Load stored FAISS vector database
# vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
# retriever = vectorstore.as_retriever()

# # %% Function to retrieve relevant sections based on chapter and topic
# def retrieve_chapter_topic(chapter, topic):
#     query = f"Find information in {chapter} about {topic}."
#     results = retriever.get_relevant_documents(query)
    
#     # If results are insufficient, expand the search to the full document
#     if len(results) < 3:
#         results += retriever.get_relevant_documents(topic)
    
#     return results

# # %% Function to generate a structured lesson-style response
# def teach_topic(chapter, topic):
#     docs = retrieve_chapter_topic(chapter, topic)
    
#     source_text = "\n".join([doc.page_content for doc in docs])

#     teaching_prompt = f"""
#     You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

#     Format the response as:
#     1. **Introduction** - Explain why this topic is important.
#     2. **Key Concepts** - Define and explain the core ideas.
#     3. **Real-World Examples** - Provide case studies or applications.
#     4. **Common Misconceptions** - Address common misunderstandings.
#     5. **Conclusion** - Summarize the key takeaways.

#     Use the following reference material:
#     {source_text}
#     """

#     response = llm.predict(teaching_prompt)
#     return response

# # %% Query function to get structured teaching response
# def get_teaching_response(chapter, topic):
#     response = teach_topic(chapter, topic)
    
#     return f"""
#     **Topic:** {topic}  
#     **Chapter:** {chapter}  
    
#     {response}
#     """

# # %% Example Query
# print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))


# # %%
# Markdown(print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return")))

# # %%
# from IPython.display import Markdown
# Markdown(print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return")))


# # %%
# # %% Install dependencies
# # pip install PyMuPDF langchain langchain_groq langchain_community faiss-cpu

# # %% Import required libraries
# import fitz  
# import re
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain_groq import ChatGroq
# from langchain.memory import ConversationBufferMemory
# from langchain.agents import initialize_agent, AgentType, Tool

# # %% Load LLM model
# llm = ChatGroq(model="llama3-8b-8192")

# # %% Function to extract structured text from PDF
# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     current_chapter = None

#     for page in doc:
#         page_text = page.get_text()
        
#         # Detecting chapters using regex (adjust as per formatting)
#         chapter_match = re.search(r'CHAPTER\s+\d+', page_text, re.IGNORECASE)
#         if chapter_match:
#             current_chapter = chapter_match.group(0)
        
#         # Tagging text with chapter information
#         if current_chapter:
#             text += f"\n\n## {current_chapter}\n\n" + page_text

#     return text

# # %% Extract and preprocess text
# # pdf_path = "assets/the_total_money_makeover.pdf"
# pdf_path = "assets/how_finance_works.pdf"
# text = extract_text_from_pdf(pdf_path)

# # %% Chunk the extracted text for vector storage
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=100, separators=["\n\n##", "\n\n"]
# )
# docs = text_splitter.create_documents([text])

# # %% Load embedding model
# embeddings_model = HuggingFaceEmbeddings(
#     model_name="jinaai/jina-embeddings-v2-base-en",
#     model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
# )

# # %% Store chunks in FAISS vector database
# #vectorstore = FAISS.from_documents(docs, embeddings_model)
# #vectorstore.save_local("faiss_index")

# # %% Load stored FAISS vector database
# vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
# retriever = vectorstore.as_retriever()

# # %% Function to retrieve relevant sections based on chapter and topic
# def retrieve_chapter_topic(chapter, topic):
#     query = f"Find information in {chapter} about {topic}."
#     results = retriever.get_relevant_documents(query)
    
#     # If results are insufficient, expand the search to the full document
#     if len(results) < 3:
#         results += retriever.get_relevant_documents(topic)
    
#     return results

# # %% Function to generate a structured lesson-style response in Markdown format
# def teach_topic(chapter, topic):
#     docs = retrieve_chapter_topic(chapter, topic)
    
#     source_text = "\n".join([doc.page_content for doc in docs])

#     teaching_prompt = f"""
#     You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

#     Format the response in Markdown as:
#     # 📘 Topic: {topic}
#     ## 📖 Chapter: {chapter}

#     ### 🔹 **Introduction**
#     Explain why this topic is important.

#     ### 🔹 **Key Concepts**
#     1. Define and explain the core ideas.
#     2. Highlight important sub-concepts.

#     ### 🔹 **Real-World Examples**
#     - Provide case studies or applications.
    
#     ### 🔹 **Common Misconceptions**
#     ❌ Address misunderstandings or incorrect beliefs.
    
#     ### 🔹 **Conclusion**
#     Summarize the key takeaways.

#     Use the following reference material:
#     {source_text}
#     """

#     response = llm.predict(teaching_prompt)
    
#     # Wrapping response in Markdown format
#     markdown_response = f"```markdown\n{response}\n```"
#     return markdown_response

# # %% Query function to get structured Markdown output
# def get_teaching_response(chapter, topic):
#     response = teach_topic(chapter, topic)
    
#     return response  # Already formatted in Markdown

# # %% Example Query
# print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))


# # %%
# # Markdown(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))

# # %%
# # %% Function to generate a structured lesson-style response with a quiz in Markdown format
# def teach_topic_with_quiz(chapter, topic):
#     docs = retrieve_chapter_topic(chapter, topic)
    
#     source_text = "\n".join([doc.page_content for doc in docs])

#     teaching_prompt = f"""
#     You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

#     **Strictly use finance and investment-related examples, avoiding personal finance cases.**

#     Format the response in Markdown as:
#     ```markdown
#     # 📘 Topic: {topic}
#     ## 📖 Chapter: {chapter}

#     ### 🔹 **Introduction**
#     Explain why this topic is important in financial decision-making.

#     ### 🔹 **Key Concepts**
#     1. Define and explain the core ideas.
#     2. Highlight important sub-concepts related to finance and investing.

#     ### 🔹 **Real-World Examples**
#     - Provide case studies on **stock markets, corporate finance, risk management**.
#     - Avoid personal finance examples like budgeting or debt repayment.

#     ### 🔹 **Common Misconceptions**
#     ❌ Address misunderstandings in finance and investing.

#     ### 🔹 **Conclusion**
#     Summarize key takeaways about risk-return tradeoff and decision-making.

#     ---
#     💡 *Key Takeaway:* A well-balanced approach to risk and return ensures financial stability.

#     ---
#     ## 📝 Quiz Time!
#     - **Question 1:** What is the primary difference between systematic and unsystematic risk?  
#     - **Question 2:** Which of the following investments has the highest risk: (A) Government Bonds, (B) Blue-chip Stocks, (C) Startups?  
#     - **Question 3:** True or False: Diversification can completely eliminate all types of investment risk.  
#     - **Question 4:** What is the risk-return tradeoff, and why is it important for investors?  

#     ---
#     ### ✅ **Quiz Answers**
#     1. Systematic risk affects the entire market (e.g., economic downturns), while unsystematic risk is specific to a company or industry.  
#     2. (C) Startups have the highest risk due to their uncertainty and volatility.  
#     3. False – Diversification reduces risk but cannot eliminate market-wide risks.  
#     4. The risk-return tradeoff is the balance between potential rewards and risks in investments; higher returns often come with higher risk.  

#     ---
#     📚 *Test your understanding and revise key concepts before moving ahead!*
#     ```

#     Use the following reference material:
#     {source_text}
#     """

#     response = llm.predict(teaching_prompt)
    
#     # Ensure Markdown format
#     markdown_response = f"```markdown\n{response}\n```"
#     return markdown_response

# # %% Query function to get structured Markdown output with a quiz
# def get_teaching_response_with_quiz(chapter, topic):
#     response = teach_topic_with_quiz(chapter, topic)
    
#     return response  # Already formatted in Markdown

# # %% Example Query


# # %%
# # Markdown(get_teaching_response_with_quiz("CHAPTER 4: Sources of Value Creation", "Risk and Return"))

# # %%



import streamlit as st
from RAG_Model.RAG_copy import get_teaching_response_with_quiz

# Set page configuration
# st.set_page_config(
#     page_title="Finance Master",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# Dark Mode Professional Custom CSS
# st.markdown("""
#     <style>
#         /* Header Styling */
#         .header-text {
#             color: #4ecdc4;
#             text-align: center;
#             font-weight: 700;
#             margin-bottom: 20px;
#         }

#         .section-header {
#             color: #4ecdc4;
#             border-bottom: 2px solid #45b7d1;
#             padding-bottom: 10px;
#             margin-bottom: 20px;
#         }

#         /* Container Styling */
#         .stContainer {
#             background-color: #1e1e1e;
#             border-radius: 12px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
#             padding: 25px;
#             margin-bottom: 20px;
#             border: 1px solid #2c2c2c;
#         }

#         /* Learning Path Visualization */
#         .path-container {
#             background-color: #1e1e1e;
#             border-radius: 12px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
#             padding: 30px;
#             margin-top: 20px;
#             border: 1px solid #2c2c2c;
#         }

#         .chapter-node {
#             text-align: center;
#             transition: all 0.3s ease;
#             color: #e0e0e0;
#         }

#         .chapter-node.active {
#             transform: scale(1.05);
#         }

#         .node-circle {
#             width: 50px;
#             height: 50px;
#             border-radius: 50%;
#             background-color: #2c2c2c;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             margin: 0 auto 10px;
#             font-weight: bold;
#             color: #4ecdc4;
#             transition: all 0.3s ease;
#             border: 2px solid #45b7d1;
#         }

#         .chapter-node.active .node-circle {
#             background-color: #45b7d1;
#             color: #121212;
#             box-shadow: 0 4px 6px rgba(69, 183, 209, 0.3);
#         }

#         .connector-line {
#             height: 3px;
#             background-color: #2c2c2c;
#             flex-grow: 1;
#             margin: 25px -10px;
#         }

#         .subtopic-list {
#             margin-top: 30px;
#             background-color: #1a1a1a;
#             border-radius: 8px;
#             padding: 20px;
#             border: 1px solid #2c2c2c;
#         }

#         .subtopic-item {
#             margin: 10px 0;
#             padding: 8px 15px;
#             border-radius: 6px;
#             transition: all 0.3s ease;
#             color: #b0b0b0;
#         }

#         .subtopic-item.active {
#             background-color: #45b7d1;
#             color: #121212;
#             font-weight: 600;
#         }

#         /* Streamlit Widget Styling */
#         .stTextInput>div>div>input,
#         .stNumberInput>div>div>input,
#         .stSelectbox>div>div>select {
#             background-color: #1e1e1e !important;
#             color: #e0e0e0 !important;
#             border: 1px solid #2c2c2c !important;
#         }

#         /* Button Styling */
#         .stButton>button {
#             background-color: #45b7d1;
#             color: #121212;
#             border: none;
#             border-radius: 8px;
#             font-weight: 600;
#             transition: all 0.3s ease;
#         }

#         .stButton>button:hover {
#             background-color: #4ecdc4;
#             transform: translateY(-2px);
#             box-shadow: 0 4px 6px rgba(69, 183, 209, 0.3);
#         }

#         /* Result Box */
#         .result-box {
#             background-color: #1e1e1e;
#             border-radius: 12px;
#             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
#             padding: 25px;
#             margin-top: 20px;
#             border: 1px solid #2c2c2c;
#             color: #e0e0e0;
#         }

#         /* Footer */
#         .footer {
#             color: #b0b0b0;
#             text-align: center;
#             padding: 20px;
#             background-color: #1a1a1a;
#             border-top: 1px solid #2c2c2c;
#         }

#         /* Markdown Styling */
#         .stMarkdown {
#             color: #e0e0e0;
#         }
#         .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
#             color: #4ecdc4;
#         }
#     </style>
# """, unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Container Styling */
        .stContainer {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid #2c2c2c;
        }

        /* Learning Path Visualization */
        .path-container {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 30px;
            margin-top: 20px;
            border: 1px solid #2c2c2c;
        }

        .chapter-node {
            text-align: center;
            transition: all 0.3s ease;
            color: #e0e0e0;
        }

        .chapter-node.active {
            transform: scale(1.05);
        }

        .node-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #2c2c2c;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-weight: bold;
            color: #4ecdc4;
            transition: all 0.3s ease;
            border: 2px solid #45b7d1;
        }

        .chapter-node.active .node-circle {
            background-color: #45b7d1;
            color: #121212;
            box-shadow: 0 4px 6px rgba(69, 183, 209, 0.3);
        }

        .connector-line {
            height: 3px;
            background-color: #2c2c2c;
            flex-grow: 1;
            margin: 25px -10px;
        }

        .subtopic-list {
            margin-top: 30px;
            background-color: #1a1a1a;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #2c2c2c;
        }

        .subtopic-item {
            margin: 10px 0;
            padding: 8px 15px;
            border-radius: 6px;
            transition: all 0.3s ease;
            color: #b0b0b0;
        }

        .subtopic-item.active {
            background-color: #45b7d1;
            color: #121212;
            font-weight: 600;
        }

            
        /* Streamlit Widget Styling */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
            border: 1px solid #2c2c2c !important;
        }

        /* Result Box */
        .result-box {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 25px;
            margin-top: 20px;
            border: 1px solid #2c2c2c;
            color: #e0e0e0;
        }

        /* Footer */
        .footer {
            color: #b0b0b0;
            text-align: center;
            padding: 20px;
            background-color: #1a1a1a;
            border-top: 1px solid #2c2c2c;
        }
            
    </style>
""", unsafe_allow_html=True)


# Chapter data remains the same
chapters = {
    "Chapter 1": [
        "Assets",
        "Liabilities and Shareholders' Equity",
        "Understanding Ratios",
        "Profitability",
        "Financing and Leverage",
        "Productivity or Efficiency",
        "Summary"
    ],
    "Chapter 2": [
        "What We Talk about When We Talk about Cash",
        "Net Profit, EBIT, and EBITDA",
        "From EBITDA to Operating Cash Flows",
        "Working capital, Accounts receivable, Inventory, Accounts payable",
        "The cash conversion cycle",
        "Free Cash Flows",
        "Fixated on the Future",
        "Discounting",
        "Summary"
    ],
    "Chapter 3": [
        "Why Can't Finance Be Simple?",
        "The Companies",
        "Buy Side:",
        "Mutual funds",
        "Pension funds.",
        "Foundations and endowment funds.",
        "Sovereign wealth funds.",
        "Hedge funds",
        "Sell Side:",
        "Traders",
        "Salespeople",
        "Investment bankers",
        "Incentives for Equity Analysts",
        "The Problem at the Heart of Capital Markets",
        "The Persistence of the Principal-Agent Problem",
        "Summary"
    ],
    "Chapter 4": [
        "How Is Value Created?",
        "What Else Matters in Value Creation?",
        "Three Ways to Create Value",
        "A Deeper Dive into Costs of Capital",
        "The cost of debt",
        "Credit spreads.",
        "Optimal capital structure",
        "The cost of equity",
        "What is risk?",
        "Calculating betas.",
        "The price of risk",
        "CAPM and the cost of equity",
        "Common Mistakes with WACC",
        "Using the same cost of capital for all investments",
        "Lowering your WACC by using more debt",
        "Exporting WACC",
        "Summary"
    ],
    "Chapter 5": [
        "Two Alternative Valuation Methods:",
        "Multiples",
        "The pros and cons of multiples",
        "Problematic Methods for Assessing Value",
        "Payback periods",
        "Internal rates of return",
        "Discounted Cash Flows",
        "Free cash flows",
        "Valuation Mistakes",
        "Ignoring Incentives",
        "Exaggerating Synergies and Ignoring Integration Costs",
        "Underestimating Capital Intensity",
        "Summary"
    ]
}
 # (Keep the original chapters dictionary here)

chapter_options = [
    "Chapter 1: Financial Analysis",
    "Chapter 2: The Finance Perspective",
    "Chapter 3: The Financial Ecosystem",
    "Chapter 4: Sources of Value Creation",
    "Chapter 5: The Art and Science of Valuation"
]  # (Keep the original chapter options here)


st.markdown("""
<div class="profile-header">
    <h1 style="font-size:55px; color:white; text-align:center;">📚 Finance Learning Companion</h1>
    <p style="text-align:center;">Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
    to create a balanced portfolio allocation tailored to your specific needs.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("")
st.markdown("")


col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📖 Choose Your Learning Path")

    selected_chapter_full = st.selectbox(
        "**Select Chapter**",
        chapter_options,
        index=0,
        help="Choose which financial concept you want to explore"
    )
    chapter_key = selected_chapter_full.split(":")[0]

    subtopics = chapters[chapter_key]
    selected_subtopic = st.selectbox(
        "**Select Subtopic**",
        subtopics,
        index=0,
        help="Pick a specific aspect to focus on"
    )

with col2:
    st.markdown("### 🎯 Personalize Your Experience")

    age = st.number_input(
        "**Your Age**",
        min_value=10,
        max_value=100,
        value=20,
        step=1,
        help="We'll adapt the content complexity based on your age"
    )
    st.markdown("")
    
    
    generate_btn = st.button(
        "🚀 Generate Learning Content",
        # use_container_width=True,
        type="primary"
    )


# # Selection section
# with st.container():
#     st.markdown('<h2 class="section-header">📖 Choose Your Learning Path</h2>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([1, 1], gap="medium")
#     with col1:
#         selected_chapter_full = st.selectbox(
#             "**Select Chapter**",
#             chapter_options,
#             index=0,
#             help="Choose which financial concept you want to explore"
#         )
#         chapter_key = selected_chapter_full.split(":")[0]
    
#     with col2:
#         subtopics = chapters[chapter_key]
#         selected_subtopic = st.selectbox(
#             "**Select Subtopic**",
#             subtopics,
#             index=0,
#             help="Pick a specific aspect to focus on"
#         )

# st.markdown("---")

# Personalization section
# with st.container():
#     st.markdown('<h2 class="section-header">🎯 Personalize Your Experience</h2>', unsafe_allow_html=True)
#     age = st.number_input(
#         "**Your Age**",
#         min_value=10,
#         max_value=100,
#         value=20,
#         step=1,
#         help="We'll adapt the content complexity based on your age"
#     )

# st.markdown("---")

# # Generate button
# generate_col, _ = st.columns([0.3, 0.7])
# with generate_col:
#     generate_btn = st.button(
#         "🚀 Generate Learning Content",
#         use_container_width=True,
#         type="primary"
#     )


# Result display
if generate_btn:
    with st.spinner("✨ Crafting your personalized learning experience..."):
        try:
            result = get_teaching_response_with_quiz(chapter_key, selected_subtopic, str(age))
            
            with st.container():
                st.markdown("---")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                st.markdown("### 📝 Teaching Content")
                if "### Quiz" in result:
                    teaching_content = result.split("### Quiz")[0]
                    quiz_content = "### ❓ Quiz\n" + result.split("### Quiz")[1]
                else:
                    teaching_content = result
                    quiz_content = ""
                
                st.markdown(teaching_content)
                
                if quiz_content:
                    st.markdown("### 📝 Teaching Content")
                    st.markdown(quiz_content)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"⚠️ Error generating content: {str(e)}")
else:
    st.markdown("""
        <div style='text-align: center; margin: 50px 0; color: #7f8c8d;'>
            Select your preferences above and click "Generate" to begin
        </div>
    """, unsafe_allow_html=True)




st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")

st.markdown('<h2 class="section-header">🗺️ Your Learning Path</h2>', unsafe_allow_html=True)

# Create the learning path visualization
with st.container():
    st.markdown('<div class="path-container">', unsafe_allow_html=True)
    
    # Create chapter nodes
    cols = st.columns(len(chapter_options) * 2 - 1)
    chapter_index = list(chapters.keys()).index(chapter_key)
    
    for i, chapter in enumerate(chapter_options):
        col_idx = i * 2
        is_active = (chapter.split(":")[0] == chapter_key)
        
        with cols[col_idx]:
            st.markdown(f'<div class="chapter-node {"active" if is_active else ""}">'
                        f'<div class="node-circle">{i+1}</div>'
                        f'<div>{"<b>" if is_active else ""}{chapter.split(":")[0]}'
                        f'{"</b>" if is_active else ""}</div></div>', 
                        unsafe_allow_html=True)
        
        # Add connector line after each chapter except last
        if i < len(chapter_options) - 1:
            with cols[col_idx + 1]:
                st.markdown('<div class="connector-line"></div>', unsafe_allow_html=True)
    
    # Add subtopic progression
    st.markdown(f'<div class="subtopic-list">', unsafe_allow_html=True)
    for subtopic in chapters[chapter_key]:
        is_active_sub = (subtopic == selected_subtopic)
        st.markdown(f'<div class="subtopic-item {"active" if is_active_sub else ""}">'
                    f'{subtopic}</div>', 
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)