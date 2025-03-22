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