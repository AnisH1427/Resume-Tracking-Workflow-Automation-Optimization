import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Retrieve and configure the API key for Google Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

# Function to get response from Gemini API
def get_gemini_response(input):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        st.write(f"API Key: {api_key}")  # Debugging line (remove in production)
        return None

# Function to extract text from a PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Prompt template for the ATS
input_prompt = """
Act as a highly skilled Applicant Tracking System (ATS) with deep expertise in various tech fields, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the provided job description. The job market is highly competitive, so provide the best assistance for improving the resume.

Evaluate the resume with the following criteria:
1. Percentage match with the job description.
2. Missing keywords with high accuracy.
3. Highlight the weakness and specify the recommendations whether the employee is fit for the role or not.

Resume:
{text}

Job Description:
{jd}

Respond in the following structure:
JD Match: percentage_match%
Missing Keywords: missing_keywords
Profile Summary: profile_summary
Recommendations: recommendations
"""



# Streamlit app
with st.sidebar:
    st.title("HR Workflow Automation")
    st.subheader("About")
    st.write(
        "This sophisticated ATS project, developed with Gemini Pro and Streamlit, "
        "seamlessly incorporates advanced features including resume match percentage, "
        "keyword analysis to identify missing criteria, and the generation of comprehensive "
        "profile summaries. These features enhance the efficiency and precision of the candidate "
        "evaluation process for discerning talent acquisition professionals."
    )

    st.markdown("""
    ### Resources
    - [Streamlit](https://streamlit.io/)
    - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
    - [Makersuite API Key](https://makersuite.google.com/)
    - [GitHub Repository](https://github.com/praj2408/End-To-End-Resume-ATS-Tracking-LLM-Project-With-Google-Gemini-Pro)
    """)

    st.markdown("---")
    st.write("Smart ATS for Resume")

st.title("HR Workflow Automation Optimization")
st.text("Automate the Hiring Process")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Candidate Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader("Response from the model")
        st.write(response) 