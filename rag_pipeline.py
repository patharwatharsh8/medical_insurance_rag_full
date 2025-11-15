import os
from retriever import search_pinecone
from utils import configure_gemini

genai = configure_gemini()

def rag_answer(query: str):
    response_chunks = search_pinecone(query)

    context = ""
    citations = []

    for match in response_chunks.matches:
        ctx = match.metadata.get("text", "")
        pg = match.metadata.get("page", "N/A")

        context += f"\nPAGE {pg}: {ctx}\n"
        citations.append(f"Page {pg} | Score: {match.score}")

    prompt = f"""
You are an insurance expert. Answer the user's question ONLY using the provided context.
If the answer is NOT in the context, reply:
"The document does not mention this."

Context:
{context}

Question: {query}

Include citations as:
- Page Number
- Snippet

Answer format:
1. Final Answer
2. Citations
"""

    model = genai.GenerativeModel("gemini-pro")
    result = model.generate_content(prompt)

    return {
        "answer": result.text,
        "citations": citations
    }
