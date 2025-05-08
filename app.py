
requirements.txt for GitHub:

streamlit
openai
langchain
PyMuPDF
pytesseract
Pillow

.streamlit/secrets.toml (create this file):

OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

Optional for Windows: If pytesseract is not in PATH, uncomment this line and correct the path:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Let me know if you want this deployed to Streamlit Cloud or converted to GitHub folder with everything!
