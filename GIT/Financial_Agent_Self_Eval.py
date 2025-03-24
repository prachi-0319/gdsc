# %%
# %%
import os
import json
import getpass
import operator
from enum import Enum
from dataclasses import dataclass, fields
from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from PIL import Image
import requests
from io import BytesIO
import base64

from langsmith import traceable
# IPython for display (if needed)
from IPython.display import Image, display, Markdown

# Import LangChain and related tools
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda, RunnableBranch
from langchain_core.tools import tool, StructuredTool
from langchain_core import tools  # if needed
from langchain_core.runnables import RunnableConfig

# For financial data via yfinance
import os
from openai import OpenAI
import yfinance as yf

# For web search and HTML parsing
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

# For environment variables
from dotenv import load_dotenv

# For YouTube video recommendations
import googleapiclient.discovery
import googleapiclient.errors

# For state graph
from langgraph.graph import StateGraph, START, END
from tavily import TavilyClient

# %%
load_dotenv()

# %%
language = 'telugu'

# %%
llm = ChatGroq(model_name='Gemma2-9b-it', api_key=os.getenv('GROQ_API_KEY'))

# %%
query_writer_instruction_web = """Your goal is to generate a targeted web search query related to financial investments or any finance-related topic specified by the user.

<TOPIC>
{finance_topic}
</TOPIC>

<FORMAT>
Format your response as a JSON object with ALL three of these exact keys:
   - "query": The actual search query string
   - "aspect": The specific aspect of the finance topic being researched
   - "rationale": Brief explanation of why this query is relevant
</FORMAT>

<EXAMPLE>
Example output:
{{
    "query": "best index funds for long-term investment 2025",
    "aspect": "investment strategy",
    "rationale": "Identifying top-performing index funds for long-term portfolio growth"
}}
</EXAMPLE>

Provide your response in JSON format:
"""

summarizer_instruction_web = """<GOAL>
Generate a high-quality summary of the web search results, focusing on financial investments or the specific finance-related topic requested by the user. REMEMBER TO ANSWER IN {language} LANGUAGE.
</GOAL>

<REQUIREMENTS>
When creating a NEW summary:
1. Highlight the most relevant financial insights, trends, or strategies from the search results.
2. Ensure a coherent flow of information while keeping it concise and actionable.

When EXTENDING an existing summary:
1. Read the existing summary and new search results carefully.
2. Compare the new information with the existing summary.
3. For each piece of new information:
    a. If it builds on an existing point, integrate it smoothly.
    b. If it introduces a new relevant aspect, add a separate paragraph.
    c. If it's irrelevant to financial investments, ignore it.
4. Ensure all additions align with the user's finance-related query.
5. Verify that the final output differs from the original summary while improving its depth.

<FORMATTING>
- Start directly with the updated summary, without preamble or titles. Do not use XML tags in the output.
</FORMATTING>
"""

reflection_instructions_web = """You are an expert financial research assistant analyzing a summary about {finance_topic}.

<GOAL>
1. Identify missing details or areas that need deeper exploration.
2. Generate a follow-up question to help expand financial knowledge.
3. Focus on investment strategies, market trends, risk factors, regulations, or financial instruments that weren't fully covered.
</GOAL>

<REQUIREMENTS>
Ensure the follow-up question is self-contained and provides necessary context for a web search.
</REQUIREMENTS>

<FORMAT>
Format your response as a JSON object with these exact keys:
- "knowledge_gap": Describe what financial information is missing or unclear.
- "follow_up_query": Write a specific question to address this gap.
</FORMAT>

<EXAMPLE>
Example output:
{{
    "knowledge_gap": "The summary does not mention tax implications of investing in ETFs vs. mutual funds.",
    "follow_up_query": "What are the tax advantages and disadvantages of ETFs compared to mutual funds?"
}}
</EXAMPLE>

Provide your analysis in JSON format:
"""

# %%
class State(TypedDict):
    route: Literal['Web_query', 'Normal_query', 'Financial_Analysis', 'YouTube_Recommender', 'Image_Analysis']
    research_topic: str
    search_query: str
    web_research_results: List[str]
    news_sources: List[Dict[str, str]]  # e.g., [{"title": "", "url": ""}]
    research_loop_count: int
    text_output: str  # Main text response accumulated across nodes
    image: List[str]
    image_processed: bool
    messages: List[Any]
    graphs: List[str]  # List of Plotly JSON strings
    youtube_recommendations: List[Dict[str, str]]  # e.g., [{"title": "", "url": "", "channel": ""}]

