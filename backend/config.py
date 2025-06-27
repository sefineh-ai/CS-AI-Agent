import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Pinecone Configuration
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENV: str = os.getenv("PINECONE_ENV", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "customer-support")
    PINECONE_DIMENSION: int = int(os.getenv("PINECONE_DIMENSION", "1536"))  # OpenAI embedding dimension
    
    # Google Search Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    MIN_CONFIDENCE_SCORE: float = float(os.getenv("MIN_CONFIDENCE_SCORE", "0.7"))
    
    # Conversation Configuration
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "50"))
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour in seconds
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present."""
        required_fields = [
            "OPENAI_API_KEY",
            "PINECONE_API_KEY", 
            "PINECONE_ENV"
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing required configuration: {', '.join(missing_fields)}")
            return False
        
        return True
    
    @classmethod
    def get_search_api_key(cls) -> Optional[str]:
        """Get the appropriate search API key (Google or SerpAPI)."""
        if cls.SERPAPI_API_KEY:
            return cls.SERPAPI_API_KEY
        elif cls.GOOGLE_API_KEY and cls.GOOGLE_CSE_ID:
            return cls.GOOGLE_API_KEY
        return None
