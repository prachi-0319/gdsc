# %%
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

# %%
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

text = extract_text_from_pdf("assets/the_total_money_makeover.pdf")

# %%
text

# %%
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([text])

# %%
embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
)

# %%
vectorstore = FAISS.from_documents(docs, embeddings_model)
vectorstore.save_local("faiss_index")

# %%
vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# %%
llm = ChatGroq(model="llama3-8b-8192")

# %%
retrieval_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# %%
def self_evaluate(input_text):
    parts = input_text.split("|||")
    query = parts[0]
    response = parts[1]
    sources = parts[2] if len(parts) > 2 else ""
    
    evaluation_prompt = f"""
    Evaluate the following response to the query:
    
    QUERY: {query}
    RESPONSE: {response}
    SOURCES: {sources}
    
    Assess based on:
    1. Factual accuracy (Does it match the sources?)
    2. Completeness (Does it address all aspects of the query?)
    3. Relevance (Is the information relevant to the query?)
    4. Hallucination (Does it contain information not supported by sources?)
    
    Return a confidence score from 0-10 and explanation.
    """
    
    evaluation = llm.predict(evaluation_prompt)
    return evaluation

# %%
tools = [
    Tool(
        name="Article Retrieval",
        func=lambda q: retrieval_qa_chain({"query": q})["result"],
        description="Retrieve knowledge from the article database."
    ),
]

# %%
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# %%
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# %%
def get_evaluated_response(query):
    response = agent.run(query)
    
    try:
        result = retrieval_qa_chain({"query": query})
        sources = [doc.page_content for doc in result.get("source_documents", [])]
        sources_text = "\n".join(sources)
    except Exception as e:
        sources_text = "No sources available"
    
    evaluation = self_evaluate(f"{query}|||{response}|||{sources_text}")
    
    return {
        "query": query,
        "response": response,
        "evaluation": evaluation,
        "sources": sources_text
    }

# %%
def transparent_response(query):
    result = get_evaluated_response(query)
    
    return f"""
    Response: {result['response']}
    
    Confidence assessment: {result['evaluation']}
    """

# %%
print(transparent_response("What are the myths about debt?"))

# %%
# %% Install dependencies
#pip install PyMuPDF langchain langchain_groq langchain_community faiss-cpu

# %% Import required libraries
import fitz  
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool

# %% Load LLM model
llm = ChatGroq(model="llama3-8b-8192")

# %% Function to extract structured text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    current_chapter = None

    for page in doc:
        page_text = page.get_text()
        
        # Detecting chapters using regex (adjust as per formatting)
        chapter_match = re.search(r'CHAPTER\s+\d+', page_text, re.IGNORECASE)
        if chapter_match:
            current_chapter = chapter_match.group(0)
        
        # Tagging text with chapter information
        if current_chapter:
            text += f"\n\n## {current_chapter}\n\n" + page_text

    return text

# %% Extract and preprocess text
pdf_path = "assets/how_finance_works.pdf"
text = extract_text_from_pdf(pdf_path)

# %% Chunk the extracted text for vector storage
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100, separators=["\n\n##", "\n\n"]
)
docs = text_splitter.create_documents([text])

# %% Load embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
)

# %% Store chunks in FAISS vector database
vectorstore = FAISS.from_documents(docs, embeddings_model)
vectorstore.save_local("faiss_index")

# %% Load stored FAISS vector database
vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# %% Function to retrieve relevant sections based on chapter and topic
def retrieve_chapter_topic(chapter, topic):
    query = f"Find information in {chapter} about {topic}."
    results = retriever.get_relevant_documents(query)
    
    # If results are insufficient, expand the search to the full document
    if len(results) < 3:
        results += retriever.get_relevant_documents(topic)
    
    return results

# %% Function to generate a structured lesson-style response
def teach_topic(chapter, topic):
    docs = retrieve_chapter_topic(chapter, topic)
    
    source_text = "\n".join([doc.page_content for doc in docs])

    teaching_prompt = f"""
    You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

    Format the response as:
    1. **Introduction** - Explain why this topic is important.
    2. **Key Concepts** - Define and explain the core ideas.
    3. **Real-World Examples** - Provide case studies or applications.
    4. **Common Misconceptions** - Address common misunderstandings.
    5. **Conclusion** - Summarize the key takeaways.

    Use the following reference material:
    {source_text}
    """

    response = llm.predict(teaching_prompt)
    return response

# %% Query function to get structured teaching response
def get_teaching_response(chapter, topic):
    response = teach_topic(chapter, topic)
    
    return f"""
    **Topic:** {topic}  
    **Chapter:** {chapter}  
    
    {response}
    """

# %% Example Query
print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))


# %%
Markdown(print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return")))

# %%
from IPython.display import Markdown
Markdown(print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return")))


# %%
# %% Install dependencies
# pip install PyMuPDF langchain langchain_groq langchain_community faiss-cpu

# %% Import required libraries
import fitz  
import re
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool

# %% Load LLM model
llm = ChatGroq(model="llama3-8b-8192")

# %% Function to extract structured text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    current_chapter = None

    for page in doc:
        page_text = page.get_text()
        
        # Detecting chapters using regex (adjust as per formatting)
        chapter_match = re.search(r'CHAPTER\s+\d+', page_text, re.IGNORECASE)
        if chapter_match:
            current_chapter = chapter_match.group(0)
        
        # Tagging text with chapter information
        if current_chapter:
            text += f"\n\n## {current_chapter}\n\n" + page_text

    return text

# %% Extract and preprocess text
# pdf_path = "assets/the_total_money_makeover.pdf"
pdf_path = "assets/how_finance_works.pdf"
text = extract_text_from_pdf(pdf_path)

# %% Chunk the extracted text for vector storage
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100, separators=["\n\n##", "\n\n"]
)
docs = text_splitter.create_documents([text])

# %% Load embedding model
embeddings_model = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-en",
    model_kwargs={'device': 'cpu'}  # Use 'cuda' if you have GPU
)

