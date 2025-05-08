import os
import pytesseract
from PIL import Image
import streamlit as st
import fitz  # PyMuPDF for PDF extraction
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Optional: If using Windows and Tesseract is not in PATH
# Uncomment the line below and set the correct path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit UI setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume (PDF or Screenshot), or paste resume text below to analyze the candidate.")

# Input options
option = st.radio("Choose Input Type:", ["Upload PDF", "Paste Text", "Upload Screenshot"])

resume_text = ""

# Upload PDF
if option == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])
    if uploaded_pdf:
        try:
            uploaded_pdf.seek(0)
            doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
            resume_text = "\n".join([page.get_text() for page in doc])
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# Paste Text
elif option == "Paste Text":
    resume_text = st.text_area("Paste your resume text below:", height=300)

# Upload Screenshot
elif option == "Upload Screenshot":
    uploaded_img = st.file_uploader("Upload Screenshot (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        try:
            image = Image.open(uploaded_img)
            resume_text = pytesseract.image_to_string(image)
        except Exception as e:
            st.error(f"OCR Error: {e}")

# Analyze Resume
if st.button("🧠 Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please provide or upload resume text first.")
    else:
        # Corrected triple-quoted string for prompt
        prompt_template = f"""
You are a senior HR manager reviewing the following resume. Provide a detailed review with the following sections:

### 🔍 Issues Found:
1. List weaknesses or misalignments with a typical job role.

### ✅ Suggestions for Improvement:
2. Suggest how the resume could be improved.

### 📘 Explanations:
3. Explain each weakness and suggestion in detail.

### 🧠 Candidate Suitability Score (out of 10):
4. Score the candidate and justify the score.

### Important:
- All sections are mandatory.
- Keep the order as defined.

Resume to analyze:
