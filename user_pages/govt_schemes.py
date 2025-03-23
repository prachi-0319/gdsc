import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os 

# Load API key for Gemini from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

# st.set_page_config(page_title="Govt. Schemes Finder", layout="centered")
st.title("📢 Find Government Schemes")
st.write("Answer a few simple questions to find government schemes you may be eligible for.")

# User Inputs
age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority", "Women", "Farmer", "Senior Citizen"])
employment = st.selectbox("Employment Status", ["Unemployed", "Salaried", "Self-Employed", "Student", "Retired"])
sector = st.selectbox("Sector of Interest", ["Education", "Business", "Housing", "Agriculture", "Health", "Pension", "Startup"])

if st.button("Find Schemes"):
    with st.spinner("🔍 Searching for best schemes..."):
        query = (
            f"Suggest government schemes in India for a {category} person aged {age} "
            f"with an annual income of ₹{income}. They are {employment} and interested in {sector}. "
            "Provide eligibility details and official links."
        )
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        schemes = response.text

        st.subheader("✅ Recommended Schemes")

        # Split response into structured parts
        scheme_list = schemes.split("\n\n")

        for scheme in scheme_list:
            if scheme.strip():  # Avoid empty responses
                with st.container():
                    # st.markdown("📌 **" + scheme.split(":")[0] + "**")  # Highlight scheme title
                    st.write(scheme)  # Preserve formatting inside cards
                    st.divider()  # Adds a visual separator for clarity

        st.info("ℹ️ Always verify details on official government websites.")
