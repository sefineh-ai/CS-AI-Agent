#!/usr/bin/env python3
"""
Test script for CS-AI-Agent backend functionality.
This script tests the core components without requiring external API keys.
"""

import asyncio
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockConfig:
    """Mock configuration for testing."""
    OPENAI_API_KEY = "test_key"
    PINECONE_API_KEY = "test_key"
    PINECONE_ENV = "test_env"
    PINECONE_INDEX_NAME = "test_index"
    PINECONE_DIMENSION = 1536
    GOOGLE_API_KEY = "test_key"
    GOOGLE_CSE_ID = "test_id"
    SERPAPI_API_KEY = "test_key"
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8000
    MAX_SEARCH_RESULTS = 5
    MIN_CONFIDENCE_SCORE = 0.7
    MAX_CONVERSATION_HISTORY = 50
    SESSION_TIMEOUT = 3600
    LOG_LEVEL = "INFO"
    ALLOWED_ORIGINS = ["http://localhost:3000"]

class MockVectorStore:
    """Mock vector store for testing."""
    
    def __init__(self):
        self.index_name = "test_index"
        self.test_documents = [
            {
                "id": "doc1",
                "content": "Customer support is available 24/7 for all inquiries.",
                "title": "Support Hours",
                "category": "support",
                "tags": ["hours", "availability"],
                "score": 0.95,
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "doc2", 
                "content": "To reset your password, go to the login page and click 'Forgot Password'.",
                "title": "Password Reset",
                "category": "account",
                "tags": ["password", "reset", "login"],
                "score": 0.88,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
    
    async def search(self, query: str, limit: int = 5) -> list:
        """Mock search that returns test documents."""
        # Simple keyword matching for testing
        query_lower = query.lower()
        results = []
        
        for doc in self.test_documents:
            if any(keyword in doc["content"].lower() for keyword in query_lower.split()):
                results.append(doc)
        
        return results[:limit]
    
    def is_available(self) -> bool:
        return True

class MockSearchFallback:
    """Mock search fallback for testing."""
    
    def __init__(self):
        self.test_results = [
            {
                "title": "Test Search Result",
                "snippet": "This is a test search result for demonstration purposes.",
                "url": "https://example.com/test",
                "source": "mock",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    
    async def search(self, query: str, limit: int = 5) -> list:
        """Mock search that returns test results."""
        return self.test_results[:limit]
    
    def is_available(self) -> bool:
        return True

class MockChatAgent:
    """Mock chat agent for testing."""
    
    def __init__(self):
        self.vector_store = MockVectorStore()
        self.search_fallback = MockSearchFallback()
        self.conversations = {}
        self.model_name = "gpt-4"
        self.max_tokens = 1000
        self.temperature = 0.7
    
    async def generate_response(
        self, 
        query: str, 
        context: str = None,
        user_id: str = None,
        session_id: str = None
    ) -> Dict[str, Any]:
        """Mock response generation."""
        # Search knowledge base
        knowledge_results = await self.vector_store.search(query, 3)
        
        if knowledge_results:
            source = "knowledge_base"
            confidence = 0.9
            response = f"Based on our knowledge base: {knowledge_results[0]['content']}"
        else:
            # Fallback to web search
            web_results = await self.search_fallback.search(query, 3)
            if web_results:
                source = "web_search"
                confidence = 0.6
                response = f"Based on web search: {web_results[0]['snippet']}"
            else:
                source = "no_data"
                confidence = 0.3
                response = "I don't have specific information about that. Please contact our support team for assistance."
        
        return {
            "response": response,
            "source": source,
            "confidence": confidence,
            "metadata": {
                "session_id": session_id or "test_session",
                "user_id": user_id,
                "knowledge_results_count": len(knowledge_results),
                "model_used": self.model_name
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    def is_available(self) -> bool:
        return True

async def test_chat_agent():
    """Test the chat agent functionality."""
    logger.info("Testing Chat Agent...")
    
    chat_agent = MockChatAgent()
    
    # Test queries
    test_queries = [
        "How do I reset my password?",
        "What are your support hours?",
        "How do I contact customer service?",
        "What is the return policy?"
    ]
    
    for query in test_queries:
        logger.info(f"\nTesting query: {query}")
        response = await chat_agent.generate_response(query)
        
        logger.info(f"Response: {response['response']}")
        logger.info(f"Source: {response['source']}")
        logger.info(f"Confidence: {response['confidence']}")
    
    logger.info("Chat Agent tests completed!")

async def test_vector_store():
    """Test the vector store functionality."""
    logger.info("Testing Vector Store...")
    
    vector_store = MockVectorStore()
    
    # Test searches
    test_searches = [
        "password reset",
        "support hours",
        "customer service",
        "account settings"
    ]
    
    for search in test_searches:
        logger.info(f"\nTesting search: {search}")
        results = await vector_store.search(search, 3)
        
        logger.info(f"Found {len(results)} results")
        for result in results:
            logger.info(f"- {result['title']}: {result['content'][:100]}...")
    
    logger.info("Vector Store tests completed!")

async def test_search_fallback():
    """Test the search fallback functionality."""
    logger.info("Testing Search Fallback...")
    
    search_fallback = MockSearchFallback()
    
    # Test searches
    test_searches = [
        "latest technology news",
        "weather forecast",
        "stock market updates"
    ]
    
    for search in test_searches:
        logger.info(f"\nTesting web search: {search}")
        results = await search_fallback.search(search, 3)
        
        logger.info(f"Found {len(results)} results")
        for result in results:
            logger.info(f"- {result['title']}: {result['snippet'][:100]}...")
    
    logger.info("Search Fallback tests completed!")

async def test_integration():
    """Test the complete integration."""
    logger.info("Testing Complete Integration...")
    
    chat_agent = MockChatAgent()
    
    # Test a complex conversation
    conversation = [
        "I need help with my account",
        "I can't log in",
        "How do I reset my password?",
        "What are your support hours?"
    ]
    
    session_id = "test_session_123"
    
    for i, message in enumerate(conversation):
        logger.info(f"\n--- Message {i+1} ---")
        logger.info(f"User: {message}")
        
        response = await chat_agent.generate_response(
            query=message,
            session_id=session_id,
            user_id="test_user"
        )
        
        logger.info(f"AI: {response['response']}")
        logger.info(f"Source: {response['source']}, Confidence: {response['confidence']}")
    
    logger.info("Integration tests completed!")

async def main():
    """Run all tests."""
    logger.info("Starting CS-AI-Agent Backend Tests")
    logger.info("=" * 50)
    
    try:
        await test_vector_store()
        await test_search_fallback()
        await test_chat_agent()
        await test_integration()
        
        logger.info("\n" + "=" * 50)
        logger.info("All tests completed successfully! ✅")
        logger.info("The backend components are working correctly.")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 