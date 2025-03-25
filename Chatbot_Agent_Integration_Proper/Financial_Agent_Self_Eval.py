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

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors as pc
import yfinance as yf
import pandas as pd
import plotly.io as pio
from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

# %%
load_dotenv()

# %%
language = 'english'

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
    c. If it’s irrelevant to financial investments, ignore it.
4. Ensure all additions align with the user’s finance-related query.
5. Verify that the final output differs from the original summary while improving its depth.

<FORMATTING>
- Start directly with the updated summary, without preamble or titles. Do not use XML tags in the output.
</FORMATTING>
"""

reflection_instructions_web = """You are an expert financial research assistant analyzing a summary about {finance_topic}.

<GOAL>
1. Identify missing details or areas that need deeper exploration.
2. Generate a follow-up question to help expand financial knowledge.
3. Focus on investment strategies, market trends, risk factors, regulations, or financial instruments that weren’t fully covered.
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
    route: Literal['Web_query', 'Normal_query', 'Financial_Analysis', 'YouTube_Recommender', 'Plot_Graph'] = Field(None)
    research_topic: str
    search_query: str
    web_research_results: List[str]
    sources_gathered: List[str]
    research_loop_count: int
    running_summary: str
    image: list[str]
    image_processed: bool
    messages: List[Any]  # This will continue to be the working messages (possibly enhanced)
    original_messages: List[Any]  # New field to store original messages
    plot_type: Optional[str]
    ticker: Optional[str]
    plot_json: Optional[str]

# %%
def fetch_stock_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def fetch_balance(ticker, tp="Annual"):
    ticker_obj = yf.Ticker(ticker)
    bs = ticker_obj.balance_sheet if tp == "Annual" else ticker_obj.quarterly_balance_sheet
    return bs.loc[:, bs.isna().mean() < 0.5]

# Plotting functions
def plot_candles_stick(df, title=""):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    fig.update_layout(title=title)
    return fig

def plot_balance(df, ticker="", currency=""):
    df.columns = pd.to_datetime(df.columns).strftime('%b %d, %Y')
    components = {
        'Total Assets': {'color': 'forestgreen', 'name': 'Assets'},
        'Stockholders Equity': {'color': 'CornflowerBlue', 'name': "Stockholder's Equity"},
        'Total Liabilities Net Minority Interest': {'color': 'tomato', 'name': "Total Liabilities"},
    }
    
    fig = go.Figure()
    for component in components:
        if component == 'Total Assets':
            fig.add_trace(go.Bar(
                x=[df.columns, ['Assets'] * len(df.columns)],
                y=df.loc[component],
                name=components[component]['name'],
                marker=dict(color=components[component]['color'])
            ))
        else:
            fig.add_trace(go.Bar(
                x=[df.columns, ['L+E'] * len(df.columns)],
                y=df.loc[component],
                name=components[component]['name'],
                marker=dict(color=components[component]['color'])
            ))

    offset = 0.03 * df.loc['Total Assets'].max()
    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=[date, "Assets"],
            y=df.loc['Total Assets', date] / 2,
            text=str(round(df.loc['Total Assets', date] / 1e9, 1)) + 'B',
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )
        percentage = round((df.loc['Total Liabilities Net Minority Interest', date] / df.loc['Total Assets', date]) * 100, 1)
        fig.add_annotation(
            x=[date, "L+E"],
            y=df.loc['Stockholders Equity', date] + df.loc['Total Liabilities Net Minority Interest', date] / 2,
            text=str(percentage) + '%',
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center"
        )
        if i > 0:
            percentage = round((df.loc['Total Assets'].iloc[i] / df.loc['Total Assets'].iloc[i - 1] - 1) * 100, 1)
            sign = '+' if percentage >= 0 else ''
            fig.add_annotation(
                x=[date, "Assets"],
                y=df.loc['Total Assets', date] + offset,
                text=sign + str(percentage) + '%',
                showarrow=False,
                font=dict(size=12, color="black"),
                align="center"
            )

    fig.update_layout(
        barmode='stack',
        title=f'Accounting Balance: {ticker}',
        xaxis_title='Year',
        yaxis_title=f'Amount (in {currency})',
        legend_title='Balance components',
    )
    return fig

