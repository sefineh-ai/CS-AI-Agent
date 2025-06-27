from openai import OpenAI
from typing import Dict, List, Optional, Any
import logging
import asyncio
import json
from datetime import datetime, timedelta
import uuid

from config import Config
from vector_store import VectorStore
from search_fallback import SearchFallback

logger = logging.getLogger(__name__)

class ChatAgent:
    def __init__(self):
        """Initialize the ChatAgent with OpenAI client and services."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model_name = Config.OPENAI_MODEL
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.temperature = Config.OPENAI_TEMPERATURE
        
        # Initialize services
        self.vector_store = VectorStore()
        self.search_fallback = SearchFallback()
        
        # In-memory conversation storage (in production, use a proper database)
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        
        # System prompt for the AI
        self.system_prompt = """You are an advanced customer support AI agent with the following capabilities:

1. **Knowledge Base Search**: You can search through a comprehensive knowledge base for relevant information.
2. **Web Search Fallback**: When knowledge base information is insufficient, you can search the web for current information.
3. **Context Awareness**: You maintain conversation context and provide personalized responses.
4. **Professional Communication**: You communicate in a professional, helpful, and empathetic manner.

**Guidelines:**
- Always be helpful and professional
- If you're unsure about something, say so rather than guessing
- Provide accurate, up-to-date information
- When referencing sources, mention them appropriately
- Keep responses concise but comprehensive
- Ask clarifying questions when needed

**Response Format:**
- Provide clear, actionable answers
- Include relevant context when appropriate
- Cite sources when using external information
- Maintain conversation flow naturally"""

    async def generate_response(
        self, 
        query: str, 
        context: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a response to a user query using hybrid search approach.
        
        Args:
            query: User's question or request
            context: Additional context for the query
            user_id: Unique identifier for the user
            session_id: Session identifier for conversation tracking
            
        Returns:
            Dictionary containing response data
        """
        try:
            # Generate session_id if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Step 1: Search knowledge base
            knowledge_results = await self.vector_store.search(query, limit=3)
            
            # Step 2: Determine response source and generate context
            if knowledge_results:
                # Use knowledge base results
                context_text = self._format_knowledge_context(knowledge_results)
                source = "knowledge_base"
                confidence = self._calculate_confidence(knowledge_results, query)
            else:
                # Fallback to web search
                web_results = await self.search_fallback.search(query, limit=3)
                if web_results:
                    context_text = self._format_web_context(web_results)
                    source = "web_search"
                    confidence = 0.6  # Lower confidence for web results
                else:
                    # No results found
                    context_text = "No relevant information found in knowledge base or web search."
                    source = "no_data"
                    confidence = 0.3
            
            # Step 3: Generate AI response
            response = await self._generate_ai_response(query, context_text, session_id)
            
            # Step 4: Store conversation
            await self._store_conversation(session_id, user_id, query, response, source, confidence)
            
            return {
                "response": response,
                "source": source,
                "confidence": confidence,
                "metadata": {
                    "session_id": session_id,
                    "user_id": user_id,
                    "knowledge_results_count": len(knowledge_results) if knowledge_results else 0,
                    "model_used": self.model_name,
                    "tokens_used": None  # Could be extracted from OpenAI response
                },
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I apologize, but I encountered an error while processing your request. Please try again later.",
                "source": "error",
                "confidence": 0.0,
                "metadata": {"error": str(e)},
                "timestamp": datetime.utcnow()
            }

    async def _generate_ai_response(self, query: str, context: str, session_id: str) -> str:
        """Generate AI response using OpenAI API."""
        try:
            # Get conversation history
            history = self.conversations.get(session_id, [])
            
            # Build messages array
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history (last 10 messages to avoid token limits)
            for msg in history[-10:]:
                messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
            
            # Add current query with context
            current_message = f"Context: {context}\n\nUser Query: {query}"
            messages.append({"role": "user", "content": current_message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise

    def _format_knowledge_context(self, results: List[Dict[str, Any]]) -> str:
        """Format knowledge base results into context string."""
        context_parts = ["Knowledge Base Information:"]
        for i, result in enumerate(results, 1):
            content = result.get("content", "")
            score = result.get("score", 0)
            context_parts.append(f"{i}. {content} (Relevance: {score:.2f})")
        
        return "\n".join(context_parts)

    def _format_web_context(self, results: List[Dict[str, Any]]) -> str:
        """Format web search results into context string."""
        context_parts = ["Web Search Results:"]
        for i, result in enumerate(results, 1):
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            url = result.get("url", "")
            context_parts.append(f"{i}. {title}\n   {snippet}\n   Source: {url}")
        
        return "\n".join(context_parts)

    def _calculate_confidence(self, results: List[Dict[str, Any]], query: str) -> float:
        """Calculate confidence score based on search results."""
        if not results:
            return 0.0
        
        # Calculate average relevance score
        scores = [result.get("score", 0) for result in results]
        avg_score = sum(scores) / len(scores)
        
        # Boost confidence if we have multiple relevant results
        if len(results) >= 2:
            avg_score *= 1.1
        
        return min(avg_score, 1.0)

    async def _store_conversation(
        self, 
        session_id: str, 
        user_id: Optional[str], 
        query: str, 
        response: str, 
        source: str, 
        confidence: float
    ):
        """Store conversation in memory."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        # Add user message
        self.conversations[session_id].append({
            "role": "user",
            "content": query,
            "timestamp": datetime.utcnow(),
            "user_id": user_id
        })
        
        # Add assistant response
        self.conversations[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.utcnow(),
            "source": source,
            "confidence": confidence
        })
        
        # Limit conversation history
        if len(self.conversations[session_id]) > Config.MAX_CONVERSATION_HISTORY:
            self.conversations[session_id] = self.conversations[session_id][-Config.MAX_CONVERSATION_HISTORY:]

    async def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        if session_id not in self.conversations:
            return []
        
        history = self.conversations[session_id]
        return history[-limit:] if limit else history

    def is_available(self) -> bool:
        """Check if the OpenAI service is available."""
        try:
            # Simple test call to check API availability
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI service unavailable: {e}")
            return False

    async def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation history for a session."""
        try:
            if session_id in self.conversations:
                del self.conversations[session_id]
            return True
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False

    def get_conversation_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a conversation session."""
        if session_id not in self.conversations:
            return {"message_count": 0, "session_duration": 0}
        
        messages = self.conversations[session_id]
        if not messages:
            return {"message_count": 0, "session_duration": 0}
        
        first_message_time = messages[0]["timestamp"]
        last_message_time = messages[-1]["timestamp"]
        duration = (last_message_time - first_message_time).total_seconds()
        
        return {
            "message_count": len(messages),
            "session_duration": duration,
            "user_messages": len([m for m in messages if m["role"] == "user"]),
            "assistant_messages": len([m for m in messages if m["role"] == "assistant"])
        }
