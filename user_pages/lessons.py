import streamlit as st
from RAG_Model.RAG_copy import get_teaching_response_with_quiz
st.markdown("""
    <style>
        /* Header Styling */
        .header-text {
            color: #4ecdc4;
            text-align: center;
            font-weight: 700;
            margin-bottom: 20px;
        }

        .section-header {
            color: #4ecdc4;
            border-bottom: 2px solid #45b7d1;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        /* Container Styling */
        .stContainer {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid #2c2c2c;
        }

        /* Learning Path Visualization */
        .path-container {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 30px;
            margin-top: 20px;
            border: 1px solid #2c2c2c;
        }

        .chapter-node {
            text-align: center;
            transition: all 0.3s ease;
            color: #e0e0e0;
        }

        .chapter-node.active {
            transform: scale(1.05);
        }

        .node-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #2c2c2c;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-weight: bold;
            color: #4ecdc4;
            transition: all 0.3s ease;
            border: 2px solid #45b7d1;
        }

        .chapter-node.active .node-circle {
            background-color: #45b7d1;
            color: #121212;
            box-shadow: 0 4px 6px rgba(69, 183, 209, 0.3);
        }

        .connector-line {
            height: 3px;
            background-color: #2c2c2c;
            flex-grow: 1;
            margin: 25px -10px;
        }

        .subtopic-list {
            margin-top: 30px;
            background-color: #1a1a1a;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #2c2c2c;
        }

        .subtopic-item {
            margin: 10px 0;
            padding: 8px 15px;
            border-radius: 6px;
            transition: all 0.3s ease;
            color: #b0b0b0;
        }

        .subtopic-item.active {
            background-color: #45b7d1;
            color: #121212;
            font-weight: 600;
        }

        /* Streamlit Widget Styling */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
            border: 1px solid #2c2c2c !important;
        }


        /* Result Box */
        .result-box {
            background-color: #1e1e1e;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            padding: 25px;
            margin-top: 20px;
            border: 1px solid #2c2c2c;
            color: #e0e0e0;
        }

        /* Footer */
        .footer {
            color: #b0b0b0;
            text-align: center;
            padding: 20px;
            background-color: #1a1a1a;
            border-top: 1px solid #2c2c2c;
        }

        /* Markdown Styling */
        .stMarkdown {
            color: #e0e0e0;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #4ecdc4;
        }
    </style>
""", unsafe_allow_html=True)

# Chapter data remains the same
chapters = {
    "Chapter 1": [
        "Assets",
        "Liabilities and Shareholders' Equity",
        "Understanding Ratios",
        "Profitability",
        "Financing and Leverage",
        "Productivity or Efficiency",
        "Summary"
    ],
    "Chapter 2": [
        "What We Talk about When We Talk about Cash",
        "Net Profit, EBIT, and EBITDA",
        "From EBITDA to Operating Cash Flows",
        "Working capital, Accounts receivable, Inventory, Accounts payable",
        "The cash conversion cycle",
        "Free Cash Flows",
        "Fixated on the Future",
        "Discounting",
        "Summary"
    ],
    "Chapter 3": [
        "Why Can't Finance Be Simple?",
        "The Companies",
        "Buy Side:",
        "Mutual funds",
        "Pension funds.",
        "Foundations and endowment funds.",
        "Sovereign wealth funds.",
        "Hedge funds",
        "Sell Side:",
        "Traders",
        "Salespeople",
        "Investment bankers",
        "Incentives for Equity Analysts",
        "The Problem at the Heart of Capital Markets",
        "The Persistence of the Principal-Agent Problem",
        "Summary"
    ],
    "Chapter 4": [
        "How Is Value Created?",
        "What Else Matters in Value Creation?",
        "Three Ways to Create Value",
        "A Deeper Dive into Costs of Capital",
        "The cost of debt",
        "Credit spreads.",
        "Optimal capital structure",
        "The cost of equity",
        "What is risk?",
        "Calculating betas.",
        "The price of risk",
        "CAPM and the cost of equity",
        "Common Mistakes with WACC",
        "Using the same cost of capital for all investments",
        "Lowering your WACC by using more debt",
        "Exporting WACC",
        "Summary"
    ],
    "Chapter 5": [
        "Two Alternative Valuation Methods:",
        "Multiples",
        "The pros and cons of multiples",
        "Problematic Methods for Assessing Value",
        "Payback periods",
        "Internal rates of return",
        "Discounted Cash Flows",
        "Free cash flows",
        "Valuation Mistakes",
        "Ignoring Incentives",
        "Exaggerating Synergies and Ignoring Integration Costs",
        "Underestimating Capital Intensity",
        "Summary"
    ]
}
 # (Keep the original chapters dictionary here)

