import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Streamlit UI setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Paste your resume text below to receive an AI-powered review and improvement suggestions.")

# Input section
resume_text = st.text_area("📄 Paste Resume Text", height=300, placeholder="Paste your resume content here...")

# Analyze Resume Button
if st.button("🧠 Analyze Resume"):
    if not resume_text.strip():
        st.warning("⚠️ Please paste your resume text before analyzing.")
    else:
        # Prompt Template
        prompt_template = """
You are a senior HR manager tasked with reviewing resumes for a variety of roles. The goal is to evaluate the resume for overall quality, clarity, professionalism, and relevance to typical job expectations in the applicant's field.

Provide a detailed review of the following resume with the following sections:

### 🔍 Issues Found:
1. List weaknesses or inconsistencies found in the resume.

### ✅ Suggestions for Improvement:
2. Suggest how the resume could be improved to enhance clarity, relevance, and professionalism.

### 📘 Explanations:
3. Explain each weakness and suggestion in detail so the candidate understands how to improve.

### 🧠 Candidate Suitability Score (out of 10):
4. Score the candidate based on overall resume quality and clarity — do not assume they are applying for any specific job role unless it is explicitly mentioned.

### Important:
- All sections are mandatory.
- Evaluate the resume based on general professional standards, not a specific job title.

Resume:
{resume}
"""

        # LangChain setup
        prompt = PromptTemplate(
            input_variables=["resume"],
            template=prompt_template,
        )
        llm = OpenAI(temperature=0.7, max_tokens=1500)  # Increased token limit for longer output
        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing your resume..."):
            response = chain.run(resume=resume_text)

        # Display result
        st.markdown("### 📊 AI Resume Review")
        st.markdown(response)
