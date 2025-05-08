import os
import streamlit as st
import pytesseract
from PIL import Image
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import fitz  # PyMuPDF for PDF extraction

# 🧠 Set Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🔐 Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# 🚀 Streamlit setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume (PDF, image) or paste text to evaluate the candidate's suitability.")

# 🎯 Input options
option = st.radio("Choose resume input method:", ["Upload Resume PDF", "Paste Resume Text", "Upload Screenshot"])

resume_text = ""

# 📄 PDF Upload
if option == "Upload Resume PDF":
    uploaded_pdf = st.file_uploader("Upload a PDF resume", type=["pdf"])
    if uploaded_pdf:
        try:
            uploaded_pdf.seek(0)
            doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
            resume_text = "\n".join([page.get_text("text") for page in doc])
        except Exception as e:
            st.error(f"Failed to extract PDF text: {e}")

# ✏️ Text Paste
elif option == "Paste Resume Text":
    resume_text = st.text_area("Paste resume text here:", height=300)

# 🖼️ Image Upload
elif option == "Upload Screenshot":
    uploaded_img = st.file_uploader("Upload a resume screenshot (jpg/png)", type=["jpg", "jpeg", "png"])
    if uploaded_img:
        try:
            image = Image.open(uploaded_img).convert("RGB")
            resume_text = pytesseract.image_to_string(image)
        except Exception as e:
            st.error(f"Failed to extract image text: {e}")

# 🚀 Analyze Button
if st.button("🧠 Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please upload or paste resume content first.")
    else:
        # 🔧 Set up LangChain with OpenAI
        llm = OpenAI(temperature=0.7)

        prompt_template = """
You are a senior HR manager reviewing the following resume. Provide a detailed review with the following sections in exact order.

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
```text
{resume_text}