# %%
def create_initial_state(user_query: str, image: List[str] = []) -> State:
    return {
        "route": None,
        "research_topic": user_query,
        "search_query": "",
        "web_research_results": [],
        "news_sources": [],
        "research_loop_count": 0,
        "text_output": "",
        "image": image,
        "image_processed": False,
        "messages": [HumanMessage(content=user_query)],
        "graphs": [],
        "youtube_recommendations": []
    }

# %%
class Route_First_Step(BaseModel):
    step: Literal['Web_query', 'Normal_query', 'Financial_Analysis', 'YouTube_Recommender', 'Plot_Data'] = Field(
        None,
        description='Determine whether to perform a web search, answer a normal question, perform a financial analysis, recommend YouTube videos, or generate a plot'
    )

# %%
class SearchAPI(Enum):
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"

@dataclass(kw_only=True)
class Configuration:
    max_web_research_loops: int = int(os.environ.get("MAX_WEB_RESEARCH_LOOPS", "3"))
    search_api: SearchAPI = SearchAPI(os.environ.get("SEARCH_API", "tavily"))
    fetch_full_page: bool = os.environ.get("FETCH_FULL_PAGE", "False").lower() in ("true", "1", "t")
    ollama_base_url: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/")

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        configurable = config["configurable"] if config and "configurable" in config else {}
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

# %%
@traceable
def tavily_search(query, include_raw_content=True, max_results=3):
    api_key = os.environ['TAVILY_API_KEY']
    if not api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not set")
    tavily_client = TavilyClient(api_key=api_key)
    return tavily_client.search(query, max_results=max_results, include_raw_content=include_raw_content)

def deduplicate_and_format_sources(search_response, max_tokens_per_source, include_raw_content=False):
    if isinstance(search_response, dict):
        sources_list = search_response['results']
    elif isinstance(search_response, list):
        sources_list = []
        for response in search_response:
            if isinstance(response, dict) and 'results' in response:
                sources_list.extend(response['results'])
            else:
                sources_list.extend(response)
    else:
        raise ValueError("Input must be either a dict with 'results' or a list of search results")

    unique_sources = {}
    for source in sources_list:
        if source['url'] not in unique_sources:
            unique_sources[source['url']] = source

    formatted_text = "Sources:\n\n"
    for source in unique_sources.values():
        formatted_text += f"Source {source['title']}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += f"Most relevant content from source: {source['content']}\n===\n"
        if include_raw_content:
            char_limit = max_tokens_per_source * 4
            raw_content = source.get('raw_content', '') or ''
            if len(raw_content) > char_limit:
                raw_content = raw_content[:char_limit] + "... [truncated]"
            formatted_text += f"Full source content limited to {max_tokens_per_source} tokens: {raw_content}\n\n"

    return formatted_text.strip()

def format_sources(search_results):
    return '\n'.join(
        f"* {source['title']} : {source['url']}"
        for source in search_results['results']
    )

def generate_query(state: State, config: RunnableConfig):
    prompt = query_writer_instruction_web.format(finance_topic=state["research_topic"]) + "\nGenerate a query for web search:"
    result = llm.invoke(prompt)
    output_text = result.content.strip()
    try:
        query_data = json.loads(output_text)
        return {"search_query": query_data['query']}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON: {e}")
        return {"search_query": f"comprehensive analysis of {state['research_topic']}"}

def web_research(state: State, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    search_api = configurable.search_api.value if isinstance(configurable.search_api, Enum) is False else configurable.search_api.value
    if search_api == "tavily":
        search_results = tavily_search(state["search_query"], include_raw_content=True, max_results=1)
        search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000, include_raw_content=True)
    else:
        raise ValueError(f"Unsupported search API: {configurable.search_api}")
    sources = [{"title": source['title'], "url": source['url']} for source in search_results['results']]
    current_sources = state.get("news_sources", [])
    return {
        "news_sources": current_sources + sources,
        "research_loop_count": state["research_loop_count"] + 1,
        "web_research_results": state["web_research_results"] + [search_str]
    }

