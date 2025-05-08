import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load API key from .streamlit/secrets.toml
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Page settings
st.set_page_config(page_title="AI Resume Screener", page_icon="📄")
st.title("📄 AI Resume Screener")
st.markdown("Upload or paste a resume to get a detailed AI-powered screening and ranking.")

# Resume input
resume_text = st.text_area("📋 Paste Resume Text Here:", height=300, placeholder="Paste candidate's resume...")

# Button
if st.button("🚀 Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please paste a resume before clicking.")
    else:
        # LLM
        llm = OpenAI(temperature=0.6, max_tokens=1000, model_name="gpt-3.5-turbo-instruct")

        # Prompt Template
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
        prompt = PromptTemplate(
            input_variables=["resume_text"],
            template=template.strip()
        )

        chain = LLMChain(llm=llm, prompt=prompt)

        with st.spinner("Analyzing resume..."):
            result = chain.run(resume_text)

        st.success("✅ Resume analyzed successfully!")
        st.subheader("📑 Resume Analysis Report")
        st.markdown(result)