def plot_assets(df, ticker="", currency=""):
    assets = {
        'Current Assets': {
            'Cash Cash Equivalents And Short Term Investments': {},
            'Receivables': {},
            'Prepaid Assets': None,
            'Inventory': {},
            'Hedging Assets Current': None,
            'Other Current Assets': None
        },
        'Total Non Current Assets': {
            'Net PPE': {},
            'Goodwill And Other Intangible Assets': {},
            'Investments And Advances': {},
            'Investment Properties': None,
            'Other Non Current Assets': None
        }
    }

    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.05,
        subplot_titles=['Current Assets', 'Non-Current Assets']
    )

    colors = pc.sequential.Blugrn[::-1]
    i = 0
    for component in assets['Current Assets']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(color=colors[i]),
                legendgroup='Current Assets',
                showlegend=True
            ), row=1, col=1)
            i += 1

    colors = pc.sequential.Purp[::-1]
    i = 0
    for component in assets['Total Non Current Assets']:
        if component in df.index:
            fig.add_trace(go.Bar(
                x=df.columns,
                y=df.loc[component],
                name=component,
                marker=dict(color=colors[i]),
                legendgroup='Non-current Assets',
                showlegend=True
            ), row=1, col=2)
            i += 1

    offset = 0.03 * max(df.loc['Current Assets'].max(), df.loc['Total Non Current Assets'].max())
    for i, date in enumerate(df.columns):
        fig.add_annotation(
            x=date,
            y=df.loc['Current Assets', date] + offset,
            text=str(round(df.loc['Current Assets', date] / 1e9, 1)) + 'B',
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=1
        )
        fig.add_annotation(
            x=date,
            y=df.loc['Total Non Current Assets', date] + offset,
            text=str(round(df.loc['Total Non Current Assets', date] / 1e9, 1)) + 'B',
            showarrow=False,
            font=dict(size=12, color="black"),
            align="center",
            row=1, col=2
        )

    fig.update_layout(
        barmode='stack',
        title=f'Assets: {ticker}',
        xaxis1=dict(title='Date', type='date', tickvals=df.columns),
        xaxis2=dict(title='Date', type='date', tickvals=df.columns),
        yaxis_title=f'Amount (in {currency})',
        legend_title='Asset Components',
    )
    return fig

# %%
def parse_query(state: State) -> State:
    """Parse the user query to determine plot type and ticker"""
    query = state["research_topic"].lower()
    #print(query)
    ticker = query.split()[-1].upper()
    #print(ticker)
    if "candlestick chart" in query:
        return {"plot_type": "candlestick", "ticker": ticker}
    elif "balance sheet" in query:
        return {"plot_type": "balance", "ticker": ticker}
    elif "assets" in query:
        return {"plot_type": "assets", "ticker": ticker}
    else:
        return {"plot_type": None, "ticker": None}
    
def generate_plot(state: State) -> State:
    """Generate the appropriate plot based on the parsed query"""
    if not state["plot_type"] or not state["ticker"]:
        return {"response": "I can generate candlestick charts, balance sheets, or assets visualizations. Please specify what you'd like to see (e.g., 'Show me a candlestick chart for AAPL')"}
    
    ticker = state["ticker"]
    plot_type = state["plot_type"]
    
    try:
        if plot_type == "candlestick":
            df = fetch_stock_data(ticker)
            fig = plot_candles_stick(df, title=f"{ticker} Candlestick Chart")
        elif plot_type == "balance":
            df = fetch_balance(ticker)
            fig = plot_balance(df, ticker=ticker, currency="INR")
        elif plot_type == "assets":
            df = fetch_balance(ticker)
            fig = plot_assets(df, ticker=ticker, currency="INR")
        
        plot_json = fig.to_json()
        return {"plot_json": plot_json}
    
    except Exception as e:
        return {"response": f"Error generating plot: {str(e)}"}
    
