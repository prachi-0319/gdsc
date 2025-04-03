# import streamlit as st
# import numpy as np
# import pandas as pd
# import json
# import os
# from bs4 import BeautifulSoup
# from urllib.request import urlopen
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# import google.generativeai as genai
# from dotenv import load_dotenv
# import matplotlib.pyplot as plt
# import altair as alt

# # Load API key for Gemini from the .env file
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")



# # -----------------------------------------------------------
# # Hybrid Investment Recommendation Code
# # -----------------------------------------------------------
# def train_ml_model():
#     np.random.seed(42)
#     data = pd.DataFrame({
#         'risk_tolerance': np.random.uniform(1, 10, 100),
#         'investment_horizon': np.random.randint(1, 30, 100),
#         'liquidity': np.random.uniform(0, 1, 100),
#         'tax_factor': np.random.uniform(0, 1, 100)
#     })
#     noise = np.random.normal(0, 5, 100)
#     data['equity_alloc'] = 30 + 5 * data['risk_tolerance'] + 2 * data['investment_horizon'] \
#                            - 10 * data['liquidity'] - 5 * data['tax_factor'] + noise
#     features = ['risk_tolerance', 'investment_horizon', 'liquidity', 'tax_factor']
#     target = 'equity_alloc'
#     X = data[features]
#     y = data[target]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#     model = RandomForestRegressor(n_estimators=100, random_state=42)
#     model.fit(X_train, y_train)
#     return model

# @st.cache_resource
# def get_model():
#     return train_ml_model()

# ml_model = get_model()

# def rule_based_allocation(risk_tolerance, investment_horizon, liquidity):
#     base_equity = 50 + (risk_tolerance - 5) * 5 + (investment_horizon - 15) * 2
#     base_equity = np.clip(base_equity, 0, 100)
#     base_cash = liquidity * 20
#     base_bonds = 100 - base_equity - base_cash
#     if base_bonds < 0:
#         base_bonds = 0
#         total = base_equity + base_cash
#         base_equity = (base_equity / total) * 100
#         base_cash = (base_cash / total) * 100
#     return {'equity': base_equity, 'bonds': base_bonds, 'cash': base_cash}

# def ml_adjustment(risk_tolerance, investment_horizon, liquidity, tax_factor):
#     input_features = np.array([[risk_tolerance, investment_horizon, liquidity, tax_factor]])
#     predicted_equity = ml_model.predict(input_features)[0]
#     return np.clip(predicted_equity, 0, 100)

# def hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor):
#     rule_alloc = rule_based_allocation(risk_tolerance, investment_horizon, liquidity)
#     ml_equity = ml_adjustment(risk_tolerance, investment_horizon, liquidity, tax_factor)
#     final_equity = (rule_alloc['equity'] + ml_equity) / 2
#     final_cash = rule_alloc['cash']
#     final_bonds = 100 - final_equity - final_cash
#     if final_bonds < 0:
#         final_bonds = 0
#         total = final_equity + final_cash
#         final_equity = (final_equity / total) * 100
#         final_cash = (final_cash / total) * 100
#     return {'equity': final_equity, 'bonds': final_bonds, 'cash': final_cash}

# def create_allocation_chart(allocation):
#     data = pd.DataFrame({
#         'Asset Class': ['Equity', 'Bonds', 'Cash'],
#         'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']]
#     })
#     chart = alt.Chart(data).mark_bar().encode(
#         x=alt.X('Asset Class', axis=alt.Axis(labelAngle=0)),
#         y=alt.Y('Percentage', title='Allocation (%)'),
#         color=alt.Color('Asset Class', scale=alt.Scale(
#             domain=['Equity', 'Bonds', 'Cash'],
#             range=['#3B82F6', '#10B981', '#F59E0B']
#         )),
#         tooltip=['Asset Class', alt.Tooltip('Percentage', format='.2f')]
#     ).properties(
#         width=600,
#         height=400,
#         title='Portfolio Allocation'
#     ).configure_title(
#         fontSize=20
#     )
#     return chart

# def create_allocation_pie(allocation):
#     data = pd.DataFrame({
#         'Asset Class': ['Equity', 'Bonds', 'Cash'],
#         'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']]
#     })
#     colors = ['#3B82F6', '#10B981', '#F59E0B']
#     fig, ax = plt.subplots(figsize=(8, 8))
#     wedges, texts, autotexts = ax.pie(
#         data['Percentage'], 
#         labels=data['Asset Class'],
#         autopct='%1.1f%%',
#         startangle=90,
#         colors=colors,
#         explode=(0.05, 0, 0),
#         shadow=True,
#         wedgeprops={'edgecolor': 'white', 'linewidth': 2}
#     )
#     plt.setp(autotexts, size=10, weight="bold")
#     ax.set_title("Recommended Portfolio Allocation", fontsize=16, fontweight='bold', pad=20)
#     ax.axis('equal')
#     return fig




