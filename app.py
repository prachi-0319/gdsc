import streamlit as st
import numpy as np
import pandas as pd
import json
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import google.generativeai as genai
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import altair as alt

# Page config for a cleaner look
st.set_page_config(
    page_title="Financial Tools Suite",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-family: 'Arial', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 20px;
        text-align: center;
    }
    .sub-header {
        font-size: 28px;
        font-weight: 600;
        color: #2563EB;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F9FAFB;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .tool-description {
        color: #4B5563;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .highlight {
        background-color: #DBEAFE;
        padding: 2px 5px;
        border-radius: 3px;
        font-weight: 500;
    }
    .result-container {
        background-color: #EFF6FF;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
        margin-top: 15px;
    }
    .sidebar-content {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load API key for Gemini from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# -----------------------------------------------------------
# Finance Dictionary Code
# -----------------------------------------------------------
def scrape_finance_terms():
    with st.spinner('Scraping financial terms from Investopedia...'):
        url = "https://www.investopedia.com/financial-term-dictionary-4769738"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        finance_dict = {}
        for tag in soup.find_all('a', attrs={'rel': 'nocaes'}):
            term = tag.get_text(strip=True)
            link = tag['href']
            finance_dict[term.lower()] = link
        with open("finance_terms.json", "w", encoding='utf-8') as json_file:
            json.dump(finance_dict, json_file, indent=4, ensure_ascii=False)
        st.success("Finance dictionary successfully scraped and saved!")

def load_finance_dictionary():
    if os.path.exists("finance_terms.json"):
        with open("finance_terms.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def generate_simple_explanation(term):
    with st.spinner(f'Generating simple explanation for "{term}"...'):
        prompt = f"The term is: {term}. Explain it in simple words that a high school student could understand. Keep it under 3 sentences."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't simplify this term."

def generate_proper_explanation(term):
    with st.spinner(f'Generating formal definition for "{term}"...'):
        prompt = f"The term is: {term}. Provide a concise but comprehensive financial dictionary definition."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if response else "I couldn't explain this term."

def generate_related_terms(term):
    with st.spinner(f'Finding related terms for "{term}"...'):
        prompt = f"Generate 4 closely related financial terms to '{term}'. Provide only the terms separated by commas, no explanations."
        model = genai.GenerativeModel("gemini-2.0-flash")
        try:
            response = model.generate_content(prompt)
            if response:
                return [t.strip() for t in response.text.split(',')[:4]]
        except:
            pass
        return ["Investment", "Portfolio", "Risk", "Return"]  # Fallback terms

# -----------------------------------------------------------
# Hybrid Investment Recommendation Code
# -----------------------------------------------------------
def train_ml_model():
    np.random.seed(42)
    data = pd.DataFrame({
        'risk_tolerance': np.random.uniform(1, 10, 100),
        'investment_horizon': np.random.randint(1, 30, 100),
        'liquidity': np.random.uniform(0, 1, 100),
        'tax_factor': np.random.uniform(0, 1, 100)
    })
    noise = np.random.normal(0, 5, 100)
    data['equity_alloc'] = 30 + 5 * data['risk_tolerance'] + 2 * data['investment_horizon'] \
                           - 10 * data['liquidity'] - 5 * data['tax_factor'] + noise
    features = ['risk_tolerance', 'investment_horizon', 'liquidity', 'tax_factor']
    target = 'equity_alloc'
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

@st.cache_resource
def get_model():
    return train_ml_model()

ml_model = get_model()

def rule_based_allocation(risk_tolerance, investment_horizon, liquidity):
    base_equity = 50 + (risk_tolerance - 5) * 5 + (investment_horizon - 15) * 2
    base_equity = np.clip(base_equity, 0, 100)
    base_cash = liquidity * 20
    base_bonds = 100 - base_equity - base_cash
    if base_bonds < 0:
        base_bonds = 0
        total = base_equity + base_cash
        base_equity = (base_equity / total) * 100
        base_cash = (base_cash / total) * 100
    return {'equity': base_equity, 'bonds': base_bonds, 'cash': base_cash}

def ml_adjustment(risk_tolerance, investment_horizon, liquidity, tax_factor):
    input_features = np.array([[risk_tolerance, investment_horizon, liquidity, tax_factor]])
    predicted_equity = ml_model.predict(input_features)[0]
    return np.clip(predicted_equity, 0, 100)

def hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor):
    rule_alloc = rule_based_allocation(risk_tolerance, investment_horizon, liquidity)
    ml_equity = ml_adjustment(risk_tolerance, investment_horizon, liquidity, tax_factor)
    final_equity = (rule_alloc['equity'] + ml_equity) / 2
    final_cash = rule_alloc['cash']
    final_bonds = 100 - final_equity - final_cash
    if final_bonds < 0:
        final_bonds = 0
        total = final_equity + final_cash
        final_equity = (final_equity / total) * 100
        final_cash = (final_cash / total) * 100
    return {'equity': final_equity, 'bonds': final_bonds, 'cash': final_cash}

def create_allocation_chart(allocation):
    data = pd.DataFrame({
        'Asset Class': ['Equity', 'Bonds', 'Cash'],
        'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']]
    })
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Asset Class', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Percentage', title='Allocation (%)'),
        color=alt.Color('Asset Class', scale=alt.Scale(
            domain=['Equity', 'Bonds', 'Cash'],
            range=['#3B82F6', '#10B981', '#F59E0B']
        )),
        tooltip=['Asset Class', alt.Tooltip('Percentage', format='.2f')]
    ).properties(
        width=600,
        height=400,
        title='Portfolio Allocation'
    ).configure_title(
        fontSize=20
    )
    return chart

