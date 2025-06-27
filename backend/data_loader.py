import os
import logging
import asyncio
import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import json
import csv
import re

from vector_store import VectorStore
from config import Config

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        """Initialize the DataLoader with vector store connection."""
        self.vector_store = VectorStore()
        self.supported_formats = ['.txt', '.md', '.json', '.csv', '.html']
        self.max_file_size = 10 * 1024 * 1024  # 10MB limit
        
    async def add_document(
        self, 
        content: str, 
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        document_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a document to the knowledge base.
        
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
            # Validate content
            if not content or len(content.strip()) == 0:
                return {
                    "success": False,
                    "message": "Document content cannot be empty"
                }
            
            # Clean and preprocess content
            processed_content = self._preprocess_content(content)
            
            # Add to vector store
            result = await self.vector_store.add_document(
                content=processed_content,
                title=title,
                category=category,
                tags=tags,
                document_id=document_id
            )
            
            logger.info(f"Document added successfully: {result.get('document_id', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            return {
                "success": False,
                "message": f"Failed to add document: {str(e)}"
            }

    async def load_file(self, file_path: str, category: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Load a file and add it to the knowledge base.
        
        Args:
            file_path: Path to the file
            category: Document category
            tags: Document tags
            
        Returns:
            Dictionary with operation result
        """
        try:
            file_path = Path(file_path)
            
            # Validate file
            if not file_path.exists():
                return {
                    "success": False,
                    "message": f"File not found: {file_path}"
                }
            
            if not file_path.is_file():
                return {
                    "success": False,
                    "message": f"Path is not a file: {file_path}"
                }
            
            # Check file size
            if file_path.stat().st_size > self.max_file_size:
                return {
                    "success": False,
                    "message": f"File too large: {file_path.stat().st_size} bytes (max: {self.max_file_size})"
                }
            
            # Check file format
            if file_path.suffix.lower() not in self.supported_formats:
                return {
                    "success": False,
                    "message": f"Unsupported file format: {file_path.suffix}"
                }
            
            # Read and process file
            content = await self._read_file(file_path)
            if not content:
                return {
                    "success": False,
                    "message": f"Failed to read file: {file_path}"
                }
            
            # Extract title from filename
            title = file_path.stem
            
            # Add to knowledge base
            result = await self.add_document(
                content=content,
                title=title,
                category=category,
                tags=tags
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to load file: {str(e)}"
            }

    async def load_directory(self, directory_path: str, category: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Load all supported files from a directory.
        
        Args:
            directory_path: Path to the directory
            category: Document category for all files
            tags: Document tags for all files
            
        Returns:
            Dictionary with batch operation result
        """
        try:
            directory_path = Path(directory_path)
            
            if not directory_path.exists():
                return {
                    "success": False,
                    "message": f"Directory not found: {directory_path}"
                }
            
            if not directory_path.is_dir():
                return {
                    "success": False,
                    "message": f"Path is not a directory: {directory_path}"
                }
            
            # Find all supported files
            supported_files = []
            for file_path in directory_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    supported_files.append(file_path)
            
            if not supported_files:
                return {
                    "success": False,
                    "message": f"No supported files found in directory: {directory_path}"
                }
            
            # Process files
            results = []
            successful = 0
            failed = 0
            
            for file_path in supported_files:
                result = await self.load_file(str(file_path), category, tags)
                results.append({
                    "file": str(file_path),
                    "result": result
                })
                
                if result["success"]:
                    successful += 1
                else:
                    failed += 1
            
            return {
                "success": True,
                "total_files": len(supported_files),
                "successful": successful,
                "failed": failed,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error loading directory {directory_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to load directory: {str(e)}"
            }

    async def _read_file(self, file_path: Path) -> Optional[str]:
        """Read and parse file content based on its format."""
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.txt' or suffix == '.md':
                return await self._read_text_file(file_path)
            elif suffix == '.json':
                return await self._read_json_file(file_path)
            elif suffix == '.csv':
                return await self._read_csv_file(file_path)
            elif suffix == '.html':
                return await self._read_html_file(file_path)
            else:
                logger.warning(f"Unsupported file format: {suffix}")
                return None
                
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

    async def _read_text_file(self, file_path: Path) -> str:
        """Read a text file."""
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file_path.read_text, 'utf-8')
        return content

    async def _read_json_file(self, file_path: Path) -> str:
        """Read and parse a JSON file."""
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file_path.read_text, 'utf-8')
        
        try:
            data = json.loads(content)
            # Convert JSON to readable text
            return self._json_to_text(data)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return content

    async def _read_csv_file(self, file_path: Path) -> str:
        """Read and parse a CSV file."""
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file_path.read_text, 'utf-8')
        
        try:
            # Parse CSV and convert to readable text
            lines = content.split('\n')
            reader = csv.reader(lines)
            
            text_parts = []
            for i, row in enumerate(reader):
                if row:  # Skip empty rows
                    text_parts.append(f"Row {i+1}: {', '.join(row)}")
            
            return '\n'.join(text_parts)
        except Exception as e:
            logger.error(f"Error parsing CSV {file_path}: {e}")
            return content

    async def _read_html_file(self, file_path: Path) -> str:
        """Read and parse an HTML file."""
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file_path.read_text, 'utf-8')
        
        # Simple HTML tag removal (in production, use BeautifulSoup)
        text = re.sub(r'<[^>]+>', '', content)
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text.strip()

    def _json_to_text(self, data: Any, indent: int = 0) -> str:
        """Convert JSON data to readable text."""
        if isinstance(data, dict):
            text_parts = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    text_parts.append(f"{key}: {self._json_to_text(value, indent + 1)}")
                else:
                    text_parts.append(f"{key}: {value}")
            return '\n'.join(text_parts)
        elif isinstance(data, list):
            text_parts = []
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    text_parts.append(f"Item {i+1}: {self._json_to_text(item, indent + 1)}")
                else:
                    text_parts.append(f"Item {i+1}: {item}")
            return '\n'.join(text_parts)
        else:
            return str(data)

    def _preprocess_content(self, content: str) -> str:
        """Preprocess and clean document content."""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove special characters that might cause issues
        content = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', '', content)
        
        # Normalize line breaks
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        return content.strip()

    async def batch_add_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add multiple documents in batch.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Dictionary with batch operation result
        """
        try:
            # Use vector store's batch operation
            result = await self.vector_store.batch_add_documents(documents)
            
            logger.info(f"Batch document addition completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in batch document addition: {e}")
            return {
                "success": False,
                "documents_added": 0,
                "message": f"Failed to add documents: {str(e)}"
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
        Update an existing document.
        
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
            if content:
                content = self._preprocess_content(content)
            
            result = await self.vector_store.update_document(
                document_id=document_id,
                content=content,
                title=title,
                category=category,
                tags=tags
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            return {
                "success": False,
                "message": f"Failed to update document: {str(e)}"
            }

    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Delete a document from the knowledge base.
        
        Args:
            document_id: Document ID to delete
            
        Returns:
            Dictionary with operation result
        """
        try:
            result = await self.vector_store.delete_document(document_id)
            return result
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return {
                "success": False,
                "message": f"Failed to delete document: {str(e)}"
            }

    async def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document from the knowledge base.
        
        Args:
            document_id: Document ID to retrieve
            
        Returns:
            Document data or None if not found
        """
        try:
            return await self.vector_store.get_document(document_id)
            
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {e}")
            return None

    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents in the knowledge base.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching documents
        """
        try:
            return await self.vector_store.search(query, limit)
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base."""
        try:
            stats = asyncio.run(self.vector_store.get_statistics())
            return {
                "total_documents": stats.get("total_vectors", 0),
                "index_name": stats.get("index_name", "unknown"),
                "dimension": stats.get("dimension", 0),
                "supported_formats": self.supported_formats,
                "max_file_size": self.max_file_size
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {"error": str(e)}