# # STREAMLIT

# st.markdown("<h2 class='sub-header'>Investment Portfolio Recommender</h2>", unsafe_allow_html=True)
# st.markdown("<div class='card'>", unsafe_allow_html=True)
# st.markdown("<p class='tool-description'>Get personalized investment recommendations based on your risk profile and financial goals. Our <span class='highlight'>hybrid recommendation system</span> combines traditional finance rules with machine learning to create a balanced portfolio allocation.</p>", unsafe_allow_html=True)

# col1, col2 = st.columns([1, 1.5])
# with col1:
#     st.markdown("### Your Investment Profile")
#     risk_tolerance = st.slider(
#         "🎯 Risk Tolerance",
#         min_value=1.0, max_value=10.0, value=5.0, step=0.5,
#         help="Lower values indicate a more conservative approach; higher values indicate a more aggressive approach.",
#         format="%.1f/10",
#         key="risk_slider"
#     )
#     investment_horizon = st.slider(
#         "⏱️ Investment Horizon (years)",
#         min_value=1, max_value=40, value=20,
#         key="horizon_slider"
#     )
#     liquidity = st.slider(
#         "💧 Liquidity Need (0 to 1)",
#         min_value=0.0, max_value=1.0, value=0.3, step=0.05,
#         key="liquidity_slider"
#     )
#     tax_factor = st.slider(
#         "💸 Tax Factor (0 to 1)",
#         min_value=0.0, max_value=1.0, value=0.4, step=0.05,
#         key="tax_slider"
#     )
# with col2:
#     st.markdown("### Recommended Portfolio Allocation")
#     rec = hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor)
#     st.write(f"**Equity:** {rec['equity']:.2f}%")
#     st.write(f"**Bonds:** {rec['bonds']:.2f}%")
#     st.write(f"**Cash:** {rec['cash']:.2f}%")
    
#     st.markdown("#### Allocation Chart")
#     chart = create_allocation_chart(rec)
#     st.altair_chart(chart, use_container_width=True)
    
#     st.markdown("#### Allocation Pie Chart")
#     fig = create_allocation_pie(rec)
#     st.pyplot(fig)


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