def format_response(state: State) -> State:
    """Format the final response"""
    print(state.get('plot_json'))
    if state.get("plot_json"):
        fig = pio.from_json(state.get("plot_json"))
        fig.show()
        return {"response": state["plot_json"]}
    elif state.get("response"):
        return {"response": state["response"]}
    else:
        return {"response": "Something went wrong while processing your request"}

# %%
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
        "image_processed": False,
        "messages": [HumanMessage(content=user_query)],  # Working messages
        "original_messages": [HumanMessage(content=user_query)],  # Store original message
        "plot_type": None,
        "ticker": None,
        "plot_json": None
    }

# %%
class Route_First_Step(BaseModel):
    # Updated to include YouTube_Recommender
    step: Literal['Web_query', 'Normal_query', 'Financial_Analysis', 'YouTube_Recommender','Plot_Graph'] = Field(
        None,
        description='Determine whether to perform a web search, answer a normal question, perform a financial analysis, recommend YouTube videos or plot graphs.'
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
    return {
        "sources_gathered": [format_sources(search_results)],
        "research_loop_count": state["research_loop_count"] + 1,
        "web_research_results": [search_str]
    }

def summarize_sources(state: State, config: RunnableConfig):
    existing_summary = state['running_summary']
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
    prompt = summarizer_instruction_web + "\n" + human_message_content
    result = llm.invoke(prompt)
    running_summary = result.content
    while "<think>" in running_summary and "</think>" in running_summary:
        start = running_summary.find("<think>")
        end = running_summary.find("</think>") + len("</think>")
        running_summary = running_summary[:start] + running_summary[end:]
    return {"running_summary": running_summary}

def reflect_on_summary(state: State, config: RunnableConfig):
    prompt = reflection_instructions_web.format(finance_topic=state['research_topic']) \
             + "\nIdentify a knowledge gap and generate a follow-up web search query based on our existing knowledge: " \
             + state['running_summary']
    result = llm.invoke(prompt)
    output_text = result.content.strip()
    try:
        follow_up_query = json.loads(output_text)
    except json.JSONDecodeError:
        #print("Error: Could not decode JSON from reflect_on_summary. Response was:", output_text)
        follow_up_query = {"follow_up_query": f"Tell me more about {state['research_topic']}"}
    query = follow_up_query.get('follow_up_query')
    if not query:
        return {"search_query": f"Tell me more about {state['research_topic']}"}
    return {"search_query": query}

def finalize_summary(state: State):
    all_sources = "\n".join(source for source in state['sources_gathered'])
    final_summary = f"## Web Research Summary\n\n{state['running_summary']}\n\n### Sources:\n{all_sources}"
    final_message = HumanMessage(content=final_summary)
    return {
        "running_summary": final_summary,
        "messages": [final_message],
        "original_messages": state["original_messages"]  # Preserve original messages
    }

def route_research(state: State, config: RunnableConfig) -> Literal["finalize_summary", "web_research"]:
    configurable = Configuration.from_runnable_config(config)
    if state['research_loop_count'] < configurable.max_web_research_loops:
        return "web_research"
    return "finalize_summary"

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
finance_tool_map = {t.name: t for t in finance_tools}

# %%
llm_normal = llm
normal_query_prompt = """
You are a financial analyst. Please answer the user's question based on what you know, don't make up anything. REMEMBER TO ANSWER IN {language} LANGUAGE.
"""

# %%
def answer_normal_query(state: State):
    messages = state.get('messages', [])
    system_message = SystemMessage(content=normal_query_prompt + "\nFormat your response in Markdown.")
    response = llm_normal.invoke([system_message] + messages)
    markdown_response = f"## Normal Query Response\n\n{response.content}"
    return {
        "running_summary": markdown_response,
        "messages": [HumanMessage(content=markdown_response)],
        "original_messages": state["original_messages"]  # Preserve original messages
    }
llm_financial_analysis = llm.bind_tools(finance_tools, tool_choice='auto')
financial_analysis_prompt = """
You are a financial analyst. You are given tools for accurate data.
"""

def call_llm(state: State):
    messages = state['messages']
    system_prompt = financial_analysis_prompt + "\nFormat your response in Markdown."
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
    if tool_results:
        markdown_output = "## Financial Analysis Results\n\n"
        for result in tool_results:
            markdown_output += f"### {result.name.replace('_', ' ').title()}\n\n{result.content}\n\n"
    else:
        markdown_output = f"## Financial Analysis\n\n{messages[-1].content}"
    return {"running_summary": markdown_output, "messages": [HumanMessage(content=markdown_output)]}

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
    # List of favorite channels (names or IDs)
    favorite_channels = [
        "ZEE Business",
        "Economic Times",
        "Times Now",
        "Times Now Business",
        "Times Now News",
        "Times Now Politics",
        "Times Now Sports",
        "Times Now Science",
        "Times Now Technology",
        "Pranjal Kamra",
        "Yadnya Investment Academy",
        "CA Rachana Phadke Ranade",
        "Invest Aaj For Kal",
        "Market Gurukul",
        "Warikoo",
        "Asset Yogi",
        "Trading Chanakya",
        "Trade Brains",
        "B Wealthy",
        "Capital Pritika",
        "The Urban Fight",
        "Kritika Yadav",
        "Gurleen Kaur Tikku"
    ]
    query = state["research_topic"]
    recommendations = recommender.recommend_videos(query, favorite_channels, videos_per_channel=1)
    if not recommendations:
        summary = f"No matching videos found for query: {query}"
    else:
        summary = f"## YouTube Video Recommendations for '{query}'\n\n"
        for i, video in enumerate(recommendations, 1):
            summary += f"### {i}. {video['title']}\n"
            summary += f"- Channel: {video['channel']}\n"
            summary += f"- URL: {video['url']}\n"
            summary += f"- Published: {video['published_at']}\n\n"
    return {"running_summary": summary, "messages": [HumanMessage(content=summary)]}

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

def evaluate_response(state: State, config: RunnableConfig):
    query = state.get("research_topic", "")
    response = state.get("running_summary", "")
    sources = "\n".join(state.get("sources_gathered", [])) or "No sources available"
    input_text = f"{query}|||{response}|||{sources}"
    evaluation = self_evaluate(input_text)
    final_summary = response# + "\n\n## Self Evaluation\n\n" + evaluation
    return {"running_summary": final_summary, "messages": [HumanMessage(content=final_summary)]}

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
    image_processed = state.get("image_processed", False)
    if state.get("image") and len(state["image"]) > 0 and not image_processed:
        return {"route": "Image_Analysis", "original_messages": state["original_messages"]}
    
    router_response = llm.with_structured_output(Route_First_Step).invoke(state["research_topic"])
    print(f"Routing result: {router_response.step}")
    return {"route": router_response.step, "original_messages": state["original_messages"]}

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

        assert len(image_b64) < 180_000, \
            "To upload larger images, use the assets API (see docs)"
        
        try:
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
            full_response = data["choices"][0]["message"]["content"] if "choices" in data and data["choices"] else ""
        except Exception as e:
            fallback_prompt = f"Describe what you see in this image. The image appears to be a financial chart or technical analysis pattern graph from Investopedia. Please describe the patterns, trends, and elements visible in the chart."
            full_response = llm.invoke(fallback_prompt).content
        
        markdown_response = f"## Image Analysis Results\n\n{full_response}"
        updated_messages = state["messages"] + [HumanMessage(content=markdown_response)]
        
        route_prompt = "Based on the image analysis of what appears to be a financial chart or technical analysis pattern, what should be the next step? Choose one: Web_query, Normal_query, Financial_Analysis, YouTube_Recommender"
        next_route = llm.invoke(route_prompt).content.strip()
        for route in ["Web_query", "Normal_query", "Financial_Analysis", "YouTube_Recommender"]:
            if route in next_route:
                next_route = route
                break
        else:
            next_route = "Normal_query"
        
        return {
            "running_summary": markdown_response,
            "messages": updated_messages,
            "image_processed": True,
            "route": next_route,
            "research_topic": state["research_topic"],
            "search_query": state.get("search_query", ""),
            "web_research_results": state.get("web_research_results", []),
            "sources_gathered": state.get("sources_gathered", []),
            "research_loop_count": state.get("research_loop_count", 0),
            "image": state["image"],
            "original_messages": state["original_messages"]  # Preserve original messages
        }
    except Exception as e:
        return {
            "running_summary": str(e),
            "messages": state["messages"] + [HumanMessage(content=str(e))],
            "image_processed": True,
            "route": "Normal_query",
            "research_topic": state["research_topic"],
            "search_query": state.get("search_query", ""),
            "web_research_results": state.get("web_research_results", []),
            "sources_gathered": state.get("sources_gathered", []),
            "research_loop_count": state.get("research_loop_count", 0),
            "image": state["image"],
            "original_messages": state["original_messages"]  # Preserve original messages
        }

# %%
def process_with_context(state: State):
    """Node for processing queries with conversation context"""
    messages = state.get("messages", [])
    original_messages = state.get("original_messages", [])
    
    if len(messages) <= 1:  # Only the current message, no context
        return state
    
    # Last message is the current query
    current_query = messages[-1].content
    
    # Add the current query to original_messages if it's not already there
    if not original_messages or original_messages[-1].content != current_query:
        original_messages.append(HumanMessage(content=current_query))
    
    context_messages = messages[:-1]
    
    # Format the context for the prompt
    context_str = "\n".join([f"{'User' if i % 2 == 0 else 'Assistant'}: {msg.content}" 
                             for i, msg in enumerate(context_messages[-6:])])
    
    prompt = f"""
    Based on the previous conversation context and the user's current query, generate an enhanced version of the query that incorporates relevant context. However, if the query is about plotting a graph, preserve its intent and format it into one of these exact structures with the company ticker as the last word:
    - "Show me a candlestick chart for TICKER"
    - "Show me the balance sheet for TICKER"
    - "Show me the assets for TICKER"
    
    Previous conversation:
    {context_str}
    
    Current query: {current_query}
    
    Instructions:
    1. If the query mentions 'candlestick', 'balance sheet', or 'assets' (or similar terms like 'chart', 'visualize'), identify the ticker (e.g., AAPL, MSFT) and rephrase it into one of the above formats.
    2. For non-plot queries, enhance the query with context as needed.
    3. Ensure the ticker, if present, is always the last word in plot-related queries.
    
    Enhanced query:
    """
    
    try:
        enhanced_query = llm.invoke(prompt).content.strip()
        # Update the last message with the enhanced query in messages
        updated_messages = messages[:-1] + [HumanMessage(content=enhanced_query)]
        return {
            "messages": updated_messages,
            "original_messages": original_messages,
            "research_topic": enhanced_query
        }
    except Exception as e:
        # On error, return state with original messages preserved
        return {
            "messages": messages,
            "original_messages": original_messages,
            "research_topic": state["research_topic"]
        }

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

    final_router.add_node("parse_query", parse_query)
    final_router.add_node("generate_plot", generate_plot)
    final_router.add_node("format_response", format_response)
    
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
        'Plot_Graph': 'parse_query'
    })
    
    # Add edge from image_analysis to subsequent routing
    final_router.add_edge("parse_query", "generate_plot")
    final_router.add_edge("generate_plot", "format_response")
    final_router.add_edge("image_analysis", "route_first_step")
    
    final_router.add_edge("answer_normal_query", 'self_evaluate_final')
    final_router.add_edge("format_response", 'self_evaluate_final')
    
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

# %%
#Query: Show me a candlestick chart for AAPL
#Query: Show me the balance sheet for MSFT
#Query: Show me the assets for GOOGL

# %%



