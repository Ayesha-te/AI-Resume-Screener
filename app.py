import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import fitz  # PyMuPDF

# Load API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Page Config
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume in PDF format or paste the content below to get a detailed AI-powered screening.")

# Resume uploader
uploaded_file = st.file_uploader("📎 Upload PDF Resume", type=["pdf"])
resume_text_area = st.text_area("📝 Or Paste Resume Text:", height=200)

# Extract text from PDF
resume_text = ""
if uploaded_file is not None:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        resume_text = "\n".join(page.get_text() for page in doc)

# Use text area if no file is uploaded
elif resume_text_area:
    resume_text = resume_text_area

# Analyze button
if st.button("🚀 Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please provide a resume by uploading or pasting text.")
    else:
        llm = OpenAI(temperature=0.6, max_tokens=1000, model_name="gpt-3.5-turbo-instruct")

        template = """
You are an AI HR specialist. Analyze the resume below and provide the following:

1. 🔍 **Key Skills Extracted**
2. 💼 **Professional Experience Summary**
3. 🎓 **Education Overview**
4. 🌟 **Strengths & Unique Selling Points**
5. ⚠️ **Potential Concerns or Gaps**
6. 📊 **Overall Resume Score (out of 10)** with a short justification

Resume:
\"\"\"{resume_text}\"\"\"
"""
        prompt = PromptTemplate(input_variables=["resume_text"], template=template.strip())
        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing resume..."):
            result = chain.run(resume_text)

        st.success("✅ Resume analyzed successfully!")
        st.subheader("📑 Resume Analysis Report")
        st.markdown(result)