def summarize_sources(state: State, config: RunnableConfig):
    existing_summary = state.get('text_output', '')
    most_recent_web_research = state['web_research_results'][-1]
    if existing_summary:
        human_message_content = (
            f"<User Input> \n {state['research_topic']} \n <User Input>\n\n"
            f"<Existing Summary> \n {existing_summary} \n <Existing Summary>\n\n"
            f"<New Search Results> \n {most_recent_web_research} \n <New Search Results>"
        )
    else:
        human_message_content = (
            f"<User Input> \n {state['research_topic']} \n <User Input>\n\n"
            f"<Search Results> \n {most_recent_web_research} \n <Search Results>"
        )
    prompt = summarizer_instruction_web.format(language=language) + "\n" + human_message_content
    result = llm.invoke(prompt)
    new_summary = result.content
    while "<think>" in new_summary and "</think>" in new_summary:
        start = new_summary.find("<think>")
        end = new_summary.find("</think>") + len("</think>")
        new_summary = new_summary[:start] + new_summary[end:]
    current_text = state.get("text_output", "")
    updated_text = current_text + "\n\n" + new_summary if current_text else new_summary
    return {"text_output": updated_text}


def reflect_on_summary(state: State, config: RunnableConfig):
    """Reflect on the summary and generate a follow-up query."""
    # Get the running summary from state, defaulting to empty string if not present
    running_summary = state.get('running_summary', '')
    
    prompt = (
        reflection_instructions_web.format(finance_topic=state['research_topic'])
        + "\nIdentify a knowledge gap and generate a follow-up web search query based on our existing knowledge: "
        + running_summary
    )

    result = llm.invoke(prompt)
    output_text = result.content.strip()
    try:
        follow_up_query = json.loads(output_text)
    except json.JSONDecodeError:
        follow_up_query = {"follow_up_query": f"Tell me more about {state['research_topic']}"}

    query = follow_up_query.get('follow_up_query')
    if not query:
        return {"search_query": f"Tell me more about {state['research_topic']}"}
    return {"search_query": query}

def finalize_summary(state: State):
    final_summary = f"## Web Research Summary\n\n{state['text_output']}"
    final_message = HumanMessage(content=final_summary)
    return {"text_output": final_summary, "messages": [final_message]}


def route_research(state: State, config: RunnableConfig) -> Literal["finalize_summary", "web_research"]:
    configurable = Configuration.from_runnable_config(config)
    if state['research_loop_count'] < configurable.max_web_research_loops:
        return "web_research"
    return "finalize_summary"

from functions import *  # Import relevant plotting functions

@tool
def generate_price_plot(ticker: str, period: str = "1y") -> str:
    """Generates price chart for a given ticker."""
    hist = fetch_history(ticker, period=period)
    fig = plot_candles_stick(hist, title=f"{ticker} Price Chart")
    return fig.to_json()  # Return plot as JSON string Return plot as JSON

@tool
def generate_balance_sheet_plot(ticker: str) -> str:
    """Generates balance sheet visualization for a company. Use when user asks about financial health, assets/liabilities, or balance sheet analysis."""
    bs = fetch_balance(ticker)
    currency = yf.Ticker(ticker).info['currency']
    fig = plot_balance(bs, ticker=ticker, currency=currency)
    return fig.to_json()

# Add more plotting tools as needed...

# Update finance_tools list


# %%
@tool
def company_address(ticker: str) -> str:
    """
    Returns company address for input ticker.
    e.g. company_address: AAPL
    Returns company address for ticker AAPL which is stock ticker for Apple Inc.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return " ".join([info[key] for key in ['address1','city','state','zip','country']])

@tool
def fulltime_employees(ticker: str) -> int:
    """
    Returns fulltime employees count for input ticker.
    e.g. company_address: MSFT
    Returns fulltime employees count for ticker MSFT which is stock ticker for Microsoft.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['fullTimeEmployees']

@tool
def last_close_price(ticker: str) -> float:
    """
    Returns last close price for input ticker.
    e.g. company_address: MSFT
    Returns last close price for ticker MSFT which is stock ticker for Microsoft.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['previousClose']

@tool
def EBITDA(ticker: str) -> float:
    """
    Returns EBITDA for input ticker.
    e.g. company_address: AAPL
    Returns EBITDA for ticker AAPL which is stock ticker for Apple Inc.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['ebitda']

