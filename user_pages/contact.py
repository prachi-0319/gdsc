# import streamlit as st
# import re

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .contact-header {
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .contact-header h1 {
#         color: #2E86C1;
#         font-size: 2.5rem;
#     }
#     .contact-form {
#         background-color: #f8f9fa;
#         border-radius: 10px;
#         padding: 2rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         max-width: 800px;
#         margin: 0 auto;
#     }
#     .stTextInput>div>div>input, 
#     .stTextArea>div>div>textarea,
#     .stSelectbox>div>div>select {
#         border: 1px solid #D4E6F1;
#         border-radius: 8px;
#     }
            
#     /* Style the file uploader to look like a drag-and-drop zone */
#     .stFileUploader>div>div>div>div {
#         border: 2px dashed #D4E6F1;
#         border-radius: 8px;
#         padding: 2rem 1rem;
#         text-align: center;
#         background-color: #fdfdfd;
#     }
#     .stFileUploader>div>div>div>div:hover {
#         border-color: #2E86C1;
#         background-color: #f5f9ff;
#     }
# </style>
# """, unsafe_allow_html=True)



# # Contact Page Header
# st.markdown("""
# <div>
#     <h1 style="font-size:60px; color:white; text-align:center;">📨 Contact Us</h1>
#     <p style="text-align:center;">Have questions or feedback? We'd love to hear from you!</p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("")
# st.markdown("")
# st.markdown("")

# # Contact Form
# with st.form("contact_form", clear_on_submit=True):
#     # st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    
#     # Form Columns
#     col1, col2, col3 = st.columns([0.9, 0.01, 0.9])
    
#     with col1:
#         name = st.text_input("Full Name*", placeholder="Enter your full name")
        
#     with col3:
#         email = st.text_input("Email Address*", placeholder="Enter your email")
    
#     st.markdown("")
#     phone = st.text_input("Phone Number (Optional)", placeholder="+91 ")
    
#     st.markdown("")
#     # Subject Dropdown with Custom option
#     subject_options = [
#         "Account Support",
#         "Technical Issues",
#         "Feature Request",
#         "Partnership Inquiry",
#         "Feedback/Suggestions",
#         "Other (Custom)"
#     ]
    
#     subject = st.selectbox("Subject*", options=subject_options)
    
#     if subject == "Other (Custom)":
#         custom_subject = st.text_input("Please specify your subject", placeholder="Enter your custom subject")
#         subject = custom_subject
    
#     st.markdown("")

#     # Message Text Area
#     message = st.text_area("Your Message*", 
#                          placeholder="Please describe your inquiry in detail...",
#                          height=150)
    
#     st.markdown("")
#     # Unified File Uploader with drag-and-drop styling
#     uploaded_file = st.file_uploader(
#         "📎 Attach File (Optional) - Max 5MB",
#         type=["pdf", "docx", "jpg", "png"],
#         help="Drag and drop files here or click to browse"
#     )

#     st.markdown("")

#     # Form Submission
#     submitted = st.form_submit_button("📤 Send Message", type="primary")
    
#     # if submitted:
#     #     errors = []

#     #     if not name or not email or not message:
#     #         st.error("Please fill in all required fields (*)")

#     #     else:
#     #         # Here you would typically process the form data
#     #         # For demo, we'll just show a success message
#     #         st.success("""
#     #         ✅ Thank you for your message!
#     #         We've received your inquiry and will get back to you within 24 hours.
#     #         """)
            
#     #         # For demo purposes - show what would be submitted
#     #         with st.expander("Preview Submission"):
#     #             st.write("**Name:**", name)
#     #             st.write("**Email:**", email)
#     #             st.write("**Phone:**", phone if phone else "Not provided")
#     #             st.write("**Subject:**", subject)
#     #             st.write("**Message:**", message)
#     #             if uploaded_file:
#     #                 st.write("**Attachment:**", uploaded_file.name)



#     if submitted:
#         errors = []
#         errors_data = []
        
#         # Name validation (not empty)
#         if not name:
#             errors.append("Please enter your name")
            
#         # Email validation
#         if not email:
#             errors.append("Please enter your email")
#         elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             errors_data.append("Please enter a valid email address")
            
#         # Phone validation (if provided)
#         if not phone:
#             errors.append("Please enter your phone number")
#         if phone and not phone.lstrip('+').isdigit():
#             errors_data.append("Please enter a valid phone number (digits only)")
            
#         # Message validation (not empty)
#         if not message:
#             errors.append("Please enter your message")
            
#         # File validation (if provided)
#         if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:  # 5MB
#             errors_data.append("File size exceeds 5MB limit")
            
#         if errors_data or errors:
#             if len(errors)>0:
#                 st.error("Please fill all the required fields.")

#             for error in errors_data:
#                 st.error(error)
#         else:
#             # Process the form data
#             st.success("""
#             ✅ Thank you for your message!
#             We've received your inquiry and will get back to you within 24 hours.
#             """)
            
#             with st.expander("Preview Submission"):
#                 st.write("**Name:**", name)
#                 st.write("**Email:**", email)
#                 st.write("**Phone:**", phone if phone else "Not provided")
#                 st.write("**Subject:**", subject)
#                 st.write("**Message:**", message)
#                 if uploaded_file:
#                     st.write("**Attachment:**", uploaded_file.name, f"({uploaded_file.size//1024} KB)")

    
#     st.markdown('</div>', unsafe_allow_html=True)

# # Additional Contact Info
# st.markdown("""
# <div style="text-align: center; margin-top: 3rem;">
#     <h3>📞 Other Ways to Reach Us</h3>
#     <p>Email: support@finfriend.com</p>
#     <p>Phone: +91 1800 123 4567</p>
#     <p>Available Monday-Friday, 9AM-6PM IST</p>
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
from streamlit_modal import Modal
import re

# # Initialize the modal
# contact_modal = Modal(
#     title="📨 Contact Us",
#     key="contact_modal",
#     # Optional - makes modal wider
#     max_width=800  
# )

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