"""
Test queries for evaluating RAG system
"""
import sys
sys.path.append('.')

from src.rag_pipeline import RAGPipeline
import json
from typing import List, Dict
import time


# Test query sets
TEST_QUERIES = {
    "product_search": [
        {
            "query": "What's the best laptop for students under $800?",
            "expected_type": "product",
            "category": "product_search"
        },
        {
            "query": "Show me affordable wireless headphones with noise cancellation",
            "expected_type": "product",
            "category": "product_search"
        },
        {
            "query": "Which smartphone has the best camera for photography?",
            "expected_type": "product",
            "category": "product_search"
        },
        {
            "query": "Gaming mouse with RGB lighting under $50",
            "expected_type": "product",
            "category": "product_search"
        }
    ],
    "review_analysis": [
        {
            "query": "What do customers say about MacBook Air battery life?",
            "expected_type": "review",
            "category": "review_analysis"
        },
        {
            "query": "Are there common complaints about gaming laptop keyboards?",
            "expected_type": "review",
            "category": "review_analysis"
        },
        {
            "query": "How reliable is this wireless mouse according to reviews?",
            "expected_type": "review",
            "category": "review_analysis"
        }
    ],
    "policy_questions": [
        {
            "query": "What is your return policy for opened electronics?",
            "expected_type": "policy",
            "category": "policy_questions"
        },
        {
            "query": "How long does standard shipping take?",
            "expected_type": "policy",
            "category": "policy_questions"
        },
        {
            "query": "Do you offer warranty on laptops?",
            "expected_type": "policy",
            "category": "policy_questions"
        },
        {
            "query": "What payment methods do you accept?",
            "expected_type": "policy",
            "category": "policy_questions"
        }
    ],
    "comparison": [
        {
            "query": "Compare MacBook Air vs Dell XPS for students",
            "expected_type": "product",
            "category": "comparison"
        },
        {
            "query": "iPhone vs Samsung Galaxy: which has better camera?",
            "expected_type": "product",
            "category": "comparison"
        }
    ]
}


def evaluate_query(pipeline: RAGPipeline, query_data: Dict) -> Dict:
    """Evaluate a single query"""
    query = query_data['query']
    
    start_time = time.time()
    result = pipeline.query(query, return_sources=True)
    latency = time.time() - start_time
    
    # Check if expected doc type is in top 3 sources
    top_types = [s['type'] for s in result['sources'][:3]]
    has_expected_type = query_data['expected_type'] in top_types
    
    evaluation = {
        'query': query,
        'category': query_data['category'],
        'answer': result['answer'],
        'num_sources': result['num_sources'],
        'latency_ms': round(latency * 1000, 2),
        'top_source_types': top_types,
        'has_expected_type': has_expected_type,
        'answer_length': len(result['answer'])
    }
    
    return evaluation


def run_evaluation(pipeline: RAGPipeline, save_results: bool = True):
    """Run full evaluation"""
    print("=" * 70)
    print("ShopAssist RAG - Evaluation")
    print("=" * 70)
    
    all_results = []
    category_stats = {}
    
    for category, queries in TEST_QUERIES.items():
        print(f"\n📊 Category: {category}")
        print("-" * 70)
        
        category_results = []
        
        for query_data in queries:
            result = evaluate_query(pipeline, query_data)
            category_results.append(result)
            all_results.append(result)
            
            # Print result
            status = "✓" if result['has_expected_type'] else "✗"
            print(f"\n{status} Query: {result['query']}")
            print(f"   Latency: {result['latency_ms']}ms")
            print(f"   Sources: {result['num_sources']} ({', '.join(result['top_source_types'][:3])})")
            print(f"   Answer: {result['answer'][:100]}...")
        
        # Category statistics
        avg_latency = sum(r['latency_ms'] for r in category_results) / len(category_results)
        success_rate = sum(r['has_expected_type'] for r in category_results) / len(category_results)
        
        category_stats[category] = {
            'total_queries': len(category_results),
            'avg_latency_ms': round(avg_latency, 2),
            'success_rate': round(success_rate * 100, 2)
        }
    
    # Overall statistics
    print("\n" + "=" * 70)
    print("📈 Overall Statistics")
    print("=" * 70)
    
    total_queries = len(all_results)
    avg_latency = sum(r['latency_ms'] for r in all_results) / total_queries
    overall_success = sum(r['has_expected_type'] for r in all_results) / total_queries
    
    print(f"\nTotal Queries: {total_queries}")
    print(f"Average Latency: {round(avg_latency, 2)}ms")
    print(f"Overall Success Rate: {round(overall_success * 100, 2)}%")
    
    print("\nBy Category:")
    for category, stats in category_stats.items():
        print(f"  {category}:")
        print(f"    - Queries: {stats['total_queries']}")
        print(f"    - Avg Latency: {stats['avg_latency_ms']}ms")
        print(f"    - Success Rate: {stats['success_rate']}%")
    
    # Save results
    if save_results:
        results_data = {
            'summary': {
                'total_queries': total_queries,
                'avg_latency_ms': round(avg_latency, 2),
                'success_rate_pct': round(overall_success * 100, 2)
            },
            'by_category': category_stats,
            'detailed_results': all_results
        }
        
        with open('tests/evaluation_results.json', 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\n✓ Results saved to tests/evaluation_results.json")
    
    return results_data


if __name__ == "__main__":
    print("Initializing RAG pipeline...")
    pipeline = RAGPipeline()
    
    print("Running evaluation...\n")
    results = run_evaluation(pipeline, save_results=True)