# %% Store chunks in FAISS vector database
#vectorstore = FAISS.from_documents(docs, embeddings_model)
#vectorstore.save_local("faiss_index")

# %% Load stored FAISS vector database
vectorstore = FAISS.load_local("faiss_index", embeddings_model, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()

# %% Function to retrieve relevant sections based on chapter and topic
def retrieve_chapter_topic(chapter, topic):
    query = f"Find information in {chapter} about {topic}."
    results = retriever.get_relevant_documents(query)
    
    # If results are insufficient, expand the search to the full document
    if len(results) < 3:
        results += retriever.get_relevant_documents(topic)
    
    return results

# %% Function to generate a structured lesson-style response in Markdown format
def teach_topic(chapter, topic):
    docs = retrieve_chapter_topic(chapter, topic)
    
    source_text = "\n".join([doc.page_content for doc in docs])

    teaching_prompt = f"""
    You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

    Format the response in Markdown as:
    # 📘 Topic: {topic}
    ## 📖 Chapter: {chapter}

    ### 🔹 **Introduction**
    Explain why this topic is important.

    ### 🔹 **Key Concepts**
    1. Define and explain the core ideas.
    2. Highlight important sub-concepts.

    ### 🔹 **Real-World Examples**
    - Provide case studies or applications.
    
    ### 🔹 **Common Misconceptions**
    ❌ Address misunderstandings or incorrect beliefs.
    
    ### 🔹 **Conclusion**
    Summarize the key takeaways.

    Use the following reference material:
    {source_text}
    """

    response = llm.predict(teaching_prompt)
    
    # Wrapping response in Markdown format
    markdown_response = f"```markdown\n{response}\n```"
    return markdown_response

# %% Query function to get structured Markdown output
def get_teaching_response(chapter, topic):
    response = teach_topic(chapter, topic)
    
    return response  # Already formatted in Markdown

# %% Example Query
print(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))


# %%
# Markdown(get_teaching_response("CHAPTER 4: Sources of Value Creation", "Risk and Return"))

# %%
# %% Function to generate a structured lesson-style response with a quiz in Markdown format
def teach_topic_with_quiz(chapter, topic):
    docs = retrieve_chapter_topic(chapter, topic)
    
    source_text = "\n".join([doc.page_content for doc in docs])

    teaching_prompt = f"""
    You are an expert finance professor. Teach the topic "{topic}" from "{chapter}" in a structured, engaging manner.

    **Strictly use finance and investment-related examples, avoiding personal finance cases.**

    Format the response in Markdown as:
    ```markdown
    # 📘 Topic: {topic}
    ## 📖 Chapter: {chapter}

    ### 🔹 **Introduction**
    Explain why this topic is important in financial decision-making.

    ### 🔹 **Key Concepts**
    1. Define and explain the core ideas.
    2. Highlight important sub-concepts related to finance and investing.

    ### 🔹 **Real-World Examples**
    - Provide case studies on **stock markets, corporate finance, risk management**.
    - Avoid personal finance examples like budgeting or debt repayment.

    ### 🔹 **Common Misconceptions**
    ❌ Address misunderstandings in finance and investing.

    ### 🔹 **Conclusion**
    Summarize key takeaways about risk-return tradeoff and decision-making.

    ---
    💡 *Key Takeaway:* A well-balanced approach to risk and return ensures financial stability.

    ---
    ## 📝 Quiz Time!
    - **Question 1:** What is the primary difference between systematic and unsystematic risk?  
    - **Question 2:** Which of the following investments has the highest risk: (A) Government Bonds, (B) Blue-chip Stocks, (C) Startups?  
    - **Question 3:** True or False: Diversification can completely eliminate all types of investment risk.  
    - **Question 4:** What is the risk-return tradeoff, and why is it important for investors?  

    ---
    ### ✅ **Quiz Answers**
    1. Systematic risk affects the entire market (e.g., economic downturns), while unsystematic risk is specific to a company or industry.  
    2. (C) Startups have the highest risk due to their uncertainty and volatility.  
    3. False – Diversification reduces risk but cannot eliminate market-wide risks.  
    4. The risk-return tradeoff is the balance between potential rewards and risks in investments; higher returns often come with higher risk.  

    ---
    📚 *Test your understanding and revise key concepts before moving ahead!*
    ```

    Use the following reference material:
    {source_text}
    """

    response = llm.predict(teaching_prompt)
    
    # Ensure Markdown format
    markdown_response = f"```markdown\n{response}\n```"
    return markdown_response

# %% Query function to get structured Markdown output with a quiz
def get_teaching_response_with_quiz(chapter, topic):
    response = teach_topic_with_quiz(chapter, topic)
    
    return response  # Already formatted in Markdown

# %% Example Query


# %%
# Markdown(get_teaching_response_with_quiz("CHAPTER 4: Sources of Value Creation", "Risk and Return"))

# %%



