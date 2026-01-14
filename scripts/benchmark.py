"""
Benchmark RAG pipeline performance
"""
import sys
sys.path.append('.')

from src.rag_pipeline_cached import CachedRAGPipeline
import time


def benchmark_queries(pipeline: CachedRAGPipeline, queries: list, num_runs: int = 3):
    """Benchmark a set of queries"""
    print(f"\nBenchmarking {len(queries)} queries ({num_runs} runs each)...")
    
    for run in range(num_runs):
        print(f"\n--- Run {run + 1}/{num_runs} ---")
        
        for i, query in enumerate(queries, 1):
            result = pipeline.query(query, return_sources=False)
            
            cache_status = "HIT" if result['from_cache'] else "MISS"
            print(f"{i}. [{cache_status}] {result['latency_ms']:6.1f}ms - {query[:50]}...")


def main():
    print("=" * 70)
    print("ShopAssist RAG - Performance Benchmark")
    print("=" * 70)
    
    # Initialize pipeline with caching
    print("\nInitializing pipeline...")
    pipeline = CachedRAGPipeline(enable_cache=True)
    
    # Clear cache for fair benchmark
    pipeline.clear_cache()
    
    # Test queries
    queries = [
        "What's the best laptop for students under $800?",
        "Show me wireless headphones with noise cancellation",
        "What is your return policy?",
        "What do customers say about gaming laptops?",
        "Which smartphone has the best camera?",
    ]
    
    # Run benchmark
    benchmark_queries(pipeline, queries, num_runs=3)
    
    # Display metrics
    print("\n" + "=" * 70)
    print("Performance Summary")
    print("=" * 70)
    
    metrics = pipeline.get_performance_metrics()
    
    print(f"\nQuery Statistics:")
    print(f"  Total Queries: {metrics['total_queries']}")
    print(f"  Cache Hits: {metrics['cache_hits']}")
    print(f"  Cache Misses: {metrics['cache_misses']}")
    print(f"  Cache Hit Rate: {metrics['cache_hit_rate_pct']:.1f}%")
    
    print(f"\nLatency:")
    print(f"  Average: {metrics['avg_latency_ms']:.1f}ms")
    print(f"  Total: {metrics['total_latency_ms']:.1f}ms")
    
    if metrics['cache_stats']:
        print(f"\nCache:")
        print(f"  Entries: {metrics['cache_stats']['total_entries']}")
        print(f"  Size: {metrics['cache_stats']['total_size_mb']} MB")


if __name__ == "__main__":
    main()