# Load API key for Gemini from the .env file
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        max-width: 900px;
        padding: 2rem;
    }
    .profile-header h1 {
        color: #2E86C1;
        font-size: 2.5rem;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .header h2 {
        color: #2E86C1;
        font-size: 2rem;
    }
    .card {
        background-color: rgba(21, 76, 121, 0.15);
        border-radius: 15px;
        border: 0.7px solid #76b5c5;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .slider-container {
        margin-bottom: 1.5rem;
    }
    .highlight {
        background-color: #2980B9;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .allocation-card {
        background-color: blue;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E86C1;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Investment Recommendation Code (unchanged)
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
        'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']],
        'Color': ['#3B82F6', '#10B981', '#F59E0B']
    })
    
    chart = alt.Chart(data).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5
    ).encode(
        x=alt.X('Asset Class', axis=alt.Axis(title=None, labelAngle=0)),
        y=alt.Y('Percentage', title='Allocation (%)', scale=alt.Scale(domain=[0, 100])),
        color=alt.Color('Asset Class', scale=alt.Scale(
            domain=['Equity', 'Bonds', 'Cash'],
            range=['#3B82F6', '#10B981', '#F59E0B']
        ), legend=None),
        tooltip=['Asset Class', alt.Tooltip('Percentage', format='.1f')]
    ).properties(
        height=300,
        # title='Recommended Portfolio Allocation'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )
    
    return chart

def create_allocation_pie(allocation):
    data = pd.DataFrame({
        'Asset Class': ['Equity', 'Bonds', 'Cash'],
        'Percentage': [allocation['equity'], allocation['bonds'], allocation['cash']],
        'Color': ['#3B82F6', '#10B981', '#F59E0B']
    })
    
    pie = alt.Chart(data).mark_arc(
        innerRadius=50,
        outerRadius=120
    ).encode(
        theta='Percentage',
        color=alt.Color('Asset Class', scale=alt.Scale(
            domain=['Equity', 'Bonds', 'Cash'],
            range=['#3B82F6', '#10B981', '#F59E0B']
        ), legend=alt.Legend(orient='right')),
        tooltip=['Asset Class', alt.Tooltip('Percentage', format='.1f')]
    ).properties(
        height=300,
        # title='Portfolio Distribution'
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )
    
    return pie

# -----------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------

# st.title("💰 Investment Portfolio Recommender")

# st.markdown("""
# <div class="header">
#     <h2>Investment Portfolio Recommender</h2>
#     <p style="color: #6c757d;">Get personalized investment recommendations based on your risk profile and financial goals</p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div>
#     <p>Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
#     to create a balanced portfolio allocation tailored to your specific needs.</p>
# </div>
# """, unsafe_allow_html=True)

st.markdown("""
<div class="profile-header">
    <h1 style="font-size:55px; color:white; text-align:center;">💰 Investment Portfolio Recommender</h1>
    <p style="text-align:center;">Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
    to create a balanced portfolio allocation tailored to your specific needs.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("")
st.markdown("")

col1, col2 = st.columns([1, 1], gap="large")


with col1:
    st.markdown("### Your Investment Profile")

    st.markdown("Tell us about your financial preferences to get personalized recommendations! Adjust these sliders to reflect your risk appetite, time horizon, cash needs, and tax preferences. Your selections will shape a portfolio tailored to your goals—from conservative to growth-focused. The more accurate your inputs, the better your results.")
    st.markdown("(All recommendations update instantly as you adjust the settings.)")
    st.markdown("")

    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    risk_tolerance = st.slider(
        "**Risk Tolerance** (1 = Conservative, 10 = Aggressive)",
        min_value=1.0, max_value=10.0, value=5.0, step=0.5,
        key="risk_slider"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    investment_horizon = st.slider(
        "**Investment Horizon** (years)",
        min_value=1, max_value=40, value=20,
        key="horizon_slider"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    liquidity = st.slider(
        "**Liquidity Need** (0 = No immediate need, 1 = High need)",
        min_value=0.0, max_value=1.0, value=0.3, step=0.05,
        key="liquidity_slider"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown('<div class="slider-container">', unsafe_allow_html=True)
    tax_factor = st.slider(
        "**Tax Sensitivity** (0 = Not sensitive, 1 = Highly sensitive)",
        min_value=0.0, max_value=1.0, value=0.4, step=0.05,
        key="tax_slider"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # rec = hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor)
    
    # st.markdown("### Recommended Allocation")
    
    # # Metrics row
    # cols = st.columns(3)
    # with cols[0]:
    #     # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
    #     st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['equity']), unsafe_allow_html=True)
    #     st.markdown('<div class="metric-label">Equity</div>', unsafe_allow_html=True)
    #     st.markdown('</div>', unsafe_allow_html=True)
    
    # with cols[1]:
    #     # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
    #     st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['bonds']), unsafe_allow_html=True)
    #     st.markdown('<div class="metric-label">Bonds</div>', unsafe_allow_html=True)
    #     st.markdown('</div>', unsafe_allow_html=True)
    
    # with cols[2]:
    #     # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
    #     st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['cash']), unsafe_allow_html=True)
    #     st.markdown('<div class="metric-label">Cash</div>', unsafe_allow_html=True)
    #     st.markdown('</div>', unsafe_allow_html=True)


with col2:
    # Calculate recommendations
    rec = hybrid_recommendation(risk_tolerance, investment_horizon, liquidity, tax_factor)
    
    st.markdown("### Recommended Allocation")
    
    # Metrics row
    cols = st.columns(3)
    with cols[0]:
        # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['equity']), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Equity</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cols[1]:
        # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['bonds']), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Bonds</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cols[2]:
        # st.markdown('<div class="allocation-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">{:.1f}%</div>'.format(rec['cash']), unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Cash</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bar chart
    st.markdown("#### Allocation Breakdown")
    bar_chart = create_allocation_chart(rec)
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Pie chart
    st.markdown("#### Portfolio Distribution")
    pie_chart = create_allocation_pie(rec)
    st.altair_chart(pie_chart, use_container_width=True)

# Explanation section
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("""
<div class="card">
    <h4>How This Works</h4>
    <p>Our hybrid recommendation system combines:</p>
    <ul>
        <li><strong>Rule-based allocation</strong>: Traditional financial planning principles based on your risk tolerance and time horizon</li>
        <li><strong>Machine learning adjustment</strong>: Predictive modeling trained on historical market data and investor behavior</li>
    </ul>
    <p>The final recommendation balances these two approaches to create a portfolio that matches your unique financial situation.</p>
</div>
""", unsafe_allow_html=True)
