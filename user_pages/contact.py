import streamlit as st
from streamlit_modal import Modal
import re


# Custom CSS for the contact form
st.markdown("""
<style>
    .contact-form-input {
        border: 1px solid #D4E6F1 !important;
        border-radius: 8px !important;
    }
    .contact-form-textarea {
        border: 1px solid #D4E6F1 !important;
        border-radius: 8px !important;
        min-height: 150px !important;
    }
    .stFileUploader>div>div>div>div {
        border: 2px dashed #D4E6F1 !important;
        border-radius: 8px !important;
        padding: 2rem 1rem !important;
        text-align: center !important;
        background-color: #fdfdfd !important;
    }
    .stFileUploader>div>div>div>div:hover {
        border-color: #2E86C1 !important;
        background-color: #f5f9ff !important;
    }
    /* Style for modal close button */
    .stModal .stButton>button {
        background: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }
</style>
""", unsafe_allow_html=True)



def show_contact_form():
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("Have questions or feedback? We'd love to hear from you!")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
        with col2:
            email = st.text_input("Email Address*", placeholder="Enter your email")
        
        phone = st.text_input("Phone Number (Optional)", placeholder="+91 ")
        
        subject_options = [
            "Account Support", "Technical Issues", "Feature Request",
            "Partnership Inquiry", "Feedback/Suggestions", "Other (Custom)"
        ]
        subject = st.selectbox("Subject*", options=subject_options)
        
        if subject == "Other (Custom)":
            custom_subject = st.text_input("Please specify your subject", 
                                         placeholder="Enter your custom subject")
            subject = custom_subject
        
        message = st.text_area("Your Message*", 
                             placeholder="Please describe your inquiry in detail...",
                             height=150)
        
        uploaded_file = st.file_uploader(
            "📎 Attach File (Optional) - Max 5MB",
            type=["pdf", "docx", "jpg", "png"],
            help="Drag and drop files here or click to browse"
        )

        submitted = st.form_submit_button("📤 Send Message", type="primary")
        
        if submitted:
            errors = []
            errors_data = []
            
            if not name:
                errors.append("Please enter your name")
            if not email:
                errors.append("Please enter your email")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors_data.append("Please enter a valid email address")
            if phone and not phone.lstrip('+').isdigit():
                errors_data.append("Please enter a valid phone number (digits only)")
            if not message:
                errors.append("Please enter your message")
            if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:
                errors_data.append("File size exceeds 5MB limit")
                
            if errors_data or errors:
                if len(errors) > 0:
                    st.error("Please fill all the required fields.")
                for error in errors_data:
                    st.error(error)
            else:
                st.success("""
                ✅ Thank you for your message!
                We've received your inquiry and will get back to you within 24 hours.
                """)
                # Here you would typically process the form data
                st.session_state.form_submitted = True