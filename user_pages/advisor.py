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

# Load API key for Gemini from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")



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




# STREAMLIT

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
