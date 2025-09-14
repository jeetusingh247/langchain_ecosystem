
from app.config import config
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=config.GEMINI_API_KEY)

def generate_sql(prompt: str) -> str:
    # This is a placeholder for LLM prompt engineering
    # You should add schema context and user question to the prompt
    response = llm(prompt)
    return response
