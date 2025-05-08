import pytesseract
from PIL import Image
import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import fitz  # PyMuPDF for PDF extraction

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume (PDF format), paste the resume text below, or upload a screenshot to evaluate the candidate's suitability.")

# Option for uploading resume, pasting text, or uploading screenshot
resume_option = st.radio("Select Resume Input Option", ("Upload Resume PDF", "Paste Resume Text", "Upload Screenshot"))

# Resume text input if user chooses paste
resume_text = ""
if resume_option == "Paste Resume Text":
    resume_text = st.text_area("Paste Resume Text Here", height=300)

# Resume PDF input if user chooses upload
uploaded_pdf = None
if resume_option == "Upload Resume PDF":
    uploaded_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])

# Screenshot input if user chooses upload screenshot
uploaded_screenshot = None
if resume_option == "Upload Screenshot":
    uploaded_screenshot = st.file_uploader("Upload Screenshot", type=["png", "jpg", "jpeg"])

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_pdf):
    try:
        uploaded_pdf.seek(0)  # Ensure we read from the start of the file
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Function to extract text from screenshot using OCR
def extract_text_from_screenshot(uploaded_screenshot):
    try:
        image = Image.open(uploaded_screenshot)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"Error reading screenshot: {e}")
        return ""

# When the user uploads a PDF, extract text from it
if uploaded_pdf:
    resume_text = extract_text_from_pdf(uploaded_pdf)
    if not resume_text:
        st.error("Could not extract text from the PDF. Please try another file or use the text input option.")

# When the user uploads a screenshot, extract text from it
if uploaded_screenshot:
    resume_text = extract_text_from_screenshot(uploaded_screenshot)
    if not resume_text:
        st.error("Could not extract text from the screenshot. Please try another image.")

# Resume analysis button
if st.button("🧠 Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please provide a resume text either by uploading a PDF, pasting the text, or uploading a screenshot.")
    else:
        # LangChain LLM setup
        llm = OpenAI(temperature=0.7)

        # Prompt template for resume analysis
        prompt_text = (
            "You are a senior HR manager reviewing the following resume. "
            "Please provide a detailed review with the following sections in **exact order**, "
            "including explanations, suggestions, and a quality score. Do not skip any sections.\n\n"
            
            "### 🔍 Issues Found:\n"
            "1. Identify all weaknesses or areas where the candidate's qualifications may not align with the role.\n\n"
            
            "### ✅ Suggestions for Improvement:\n"
            "2. Provide suggestions for how the candidate could improve their resume.\n\n"
            
            "### 📘 Explanations:\n"
            "3. Provide detailed explanations for each weakness and suggestion, and how the candidate could improve.\n\n"
            
            "### 🧠 Candidate Suitability Score (out of 10):\n"
            "4. Based on the resume, provide a suitability score for the role and explain why the score is justified.\n\n"
            
            "### Important Instructions:\n"
            "- Do **not** skip any of these sections. All sections are mandatory.\n"
            "- Follow the **exact** order of sections as specified.\n\n"
            
            "Resume to analyze:\n"
            "```text\n{resume_text}\n```"
        )

        # Create prompt template with resume text input
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template=prompt_text
        )

        # Create the LLM chain
        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing the resume..."):
            # Run the chain to generate the response
            result = chain.run(resume_text)

        # Display the formatted review
        st.markdown("---")
        st.subheader("📋 Resume Review Summary")
        st.markdown(result)


