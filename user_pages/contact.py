import streamlit as st
from streamlit.components.v1 import html
import base64

# Custom CSS for styling
st.markdown("""
<style>
    .contact-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .contact-header h1 {
        color: #2E86C1;
        font-size: 2.5rem;
    }
    .contact-form {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: 0 auto;
    }
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        border: 1px solid #D4E6F1;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E5F8B;
        transform: translateY(-2px);
    }
    .file-upload {
        border: 2px dashed #D4E6F1;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Contact Page Header
st.markdown("""
<div class="contact-header">
    <h1>📨 Contact Us</h1>
    <p>Have questions or feedback? We'd love to hear from you!</p>
</div>
""", unsafe_allow_html=True)

# Contact Form
with st.form("contact_form", clear_on_submit=True):
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    
    # Form Columns
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        
    with col2:
        email = st.text_input("Email Address*", placeholder="Enter your email")
    
    phone = st.text_input("Phone Number (Optional)", placeholder="+91 ")
    
    # Subject Dropdown with Custom option
    subject_options = [
        "Account Support",
        "Technical Issues",
        "Feature Request",
        "Partnership Inquiry",
        "Feedback/Suggestions",
        "Other (Custom)"
    ]
    subject = st.selectbox("Subject*", options=subject_options)
    
    if subject == "Other (Custom)":
        custom_subject = st.text_input("Please specify your subject", placeholder="Enter your custom subject")
        subject = custom_subject
    
    # Message Text Area
    message = st.text_area("Your Message*", 
                         placeholder="Please describe your inquiry in detail...",
                         height=150)
    
    # File Upload
    st.markdown("""
    <div class="file-upload">
        <p>📎 Attach File (Optional)</p>
        <p style="font-size: 0.8rem; color: #666;">Max file size: 5MB</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf", "docx", "jpg", "png"], 
                                   label_visibility="collapsed")
    
    # Form Submission
    submitted = st.form_submit_button("📤 Send Message", type="primary")
    
    if submitted:
        if not name or not email or not message:
            st.error("Please fill in all required fields (*)")
        else:
            # Here you would typically process the form data
            # For demo, we'll just show a success message
            st.success("""
            ✅ Thank you for your message!
            We've received your inquiry and will get back to you within 24 hours.
            """)
            
            # For demo purposes - show what would be submitted
            with st.expander("Preview Submission"):
                st.write("**Name:**", name)
                st.write("**Email:**", email)
                st.write("**Phone:**", phone if phone else "Not provided")
                st.write("**Subject:**", subject)
                st.write("**Message:**", message)
                if uploaded_file:
                    st.write("**Attachment:**", uploaded_file.name)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Additional Contact Info
st.markdown("""
<div style="text-align: center; margin-top: 3rem;">
    <h3>📞 Other Ways to Reach Us</h3>
    <p>Email: support@finfriend.com</p>
    <p>Phone: +91 1800 123 4567</p>
    <p>Available Monday-Friday, 9AM-6PM IST</p>
</div>
""", unsafe_allow_html=True)