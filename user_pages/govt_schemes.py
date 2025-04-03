# import streamlit as st
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os 

# # Load API key for Gemini from the .env file
# # load_dotenv()
# # api_key = os.getenv("GEMINI_API_KEY")
# # if api_key:
# #     genai.configure(api_key=api_key)
# # else:
# #     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
# if api_key:
#     genai.configure(api_key=api_key)
# else:
#     st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")


# # st.set_page_config(page_title="Govt. Schemes Finder", layout="centered")
# # st.title("📢 Find Government Schemes")
# # st.write("Never miss out on benefits - find schemes made for your situation! Answer these quick questions to uncover government schemes matching your profile. We’ll help you identify benefits, subsidies, and assistance programs you may qualify for based on your age, income, and background.")
# # st.write("Note: Recommendations are based on current schemes - always verify details with official sources.")


# st.markdown("""
# <div>
#     <h1 style="font-size:60px; color:white; text-align:center;">📢 Find Government Schemes</h1>
#     <p style="text-align:center;">Never miss out on benefits - find schemes made for your situation! Answer these quick questions to uncover government schemes matching your profile. We’ll help you identify benefits, subsidies, and assistance programs you may qualify for based on your age, income, and background.</p>
#     <p>Note: Recommendations are based on current schemes - always verify details with official sources.</p>
# </div>
# """, unsafe_allow_html=True)
# st.markdown("")
# st.markdown("")
# # User Inputs
# age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
# income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
# category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority", "Women", "Farmer", "Senior Citizen"])
# employment = st.selectbox("Employment Status", ["Unemployed", "Salaried", "Self-Employed", "Student", "Retired"])
# sector = st.selectbox("Sector of Interest", ["Education", "Business", "Housing", "Agriculture", "Health", "Pension", "Startup"])

# st.markdown("")
# if st.button("Find Schemes"):
#     with st.spinner("🔍 Searching for best schemes..."):
#         query = (
#             f"Suggest government schemes in India for a {category} person aged {age} "
#             f"with an annual income of ₹{income}. They are {employment} and interested in {sector}. "
#             "Provide eligibility details and official links."
#         )
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content(query)
#         schemes = response.text

#         st.subheader("✅ Recommended Schemes")

#         # Split response into structured parts
#         scheme_list = schemes.split("\n\n")

#         for scheme in scheme_list:
#             if scheme.strip():  # Avoid empty responses
#                 with st.container():
#                     # st.markdown("📌 **" + scheme.split(":")[0] + "**")  # Highlight scheme title
#                     st.write(scheme)  # Preserve formatting inside cards
#                     st.divider()  # Adds a visual separator for clarity

#         st.info("ℹ️ Always verify details on official government websites.")


import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os 

# Configure API
api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# Custom CSS for styling
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        text-align: center;
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .disclaimer {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    .form-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .scheme-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #4b6cb7;
    }
    .scheme-title {
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        border: 1px solid #ddd;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-container">
    <div class="header-title">📢 Government Schemes Finder</div>
    <div class="header-subtitle">Never miss out on benefits - find schemes made for your situation!</div>
    <div class="disclaimer">Note: Recommendations are based on current schemes - always verify details with official sources.</div>
</div>
""", unsafe_allow_html=True)

# Form Section
with st.container():
    st.markdown("""
    <div class="form-container">
        <h3 style="color: #2c3e50; margin-bottom: 1.5rem;">Tell us about yourself</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
        income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
        category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority", "Women", "Farmer", "Senior Citizen"])
    
    with col2:
        employment = st.selectbox("Employment Status", ["Unemployed", "Salaried", "Self-Employed", "Student", "Retired"])
        sector = st.selectbox("Sector of Interest", ["Education", "Business", "Housing", "Agriculture", "Health", "Pension", "Startup"])
    
    st.markdown("</div>", unsafe_allow_html=True)

# Search Button (centered)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    search_clicked = st.button("🔍 Find Suitable Schemes", use_container_width=True)

# Results Section
if search_clicked:
    with st.spinner("🔍 Searching for best schemes..."):
        query = (
            f"Suggest government schemes in India for a {category} person aged {age} "
            f"with an annual income of ₹{income}. They are {employment} and interested in {sector}. "
            "Provide eligibility details and official links. Format each scheme with: "
            "1. Scheme Name (bold heading) \n"
            "2. Brief description \n"
            "3. Eligibility criteria \n"
            "4. Benefits \n"
            "5. Official link (if available)"
        )
        
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        schemes = response.text

        st.subheader("✅ Recommended Schemes", divider="blue")
        
        # Split response into structured parts
        scheme_list = schemes.split("\n\n")
        
        for scheme in scheme_list:
            if scheme.strip():  # Avoid empty responses
                with st.container():
                    st.markdown(f"""
                    <div class="scheme-card">
                        {scheme.replace("**", "<span class='scheme-title'>").replace("**", "</span>")}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.info("ℹ️ Always verify details on official government websites before applying.")