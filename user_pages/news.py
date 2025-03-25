# import streamlit as st
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# from GoogleNews import GoogleNews

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Load API Key for Gemini AI
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Streamlit UI Setup
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # st.set_page_config(page_title="Finance Newsstand", layout="wide")
# st.title("📰 Finance & Business Newsstand")

# # Sidebar for Category Selection
# categories = {
#     "Finance": "finance",
#     "Business": "business",
#     "Economy": "economy"
# }
# selected_category = st.sidebar.selectbox("Choose a category:", list(categories.keys()))

# # Fetch Google News Articles
# googlenews = GoogleNews(lang='en', region='US')
# googlenews.search(categories[selected_category])
# results = googlenews.results()

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Function to Summarize News with Gemini AI
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def summarize_article(title, link):
#     """Generate a 200-word summary using Google Gemini AI"""
#     prompt = f"Summarize this news article in 200 words:\n\nTitle: {title}\nLink: {link}\n\nKeep it informative and concise."

#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content(prompt)
#         # response = genai.generate_content(prompt)
#         return response.text if response else "Summary not available."
#     except Exception as e:
#         return f"Error: {e}"

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Display Articles in Streamlit with Styled Cards
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# if results:
#     cols = st.columns(2)  # Two-column layout for better readability
    
#     for idx, news in enumerate(results[:6]):  # Show top 6 articles
#         with cols[idx % 2]:  # Alternate articles between columns
#             with st.container():
#                 st.markdown(
#                     f"""
#                     <div style="
#                         background-color: #f8f9fa;
#                         padding: 15px;
#                         border-radius: 10px;
#                         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
#                         margin-bottom: 10px;">
#                         <h3 style="color: #333;">{news['title']}</h3>
#                         <p><b>Published:</b> {news.get('date', 'Unknown Date')}</p>
#                         <p style="color: #555;">{summarize_article(news['title'], news['link'])}</p>
#                         <a href="{news['link']}" target="_blank" style="color: #007bff; text-decoration: none;">🔗 Read More</a>
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )
# else:
#     st.warning("No news articles found. Try again later!")




# import streamlit as st
# from newsapi import NewsApiClient
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load API Keys
# load_dotenv()
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Configure Gemini AI
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
# else:
#     st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")

# # Initialize News API Client
# newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# # Fetch Financial & Business News
# def fetch_news():
#     try:
#         categories = ['business', 'general']  # Covers business, economy, and finance
#         articles = []
#         for category in categories:
#             headlines = newsapi.get_top_headlines(category=category, language='en', country='us', page_size=50)
#             articles.extend(headlines['articles'])
#         return articles[:100]  # Limit to top 100 articles
#     except Exception as e:
#         st.error(f"Error fetching news: {e}")
#         return []

# # Generate AI Summary
# def generate_summary(article_text):
#     prompt = f"Summarize this news article in 200 words:\n\nArticle text: {article_text}\n\nKeep it informative and concise."
#     if not article_text:
#         return "Summary not available."
    
#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content(prompt)
#         return response.text if response else "Summary not available."
#     except Exception as e:
#         return "Summary generation failed."


# # Streamlit App Layout
# # st.set_page_config(page_title="Finance & Economic News", layout="wide")

# st.title("📊 Finance & Economic News Stand")
# st.markdown("**Stay updated with the latest in Business, Finance, Economy, and Investments.**")

# # Fetch Articles
# articles = fetch_news()

# # Pagination Settings
# articles_per_page = 10
# total_pages = (len(articles) + articles_per_page - 1) // articles_per_page  # Total number of pages

# # Initialize Page Number in Session State
# if 'page' not in st.session_state:
#     st.session_state.page = 0

# # Get Articles for Current Page
# start_idx = st.session_state.page * articles_per_page
# end_idx = min(start_idx + articles_per_page, len(articles))
# articles_to_display = articles[start_idx:end_idx]

# if articles_to_display:
#     for article in articles_to_display:
#         with st.container():
#             summary = generate_summary(article['description'])

#             st.markdown(
#                 f"""
#                 <div style="border: 2px solid #e0e0e0; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #f9f9f9;">
#                     <h3 style="color: #333;">{article['title']}</h3>
#                     <p style="font-size: 14px; color: #666;">{summary}</p>
#                     <p style="font-size: 12px;"><strong>Source:</strong> {article['source']['name']} | <strong>Published:</strong> {article['publishedAt'][:10]}</p>
#                     <a href="{article['url']}" target="_blank" style="color: #007bff; text-decoration: none;">🔗 Read Full Article</a>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )
# else:
#     st.warning("No articles found. Try again later.")

