"""
Document retrieval logic
"""
from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass


@dataclass
class RetrievedDocument:
    """Document retrieved from vector store"""
    content: str
    metadata: Dict[str, Any]
    doc_type: str
    doc_id: str
    score: float


class Retriever:
    """Base retriever class"""
    
    def __init__(self, top_k: int = 5):
        self.top_k = top_k
    
    def retrieve(self, query: str) -> List[RetrievedDocument]:
        """Retrieve documents for a query"""
        raise NotImplementedError
    
    def format_context(self, documents: List[RetrievedDocument]) -> str:
        """Format retrieved documents into context string"""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            doc_type_label = doc.doc_type.upper()
            context_parts.append(f"[{doc_type_label} {i}]")
            context_parts.append(doc.content)
            context_parts.append("")  # blank line
        
        return "\n".join(context_parts)
    
    def rerank_by_relevance(self, documents: List[RetrievedDocument], query: str) -> List[RetrievedDocument]:
        """Simple reranking based on keyword overlap (placeholder)"""
        # This is a simple implementation - in production you'd use a cross-encoder
        query_words = set(query.lower().split())
        
        for doc in documents:
            doc_words = set(doc.content.lower().split())
            overlap = len(query_words & doc_words)
            # Adjust score based on overlap (simple boost)
            doc.score = doc.score * (1 + overlap * 0.01)
        
        # Re-sort by updated scores
        documents.sort(key=lambda x: x.score, reverse=True)
        return documents