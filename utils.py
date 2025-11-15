import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def configure_gemini():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai
