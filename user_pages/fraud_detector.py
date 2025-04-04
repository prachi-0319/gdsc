import streamlit as st
import google.generativeai as genai
import os


with st.expander("Fraud Analysis"):
    import streamlit as st
  
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

with st.expander("Government Schemes"):
    import streamlit as st
    api_key = st.secrets['GOOGLE']['GEMINI_API_KEY']
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.error("API key not found. Please set GEMINI_API_KEY in your .env file.")

    st.markdown("""
    <div>
        <h1 style="font-size:60px; color:white; text-align:center;">📢 Find Government Schemes</h1>
        <p style="text-align:center;">Never miss out on benefits - find schemes made for your situation! Answer these quick questions to uncover government schemes matching your profile. We’ll help you identify benefits, subsidies, and assistance programs you may qualify for based on your age, income, and background.</p>
        <p>Note: Recommendations are based on current schemes - always verify details with official sources.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    # User Inputs
    age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
    income = st.number_input("Annual Income (₹)", min_value=0, step=10000)
    category = st.selectbox("Category", ["General", "SC/ST", "OBC", "Minority", "Women", "Farmer", "Senior Citizen"])
    employment = st.selectbox("Employment Status", ["Unemployed", "Salaried", "Self-Employed", "Student", "Retired"])
    sector = st.selectbox("Sector of Interest", ["Education", "Business", "Housing", "Agriculture", "Health", "Pension", "Startup"])

    st.markdown("")
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
