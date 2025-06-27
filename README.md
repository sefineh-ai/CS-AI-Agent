# 🤖 CS-AI-Agent

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.0-000000?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-412991?style=for-the-badge&logo=openai)](https://openai.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-5A4FCF?style=for-the-badge)](https://www.pinecone.io/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7.3-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

An advanced AI-driven customer support agent that combines vector search with real-time web search to provide intelligent, context-aware responses. Built with FastAPI, Next.js, OpenAI GPT, and Pinecone vector database.

## 🚀 Features

### Core Capabilities
- **🔍 Hybrid Search System** - Combines vector database search with real-time Google Search fallback
- **🧠 Intelligent Response Generation** - Uses OpenAI's GPT for natural, context-aware conversations
- **⚡ Real-time Communication** - Interactive chat interface with instant responses
- **📚 Knowledge Base Integration** - Stores and retrieves relevant support documents
- **🌐 Web Search Fallback** - Automatically searches the web when local knowledge is insufficient

### Technical Features
- **🏗️ Scalable Architecture** - Microservices-based design with FastAPI backend
- **🎨 Modern UI/UX** - Responsive Next.js frontend with TypeScript
- **🔐 Secure API Integration** - Protected endpoints with proper authentication
- **📊 Vector Database** - Efficient similarity search with Pinecone
- **🤖 Multi-Agent Support** - AutoGen integration for collaborative AI workflows (planned)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat UI       │    │   Vector Store  │    │   OpenAI GPT    │
│   Components    │    │   (Pinecone)    │    │   Google Search │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework for building APIs
- **OpenAI GPT** - Advanced language model for response generation
- **Pinecone** - Vector database for similarity search
- **LangChain** - Framework for building LLM applications
- **SerpAPI** - Google Search API integration
- **Uvicorn** - ASGI server for production deployment

### Frontend
- **Next.js 14** - React framework with server-side rendering
- **TypeScript** - Type-safe JavaScript development
- **React 19** - Modern UI library
- **Axios** - HTTP client for API communication

### Infrastructure
- **Docker** - Containerization for consistent deployment
- **Vercel** - Frontend hosting and deployment
- **Environment Variables** - Secure configuration management

## 📁 Project Structure

```
CS-AI-Agent/
├── backend/                     # FastAPI backend application
│   ├── main.py                 # FastAPI entry point and routes
│   ├── config.py               # Environment configuration
│   ├── chat_agent.py           # Core AI chatbot logic
│   ├── vector_store.py         # Pinecone vector database operations
│   ├── search_fallback.py      # Google Search API integration
│   ├── data_loader.py          # Document ingestion utilities
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (not tracked)
│
├── frontend/                    # Next.js frontend application
│   ├── pages/                  # Next.js pages
│   │   ├── index.tsx           # Main chat interface
│   │   └── api/                # API routes
│   │       └── chat.ts         # Frontend API handlers
│   ├── components/             # React components
│   │   ├── chat_box.tsx        # Main chat container
│   │   ├── message.tsx         # Individual message component
│   │   └── input.tsx           # User input component
│   ├── package.json            # Node.js dependencies
│   └── tsconfig.json           # TypeScript configuration
│
├── docs/                       # Documentation and knowledge base
├── scripts/                    # Utility scripts and automation
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key
- Pinecone API key
- Google Search API key (SerpAPI)

### 1. Clone the Repository

```bash
git clone https://github.com/sefineh-ai/CS-AI-Agent.git
cd CS-AI-Agent
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local with your backend URL
```

### 4. Environment Configuration

Create `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_index_name

# Google Search API (SerpAPI)
SERPAPI_API_KEY=your_serpapi_key_here

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### 5. Start the Application

```bash
# Start backend (from backend directory)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (from frontend directory, in new terminal)
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔄 Workflow

### 1. User Query Processing
```
User Input → Frontend → Backend API → Query Analysis
```

### 2. Knowledge Base Search
```
Query → Vector Embedding → Pinecone Search → Relevant Documents
```

### 3. Response Generation
```
If Knowledge Found:
  Documents + Query → OpenAI GPT → Contextual Response

If Knowledge Not Found:
  Query → Google Search → Web Results → OpenAI GPT → Web-based Response
```

### 4. Response Delivery
```
Generated Response → Backend → Frontend → User Interface
```

## 📚 API Documentation

### Chat Endpoint

**POST** `/chat/`

Send a chat message and receive an AI-generated response.

**Request:**
```json
{
  "query": "How do I reset my password?",
  "context": "optional_context"
}
```

**Response:**
```json
{
  "response": "To reset your password, please follow these steps...",
  "source": "knowledge_base",
  "confidence": 0.95
}
```

### Health Check

**GET** `/health/`

Check the API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🔧 Configuration

### Vector Database Setup

1. Create a Pinecone account and get your API key
2. Create an index with appropriate dimensions
3. Configure the index name in your environment variables

### OpenAI Configuration

1. Get your OpenAI API key from the OpenAI platform
2. Ensure you have sufficient credits for API calls
3. Configure the model and parameters in `chat_agent.py`

### Search API Setup

1. Sign up for SerpAPI to get Google Search access
2. Configure your API key in the environment variables
3. Test the search functionality

## 🚀 Deployment

### Docker Deployment

```bash
# Build the Docker image
docker build -t cs-ai-agent .

# Run the container
docker run -p 8000:8000 cs-ai-agent
```

### Vercel Deployment (Frontend)

```bash
# Deploy to Vercel
vercel --prod
```

### Production Considerations

- Use environment variables for all sensitive data
- Implement proper authentication and rate limiting
- Set up monitoring and logging
- Configure CORS properly for production
- Use HTTPS in production

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Pinecone](https://www.pinecone.io/) for vector database services
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Next.js](https://nextjs.org/) for the React framework
- [SerpAPI](https://serpapi.com/) for Google Search integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sefineh-ai/CS-AI-Agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sefineh-ai/CS-AI-Agent/discussions)
- **Documentation**: [Project Wiki](https://github.com/sefineh-ai/CS-AI-Agent/wiki)

## 🔮 Roadmap

- [ ] **Multi-Agent Collaboration** - Implement AutoGen for complex workflows
- [ ] **Advanced Analytics** - Add conversation analytics and insights
- [ ] **Multi-language Support** - Support for multiple languages
- [ ] **Voice Integration** - Add voice-to-text and text-to-speech
- [ ] **Mobile App** - Native mobile application
- [ ] **Advanced Security** - Implement role-based access control
- [ ] **Performance Optimization** - Caching and optimization improvements

---

**Made with ❤️ by the CS-AI-Agent Team**