# # Pagination Controls
# col1, col2, col3 = st.columns([1, 2, 1])

# with col1:
#     if st.session_state.page > 0:
#         if st.button("⬅️ Previous Page"):
#             st.session_state.page -= 1
#             st.rerun()

# with col2:
#     st.markdown(f"### Page {st.session_state.page + 1} of {total_pages}")

# with col3:
#     if st.session_state.page < total_pages - 1:
#         if st.button("Next Page ➡️"):
#             st.session_state.page += 1
#             st.rerun()





# Refer - https://github.com/dcarpintero/st-newsapi-connector
import streamlit as st
import pandas as pd
from datetime import datetime
from pycountry import countries
from typing import Any, Dict, List, Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
from user_pages.news_api_connection import NewsAPIConnection

# Load API Keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")

# Initialize NewsAPI Connection
conn_newsapi = st.connection("NewsAPI", type=NewsAPIConnection)

# Helper Functions
def get_country_code(name: str) -> str:
    """Return the 2-letter country code for a given country name."""
    try:
        return countries.get(name=name).alpha_2
    except AttributeError:
        raise ValueError(f'No country code found for "{name}"')

def format_date(date_string: str) -> Optional[str]:
    try:
        date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    except (ValueError, TypeError):
        return None
    return date.strftime('%d %B %Y')

def to_dataframe(data: Optional[Dict[str, Any]]) -> Optional[pd.DataFrame]:
    if data is None:
        return None
    articles = data.get('articles', None)
    return pd.DataFrame(articles)

def generate_summary(article_text: str) -> str:
    """Generate a 200-word summary using Google Gemini AI."""
    prompt = f"Summarize this news article in 200 words:\n\nArticle text: {article_text}\n\nKeep it informative and concise."
    if not article_text:
        return "Summary not available."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response else "Summary not available."
    except Exception as e:
        return f"Summary generation failed: {e}"

# # Streamlit App Layout
# st.set_page_config(
#     page_title="Finance & Economic News Stand",
#     page_icon="📰",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.title("📊 Finance & Economic News Stand")
# st.markdown("**Stay updated with the latest in Business, Finance, Economy, and Investments.**")



st.markdown("""
<div>
    <h1 style="font-size:60px; color:white; text-align:center;">📊 Finance & Economic News Stand</h1>
    <p style="text-align:center;">Stay updated with the latest in Business, Finance, Economy, and Investments.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("")
st.markdown("")

# Main Page Options
col1, col2, col3 = st.columns(3)

with col1:
    topic = st.text_input("Keywords or phrases to search in the News", "Finance, Economy")
    topic = topic.strip()

with col2:
    category = st.selectbox(
        "Category",
        ("Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"),
        index=0,
    )

with col3:
    country = st.selectbox("Country", ["United States", "United Kingdom", "India", "Canada", "Australia"], index=0)

st.markdown("")
st.markdown("")

feed = st.slider("Number of Articles to Display", min_value=1, max_value=50, value=10)

# Fetch and Display News
if st.button("Fetch News"):
    st.header("📰 Your Briefing Articles")
    tab_topic, tab_headlines = st.tabs([topic, f'Top Stories in {category} ({country})'])

    # Your Topic
    with tab_topic:
        if topic:
            data = conn_newsapi.everything(q=topic)
            df = to_dataframe(data)
            if df is not None:
                for i in range(min(feed, len(df))):
                    story = df.iloc[i]
                    title = story["title"]
                    url = story["url"]
                    urlToImage = story["urlToImage"]
                    publishedAt = format_date(story["publishedAt"])
                    summary = generate_summary(story["description"])

                    if title:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if urlToImage:
                                st.image(urlToImage, width=150)
                        with col2:
                            st.markdown(f'[{title}]({url})')
                            st.text(publishedAt)
                            st.markdown(f"**Summary:** {summary}")

    # Top Stories
    with tab_headlines:
        data = conn_newsapi.top_headlines(country=get_country_code(country), category=category.lower())
        df = to_dataframe(data)
        if df is not None:
            for i in range(min(feed, len(df))):
                story = df.iloc[i]
                title = story["title"]
                url = story["url"]
                urlToImage = story["urlToImage"]
                publishedAt = format_date(story["publishedAt"])
                summary = generate_summary(story["description"])

                if title:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if urlToImage:
                            st.image(urlToImage, width=150)
                    with col2:
                        st.markdown(f'[{title}]({url})')
                        st.text(publishedAt)
                        st.markdown(f"**Summary:** {summary}")