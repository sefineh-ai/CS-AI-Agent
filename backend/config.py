import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
