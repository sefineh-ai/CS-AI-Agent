An advanced AI-driven customer support agent powered by FastAPI, OpenAI's GPT, Pinecone for vector search, AutoGen, and Google Search API.<br>
This agent first searches a vector database for relevant support documents and, if no relevant data is found, it automatically falls back to a real-time Google search.

# Features
✅ Hybrid Search (Vector + Web) – Retrieves answers from a knowledge base, or falls back to Google Search when needed.<br>
✅ Context-Aware Chatbot – Uses OpenAI's GPT for natural, context-aware responses.<br>
✅ FastAPI Backend – Lightweight & scalable API to handle chat queries efficiently.<br>
✅ Next.js Frontend – Interactive chat UI for real-time communication.<br>
✅ Pinecone Vector Database – Stores and retrieves relevant customer support documents.<br>
✅ AutoGen for Multi-Agent Collaboration (Planned Feature) – Multiple AI agents working together for better responses.<br>

# Tech Stack<br>
Backend: FastAPI, LangChain, OpenAI GPT, Pinecone, Google Search API (SerpAPI)<br>
Frontend: Next.js, TypeScript, React<br>
Database: Pinecone (Vector Database for efficient search)<br>
Environment & Deployment: Docker, Uvicorn, Vercel<br>
