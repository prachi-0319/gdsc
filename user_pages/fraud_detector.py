import streamlit as st
import google.generativeai as genai
# from dotenv import load_dotenv
import os

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

st.markdown("""
<style>
    .main {
        max-width: 900px;
        padding: 2rem;
    }
    .highlight {
        background-color: #2980B9;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div>
    <h1 style="font-size:60px; color:white; text-align:center;">🚨 Fraud & Scam Detection Alerts</h1>
    <p style="text-align:center;">Verify before you invest—protect your hard-earned money! Enter details of any investment offer to check for red flags. Our system cross-references known scam patterns, unrealistic returns, and regulatory warnings to assess legitimacy.</p>
    <p style="text-align:center;">Note: <span class="highlight">Always consult a certified financial advisor</span> for high-risk investments.</p>
</div>
""", unsafe_allow_html=True)

# st.set_page_config(page_title="Fraud & Scam Detector", layout="centered")
# st.title("🚨 Fraud & Scam Detection Alerts")

# st.markdown("""
# <div>
#     <Enter>Verify before you invest—protect your hard-earned money! Enter details of any investment offer to check for red flags. Our system cross-references known scam patterns, unrealistic returns, and regulatory warnings to assess legitimacy.</p>
#     <p>Note: <span class="highlight">Always consult a certified financial advisor</span> for high-risk investments.</p>
# </div>
# """, unsafe_allow_html=True)

st.markdown("")
st.markdown("")

# st.write("Enter details of an investment scheme to check if it's legitimate.")

# User input fields
scheme_name = st.text_input("Scheme Name", placeholder="e.g., Golden Future Investment Plan")
promised_returns = st.text_input("Promised Returns", placeholder="e.g., 20% monthly")
minimum_investment = st.number_input("Minimum Investment (₹)", min_value=0, step=100)
company_info = st.text_area("Company Details", placeholder="Enter any details you have about the company.")

if st.button("Check Legitimacy"):
    with st.spinner("Analyzing..."):
        # Query Gemini API
        query = f"Is '{scheme_name}' a legitimate investment scheme in India? It promises {promised_returns} returns with a minimum investment of ₹{minimum_investment}. The company details are: {company_info}. Provide a scam risk assessment."
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        result = response.text

        # Display result
        if "scam" in result.lower() or "high risk" in result.lower():
            st.error(f"⚠️ Warning: This scheme appears to be risky or a potential scam! 🚨\n\n**Reasoning:**\n{result}")
        else:
            st.success(f"✅ This scheme appears to be legitimate, but always do further research.\n\n**Analysis:**\n{result}")

        st.write("🔍 **Tips to Avoid Scams:**")
        st.markdown("""
        - Verify if the scheme is **registered with SEBI**.
        - Be cautious of **guaranteed high returns**.
        - Avoid **pressure tactics** and **urgency-based investments**.
        - Cross-check with **official government sources**.
        """)