@tool
def total_debt(ticker: str) -> float:
    """
    Returns total debt for input ticker.
    e.g. company_address: AAPL
    Returns total debt for ticker AAPL which is stock ticker for Apple Inc.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['totalDebt']

@tool
def total_revenue(ticker: str) -> float:
    """
    Returns total revenue for input ticker.
    e.g. company_address: MSFT
    Returns total revenue for ticker MSFT which is stock ticker for Microsoft.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['totalRevenue']

@tool
def debt_to_equity_ratio(ticker: str) -> float:
    """
    Returns debt to equity ratio for input ticker.
    e.g. company_address: AAPL
    Returns debt to equity ratio for ticker AAPL which is stock ticker for Apple Inc.
    """
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.get_info()

    return info['debtToEquity']

finance_tools = [
    company_address,
    fulltime_employees,
    last_close_price,
    EBITDA,
    total_debt,
    total_revenue,
    debt_to_equity_ratio
]
finance_tools += [generate_price_plot, generate_balance_sheet_plot]
finance_tool_map = {t.name: t for t in finance_tools}

# %%
llm_normal = llm
normal_query_prompt = """
You are a financial analyst. Please answer the user's question based on what you know, don't make up anything. REMEMBER TO ANSWER IN {language} LANGUAGE.
"""

# %%
def answer_normal_query(state: State):
    messages = state.get('messages', [])
    system_message = SystemMessage(content=normal_query_prompt.format(language=language) + "\nFormat your response in Markdown.")
    response = llm_normal.invoke([system_message] + messages)
    markdown_response = f"## Normal Query Response\n\n{response.content}"
    return {"text_output": markdown_response, "messages": [HumanMessage(content=markdown_response)]}

llm_financial_analysis = llm.bind_tools(finance_tools, tool_choice='auto')
financial_analysis_prompt = """
You are a financial analyst. You are given tools for accurate data.
"""

def call_llm(state: State):
    messages = state['messages']
    system_prompt = financial_analysis_prompt + "\nFormat your response in Markdown. Use plots when visualization would help explain financial concepts."
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm_financial_analysis.invoke(messages)
    return {'messages': [message]}

def exists_action(state: State):
    result = state['messages'][-1]
    return len(result.tool_calls) > 0

def take_action(state: State):
    tool_calls = state['messages'][-1].tool_calls
    tool_results = []
    for t in tool_calls:
        try:
            tool_func = finance_tool_map[t['name']]
            result = tool_func.invoke(t['args'])
        except KeyError:
            result = f"Error: Tool {t['name']} not found"
        except Exception as e:
            result = f"Error executing tool: {str(e)}"
        tool_results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
    markdown_output = "## Financial Analysis Results\n\n"
    for result in tool_results:
        markdown_output += f"### {result.name.replace('_', ' ').title()}\n\n{result.content}\n\n"
    return {'messages': tool_results, 'running_summary': markdown_output}

def format_financial_analysis(state: State):
    messages = state['messages']
    tool_results = [msg for msg in messages if isinstance(msg, ToolMessage)]
    text_parts = []
    graphs = state.get("graphs", [])
    for result in tool_results:
        if 'plot' in result.name.lower():
            graphs.append(result.content)  # Plot JSON string
        else:
            text_parts.append(f"### {result.name.replace('_', ' ').title()}\n\n{result.content}")
    current_text = state.get("text_output", "")
    if text_parts:
        analysis_text = "\n\n".join(text_parts)
        updated_text = current_text + "\n\n## Financial Analysis\n\n" + analysis_text if current_text else "## Financial Analysis\n\n" + analysis_text
    else:
        updated_text = current_text + "\n\n## Financial Analysis\n\n" + messages[-1].content if current_text else "## Financial Analysis\n\n" + messages[-1].content
    return {"text_output": updated_text, "graphs": graphs, "messages": [HumanMessage(content=updated_text)]}

