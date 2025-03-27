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
import json

def get_chapter_path(chapter_key):
    chapter_list = ['faiss_indexes/faiss_index_chapter_1',
                    'faiss_indexes/faiss_index_chapter_2',
                    'faiss_indexes/faiss_index_chapter_3',
                    'faiss_indexes/faiss_index_chapter_4',
                    'faiss_indexes/faiss_index_chapter_5',
                    'faiss_indexes/faiss_index_chapter_6']
    index = int(chapter_key[-1])
    return chapter_list[index-1]

load_dotenv()
FAISS_INDEX_FOLDER = "faiss_indexes"
def load_chapter_vectorstore(chapter):
    embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
    )
    # Convert chapter to a safe filename (e.g., "CHAPTER 4" -> "chapter_4")
    chapter_key = chapter.lower().replace(":", "").replace(" ", "_")
    cwd_path = os.getcwd()
    print(cwd_path)
    index_path = cwd_path + '\\RAG_Model\\' +  get_chapter_path(chapter_key)
    #index_path = os.path.join(cwd_path,'RAG_Model',get_chapter_path(chapter_key))
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
    llm = ChatGroq(model="llama3-8b-8192", api_key = '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')
    docs = retrieve_chapter_topic(chapter, topic)
    print(type(docs[0]))
    print(docs)
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