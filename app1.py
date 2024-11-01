# Import necessary libraries
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure Google Generative AI with the API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to handle PDF upload and conversion to image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Define Streamlit app
def run_app():
    st.set_page_config(page_title="ATS Resume Expert")
    st.header("ATS Tracking System")
    input_text = st.text_area("Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    submit1 = st.button("Tell Me About the Resume")
    submit3 = st.button("Percentage match")

    input_prompt1 = """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
    Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
    the job description. First, the output should come as a percentage, then keywords missing, and last final thoughts.
    """

    if submit1 and uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

    elif submit3 and uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

if __name__ == "__main__":
    run_app()  # start the Streamlit app
