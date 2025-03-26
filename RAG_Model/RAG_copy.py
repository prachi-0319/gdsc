# %%
import fitz  
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

# %%
import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Define the folder for FAISS indexes
FAISS_INDEX_FOLDER = "faiss_indexes"

# Create the folder if it doesn't exist
if not os.path.exists(FAISS_INDEX_FOLDER):
    os.makedirs(FAISS_INDEX_FOLDER)

# Function to get content from JSON file
def get_content_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data[0].get('content', 'No content key found')
    except FileNotFoundError:
        return "File not found"
    except json.JSONDecodeError:
        return "Invalid JSON format"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Initialize embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
)

# Text splitter configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100
)

# Function to process a single chapter
def process_chapter(chapter_num):
    # Define file path for JSON
    json_path = rf"Faiss_index\Chapter {chapter_num}.json"
    # Define full path for FAISS index
    index_path = os.path.join(FAISS_INDEX_FOLDER, f"faiss_index_chapter_{chapter_num}")
    
    # Get content from JSON
    text = get_content_from_file(json_path)
    
    if "Error" in text or "not found" in text:
        print(f"Failed to process Chapter {chapter_num}: {text}")
        return False
    
    # Create documents
    docs = text_splitter.create_documents([text])
    
    # Create and save FAISS index
    vectorstore = FAISS.from_documents(docs, embeddings_model)
    vectorstore.save_local(index_path)
    print(f"Successfully created FAISS index for Chapter {chapter_num} in {index_path}")
    return True

# Process all chapters (1 through 6)
def create_all_indexes():
    for chapter_num in range(1, 7):  # 1 to 6 inclusive
        process_chapter(chapter_num)

# Optional: Function to load and test a specific chapter's index
def load_and_test_index(chapter_num):
    index_path = os.path.join(FAISS_INDEX_FOLDER, f"faiss_index_chapter_{chapter_num}")
    try:
        vectorstore = FAISS.load_local(
            index_path, 
            embeddings_model, 
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever()
        print(f"Successfully loaded FAISS index for Chapter {chapter_num} from {index_path}")
        return retriever
    except Exception as e:
        print(f"Error loading index for Chapter {chapter_num}: {str(e)}")
        return None

# %%
llm = ChatGroq(model="llama3-8b-8192")

# %%
retriever = load_and_test_index(1)
retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# %%

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Text splitter configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100, 
    separators=["\n\n##", "\n\n"]
)

# Load embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
)

# Function to load the appropriate FAISS index for a given chapter
def load_chapter_vectorstore(chapter):
    # Convert chapter to a safe filename (e.g., "CHAPTER 4" -> "chapter_4")
    chapter_key = chapter.lower().replace(":", "").replace(" ", "_")
    index_path = f"faiss_indexes/faiss_index_{chapter_key}"
    print(index_path)
    
    try:
        vectorstore = FAISS.load_local(
            index_path, 
            embeddings_model, 
            allow_dangerous_deserialization=True
        )
        return vectorstore.as_retriever()
    except Exception as e:
        return f"Error loading FAISS index for {chapter}: {str(e)}"

# Function to retrieve relevant sections based on chapter and topic
def retrieve_chapter_topic(chapter, topic):
    retriever = load_chapter_vectorstore(chapter)
    
    if isinstance(retriever, str):  # Check if an error occurred
        return [retriever]  # Return error message as a list for consistency
    
    query = f"Find information in {chapter} about {topic}."
    results = retriever.get_relevant_documents(query)
    
    # If results are insufficient, we'll stick to chapter-specific search only
    # since we have separate indexes per chapter
    return results

# %%

def teach_topic_with_quiz(chapter, topic, year):
    docs = retrieve_chapter_topic(chapter, topic)
    
    source_text = "\n".join([doc.page_content for doc in docs])

    teaching_prompt = f"""
    You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner to a {year}-year-old student. Adapt the complexity of the explanations, language, and examples to be suitable for the student's age. Ensure all content is strictly derived from the reference material provided and is relevant to the specified topic and chapter.

    **Strictly use finance and investment-related examples, avoiding personal finance cases.**

    Format the response as:

    📖 Chapter: {chapter}
    📘 Topic: {topic}

    🔹 **Introduction**
    Explain why this topic is important in financial decision-making.

    🔹 **Key Concepts**
    1. Define and explain the core ideas.
    2. Highlight important sub-concepts related to finance and investing.

    🔹 **Real-World Examples**
    - Provide case studies on **stock markets, corporate finance, risk management**.
    - Avoid personal finance examples like budgeting or debt repayment.

    🔹 **Common Misconceptions**
    ❌ Address misunderstandings in finance and investing.

    🔹 **Conclusion**
    Summarize the key takeaways of the topic and its significance in finance.

    ---
    💡 *Key Takeaway:* [Provide a concise summary of the most important point about the topic.]
    ---

    📝 Quiz Time!
    Formulate quiz questions that are appropriate for a {year}-year-old student and are directly based on the reference material.

    ---
    ✅ **Quiz Answers**
    Provide answers strictly based on the reference material, and explain them in a way that a {year}-year-old student can understand.
    ---

    Use the following reference material:
    {source_text}
    """

    response = llm.predict(teaching_prompt)
    
    # Ensure Markdown format
    markdown_response = f"\n{response}\n"
    return markdown_response


