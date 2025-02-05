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

# CS-AI-Agent/ <br>
│── backend/ <br>
│   ├── main.py                  # FastAPI entry point <br>
│   ├── config.py                # Environment variables <br>
│   ├── vector_store.py          # Pinecone setup and retrieval <br>
│   ├── search_fallback.py       # Google Search API integration <br>
│   ├── chat_agent.py            # Core AI chatbot logic <br>
│   ├── data_loader.py           # Document ingestion to Pinecone <br>
│   ├── requirements.txt        # Dependencies <br>
│   └── .env                    # API keys and secrets <br>
│
│── frontend/ <br>
│   ├── pages/ <br>
│   │   ├── index.tsx           # Chat UI <br>
│   │   ├── api/chat.ts         # API calls to backend <br>
│   └── components/ <br>
│       ├── ChatBox.tsx         # Chat component <br>
│       ├── Message.tsx         # Message UI <br>
│       ├── Input.tsx           # User input field <br>
│
│── docs/                       # Knowledge base & datasets <br>
│── scripts/                    # Utility scripts (e.g., testing, ingestion) <br>
│── README.md                   # Project documentation <br>
