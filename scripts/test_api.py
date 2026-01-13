"""
Test the FastAPI endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_query(query: str):
    """Test query endpoint"""
    print(f"Testing query: '{query}'")
    
    payload = {
        "query": query,
        "return_sources": True
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['num_sources']}\n")
    else:
        print(f"Error: {response.status_code}")
        print(f"Detail: {response.text}\n")


def test_examples():
    """Test examples endpoint"""
    print("Testing /examples endpoint...")
    response = requests.get(f"{BASE_URL}/examples")
    print(f"Status: {response.status_code}")
    examples = response.json()
    print(f"Product queries: {len(examples['product_queries'])}")
    print(f"Review queries: {len(examples['review_queries'])}")
    print(f"Policy queries: {len(examples['policy_queries'])}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing ShopAssist RAG API")
    print("=" * 60)
    
    print("\n1. Health Check")
    print("-" * 60)
    test_health()
    
    print("\n2. Example Queries")
    print("-" * 60)
    test_examples()
    
    print("\n3. Sample Queries")
    print("-" * 60)
    
    test_queries = [
        "What's a good laptop for students under $800?",
        "What do customers say about gaming laptops?",
        "What is your return policy?"
    ]
    
    for query in test_queries:
        test_query(query)