# Query function to get structured Markdown output
def get_teaching_response_with_quiz(chapter, topic, year):
    response = teach_topic_with_quiz(chapter, topic, year)
    
    return response # Already formatted in Markdown




# %% [markdown]
# # 📖 Chapter: Chapter 1
# ## 📘 Topic:  Liabilities and Shareholders’ Equity
# 
# ### 🔹 **Introduction**
# In the world of finance, understanding liabilities and shareholders’ equity is crucial for making informed decisions. A company's financial health is directly linked to its ability to manage its liabilities and maintain a healthy balance between its assets and equity. This topic is vital in financial decision-making, as it helps investors, analysts, and financial professionals evaluate a company's financial performance, solvency, and growth potential.
# 
# ### 🔹 **Key Concepts**
# 
# 1. **Liabilities**: A liability is a debt or obligation that a company must pay or fulfill in the future. Examples of liabilities include loans, accounts payable, and accrued expenses.
# 2. **Shareholders’ Equity**: Shareholders’ equity represents the amount of money that shareholders have invested in a company, minus the amount of money the company has borrowed. It is also known as net worth or book value.
# 3. **Financial Leverage**: Financial leverage refers to the use of debt to amplify returns on equity. A higher level of financial leverage can increase a company's potential returns, but it also increases its risk of default.
# 
# ### 🔹 **Real-World Examples**
# 
# * **Case Study: Apple Inc.** Apple's liabilities include long-term debt and accounts payable. Its shareholders’ equity is primarily composed of common stock and retained earnings. By analyzing Apple's balance sheet, investors can gain insights into its financial health and potential for growth.
# * **Example: Risk Management** A company like Coca-Cola might use financial leverage to take on debt to fund expansion plans. However, if interest rates rise, the company's debt becomes more expensive, increasing its risk of default.
# 
# ### 🔹 **Common Misconceptions**
# 
# ❌ Don't confuse liabilities with assets. Liabilities are debts or obligations that must be paid, whereas assets are tangible or intangible resources that generate value.
# 
# ### 🔹 **Conclusion**
# In this topic, we've explored the importance of liabilities and shareholders’ equity in financial decision-making. Understanding these concepts is crucial for evaluating a company's financial performance, solvency, and growth potential. By analyzing a company's balance sheet and financial statements, investors and analysts can gain insights into its financial health and make informed decisions.
# 
# ---
# 💡 *Key Takeaway:* Liabilities and shareholders’ equity are critical components of a company's financial statements, and understanding them is essential for evaluating a company's financial performance and potential.
# 
# ---
# 
# ## 📝 Quiz Time!
# 1. What is the primary difference between liabilities and assets?
# a) Liabilities are debts, while assets are tangible resources.
# b) Liabilities are tangible resources, while assets are debts.
# c) Liabilities are intangible resources, while assets are tangible resources.
# d) Liabilities are assets, while assets are liabilities.
# 
# ---
# 
# ### ✅ **Quiz Answers**
# 1. a) Liabilities are debts, while assets are tangible resources.
# 
# ---
# 📚 *Test your understanding and revise key concepts before moving ahead!*

# %% [markdown]
# Chapter 1, Financial Analysis:
#     Assets
#     Liabilities and Shareholders’ Equity
#     Understanding Ratios
#     Profitability
#     Financing and Leverage
#     Productivity or Efficiency
#     Summary

# %% [markdown]
# Chapter 2, The Finance Perspective:
#     What We Talk about When We Talk about Cash
#     Net Profit, EBIT, and EBITDA
#     From EBITDA to Operating Cash Flows
#     Working capital, Accounts receivable, Inventory, Accounts payable
#     The cash conversion cycle
#       Free Cash Flows
#     Fixated on the  Future
#     Discounting
#     Summary

# %% [markdown]
# Chapter 3, The Financial Ecosystem:
#     Why  Can’t Finance Be  Simple?
#     The Companies
#     Buy Side:
#      Mutual funds
#      Pension funds. 
#      Foundations and endowment funds. 
#       Sovereign wealth funds.
#       Hedge funds
#     Sell Side:
#     Traders
#     Salespeople
#      Investment bankers
#     Incentives for Equity Analysts
#     The Problem at the Heart of Capital Markets
#     The Persistence of the Principal-Agent Problem
#     Summary

# %% [markdown]
# Chapter 4, Sources of Value Creation:
#     How Is Value Created?
#     What Else  Matters in Value Creation?
#     Three Ways to Create Value
#     A Deeper Dive into Costs of Capital
#      The cost of debt
#      Credit spreads.
#       Optimal capital structure
#        The cost of equity
#        What is risk? 
#         Calculating betas.
#         The price of risk
#         CAPM and the cost of equity
#         Common  Mistakes with WACC
#             Using the same cost of capital for all investments
#             Lowering your WACC by using more debt
#             Exporting WACC
#     Summary

# %% [markdown]
# Chapter 5, The Art and Science of Valuation:
#      Two Alternative Valuation Methods:
#         Multiples
#          The pros and cons of multiples
#         Problematic Methods for Assessing Value
#             Payback periods
#              Internal rates of return
#         Discounted Cash Flows
#             Free cash flows
#     Valuation  Mistakes
#         Ignoring Incentives
#         Exaggerating Synergies and Ignoring Integration Costs
#         Underestimating Capital Intensity
#     Summary
