import streamlit as st
import os
import fitz  # PyMuPDF for PDF reading
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit UI Setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume PDF and get insights powered by AI.")

# Upload PDF
uploaded_file = st.file_uploader("📎 Upload Resume (PDF format only)", type=["pdf"])

# Helper to extract text
def extract_text_from_pdf(uploaded_pdf):
    try:
        doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Analyze Resume
if uploaded_file and st.button("🤖 Analyze Resume"):
    resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract any text from the PDF. Please try another file.")
    else:
        # Shorten the resume if it's too long
        if len(resume_text) > 3000:
            resume_text = resume_text[:3000] + "\n\n[Truncated for token limits]"

        # Setup LLM
        llm = OpenAI(temperature=0.5, max_tokens=1000)

        # Prompt template
        prompt_template = PromptTemplate(
            input_variables=["resume_text"],
            template="""
You are an HR specialist. Analyze the following resume and provide:

1. 🏆 Candidate Strengths
2. ❌ Weaknesses or Concerns
3. 💡 Suggestions for Improvement
4. ⭐ Overall Fit Score (0 to 10) with explanation

Resume:
\"\"\"{resume_text}\"\"\"
"""
        )

        chain = LLMChain(llm=llm, prompt=prompt_template)

        with st.spinner("Analyzing the resume..."):
            output = chain.run(resume_text)

        # Display results
        st.subheader("📋 AI-Powered Resume Analysis")
        st.markdown(output)
