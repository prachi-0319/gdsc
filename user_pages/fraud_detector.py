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


# import streamlit as st
# import google.generativeai as genai

# # Configure API
# api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .header-container {
#         background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
#         padding: 2.5rem;
#         border-radius: 12px;
#         margin-bottom: 2rem;
#         color: white;
#     }
#     .header-title {
#         font-size: 2.8rem;
#         font-weight: 700;
#         text-align: center;
#         margin-bottom: 0.5rem;
#     }
#     .header-subtitle {
#         text-align: center;
#         font-size: 1.2rem;
#         opacity: 0.9;
#         margin-bottom: 0.5rem;
#     }
#     .tool-container {
#         background-color: #f8f9fa;
#         padding: 2rem;
#         border-radius: 12px;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#     }
#     .tool-title {
#         color: #2c3e50;
#         font-size: 1.8rem;
#         font-weight: 600;
#         margin-bottom: 1.5rem;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }
#     .scheme-card {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1.5rem;
#         margin-bottom: 1rem;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         border-left: 4px solid #4b6cb7;
#     }
#     .warning-card {
#         background-color: white;
#         border-radius: 10px;
#         padding: 1.5rem;
#         margin-bottom: 1rem;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#         border-left: 4px solid #e74c3c;
#     }
#     .stButton>button {
#         background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 0.75rem 1.5rem;
#         font-size: 1rem;
#         transition: all 0.3s;
#         width: 100%;
#     }
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#     }
#     .danger-button {
#         background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
#     }
#     .highlight {
#         background-color: #f39c12;
#         padding: 0.2rem 0.4rem;
#         border-radius: 4px;
#         font-weight: 500;
#         color: white;
#     }
#     .tab-container {
#         display: flex;
#         gap: 1rem;
#         margin-bottom: 1.5rem;
#     }
#     .tab {
#         padding: 0.75rem 1.5rem;
#         border-radius: 8px;
#         cursor: pointer;
#         font-weight: 600;
#         transition: all 0.3s;
#     }
#     .tab.active {
#         background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
#         color: white;
#     }
#     .tab.inactive {
#         background-color: #ecf0f1;
#         color: #7f8c8d;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state for active tab
# if 'active_tab' not in st.session_state:
#     st.session_state.active_tab = 'schemes'

# # Header Section
# st.markdown("""
# <div class="header-container">
#     <div class="header-title">🔍 Financial Safety Toolkit</div>
#     <div class="header-subtitle">Discover government benefits and protect yourself from scams - all in one place</div>
# </div>
# """, unsafe_allow_html=True)

# # Tab Navigation
# col1, col2 = st.columns(2)
# with col1:
#     if st.button("🏛️ Find Government Schemes", key="schemes_tab", 
#                 use_container_width=True, 
#                 type="primary" if st.session_state.active_tab == 'schemes' else "secondary"):
#         st.session_state.active_tab = 'schemes'
# with col2:
#     if st.button("🚨 Fraud Detection", key="fraud_tab", 
#                 use_container_width=True, 
#                 type="primary" if st.session_state.active_tab == 'fraud' else "secondary"):
#         st.session_state.active_tab = 'fraud'

# # Government Schemes Finder
# if st.session_state.active_tab == 'schemes':
#     with st.container():
#         st.markdown("")
#         st.markdown("")
#         st.markdown("Never miss out on benefits - find schemes made for your situation!")
#         # st.markdown("""
#         # <div>
#         #     <div class="tool-title">🏛️ Find Government Schemes</div>
#         #     <p>Never miss out on benefits - find schemes made for your situation!</p>
#         # """, unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
#             income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
#             category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority", "Women", "Farmer", "Senior Citizen"])
        
#         with col2:
#             employment = st.selectbox("Employment Status", ["Unemployed", "Salaried", "Self-Employed", "Student", "Retired"])
#             sector = st.selectbox("Sector of Interest", ["Education", "Business", "Housing", "Agriculture", "Health", "Pension", "Startup"])
        
#         st.markdown("</div>", unsafe_allow_html=True)

