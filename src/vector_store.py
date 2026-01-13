"""
ChromaDB vector store integration
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import yaml
import os
from tqdm import tqdm

from src.embeddings import EmbeddingGenerator
from src.retriever import Retriever, RetrievedDocument
from src.data_processor import Document


class ChromaVectorStore:
    """ChromaDB vector store for RAG"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        persist_dir = self.config['vector_db']['persist_directory']
        collection_name = self.config['vector_db']['collection_name']
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.embedding_generator = EmbeddingGenerator(config_path)
    
    def add_documents(self, documents: List[Document], batch_size: int = 100):
        """Add documents to vector store"""
        print(f"Adding {len(documents)} documents to vector store...")
        
        for i in tqdm(range(0, len(documents), batch_size), desc="Indexing"):
            batch = documents[i:i + batch_size]
            
            # Prepare batch data
            ids = [doc.doc_id for doc in batch]
            contents = [doc.content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            # Generate embeddings
            embeddings = self.embedding_generator.generate_embeddings_batch(contents)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        
        print(f"✓ Added {len(documents)} documents to vector store")
    
    def search(self, query: str, top_k: int = 5, filter_dict: Optional[Dict] = None) -> List[RetrievedDocument]:
        """Search for documents similar to query"""
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict
        )
        
        # Convert to RetrievedDocument objects
        retrieved_docs = []
        
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                doc = RetrievedDocument(
                    content=results['documents'][0][i],
                    metadata=results['metadatas'][0][i],
                    doc_type=results['metadatas'][0][i].get('doc_type', 'unknown'),
                    doc_id=results['ids'][0][i],
                    score=1 - results['distances'][0][i]  # Convert distance to similarity
                )
                retrieved_docs.append(doc)
        
        return retrieved_docs
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.collection.name
        }
    
    def clear_collection(self):
        """Clear all documents from collection"""
        self.client.delete_collection(self.config['vector_db']['collection_name'])
        self.collection = self.client.create_collection(
            name=self.config['vector_db']['collection_name'],
            metadata={"hnsw:space": "cosine"}
        )


class ChromaRetriever(Retriever):
    """Retriever using ChromaDB backend"""
    
    def __init__(self, vector_store: ChromaVectorStore, top_k: int = 5):
        super().__init__(top_k)
        self.vector_store = vector_store
    
    def retrieve(self, query: str) -> List[RetrievedDocument]:
        """Retrieve documents for a query"""
        return self.vector_store.search(query, top_k=self.top_k)
    
    def retrieve_by_type(self, query: str, doc_type: str) -> List[RetrievedDocument]:
        """Retrieve documents of a specific type"""
        # Note: ChromaDB filtering syntax
        filter_dict = {"doc_type": doc_type}
        return self.vector_store.search(query, top_k=self.top_k, filter_dict=filter_dict)


if __name__ == "__main__":
    # Test vector store
    vector_store = ChromaVectorStore()
    stats = vector_store.get_collection_stats()
    print(f"Collection stats: {stats}")