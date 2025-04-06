import streamlit as st
import requests
from bs4 import BeautifulSoup

# Custom CSS styling
def inject_custom_css():
    st.markdown("""
    <style>
        .profile-header h1 {
            color: #556b3b;
            font-size: 60px;
        }
        .main {
            max-width: 1000px;
            padding: 2rem;
        }
        .header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, #2c3e50 0%, #4b6cb7 100%);
            border-radius: 12px;
            color: white;
        }
        .header h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
        }
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .article-card {
            border: none;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            background: #f5f3eb;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .article-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
        }
        .article-title {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        .article-meta {
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .article-content {
            color: #34495e;
            line-height: 1.8;
            font-size: 1.05rem;
            max-height: 500px;
            overflow-y: auto;
            padding-right: 1rem;
            margin-top: 1rem;
        }
        .source-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #839E65 !important;
            font-weight: 500;
            margin-top: 1.5rem;
            text-decoration: none;
            transition: color 0.2s;
        }
        .source-link:hover {
            color: #2980b9 !important;
            text-decoration: underline;
        }
        .load-more-btn {
            width: 100%;
            margin: 2rem 0;
            background: linear-gradient(135deg, #4b6cb7 0%, #2c3e50 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s;
        }
        .load-more-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stExpander {
            border: none !important;
            background: transparent !important;
        }
        .stExpander > div {
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: 1rem;
            padding: 1.5rem;
            border-left: 4px solid #3498db;
        }
        .progress-text {
            text-align: center;
            color: #7f8c8d;
            margin-top: 2rem;
            font-size: 0.95rem;
        }
        .news-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)



@st.cache_data(ttl=3600)
def get_article_content(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        article_div = soup.find('div', class_='artText')
        if article_div:
            content = article_div.get_text().strip()
            subscription_text = "(You can now subscribe to our ETMarkets WhatsApp channel)"
            if subscription_text in content:
                content = content.replace(subscription_text, "").strip()
            return content
        return "Article content not found."
    except requests.RequestException as e:
        return f"Error fetching article: {e}"



def stock_news():
    inject_custom_css()
    
    st.markdown("""
    <div class="profile-header">
        <h1 style="text-align:center;">📈 Market Pulse</h1>
        <p style="text-align:center;">Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
        to create a balanced portfolio allocation tailored to your specific needs.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")
    # st.markdown('''
    # <div class="header">
    #     <h1>📈 Market Pulse</h1>
    #     <p>Real-time financial updates & market intelligence</p>
    # </div>
    # ''', unsafe_allow_html=True)
    
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
                # st.markdown('<h2 style="color: #2c3e50; margin-bottom: 1.5rem;">📰 Latest Financial Headlines</h2>', unsafe_allow_html=True)
                st.markdown("")
                st.markdown("")
                for idx, (headline, link, content) in enumerate(st.session_state.displayed_articles):
                    with st.container():
                        st.markdown(f"""
                        <div class="article-card">
                            <div class="article-title">{headline}</div>
                            <div class="article-meta">
                                <span>📅 Latest Update</span>
                                <span>•</span>
                                <span>📊 Market News</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("Read Full Analysis", expanded=False):
                            st.markdown(f'<div class="article-content">{content}</div>', unsafe_allow_html=True)
                            st.markdown(
                                f'<a href="{link}" class="source-link" target="_blank">'
                                f'<span>📖 Read full article on Economic Times</span>'
                                f'<span>→</span>'
                                f'</a>', 
                                unsafe_allow_html=True
                            )
                
                st.markdown(
                    f'<div class="progress-text">'
                    f'Displaying {len(st.session_state.displayed_articles)} of {len(st.session_state.all_articles)} articles • '
                    f'Last updated: {st.session_state.last_update if "last_update" in st.session_state else "Just now"}'
                    f'</div>', 
                    unsafe_allow_html=True
                )
            else:
                st.warning("No articles available at the moment. Please try again later.")

    except Exception as e:
        st.error(f"Error fetching news updates: {str(e)}")
        
stock_news()