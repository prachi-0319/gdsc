import streamlit as st
from RAG_Model.RAG_copy import get_teaching_response_with_quiz

# CSS Styling (keeping your original styles but adding improvements)
st.markdown("""
<style>
    .profile-header h1 {
        color: #556b3b;
        font-size: 60px;
        margin-bottom: 0.5rem;
    }
    
    .section-header {
        color: #4ecdc4;
        border-bottom: 2px solid #45b7d1;
        padding-bottom: 10px;
        margin: 2rem 0 1rem;
    }
    
    /* Improved container styling */
    .stContainer {
        background-color: #1e1e1e;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #2c2c2c;
    }
    
    /* Better learning path visualization */
    .path-container {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid #2c2c2c;
    }
    
    .chapter-nodes-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .chapter-node {
        text-align: center;
        transition: all 0.3s ease;
        color: #e0e0e0;
        flex: 1;
        position: relative;
    }
    
    .chapter-node.active {
        transform: scale(1.05);
    }
    
    .node-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #2c2c2c;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 8px;
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
        height: 2px;
        background-color: #2c2c2c;
        flex-grow: 1;
        margin: 0 10px;
    }
    
    .subtopic-list {
        margin-top: 1.5rem;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #2c2c2c;
    }
    
    .subtopic-item {
        margin: 0.5rem 0;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.3s ease;
        color: #b0b0b0;
    }
    
    .subtopic-item.active {
        background-color: #45b7d1;
        color: #121212;
        font-weight: 600;
    }
    
            
    /* Content formatting */
    .teaching-content {
        line-height: 1.6;
        color: rgb(100,117,80);
    }
    
    .teaching-content h3 {
        margin-top: 1.5rem;
        font-weight: bold;
    }
    
    .teaching-content ul, 
    .teaching-content ol {
        padding-left: 1.5rem;
        margin: 0.5rem 0;
    }
    
    .teaching-content li {
        margin-bottom: 0.5rem;
    }
    
    /* Quiz styling */
    .quiz-container {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        border: 1px solid #2c2c2c;
    }
    
    .quiz-question {
        font-weight: bold;
        color: #e0e0e0;
        margin-bottom: 0.5rem;
    }
    
    .quiz-option {
        margin-left: 1rem;
        margin-bottom: 0.25rem;
    }
            
    .chapter-node {
        text-align: center;
        padding: 10px;
    }
    .node-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #a8ba95;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 5px auto;
        font-weight: bold;
        color: #edf5e4;
        border: 2px solid #edf5e4;
    }
    .node-circle.active {
        background-color: #727d66;
        color: #edf5e4;
        box-shadow: 0 4px 6px rgba(141, 156, 124, 0.3);
    }
    .chapter-title {
        text-align: center;
        font-size: 0.9rem;
        color: #88947b;
        margin-top: 5px;
    }
    .chapter-node.active .chapter-title {
        font-weight: bold;
        color: #58614e;
    }
    .subtopic-list {
        margin-top: 20px;
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 15px;
    }
    .subtopic-item {
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 4px;
        color: #88947b;
        background-color: #f5f5f5;
    }
    .subtopic-item.active {
        background-color: rgba(141, 156, 124, 0.3);
        color: #58614e;
        font-weight: 600;
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

chapter_options = [
    "Chapter 1: Financial Analysis",
    "Chapter 2: The Finance Perspective",
    "Chapter 3: The Financial Ecosystem",
    "Chapter 4: Sources of Value Creation",
    "Chapter 5: The Art and Science of Valuation"
]



st.markdown("""
<div class="profile-header">
    <h1 style="text-align:center;">📚 Personalized Study Companion</h1>
    <p style="text-align:center;">
        Say hello to your smart learning buddy!<br>
        This AI uses Retrieval-Augmented Generation (RAG) to tailor chapters just for you — based on your profile!<br>
        Whether you're brushing up or diving deep, your personalized content is only a click away.
    </p>
</div>
""", unsafe_allow_html=True)



st.markdown("")
st.markdown("")
st.markdown("")

# Selection section
with st.container():    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('### 📖 Choose Your Concept')
        selected_chapter_full = st.selectbox(
            "**Select Chapter**",
            chapter_options,
            index=0,
            help="Choose which financial concept you want to explore"
        )
        chapter_key = selected_chapter_full.split(":")[0]
    
        subtopics = chapters[chapter_key]
        selected_subtopic = st.selectbox(
            "**Select Subtopic**",
            subtopics,
            index=0,
            help="Pick a specific aspect to focus on"
        )
    
    with col2:
        st.markdown('### 🎯 Personalize Your Experience')
        age = st.number_input(
            "**Your Age**",
            min_value=10,
            max_value=100,
            value=20,
            step=1,
            help="We'll adapt the content complexity based on your age"
        )
        
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)  # Spacer
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
            
            # Split teaching content and quiz
            if "### Quiz" in result:
                teaching_content = result.split("### Quiz")[0]
                quiz_content = result.split("### Quiz")[1]
            else:
                teaching_content = result
                quiz_content = ""
            
            # Display teaching content with proper formatting
            st.markdown("---")
            st.markdown("### 📝 Teaching Content")
            st.markdown(f'<div class="teaching-content">{teaching_content}</div>', unsafe_allow_html=True)
            
            # Display quiz if exists
            if quiz_content:
                st.markdown("---")
                st.markdown("### ❓ Quiz")
                st.markdown(f'<div class="quiz-container">{quiz_content}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"⚠️ Error generating content: {str(e)}")
else:
    st.markdown("""
        <div style='text-align: center; margin: 3rem 0; color: #7f8c8d;'>
            Select your preferences above and click "Generate" to begin
        </div>
    """, unsafe_allow_html=True)



# Learning Path Visualization - Improved Version
st.markdown("")
st.markdown("")
st.markdown("---")
st.markdown("")
st.markdown("")
st.markdown('## 🗺️ Your Learning Path')

st.markdown("")
with st.container():
    # Create columns for chapter nodes
    cols = st.columns(5)
    for i, (col, chapter) in enumerate(zip(cols, chapter_options)):
        is_active = (chapter.split(":")[0] == chapter_key)
        chapter_num = chapter.split(":")[0]
        
        col.markdown(
            f"""
            <div class="chapter-node">
                <div class="node-circle {'active' if is_active else ''}">{i+1}</div>
                <div class="chapter-title">{chapter_num}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    for subtopic in chapters[chapter_key]:
        is_active_sub = (subtopic == selected_subtopic)
        st.markdown(
            f"""
            <div class="subtopic-item {'active' if is_active_sub else ''}">
                {subtopic}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)