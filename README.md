An advanced AI-driven customer support agent powered by FastAPI, OpenAI's GPT, Pinecone for vector search, AutoGen, and Google Search API.
This agent first searches a vector database for relevant support documents and, if no relevant data is found, it automatically falls back to a real-time Google search.

# Features
✅ Hybrid Search (Vector + Web) – Retrieves answers from a knowledge base, or falls back to Google Search when needed.
✅ Context-Aware Chatbot – Uses OpenAI's GPT for natural, context-aware responses.
✅ FastAPI Backend – Lightweight & scalable API to handle chat queries efficiently.
✅ Next.js Frontend – Interactive chat UI for real-time communication.
✅ Pinecone Vector Database – Stores and retrieves relevant customer support documents.
✅ AutoGen for Multi-Agent Collaboration (Planned Feature) – Multiple AI agents working together for better responses.

# Tech Stack
Backend: FastAPI, LangChain, OpenAI GPT, Pinecone, Google Search API (SerpAPI)
Frontend: Next.js, TypeScript, React
Database: Pinecone (Vector Database for efficient search)
Environment & Deployment: Docker, Uvicorn, Vercel