#         st.markdown("")
#         st.markdown("")
#         # Search Button
#         if st.button("🔍 Find Suitable Schemes", use_container_width=True):
#             with st.spinner("🔍 Searching for best schemes..."):
#                 query = (
#                     f"Suggest government schemes in India for a {category} person aged {age} "
#                     f"with an annual income of ₹{income}. They are {employment} and interested in {sector}. "
#                     "Provide eligibility details and official links. Format each scheme with: "
#                     "1. Scheme Name (bold heading) \n"
#                     "2. Brief description \n"
#                     "3. Eligibility criteria \n"
#                     "4. Benefits \n"
#                     "5. Official link (if available)"
#                 )
                
#                 model = genai.GenerativeModel("gemini-2.0-flash")
#                 response = model.generate_content(query)
#                 schemes = response.text

#                 st.markdown("")
#                 st.markdown("")
#                 st.subheader("✅ Recommended Schemes", divider="blue")
                
#                 scheme_list = schemes.split("\n\n")
                
#                 for scheme in scheme_list:
#                     if scheme.strip():
#                         with st.container():
#                             st.markdown(f"""
#                             <div class="scheme-card">
#                                 {scheme.replace("**", "<span style='font-weight:600;color:#2c3e50;'>").replace("**", "</span>")}
#                             </div>
#                             """, unsafe_allow_html=True)
                
#                 st.info("ℹ️ Always verify details on official government websites before applying.")

# # Fraud Detector
# else:
#     with st.container():
#         st.markdown("")
#         st.markdown("")
#         st.markdown("Verify before you invest—protect your hard-earned money")
#         st.markdown("Always consult a certified financial advisor for high-risk investments.")
#         st.markdown("")
#         st.markdown("")
#         # st.markdown("""
#         # <div class="tool-container">
#         #     <div class="tool-title">🚨 Fraud & Scam Detection</div>
#         #     <p>Verify before you invest—protect your hard-earned money!</p>
#         #     <p>Note: <span class="highlight">Always consult a certified financial advisor</span> for high-risk investments.</p>
#         # """, unsafe_allow_html=True)
        
#         scheme_name = st.text_input("Scheme Name", placeholder="e.g., Golden Future Investment Plan")
#         promised_returns = st.text_input("Promised Returns", placeholder="e.g., 20% monthly")
#         minimum_investment = st.number_input("Minimum Investment (₹)", min_value=0, step=100)
#         company_info = st.text_area("Company Details", placeholder="Enter any details you have about the company.")
        
#         st.markdown("</div>", unsafe_allow_html=True)

#         if st.button("🔎 Check Legitimacy", use_container_width=True, type="primary"):
#             with st.spinner("Analyzing..."):
#                 query = f"Is '{scheme_name}' a legitimate investment scheme in India? It promises {promised_returns} returns with a minimum investment of ₹{minimum_investment}. The company details are: {company_info}. Provide a scam risk assessment."
#                 model = genai.GenerativeModel("gemini-2.0-flash")
#                 response = model.generate_content(query)
#                 result = response.text

#                 if "scam" in result.lower() or "high risk" in result.lower():
#                     st.error(f"""
#                     <div class="warning-card">
#                         <h3>⚠️ Warning: Potential Scam Detected!</h3>
#                         <p>{result}</p>
#                     </div>
#                     """)
#                 else:
#                     st.success(f"""
#                     <div class="scheme-card">
#                         <h3>✅ This scheme appears legitimate</h3>
#                         <p>{result}</p>
#                     </div>
#                     """, unsafe_allow_html=True)

#                 st.markdown("""
#                 <div class="scheme-card">
#                     <h4>🔍 Tips to Avoid Scams:</h4>
#                     <ul>
#                         <li>Verify if the scheme is <b>registered with SEBI/RBI</b></li>
#                         <li>Be cautious of <b>guaranteed high returns</b></li>
#                         <li>Avoid <b>pressure tactics</b> and urgency-based investments</li>
#                         <li>Cross-check with <b>official government sources</b></li>
#                     </ul>
#                 </div>
#                 """, unsafe_allow_html=True)