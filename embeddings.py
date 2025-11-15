from utils import configure_gemini

genai = configure_gemini()

def embed_text(text: str):
    data = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return data["embedding"]
