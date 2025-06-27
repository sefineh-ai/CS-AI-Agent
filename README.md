# 🤖 CS-AI-Agent

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.0-000000?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT-412991?style=for-the-badge&logo=openai)](https://openai.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-5A4FCF?style=for-the-badge)](https://www.pinecone.io/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7.3-3178C6?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg?style=for-the-badge&logo=node.js)](https://nodejs.org/)

> **Advanced AI-driven customer support agent** that combines vector search with real-time web search to provide intelligent, context-aware responses. Built with FastAPI, Next.js, OpenAI GPT, and Pinecone vector database.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)

## 🎯 Overview

CS-AI-Agent is a sophisticated customer support solution that leverages cutting-edge AI technologies to provide intelligent, context-aware responses. The system combines the power of vector search for knowledge base queries with real-time web search capabilities, ensuring users receive accurate and up-to-date information.

### Key Benefits

- **🔍 Intelligent Search**: Hybrid approach combining knowledge base and web search
- **🧠 Context Awareness**: Maintains conversation context for personalized responses
- **⚡ Real-time Performance**: Fast response times with async processing
- **🔐 Enterprise Ready**: Secure, scalable, and production-ready architecture
- **📊 Analytics**: Comprehensive logging and performance monitoring
- **🔄 Extensible**: Modular design for easy customization and extension

## 🚀 Features

### Core Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| **🔍 Hybrid Search System** | Combines vector database search with real-time Google Search fallback | ✅ Implemented |
| **🧠 Intelligent Response Generation** | Uses OpenAI's GPT for natural, context-aware conversations | ✅ Implemented |
| **⚡ Real-time Communication** | Interactive chat interface with instant responses | ✅ Implemented |
| **📚 Knowledge Base Integration** | Stores and retrieves relevant support documents | ✅ Implemented |
| **🌐 Web Search Fallback** | Automatically searches the web when local knowledge is insufficient | ✅ Implemented |
| **🔄 Conversation Management** | Tracks chat history and maintains context across sessions | ✅ Implemented |

### Technical Features

| Feature | Description | Status |
|---------|-------------|--------|
| **🏗️ Scalable Architecture** | Microservices-based design with FastAPI backend | ✅ Implemented |
| **🎨 Modern UI/UX** | Responsive Next.js frontend with TypeScript | ✅ Implemented |
| **🔐 Secure API Integration** | Protected endpoints with proper authentication | ✅ Implemented |
| **📊 Vector Database** | Efficient similarity search with Pinecone | ✅ Implemented |
| **📝 Document Management** | Multi-format document ingestion and processing | ✅ Implemented |
| **🔍 Advanced Search** | Support for multiple search APIs with fallback | ✅ Implemented |

### Planned Features

- [ ] **🤖 Multi-Agent Collaboration** - AutoGen integration for complex workflows
- [ ] **📈 Advanced Analytics** - Conversation analytics and insights dashboard
- [ ] **🌍 Multi-language Support** - Support for multiple languages
- [ ] **🎤 Voice Integration** - Voice-to-text and text-to-speech capabilities
- [ ] **📱 Mobile App** - Native mobile application
- [ ] **🔒 Advanced Security** - Role-based access control and encryption
- [ ] **⚡ Performance Optimization** - Caching and optimization improvements

## 🏗️ Architecture

### System Overview

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

### Data Flow

1. **User Query Processing**
   ```
   User Input → Frontend → Backend API → Query Analysis
   ```

2. **Knowledge Base Search**
   ```
   Query → Vector Embedding → Pinecone Search → Relevant Documents
   ```

3. **Response Generation**
   ```
   If Knowledge Found:
     Documents + Query → OpenAI GPT → Contextual Response
   
   If Knowledge Not Found:
     Query → Google Search → Web Results → OpenAI GPT → Web-based Response
   ```

4. **Response Delivery**
   ```
   Generated Response → Backend → Frontend → User Interface
   ```

## 🛠️ Tech Stack

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.115.8 | High-performance web framework for building APIs |
| **OpenAI GPT** | Latest | Advanced language model for response generation |
| **Pinecone** | 5.4.2 | Vector database for similarity search |
| **LangChain** | 0.3.17 | Framework for building LLM applications |
| **SerpAPI** | 0.1.5 | Google Search API integration |
| **Uvicorn** | 0.34.0 | ASGI server for production deployment |
| **Pydantic** | 2.10.6 | Data validation and settings management |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.0.0 | React framework with server-side rendering |
| **TypeScript** | 5.7.3 | Type-safe JavaScript development |
| **React** | 19.0.0 | Modern UI library |
| **Axios** | 1.7.9 | HTTP client for API communication |

