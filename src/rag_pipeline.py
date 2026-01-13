"""
Complete RAG pipeline
"""
import yaml
from typing import Dict, Any, List, Optional

from src.vector_store import ChromaVectorStore, ChromaRetriever
from src.llm import LLMGenerator
from src.retriever import RetrievedDocument


class RAGPipeline:
    """End-to-end RAG pipeline"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        self.vector_store = ChromaVectorStore(config_path)
        self.retriever = ChromaRetriever(
            self.vector_store,
            top_k=self.config['retrieval']['top_k']
        )
        self.llm_generator = LLMGenerator(config_path)
    
    def query(
        self, 
        query: str,
        return_sources: bool = True,
        filter_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG pipeline
        
        Args:
            query: User question
            return_sources: Whether to include source documents
            filter_type: Filter by document type ('product', 'review', 'policy')
        
        Returns:
            Dictionary with answer and optionally sources
        """
        
        # Retrieve relevant documents
        if filter_type:
            retrieved_docs = self.retriever.retrieve_by_type(query, filter_type)
        else:
            retrieved_docs = self.retriever.retrieve(query)
        
        # Generate answer with sources
        result = self.llm_generator.generate_answer_with_sources(query, retrieved_docs)
        
        if not return_sources:
            return {'answer': result['answer'], 'query': query}
        
        # Format sources for output
        formatted_sources = []
        for doc, source_info in zip(retrieved_docs, result['sources']):
            formatted_source = {
                'type': source_info['type'],
                'score': source_info['score'],
                'content_preview': doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                'metadata': source_info['metadata']
            }
            formatted_sources.append(formatted_source)
        
        return {
            'answer': result['answer'],
            'query': query,
            'sources': formatted_sources,
            'num_sources': len(formatted_sources)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return self.vector_store.get_collection_stats()


if __name__ == "__main__":
    # Test RAG pipeline
    pipeline = RAGPipeline()
    
    test_queries = [
        "What's the best laptop for video editing under $1500?",
        "What do customers say about the battery life of gaming laptops?",
        "What is your return policy for electronics?"
    ]
    
    print("=" * 60)
    print("Testing RAG Pipeline")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        result = pipeline.query(query)
        
        print(f"Answer: {result['answer']}")
        print(f"\nSources: {result['num_sources']} documents")
        print()