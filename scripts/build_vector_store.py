"""
Build vector store from processed documents
"""
import sys
sys.path.append('.')

import json
from src.vector_store import ChromaVectorStore
from src.data_processor import Document


def load_processed_documents(filepath: str) -> list:
    """Load processed documents from JSON"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    documents = []
    for item in data:
        doc = Document(
            content=item['content'],
            metadata=item['metadata'],
            doc_type=item['doc_type'],
            doc_id=item['doc_id']
        )
        documents.append(doc)
    
    return documents


def main():
    print("=" * 60)
    print("Building Vector Store")
    print("=" * 60)
    
    # Load processed documents
    print("\nLoading processed documents...")
    documents = load_processed_documents("data/processed/documents.json")
    print(f"✓ Loaded {len(documents)} documents")
    
    # Initialize vector store
    print("\nInitializing vector store...")
    vector_store = ChromaVectorStore()
    
    # Clear existing data (optional)
    # vector_store.clear_collection()
    
    # Add documents
    print("\nAdding documents to vector store...")
    vector_store.add_documents(documents, batch_size=100)
    
    # Get stats
    stats = vector_store.get_collection_stats()
    print("\n" + "=" * 60)
    print("✓ Vector store built successfully!")
    print("=" * 60)
    print(f"Total documents indexed: {stats['total_documents']}")
    
    # Test search
    print("\nTesting search...")
    test_query = "laptop for gaming"
    results = vector_store.search(test_query, top_k=3)
    print(f"\nQuery: '{test_query}'")
    print(f"Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. [{doc.doc_type}] Score: {doc.score:.3f}")
        print(f"   {doc.content[:100]}...")


if __name__ == "__main__":
    main()