chapter_options = [
    "Chapter 1: Financial Analysis",
    "Chapter 2: The Finance Perspective",
    "Chapter 3: The Financial Ecosystem",
    "Chapter 4: Sources of Value Creation",
    "Chapter 5: The Art and Science of Valuation"
]  # (Keep the original chapter options here)


# Main app content
st.markdown("""
<div class="profile-header">
    <h1 style="font-size:55px; color:white; text-align:center;">📚 Finance Learning Companion</h1>
    <p style="text-align:center;">Our <span class="highlight">hybrid recommendation system</span> combines traditional finance rules with machine learning 
    to create a balanced portfolio allocation tailored to your specific needs.</p>
</div>
""", unsafe_allow_html=True)
# Selection section
st.markdown("")
st.markdown("")
st.markdown("")
with st.container():
    st.markdown('<h2 class="section-header">📖 Choose Your Learning Path</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        selected_chapter_full = st.selectbox(
            "**Select Chapter**",
            chapter_options,
            index=0,
            help="Choose which financial concept you want to explore"
        )
        chapter_key = selected_chapter_full.split(":")[0]
    
    with col2:
        subtopics = chapters[chapter_key]
        selected_subtopic = st.selectbox(
            "**Select Subtopic**",
            subtopics,
            index=0,
            help="Pick a specific aspect to focus on"
        )

st.markdown("---")

# Personalization section
with st.container():
    st.markdown('<h2 class="section-header">🎯 Personalize Your Experience</h2>', unsafe_allow_html=True)
    age = st.number_input(
        "**Your Age**",
        min_value=10,
        max_value=100,
        value=20,
        step=1,
        help="We'll adapt the content complexity based on your age"
    )

st.markdown("---")

# Generate button
generate_col, _ = st.columns([0.3, 0.7])
with generate_col:
    generate_btn = st.button(
        "🚀 Generate Learning Content",
        use_container_width=True,
        type="primary"
    )

# Result display
if generate_btn:
    with st.spinner("✨ Crafting your personalized learning experience..."):
        try:
            result = get_teaching_response_with_quiz(chapter_key, selected_subtopic, str(age))
            
            with st.container():
                st.markdown("---")
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                st.markdown("### 📝 Teaching Content")
                if "### Quiz" in result:
                    teaching_content = result.split("### Quiz")[0]
                    quiz_content = "### ❓ Quiz\n" + result.split("### Quiz")[1]
                else:
                    teaching_content = result
                    quiz_content = ""
                
                st.markdown(teaching_content)
                
                if quiz_content:
                    st.markdown("---")
                    st.markdown("### 📝 Teaching Content")
                    st.markdown(quiz_content)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"⚠️ Error generating content: {str(e)}")
else:
    st.markdown("""
        <div style='text-align: center; margin: 50px 0; color: #7f8c8d;'>
            Select your preferences above and click "Generate" to begin
        </div>
    """, unsafe_allow_html=True)



# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; margin-top: 30px;'>
        Made with ❤️ using Streamlit | Finance Master v1.0
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown('<h2 class="section-header">🗺️ Your Learning Path</h2>', unsafe_allow_html=True)

# Create the learning path visualization
with st.container():
    st.markdown('<div class="path-container">', unsafe_allow_html=True)
    
    # Create chapter nodes
    cols = st.columns(len(chapter_options) * 2 - 1)
    chapter_index = list(chapters.keys()).index(chapter_key)
    
    for i, chapter in enumerate(chapter_options):
        col_idx = i * 2
        is_active = (chapter.split(":")[0] == chapter_key)
        
        with cols[col_idx]:
            st.markdown(f'<div class="chapter-node {"active" if is_active else ""}">'
                        f'<div class="node-circle">{i+1}</div>'
                        f'<div>{"<b>" if is_active else ""}{chapter.split(":")[0]}'
                        f'{"</b>" if is_active else ""}</div></div>', 
                        unsafe_allow_html=True)
        
        # Add connector line after each chapter except last
        if i < len(chapter_options) - 1:
            with cols[col_idx + 1]:
                st.markdown('<div class="connector-line"></div>', unsafe_allow_html=True)
    
    # Add subtopic progression
    st.markdown(f'<div class="subtopic-list">', unsafe_allow_html=True)
    for subtopic in chapters[chapter_key]:
        is_active_sub = (subtopic == selected_subtopic)
        st.markdown(f'<div class="subtopic-item {"active" if is_active_sub else ""}">'
                    f'{subtopic}</div>', 
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)