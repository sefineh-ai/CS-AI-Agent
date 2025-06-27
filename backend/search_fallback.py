import requests
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config import Config

logger = logging.getLogger(__name__)

class SearchFallback:
    def __init__(self):
        """Initialize the SearchFallback with API configuration."""
        self.google_api_key = Config.GOOGLE_API_KEY
        self.google_cse_id = Config.GOOGLE_CSE_ID
        self.serpapi_key = Config.SERPAPI_API_KEY
        self.max_results = Config.MAX_SEARCH_RESULTS
        
        # Determine which search API to use
        self.search_api = self._determine_search_api()

    def _determine_search_api(self) -> str:
        """Determine which search API to use based on available credentials."""
        if self.serpapi_key:
            logger.info("Using SerpAPI for web search")
            return "serpapi"
        elif self.google_api_key and self.google_cse_id:
            logger.info("Using Google Custom Search API for web search")
            return "google"
        else:
            logger.warning("No search API credentials configured")
            return "none"

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search using the configured search API.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of search results with title, snippet, and URL
        """
        try:
            if self.search_api == "serpapi":
                return await self._search_serpapi(query, limit)
            elif self.search_api == "google":
                return await self._search_google(query, limit)
            else:
                logger.warning("No search API available")
                return []
                
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return []

    async def _search_serpapi(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search using SerpAPI."""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": min(limit, 10),  # SerpAPI max is 10
                "engine": "google"
            }
            
            # Use asyncio to make the request
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(url, params=params, timeout=10)
            )
            
            if response.status_code != 200:
                logger.error(f"SerpAPI request failed with status {response.status_code}")
                return []
            
            data = response.json()
            results = []
            
            # Extract organic results
            organic_results = data.get("organic_results", [])
            for result in organic_results[:limit]:
                results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", ""),
                    "source": "serpapi",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            logger.info(f"SerpAPI search returned {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error in SerpAPI search: {e}")
            return []

    async def _search_google(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API."""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "q": query,
                "cx": self.google_cse_id,
                "key": self.google_api_key,
                "num": min(limit, 10),  # Google CSE max is 10
                "safe": "active"
            }
            
            # Use asyncio to make the request
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(url, params=params, timeout=10)
            )
            
            if response.status_code != 200:
                logger.error(f"Google Search API request failed with status {response.status_code}")
                return []
            
            data = response.json()
            results = []
            
            # Extract search results
            items = data.get("items", [])
            for item in items[:limit]:
                results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": item.get("link", ""),
                    "source": "google",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            logger.info(f"Google Search returned {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error in Google Search: {e}")
            return []

    async def search_with_fallback(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform search with fallback between different APIs.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            # Try primary search API
            if self.search_api == "serpapi":
                results = await self._search_serpapi(query, limit)
                if results:
                    return results
                
                # Fallback to Google if SerpAPI fails
                if self.google_api_key and self.google_cse_id:
                    logger.info("SerpAPI failed, falling back to Google Search")
                    return await self._search_google(query, limit)
                    
            elif self.search_api == "google":
                results = await self._search_google(query, limit)
                if results:
                    return results
                
                # Fallback to SerpAPI if Google fails
                if self.serpapi_key:
                    logger.info("Google Search failed, falling back to SerpAPI")
                    return await self._search_serpapi(query, limit)
            
            return []
            
        except Exception as e:
            logger.error(f"Error in search with fallback: {e}")
            return []

    def is_available(self) -> bool:
        """Check if any search API is available."""
        return self.search_api != "none"

    async def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query.
        
        Args:
            query: Partial query to get suggestions for
            
        Returns:
            List of suggested search terms
        """
        try:
            if self.search_api == "serpapi":
                return await self._get_serpapi_suggestions(query)
            elif self.search_api == "google":
                return await self._get_google_suggestions(query)
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return []

    async def _get_serpapi_suggestions(self, query: str) -> List[str]:
        """Get search suggestions from SerpAPI."""
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "engine": "google",
                "num": 1  # We only need suggestions, not results
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(url, params=params, timeout=5)
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            suggestions = data.get("suggested_searches", [])
            
            return [suggestion.get("query", "") for suggestion in suggestions[:5]]
            
        except Exception as e:
            logger.error(f"Error getting SerpAPI suggestions: {e}")
            return []

    async def _get_google_suggestions(self, query: str) -> List[str]:
        """Get search suggestions from Google."""
        try:
            # Google doesn't provide suggestions in CSE API, so we'll return empty
            # In a real implementation, you might use a different endpoint
            return []
            
        except Exception as e:
            logger.error(f"Error getting Google suggestions: {e}")
            return []

    async def search_multiple_queries(self, queries: List[str], limit_per_query: int = 3) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search multiple queries and return results for each.
        
        Args:
            queries: List of search queries
            limit_per_query: Maximum results per query
            
        Returns:
            Dictionary mapping queries to their results
        """
        try:
            results = {}
            
            for query in queries:
                query_results = await self.search(query, limit_per_query)
                results[query] = query_results
            
            return results
            
        except Exception as e:
            logger.error(f"Error in multiple query search: {e}")
            return {}

    def get_search_stats(self) -> Dict[str, Any]:
        """Get statistics about the search service."""
        return {
            "search_api": self.search_api,
            "google_api_configured": bool(self.google_api_key and self.google_cse_id),
            "serpapi_configured": bool(self.serpapi_key),
            "max_results": self.max_results,
            "available": self.is_available()
        }

    async def test_search_api(self) -> Dict[str, Any]:
        """
        Test the search API functionality.
        
        Returns:
            Dictionary with test results
        """
        try:
            test_query = "test search"
            results = await self.search(test_query, 1)
            
            return {
                "success": len(results) > 0,
                "api_used": self.search_api,
                "results_count": len(results),
                "test_query": test_query
            }
            
        except Exception as e:
            logger.error(f"Search API test failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "api_used": self.search_api
            }