def create_allocation_pie(allocation):
    data = pd.DataFrame({
        'Asset Class': ['Equity', 'Bonds', 'Cash'],
        'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']]
    })
    colors = ['#3B82F6', '#10B981', '#F59E0B']
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        data['Percentage'], 
        labels=data['Asset Class'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        explode=(0.05, 0, 0),
        shadow=True,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title("Recommended Portfolio Allocation", fontsize=16, fontweight='bold', pad=20)
    ax.axis('equal')
    return fig

# -----------------------------------------------------------
# Streamlit App Layout
# -----------------------------------------------------------
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>Financial Tools</h3>", unsafe_allow_html=True)
    st.markdown("---")
    tool_option = st.radio(
        "Select a Tool",
        ["Finance Dictionary", "Investment Recommendation"],
        format_func=lambda x: f"📚 {x}" if x == "Finance Dictionary" else f"📊 {x}"
    )
    st.markdown("---")
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("### About")
    st.markdown("This app provides financial tools to help you understand financial terms and get investment recommendations based on your profile.")
    st.markdown("</div>", unsafe_allow_html=True)
    if tool_option == "Finance Dictionary":
        st.markdown("---")
        st.markdown("### Admin Controls")
        if st.button("🔄 Update Finance Dictionary", help="Scrape the latest finance terms from Investopedia"):
            scrape_finance_terms()

st.markdown("<h1 class='main-header'>Financial Tools Suite</h1>", unsafe_allow_html=True)

if tool_option == "Finance Dictionary":
    st.markdown("<h2 class='sub-header'>Finance Dictionary Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='tool-description'>Learn about financial terms with clear explanations. Just enter a term below, and I'll provide both a <span class='highlight'>formal definition</span> and a <span class='highlight'>simple explanation</span>.</p>", unsafe_allow_html=True)
    
    # Improved input layout
    col_input, col_button = st.columns([4, 1])
    with col_input:
        user_term = st.text_input(
            "Enter a finance term:",
            key="finance_term",
            placeholder="e.g., Compound Interest, ETF, Liquidity...",
            value=st.session_state.get('selected_term', '')
        )
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("🔍 Explain Term", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_button and user_term:
        finance_dict = load_finance_dictionary()
        term = user_term.strip().lower()
        
        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### 📘 Formal Definition")
            if term in finance_dict:
                proper_def = finance_dict[term]
            else:
                proper_def = generate_proper_explanation(term)
                finance_dict[term] = proper_def
                with open("finance_terms.json", "w", encoding="utf-8") as file:
                    json.dump(finance_dict, file, indent=4, ensure_ascii=False)
            st.markdown(proper_def)
        
        with col2:
            st.markdown(f"### 🔄 Simple Explanation")
            simple_expl = generate_simple_explanation(term)
            st.markdown(simple_expl)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate and display related terms
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Related Terms You Might Like")
        related_terms = generate_related_terms(term)
        
        related_cols = st.columns(4)
        for i, rt in enumerate(related_terms):
            with related_cols[i]:
                if st.button(rt, key=f"related_{i}"):
                    st.session_state.selected_term = rt
                    st.experimental_rerun()
    
    elif search_button and not user_term:
        st.error("Please enter a finance term to search.")

elif tool_option == "Investment Recommendation":
    st.markdown("<h2 class='sub-header'>Investment Portfolio Recommender</h2>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='tool-description'>Get personalized investment recommendations based on your risk profile and financial goals. Our <span class='highlight'>hybrid recommendation system</span> combines traditional finance rules with machine learning to create a balanced portfolio allocation.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown("### Your Investment Profile")
        risk_tolerance = st.slider(
            "🎯 Risk Tolerance",
            min_value=1.0, max_value=10.0, value=5.0, step=0.5,
            help="Lower values indicate a more conservative approach; higher values indicate a more aggressive approach.",
            format="%.1f/10",
            key="risk_slider"
        )
        investment_horizon = st.slider(
            "⏱️ Investment Horizon (years)",
            min_value=1, max_value=40, value=20,
            key="horizon_slider"
        )
        liquidity = st.slider(
            "💧 Liquidity Need (0 to 1)",
            min_value=0.0, max_value=1.0, value=0.3, step=0.05,
            key="liquidity_slider"
        )
        tax_factor = st.slider(
            "💸 Tax Factor (0 to 1)",
            min_value=0.0, max_value=1.0, value=0.4, step=0.05,
            key="tax_slider"
        )
    with col2:
        st.markdown("### Recommended Portfolio Allocation")
        rec = hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor)
        st.write(f"**Equity:** {rec['equity']:.2f}%")
        st.write(f"**Bonds:** {rec['bonds']:.2f}%")
        st.write(f"**Cash:** {rec['cash']:.2f}%")
        
        st.markdown("#### Allocation Chart")
        chart = create_allocation_chart(rec)
        st.altair_chart(chart, use_container_width=True)
        
        st.markdown("#### Allocation Pie Chart")
        fig = create_allocation_pie(rec)
        st.pyplot(fig)

# Session state management
if 'selected_term' not in st.session_state:
    st.session_state.selected_term = ''

# Handle related term clicks
for i in range(4):
    if f"related_{i}" in st.session_state and st.session_state[f"related_{i}"]:
        st.session_state.selected_term = st.session_state[f"related_{i}"]
        st.experimental_rerun()

if __name__ == "__main__":
    if not os.path.exists("finance_terms.json"):
        with open("finance_terms.json", "w") as f:
            json.dump({}, f)