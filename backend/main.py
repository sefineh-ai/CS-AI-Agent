from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import uvicorn

from chat_agent import ChatAgent
from vector_store import VectorStore
from search_fallback import SearchFallback
from data_loader import DataLoader
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CS-AI-Agent API",
    description="Advanced AI-driven customer support agent with hybrid search capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chat_agent = ChatAgent()
vector_store = VectorStore()
search_fallback = SearchFallback()
data_loader = DataLoader()

# Pydantic models
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="User's question or request")
    context: Optional[str] = Field(None, max_length=2000, description="Additional context for the query")
    user_id: Optional[str] = Field(None, description="Unique identifier for the user")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation tracking")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI-generated response")
    source: str = Field(..., description="Source of the response (knowledge_base, web_search, or hybrid)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the response")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    services: Dict[str, str] = Field(..., description="Status of individual services")

class DocumentUploadRequest(BaseModel):
    content: str = Field(..., description="Document content to be added to knowledge base")
    title: Optional[str] = Field(None, description="Document title")
    category: Optional[str] = Field(None, description="Document category")
    tags: Optional[List[str]] = Field(None, description="Document tags")

class DocumentUploadResponse(BaseModel):
    success: bool = Field(..., description="Upload success status")
    document_id: str = Field(..., description="Unique identifier for the uploaded document")
    message: str = Field(..., description="Upload result message")

# Health check endpoint
@app.get("/health/", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check the health status of the API and its dependencies."""
    try:
        services = {
            "api": "healthy",
            "openai": "healthy" if chat_agent.is_available() else "unhealthy",
            "pinecone": "healthy" if vector_store.is_available() else "unhealthy",
            "search": "healthy" if search_fallback.is_available() else "unhealthy"
        }
        
        overall_status = "healthy" if all(status == "healthy" for status in services.values()) else "degraded"
        
        return HealthResponse(
            status=overall_status,
            services=services
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Chat endpoint
@app.post("/chat/", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """Process a chat message and return an AI-generated response."""
    try:
        logger.info(f"Processing chat request: {request.query[:100]}...")
        
        # Generate response using the chat agent
        response_data = await chat_agent.generate_response(
            query=request.query,
            context=request.context,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        logger.info(f"Chat response generated successfully for query: {request.query[:50]}...")
        
        return ChatResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process chat request: {str(e)}")

# Knowledge base search endpoint
@app.get("/search/knowledge/", tags=["Search"])
async def search_knowledge_base(query: str, limit: int = 5):
    """Search the knowledge base for relevant documents."""
    try:
        results = await vector_store.search(query, limit=limit)
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search knowledge base: {str(e)}")

# Web search endpoint
@app.get("/search/web/", tags=["Search"])
async def search_web(query: str, limit: int = 5):
    """Perform a web search using Google Search API."""
    try:
        results = await search_fallback.search(query, limit=limit)
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"Error performing web search: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to perform web search: {str(e)}")

# Document upload endpoint
@app.post("/documents/upload/", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_document(request: DocumentUploadRequest):
    """Upload a document to the knowledge base."""
    try:
        result = await data_loader.add_document(
            content=request.content,
            title=request.title,
            category=request.category,
            tags=request.tags
        )
        
        return DocumentUploadResponse(
            success=True,
            document_id=result["document_id"],
            message="Document uploaded successfully"
        )
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

# Get conversation history endpoint
@app.get("/conversations/{session_id}/", tags=["Conversations"])
async def get_conversation_history(session_id: str, limit: int = 50):
    """Retrieve conversation history for a specific session."""
    try:
        history = await chat_agent.get_conversation_history(session_id, limit=limit)
        return {
            "session_id": session_id,
            "messages": history,
            "total": len(history)
        }
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve conversation history: {str(e)}")

# Configuration endpoint
@app.get("/config/", tags=["Configuration"])
async def get_configuration():
    """Get current configuration (without sensitive data)."""
    return {
        "openai_model": chat_agent.model_name,
        "pinecone_index": vector_store.index_name,
        "max_tokens": chat_agent.max_tokens,
        "temperature": chat_agent.temperature
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "CS-AI-Agent API",
        "version": "1.0.0",
        "description": "Advanced AI-driven customer support agent",
        "docs": "/docs",
        "health": "/health/"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info"
    )
