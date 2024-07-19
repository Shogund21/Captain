import chromadb
from chromadb.config import Settings

def setup_chroma():
    chroma_client = chromadb.Client(Settings())
    resume_collection = chroma_client.create_collection("resumes")
    return resume_collection
