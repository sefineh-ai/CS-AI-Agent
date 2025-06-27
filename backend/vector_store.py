import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from typing import List, Dict, Any, Optional
import logging
import asyncio
from datetime import datetime
import uuid

from config import Config

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        """Initialize the VectorStore with Pinecone configuration."""
        self.api_key = Config.PINECONE_API_KEY
        self.environment = Config.PINECONE_ENV
        self.index_name = Config.PINECONE_INDEX_NAME
        self.dimension = Config.PINECONE_DIMENSION
        
        # Initialize Pinecone
        try:
            pinecone.init(api_key=self.api_key, environment=self.environment)
            self.pinecone = pinecone
            self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
            self._initialize_index()
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise

    def _initialize_index(self):
        """Initialize or connect to the Pinecone index."""
        try:
            # Check if index exists
            if self.index_name not in pinecone.list_indexes():
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
                # Wait for index to be ready
                while not pinecone.describe_index(self.index_name).status['ready']:
                    asyncio.sleep(1)
            
            # Get the index
            self.index = pinecone.Index(self.index_name)
            logger.info(f"Successfully connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone index: {e}")
            raise

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents in the vector store.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of search results with content and metadata
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=limit,
                include_metadata=True
            )
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "content": match.metadata.get("content", ""),
                    "title": match.metadata.get("title", ""),
                    "category": match.metadata.get("category", ""),
                    "tags": match.metadata.get("tags", []),
                    "score": match.score,
                    "created_at": match.metadata.get("created_at", "")
                })
            
            logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []

    async def add_document(
        self, 
        content: str, 
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a document to the vector store.
        
        Args:
            content: Document content
            title: Document title
            category: Document category
            tags: Document tags
            document_id: Optional custom document ID
            
        Returns:
            Dictionary with operation result
        """
        try:
            # Generate document ID if not provided
            if not document_id:
                document_id = str(uuid.uuid4())
            
            # Generate embedding for the content
            embedding = self.embeddings.embed_query(content)
            
            # Prepare metadata
            metadata = {
                "content": content,
                "title": title or "Untitled",
                "category": category or "general",
                "tags": tags or [],
                "created_at": datetime.utcnow().isoformat(),
                "document_id": document_id
            }
            
            # Upsert to Pinecone
            self.index.upsert(
                vectors=[{
                    "id": document_id,
                    "values": embedding,
                    "metadata": metadata
                }]
            )
            
            logger.info(f"Successfully added document: {document_id}")
            
            return {
                "success": True,
                "document_id": document_id,
                "message": "Document added successfully"
            }
            
        except Exception as e:
            logger.error(f"Error adding document to vector store: {e}")
            return {
                "success": False,
                "document_id": document_id,
                "message": f"Failed to add document: {str(e)}"
            }

    async def update_document(
        self, 
        document_id: str, 
        content: Optional[str] = None,
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing document in the vector store.
        
        Args:
            document_id: Document ID to update
            content: New content
            title: New title
            category: New category
            tags: New tags
            
        Returns:
            Dictionary with operation result
        """
        try:
            # First, get the existing document
            existing = self.index.fetch(ids=[document_id])
            if not existing.vectors:
                return {
                    "success": False,
                    "message": f"Document {document_id} not found"
                }
            
            # Get existing metadata
            existing_metadata = existing.vectors[document_id].metadata
            
            # Update metadata
            updated_metadata = existing_metadata.copy()
            if content is not None:
                updated_metadata["content"] = content
            if title is not None:
                updated_metadata["title"] = title
            if category is not None:
                updated_metadata["category"] = category
            if tags is not None:
                updated_metadata["tags"] = tags
            
            updated_metadata["updated_at"] = datetime.utcnow().isoformat()
            
            # Generate new embedding if content changed
            if content is not None:
                new_embedding = self.embeddings.embed_query(content)
                # Update the vector
                self.index.upsert(
                    vectors=[{
                        "id": document_id,
                        "values": new_embedding,
                        "metadata": updated_metadata
                    }]
                )
            else:
                # Update only metadata
                self.index.update(
                    id=document_id,
                    set_metadata=updated_metadata
                )
            
            logger.info(f"Successfully updated document: {document_id}")
            
            return {
                "success": True,
                "document_id": document_id,
                "message": "Document updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return {
                "success": False,
                "document_id": document_id,
                "message": f"Failed to update document: {str(e)}"
            }

    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from the vector store.
        
        Args:
            document_id: Document ID to delete
            
        Returns:
            Dictionary with operation result
        """
        try:
            self.index.delete(ids=[document_id])
            
            logger.info(f"Successfully deleted document: {document_id}")
            
            return {
                "success": True,
                "document_id": document_id,
                "message": "Document deleted successfully"
            }
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return {
                "success": False,
                "document_id": document_id,
                "message": f"Failed to delete document: {str(e)}"
            }

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document from the vector store.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Document data or None if not found
        """
        try:
            result = self.index.fetch(ids=[document_id])
            
            if not result.vectors:
                return None
            
            vector = result.vectors[document_id]
            return {
                "id": document_id,
                "content": vector.metadata.get("content", ""),
                "title": vector.metadata.get("title", ""),
                "category": vector.metadata.get("category", ""),
                "tags": vector.metadata.get("tags", []),
                "created_at": vector.metadata.get("created_at", ""),
                "updated_at": vector.metadata.get("updated_at", "")
            }
            
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            return None

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with statistics
        """
        try:
            stats = self.index.describe_index_stats()
            
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_name": self.index_name,
                "namespaces": stats.namespaces if hasattr(stats, 'namespaces') else {}
            }
            
        except Exception as e:
            logger.error(f"Error getting vector store statistics: {e}")
            return {
                "error": str(e)
            }

    def is_available(self) -> bool:
        """Check if the vector store is available."""
        try:
            # Try to get index stats
            self.index.describe_index_stats()
            return True
        except Exception as e:
            logger.error(f"Vector store unavailable: {e}")
            return False

    async def batch_add_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple documents in batch.
        
        Args:
            documents: List of document dictionaries with content, title, category, tags
            
        Returns:
            Dictionary with batch operation result
        """
        try:
            vectors = []
            
            for doc in documents:
                document_id = doc.get("document_id", str(uuid.uuid4()))
                content = doc["content"]
                
                # Generate embedding
                embedding = self.embeddings.embed_query(content)
                
                # Prepare metadata
                metadata = {
                    "content": content,
                    "title": doc.get("title", "Untitled"),
                    "category": doc.get("category", "general"),
                    "tags": doc.get("tags", []),
                    "created_at": datetime.utcnow().isoformat(),
                    "document_id": document_id
                }
                
                vectors.append({
                    "id": document_id,
                    "values": embedding,
                    "metadata": metadata
                })
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Successfully added {len(documents)} documents in batch")
            
            return {
                "success": True,
                "documents_added": len(documents),
                "message": f"Successfully added {len(documents)} documents"
            }
            
        except Exception as e:
            logger.error(f"Error in batch document addition: {e}")
            return {
                "success": False,
                "documents_added": 0,
                "message": f"Failed to add documents: {str(e)}"
            }