# %%
class YouTubeVideoRecommender:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    def get_channel_id(self, channel_name):
        request = self.youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            return response['items'][0]['id']['channelId']
        return None
    
    def search_videos_in_channel(self, channel_id, query, max_results=10):
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            q=query,
            type="video",
            maxResults=max_results
        )
        response = request.execute()
        videos = []
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_at = item['snippet']['publishedAt']
            thumbnail = item['snippet']['thumbnails']['high']['url']
            channel_title = item['snippet']['channelTitle']
            videos.append({
                'video_id': video_id,
                'title': title,
                'description': description,
                'published_at': published_at,
                'thumbnail': thumbnail,
                'channel': channel_title,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })
        return videos

    def recommend_videos(self, query, channels, videos_per_channel=5):
        all_videos = []
        for channel in channels:
            if channel.startswith('UC') and len(channel) == 24:
                channel_id = channel
            else:
                channel_id = self.get_channel_id(channel)
                if not channel_id:
                    print(f"Could not find channel: {channel}")
                    continue
            videos = self.search_videos_in_channel(channel_id, query, videos_per_channel)
            all_videos.extend(videos)
        return all_videos

def youtube_recommend(state: State, config: RunnableConfig):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is not set")
    recommender = YouTubeVideoRecommender(api_key)
    favorite_channels = [
        "ZEE Business", "Economic Times", "Times Now", "Times Now Business", "Times Now News",
        "Pranjal Kamra", "Yadnya Investment Academy", "CA Rachana Phadke Ranade", "Invest Aaj For Kal",
        "Market Gurukul", "Warikoo", "Asset Yogi", "Trading Chanakya", "Trade Brains", "B Wealthy",
        "Capital Pritika", "The Urban Fight", "Kritika Yadav", "Gurleen Kaur Tikku"
    ]
    query = state["research_topic"]
    recommendations = recommender.recommend_videos(query, favorite_channels, videos_per_channel=1)
    youtube_recs = []
    if recommendations:
        for video in recommendations:
            youtube_recs.append({
                "title": video['title'],
                "url": video['url'],
                "channel": video['channel']
            })
    current_youtube = state.get("youtube_recommendations", [])
    return {"youtube_recommendations": current_youtube + youtube_recs, "messages": [HumanMessage(content="YouTube recommendations generated")]}

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
    
    Return a confidence score from 0-10 and a brief explanation.
    """
    
    evaluation = llm.predict(evaluation_prompt)
    return evaluation

def format_final_output(state: State) -> Dict[str, Any]:
    return {
        "text_output": state.get("text_output", ""),
        "graphs": state.get("graphs", []),
        "news_sources": state.get("news_sources", []),
        "youtube_recommendations": state.get("youtube_recommendations", [])
    }

def evaluate_response(state: State, config: RunnableConfig):
    query = state.get("research_topic", "")
    response = state.get("text_output", "")
    sources = "\n".join([f"{s['title']}: {s['url']}" for s in state.get("news_sources", [])]) or "No sources available"
    input_text = f"{query}|||{response}|||{sources}"
    evaluation = self_evaluate(input_text)
    current_text = state.get("text_output", "")
    updated_text = current_text + "\n\n## Self Evaluation\n\n" + evaluation if current_text else "## Self Evaluation\n\n" + evaluation
    return {"text_output": updated_text, "messages": [HumanMessage(content=updated_text)]}

def evaluation_decision(state: State, config: RunnableConfig):
    final_text = state.get("running_summary", "")
    prompt = f"""
    The final output and self-evaluation are as follows:
    {final_text}
    
    Based on the above, do you think additional insights should be added?
    If yes, return a JSON object with the key "next_route" set to one of the following options:
      - "call_llm" for additional financial analysis,
      - "web_research" for further web research,
      - "answer_normal_query" for more normal query insights,
      #- "parallel_branches" to combine branches again.
    If no additional insights are needed, return "done".
    
    For example:
    {{"next_route": "call_llm"}}
    """
    result = llm.invoke(prompt)
    output_text = result.content.strip()
    try:
        decision = json.loads(output_text)
        next_route = decision.get("next_route", "done")
    except Exception as e:
        #print("Error in evaluation_decision:", e)
        next_route = "done"
    # Optionally update state with next_route
    state["next_route"] = next_route
    return {"next_route": next_route}

def get_route(state: State) -> str:
    return state["route"]

def call_route_first_step(state: State):
    # Debug print
    #print(f"Checking for image in state: {bool(state.get('image') and len(state['image']) > 0)}")
    #print(f"Image processed status: {state.get('image_processed', False)}")
    
    # Make sure to check the flag explicitly
    image_processed = state.get("image_processed", False)
    # Only route to image analysis if we have an image AND it's not been processed
    if state.get("image") and len(state["image"]) > 0 and not image_processed:
        #print("Routing to Image_Analysis")
        return {"route": "Image_Analysis"}
    
    # Otherwise proceed with regular routing
    router_response = llm.with_structured_output(Route_First_Step).invoke(state["research_topic"])
    #print('Image Analysis Done, now proceeding with regular routing, which is: ', router_response.step)
    #print(f"Regular routing result: {router_response.step}")
    return {"route": router_response.step}

def validate_state_transition(old_state: State, new_state: State):
    required_fields = set(State.__annotations__.keys())
    missing = required_fields - set(new_state.keys())
    if missing:
        raise ValueError(f"Missing state updates for: {missing}")
    return True

def after_image_analysis(state):
    return {**state}

# %%
def call_gemma3(state: State):
    try:
        image_path = state["image"][0]
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
        assert len(image_b64) < 180_000, "Image too large; use assets API for larger images"
        
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
            "Accept": "application/json"
        }
        payload = {
            "model": "google/gemma-3-27b-it",
            "messages": [
                {
                    "role": "user",
                    "content": f"Describe what you see in this image. Focus on any charts, financial data, or technical analysis elements if present.\n<img src=\"data:image/png;base64,{image_b64}\" />"
                }
            ],
            "max_tokens": 512,
            "temperature": 0.20,
            "top_p": 0.70,
            "stream": False
        }
        gemma_response = requests.post(invoke_url, headers=headers, json=payload)
        gemma_response.raise_for_status()
        data = gemma_response.json()
        if "choices" in data and data["choices"]:
            full_response = data["choices"][0]["message"]["content"]
        else:
            raise ValueError("No valid response from Gemma API")
    except Exception as e:
        fallback_prompt = "Describe what you see in this image. Assume it's a financial chart or technical analysis pattern graph from Investopedia."
        full_response = llm.invoke(fallback_prompt).content
    
    analysis_text = f"## Image Analysis Results\n\n{full_response}"
    current_text = state.get("text_output", "")
    updated_text = current_text + "\n\n" + analysis_text if current_text else analysis_text
    updated_messages = state["messages"] + [HumanMessage(content=analysis_text)]
    route_prompt = "Based on the image analysis, what's the next step? Choose: Web_query, Normal_query, Financial_Analysis, YouTube_Recommender"
    next_route = llm.invoke(route_prompt).content.strip().split()[0] if " " in llm.invoke(route_prompt).content else llm.invoke(route_prompt).content
    return {
        "text_output": updated_text,
        "messages": updated_messages,
        "image_processed": True,
        "route": next_route,
        "research_topic": state["research_topic"],
        "search_query": state.get("search_query", ""),
        "web_research_results": state.get("web_research_results", []),
        "news_sources": state.get("news_sources", []),
        "research_loop_count": state.get("research_loop_count", 0),
        "image": state["image"],
        "graphs": state.get("graphs", []),
        "youtube_recommendations": state.get("youtube_recommendations", [])
    }

import json
import plotly.graph_objects as go

def generate_plot(state: State):
    """Node for generating plots"""
    messages = state['messages']
    plots = []
    
    # Extract plot data from tool calls
    for msg in messages:
        if isinstance(msg, ToolMessage) and 'plot' in msg.name.lower():
            try:
                # Convert JSON string back to Plotly figure
                fig_dict = json.loads(msg.content)
                fig = go.Figure(fig_dict)
                plots.append(fig)
            except Exception as e:
                print(f"Error creating plot: {e}")
    
    return {
        "running_summary": "Here is the requested visualization:",
        "messages": [HumanMessage(content="Plot generated")],
        "plots": plots
    }

# %%
def process_with_context(state: State):
    """Node for processing queries with conversation context"""
    messages = state.get("messages", [])
    
    if len(messages) <= 1:  # Only the current message, no context
        return state
    
    # Last message is the current query
    current_query = messages[-1].content
    context_messages = messages[:-1]
    
    # Format the context for the prompt
    context_str = "\n".join([f"{'User' if i % 2 == 0 else 'Assistant'}: {msg.content}" 
                             for i, msg in enumerate(context_messages[-6:])])
    
    prompt = f"""
    Based on the previous conversation context and the user's current query, 
    generate an enhanced version of the query that incorporates relevant context.
    
    Previous conversation:
    {context_str}
    
    Current query: {current_query}
    
    Enhanced query:
    """
    
    try:
        enhanced_query = llm.invoke(prompt).content.strip()
        # Update the last message with the enhanced query
        updated_messages = messages[:-1] + [HumanMessage(content=enhanced_query)]
        return {"messages": updated_messages, "research_topic": enhanced_query}
    except Exception as e:
        # On error, return original state
        return state

# %%
def update_router():
    final_router = StateGraph(State)
    
    # Add all nodes
    final_router.add_node("route_first_step", call_route_first_step)
    final_router.add_node("generate_query", generate_query)
    final_router.add_node("web_research", web_research)
    final_router.add_node("summarize_sources", summarize_sources)
    final_router.add_node("reflect_on_summary", reflect_on_summary)
    final_router.add_node("finalize_summary", finalize_summary)
    final_router.add_node('call_llm', call_llm)
    final_router.add_node('take_action', take_action)
    final_router.add_node('format_financial_analysis', format_financial_analysis)
    final_router.add_node('answer_normal_query', answer_normal_query)
    final_router.add_node('youtube_recommend', youtube_recommend)
    final_router.add_node("self_evaluate_final", evaluate_response)
    final_router.add_node("evaluation_decision", evaluation_decision)
    final_router.add_node("process_with_context", process_with_context)
    # Add the new image processing node
    final_router.add_node("image_analysis", call_gemma3)
    
    # Define connections
    final_router.add_edge(START, "process_with_context")
    final_router.add_edge("process_with_context", "route_first_step")
    
    # Update conditional edges to include Image_Analysis route
    final_router.add_conditional_edges("route_first_step", get_route, {
        'Image_Analysis': 'image_analysis',
        'Web_query': 'generate_query',
        'Normal_query': 'answer_normal_query',
        'Financial_Analysis': 'call_llm',
        'YouTube_Recommender': 'youtube_recommend',
        'Plot_Data': 'generate_plot'  # New route
    })
    
    # Add new node for plot generation
    final_router.add_node("generate_plot", generate_plot)
    final_router.add_edge("generate_plot", END)
    # Add edge from image_analysis to subsequent routing
    final_router.add_edge("image_analysis", "route_first_step")
    
    final_router.add_edge("answer_normal_query", 'self_evaluate_final')
    
    final_router.add_conditional_edges(
        "call_llm",
        exists_action,
        {True: "take_action", False: "format_financial_analysis"}
    )
    final_router.add_edge("take_action", "format_financial_analysis")
    final_router.add_edge("format_financial_analysis", END)
    
    final_router.add_edge("generate_query", "web_research")
    final_router.add_edge("web_research", "summarize_sources")
    final_router.add_edge("summarize_sources", "reflect_on_summary")
    final_router.add_conditional_edges("reflect_on_summary", route_research)
    final_router.add_edge("finalize_summary", 'self_evaluate_final')
    final_router.add_edge("self_evaluate_final", 'evaluation_decision')
    
    final_router.add_conditional_edges("evaluation_decision", lambda x: x.get("next_route", "done"), {
        'done': END,
        'call_llm': 'call_llm',
        'web_research': 'web_research',
        'answer_normal_query': 'answer_normal_query',
        'YouTube_Recommender': 'youtube_recommend'
    })
    final_router.add_edge("youtube_recommend", END)
    
    return final_router.compile()

# Update the create_initial_state function to better handle images
def create_initial_state(user_query: str, image: list[str] = []) -> State:
    return {
        "route": None,
        "research_topic": user_query,
        "search_query": "",
        "web_research_results": [],
        "sources_gathered": [],
        "research_loop_count": 0,
        "running_summary": "",
        "image": image,
        "messages": [HumanMessage(content=user_query)]
    }

# %%



