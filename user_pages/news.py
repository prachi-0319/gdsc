import streamlit as st
import requests
from bs4 import BeautifulSoup

# Custom CSS styling
def inject_custom_css():
    st.markdown("""
    <style>
        .main {
            max-width: 1000px;
            padding: 2rem;
        }
        .article-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            padding: 2rem 0;
            border-bottom: 2px solid #f0f2f6;
            margin-bottom: 2rem;
        }
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
        }
        .stExpander {
            border: none !important;
            box-shadow: none !important;
        }
        .stExpander > div {
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: 1rem;
            padding: 1rem;
        }
        .article-content {
            color: #34495e;
            line-height: 1.8;
            font-size: 1rem;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 1rem;
        }
        .source-link {
            font-size: 0.9em;
            color: #7f8c8d !important;
            margin-top: 1rem;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_article_content(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(resp.content, 'html.parser')
        article_div = soup.find('div', class_='artText')  # Locate article content
        if article_div:
            content = article_div.get_text().strip()
            # Remove the specific subscription text if present
            subscription_text = "(You can now subscribe to our ETMarkets WhatsApp channel)"
            if subscription_text in content:
                content = content.replace(subscription_text, "").strip()
            return content
        else:
            return "Article content not found."
    except requests.RequestException as e:
        return f"Error fetching article: {e}"

def stock_news():
    inject_custom_css()
    
    st.markdown('<div class="header"><h1>📈 Market Pulse: Real-Time Financial Updates</h1></div>', unsafe_allow_html=True)
    
    try:
        with st.spinner('Fetching latest market updates...'):
            resp = requests.get(
                "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, features='xml')
            items = soup.findAll('item')

            if 'all_articles' not in st.session_state:
                st.session_state.all_articles = [
                    (item.find('title').get_text().strip(), 
                     item.find('link').get_text().strip()) 
                    for item in items
                ]

            if 'displayed_articles' not in st.session_state:
                st.session_state.displayed_articles = []
                st.session_state.last_index = 0

            def load_articles(batch_size=5):
                available = []
                index = st.session_state.last_index
                while len(available) < batch_size and index < len(st.session_state.all_articles):
                    headline, link = st.session_state.all_articles[index]
                    content = get_article_content(link)
                    # Remove the specific subscription text if present
                    content = content.replace("(You can now subscribe to our ETMarkets WhatsApp channel)", "").strip()
                    if "Error" not in content and "not available" not in content:
                        available.append((headline, link, content))
                    index += 1
                return available, index

            if st.button('Load More Articles', key='load_more'):
                new_articles, new_index = load_articles()
                st.session_state.displayed_articles.extend(new_articles)
                st.session_state.last_index = new_index

            if not st.session_state.displayed_articles:
                initial_articles, initial_index = load_articles(10)
                st.session_state.displayed_articles = initial_articles
                st.session_state.last_index = initial_index

            if st.session_state.displayed_articles:
                st.subheader('Latest Financial Headlines')
                for idx, (headline, link, content) in enumerate(st.session_state.displayed_articles):
                    with st.container():
                        st.markdown(f"""
                        <div class="article-card">
                            <h3>{headline}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Read Full Analysis", expanded=False):
                            st.markdown(f'<div class="article-content">{content}</div>', unsafe_allow_html=True)
                            st.markdown(f'<a href="{link}" class="source-link" target="_blank">Read full article on Economic Times →</a>', unsafe_allow_html=True)
                
                st.markdown(f'<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">Displaying {len(st.session_state.displayed_articles)} of {len(st.session_state.all_articles)} articles</div>', unsafe_allow_html=True)
            else:
                st.warning("No articles available at the moment. Please try again later.")

    except Exception as e:
        st.error(f"Error fetching news updates: {str(e)}")
        
stock_news()