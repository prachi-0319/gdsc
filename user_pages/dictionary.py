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
# from dotenv import load_dotenv
import matplotlib.pyplot as plt
import altair as alt


api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

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


st.markdown("""
    <style>
    .profile-header h1 {
        color: #556b3b;
        font-size: 60px;
    }
    """,unsafe_allow_html=True)

st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">📚 Finance Dictionary</h1>
    <p style="text-align:center;">Your personal guide to financial terminology - understand complex concepts in simple terms!</p>
    <p>Search any financial term to get:</p>
    <ul>
        <li><span class="highlight">Simple explanations</span> anyone can understand</li>
        <li><span class="highlight">Formal definitions</span> for precise understanding</li>
        <li><span class="highlight">Related terms</span> to expand your knowledge</li>
    </ul>
    <p>Perfect for students, beginners, and professionals looking for quick refreshers.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("")
st.markdown("")
st.markdown("")

# Initialize session state for term if not exists
if 'current_term' not in st.session_state:
    st.session_state.current_term = ''

# Unified search handling
def handle_search(term):
    st.session_state.current_term = term

# Search Input
col_input, col_button = st.columns([4, 1])
with col_input:
    user_input = st.text_input(
        "Enter a finance term:",
        key="term_input",
        placeholder="e.g., Compound Interest, ETF, Liquidity...",
        value=st.session_state.current_term,
        label_visibility="collapsed"
    )
with col_button:
    # st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Search", use_container_width=True, type="primary"):
        handle_search(user_input)

# Check if we should perform a search
should_search = st.session_state.current_term and (
    'selected_term' not in st.session_state or 
    st.session_state.selected_term != st.session_state.current_term
)

if should_search:
    term = st.session_state.current_term.strip().lower()
    st.session_state.selected_term = term  # Mark as searched
    
    finance_dict = load_finance_dictionary()
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### 📘 Formal Definition")
            if term in finance_dict:
                proper_def = finance_dict[term]
            else:
                proper_def = generate_proper_explanation(term)
                finance_dict[term] = proper_def
                with open("finance_terms.json", "w", encoding="utf-8") as file:
                    json.dump(finance_dict, file, indent=4, ensure_ascii=False)
            st.markdown(proper_def)
        
    with col2:
        with st.container(border=True):
            st.markdown("#### 🔄 Simple Explanation")
            simple_expl = generate_simple_explanation(term)
            st.markdown(simple_expl)
    
    # Related terms section
    st.markdown("")
    st.markdown("")
    st.markdown("#### 🔗 Related Terms")
    st.markdown("Explore these related financial concepts:")
    
    related_terms = generate_related_terms(term)
    cols = st.columns(4)
    
    for i, rt in enumerate(related_terms):
        with cols[i]:
            if st.button(
                rt,
                key=f"related_{i}_{term}",  # Unique key per term
                help=f"Click to look up '{rt}'",
                use_container_width=True,
                on_click=handle_search,
                args=(rt,)
            ):
                pass  # Handled by on_click

elif not st.session_state.current_term:
    st.info("Enter a financial term above to get started")