### Infrastructure & DevOps

| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization for consistent deployment |
| **Vercel** | Frontend hosting and deployment |
| **Environment Variables** | Secure configuration management |
| **Git** | Version control and collaboration |

## 📁 Project Structure

```
CS-AI-Agent/
├── 📁 backend/                     # FastAPI backend application
│   ├── 🐍 main.py                 # FastAPI entry point and routes
│   ├── ⚙️ config.py               # Environment configuration
│   ├── 🤖 chat_agent.py           # Core AI chatbot logic
│   ├── 🔍 vector_store.py         # Pinecone vector database operations
│   ├── 🌐 search_fallback.py      # Google Search API integration
│   ├── 📚 data_loader.py          # Document ingestion utilities
│   ├── 📋 requirements.txt        # Python dependencies
│   ├── 🔧 .env.example            # Environment variables template
│   └── 🧪 test_backend.py         # Backend test suite
│
├── 📁 frontend/                    # Next.js frontend application
│   ├── 📁 pages/                  # Next.js pages
│   │   ├── 🏠 index.tsx           # Main chat interface
│   │   └── 📁 api/                # API routes
│   │       └── 💬 chat.ts         # Frontend API handlers
│   ├── 📁 components/             # React components
│   │   ├── 💬 chat_box.tsx        # Main chat container
│   │   ├── 💭 message.tsx         # Individual message component
│   │   └── ⌨️ input.tsx           # User input component
│   ├── 📋 package.json            # Node.js dependencies
│   └── ⚙️ tsconfig.json           # TypeScript configuration
│
├── 📁 docs/                       # Documentation and knowledge base
├── 📁 scripts/                    # Utility scripts and automation
├── 📄 .gitignore                  # Git ignore rules
└── 📖 README.md                   # Project documentation
```

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

### Required API Keys

You'll need the following API keys:

