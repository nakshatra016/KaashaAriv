from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI(title="KaashaAriv API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "KaashaAriv Backend Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    prompt = f"""
You are a senior financial analyst.

Analyze the following annual report.

Return ONLY:

1. Executive Summary

2. Top 5 Business Insights

3. Risks

4. Opportunities

5. Overall Financial Health

Annual Report:

{text[:120000]}
"""

    response = model.generate_content(prompt)

    return {
        "summary": response.text
    }