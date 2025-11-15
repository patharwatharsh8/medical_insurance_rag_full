from pinecone import Pinecone
from embeddings import embed_text
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def search_pinecone(query: str, top_k=5):
    q_embed = embed_text(query)
    results = index.query(
        vector=q_embed,
        top_k=top_k,
        include_metadata=True
    )
    return results