- **OpenAI API Key** - [Get OpenAI API Key](https://platform.openai.com/api-keys)
- **Pinecone API Key** - [Get Pinecone API Key](https://www.pinecone.io/)
- **Google Search API Key** - [Get Google API Key](https://developers.google.com/custom-search)
- **SerpAPI Key** (Optional) - [Get SerpAPI Key](https://serpapi.com/)

## 📦 Installation

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

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
```

### 4. Environment Configuration

Edit the `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX_NAME=customer-support
PINECONE_DIMENSION=1536

# Google Search Configuration
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id

# SerpAPI Configuration (Alternative to Google Search)
SERPAPI_API_KEY=your_serpapi_key_here

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Search Configuration
MAX_SEARCH_RESULTS=5
MIN_CONFIDENCE_SCORE=0.7

# Conversation Configuration
MAX_CONVERSATION_HISTORY=50
SESSION_TIMEOUT=3600

# Logging Configuration
LOG_LEVEL=INFO

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

### 5. Start the Application

```bash
# Start backend (from backend directory)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend (from frontend directory, in new terminal)
cd frontend
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## ⚙️ Configuration

### Vector Database Setup

1. **Create Pinecone Account**
   - Sign up at [Pinecone](https://www.pinecone.io/)
   - Get your API key from the dashboard

2. **Create Index**
   - Use the default index name: `customer-support`
   - Set dimension to: `1536` (OpenAI embedding dimension)
   - Choose your preferred environment

3. **Configure Environment**
   - Set `PINECONE_API_KEY` in your `.env` file
   - Set `PINECONE_ENV` to your environment
   - Set `PINECONE_INDEX_NAME` to your index name

### OpenAI Configuration

1. **Get API Key**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Generate an API key in the dashboard

2. **Configure Settings**
   - Set `OPENAI_API_KEY` in your `.env` file
   - Adjust `OPENAI_MODEL` (default: gpt-4)
   - Configure `OPENAI_MAX_TOKENS` and `OPENAI_TEMPERATURE`

### Search API Setup

#### Option 1: Google Custom Search API

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing

2. **Enable Custom Search API**
   - Navigate to APIs & Services > Library
   - Search for "Custom Search API" and enable it

3. **Create API Key**
   - Go to APIs & Services > Credentials
   - Create API Key

4. **Create Custom Search Engine**
   - Go to [Custom Search Engine](https://cse.google.com/)
   - Create a new search engine
   - Get the Search Engine ID

5. **Configure Environment**
   - Set `GOOGLE_API_KEY` and `GOOGLE_CSE_ID` in your `.env` file

#### Option 2: SerpAPI (Alternative)

1. **Sign up for SerpAPI**
   - Go to [SerpAPI](https://serpapi.com/)
   - Create an account and get your API key

2. **Configure Environment**
   - Set `SERPAPI_API_KEY` in your `.env` file

## 📚 API Documentation

### Authentication

Currently, the API uses simple API key authentication. In production, implement proper JWT authentication.

### Endpoints

#### Chat Endpoint

**POST** `/chat/`

Send a chat message and receive an AI-generated response.

**Request Body:**
```json
{
  "query": "How do I reset my password?",
  "context": "optional_context",
  "user_id": "optional_user_id",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "To reset your password, please follow these steps...",
  "source": "knowledge_base",
  "confidence": 0.95,
  "metadata": {
    "session_id": "session_123",
    "user_id": "user_456",
    "knowledge_results_count": 2,
    "model_used": "gpt-4"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Health Check

**GET** `/health/`

Check the API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "api": "healthy",
    "openai": "healthy",
    "pinecone": "healthy",
    "search": "healthy"
  }
}
```

#### Knowledge Base Search

**GET** `/search/knowledge/`

Search the knowledge base for relevant documents.

**Parameters:**
- `query` (string, required): Search query
- `limit` (integer, optional): Maximum results (default: 5)

**Response:**
```json
{
  "query": "password reset",
  "results": [
    {
      "id": "doc_123",
      "content": "To reset your password...",
      "title": "Password Reset Guide",
      "category": "account",
      "tags": ["password", "reset"],
      "score": 0.95,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### Document Upload

**POST** `/documents/upload/`

Upload a document to the knowledge base.

**Request Body:**
```json
{
  "content": "Document content here...",
  "title": "Document Title",
  "category": "support",
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "success": true,
  "document_id": "doc_456",
  "message": "Document uploaded successfully"
}
```

## 💡 Usage Examples

### Basic Chat Interaction

```python
import requests

# Send a chat message
response = requests.post("http://localhost:8000/chat/", json={
    "query": "How do I reset my password?",
    "user_id": "user_123"
})

print(response.json()["response"])
```

### Knowledge Base Search

```python
import requests

# Search knowledge base
response = requests.get("http://localhost:8000/search/knowledge/", params={
    "query": "password reset",
    "limit": 5
})

results = response.json()["results"]
for result in results:
    print(f"Title: {result['title']}")
    print(f"Content: {result['content'][:100]}...")
```

### Document Upload

```python
import requests

# Upload a document
response = requests.post("http://localhost:8000/documents/upload/", json={
    "content": "This is a support document about password reset procedures...",
    "title": "Password Reset Guide",
    "category": "account",
    "tags": ["password", "reset", "security"]
})

if response.json()["success"]:
    print("Document uploaded successfully!")
```

### Frontend Integration

```typescript
// Send chat message
const sendMessage = async (message: string) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: message,
      user_id: 'user_123'
    })
  });
  
  const data = await response.json();
  return data.response;
};
```

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
python test_backend.py
```

### Test API Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/health/

# Test chat endpoint
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, how can you help me?"}'

# Test knowledge search
curl "http://localhost:8000/search/knowledge/?query=password&limit=3"
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🚀 Deployment

### Docker Deployment

1. **Build Docker Image**

```bash
# Build the image
docker build -t cs-ai-agent .

# Run the container
docker run -p 8000:8000 cs-ai-agent
```

2. **Docker Compose**

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### Vercel Deployment (Frontend)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod
```

### Production Considerations

- **Environment Variables**: Use secure environment variable management
- **Authentication**: Implement proper JWT authentication
- **Rate Limiting**: Add rate limiting to prevent abuse
- **Monitoring**: Set up logging and monitoring (e.g., Sentry, DataDog)
- **HTTPS**: Use HTTPS in production
- **CORS**: Configure CORS properly for your domain
- **Database**: Use production-grade database for conversation storage
- **Caching**: Implement Redis caching for better performance

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/CS-AI-Agent.git
   cd CS-AI-Agent
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow PEP 8 for Python code
   - Use TypeScript for frontend development
   - Write tests for new features
   - Update documentation

4. **Test Your Changes**
   ```bash
   # Backend tests
   cd backend && python test_backend.py
   
   # Frontend tests
   cd frontend && npm test
   ```

5. **Commit and Push**
   ```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

6. **Create Pull Request**
   - Open a pull request on GitHub
   - Provide clear description of changes
   - Include tests and documentation updates

### Development Guidelines

- **Code Style**: Follow PEP 8 (Python) and ESLint (TypeScript)
- **Testing**: Write unit tests for new features
- **Documentation**: Update README and API docs
- **Commits**: Use conventional commit messages
- **Reviews**: All PRs require code review

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'openai'`
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Issue**: `Pinecone API key not found`
```bash
# Solution: Check environment variables
echo $PINECONE_API_KEY
# Add to .env file if missing
```

**Issue**: `OpenAI API rate limit exceeded`
```bash
# Solution: Check API usage and limits
# Consider implementing retry logic
```

#### Frontend Issues

**Issue**: `npm install fails`
```bash
# Solution: Clear npm cache
npm cache clean --force
npm install
```

**Issue**: `Cannot connect to backend`
```bash
# Solution: Check backend is running
curl http://localhost:8000/health/
```

#### API Issues

**Issue**: `CORS errors`
```bash
# Solution: Update ALLOWED_ORIGINS in .env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Issue**: `Authentication errors`
```bash
# Solution: Check API keys are valid
# Test with curl or Postman
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Backend
DEBUG=True uvicorn main:app --reload

# Frontend
NODE_ENV=development npm run dev
```

### Logs

Check logs for detailed error information:

```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend logs
# Check browser console and terminal output
```

## ❓ FAQ

### General Questions

**Q: What makes this different from other chatbots?**
A: CS-AI-Agent combines knowledge base search with real-time web search, providing more accurate and up-to-date responses than traditional chatbots.

**Q: Can I use my own knowledge base?**
A: Yes! You can upload your own documents using the document upload API or load files from directories.

**Q: Is this production-ready?**
A: The core functionality is production-ready, but you should add authentication, rate limiting, and monitoring for enterprise use.

### Technical Questions

**Q: What's the difference between knowledge base and web search?**
A: Knowledge base search uses your uploaded documents for responses, while web search fetches real-time information from the internet.

**Q: How do I add new documents to the knowledge base?**
A: Use the `/documents/upload/` API endpoint or the DataLoader class to upload files.

**Q: Can I customize the AI responses?**
A: Yes, you can modify the system prompt in `chat_agent.py` to customize response style and behavior.

### Performance Questions

**Q: How fast are the responses?**
A: Typical response times are 1-3 seconds, depending on query complexity and search results.

**Q: How many concurrent users can it handle?**
A: Performance depends on your infrastructure. The async design supports high concurrency.

**Q: How much does it cost to run?**
A: Costs depend on API usage (OpenAI, Pinecone, Google Search). Estimate $50-200/month for moderate usage.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Pinecone](https://www.pinecone.io/) for vector database services
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Next.js](https://nextjs.org/) for the React framework
- [SerpAPI](https://serpapi.com/) for Google Search integration
- [Vercel](https://vercel.com/) for hosting and deployment

## 📞 Support

### Getting Help

- **Documentation**: Check this README and API docs
- **Issues**: [GitHub Issues](https://github.com/sefineh-ai/CS-AI-Agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sefineh-ai/CS-AI-Agent/discussions)
- **Wiki**: [Project Wiki](https://github.com/sefineh-ai/CS-AI-Agent/wiki)

### Community

- **Discord**: Join our [Discord server](https://discord.gg/cs-ai-agent)
- **Twitter**: Follow [@CS_AI_Agent](https://twitter.com/CS_AI_Agent)
- **Blog**: Read our [blog posts](https://blog.cs-ai-agent.com)

### Enterprise Support

For enterprise customers, we offer:
- **Priority Support**: 24/7 technical support
- **Custom Development**: Tailored features and integrations
- **Training**: Team training and workshops
- **Consulting**: Architecture and deployment guidance

Contact us at: enterprise@cs-ai-agent.com

---

**Made with ❤️ by the CS-AI-Agent Team**

*Empowering customer support with intelligent AI solutions*
