"""
RAG pipeline with caching
"""
from src.rag_pipeline import RAGPipeline
from src.cache import SimpleCache
from typing import Dict, Any, Optional
import time


class CachedRAGPipeline(RAGPipeline):
    """RAG Pipeline with response caching"""
    
    def __init__(self, config_path: str = "config/config.yaml", enable_cache: bool = True):
        super().__init__(config_path)
        self.enable_cache = enable_cache
        self.cache = SimpleCache() if enable_cache else None
        
        # Performance metrics
        self.metrics = {
            'total_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_latency_ms': 0,
            'total_latency_ms': 0
        }
    
    def query(
        self, 
        query: str,
        return_sources: bool = True,
        filter_type: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Query with caching support
        """
        start_time = time.time()
        
        # Try cache first
        if use_cache and self.enable_cache:
            cached_result = self.cache.get(query)
            if cached_result is not None:
                # Cache hit
                self.metrics['cache_hits'] += 1
                self.metrics['total_queries'] += 1
                
                latency_ms = (time.time() - start_time) * 1000
                self.metrics['total_latency_ms'] += latency_ms
                self.metrics['avg_latency_ms'] = self.metrics['total_latency_ms'] / self.metrics['total_queries']
                
                cached_result['from_cache'] = True
                cached_result['latency_ms'] = round(latency_ms, 2)
                return cached_result
        
        # Cache miss - run actual query
        result = super().query(query, return_sources, filter_type)
        
        # Update metrics
        self.metrics['cache_misses'] += 1
        self.metrics['total_queries'] += 1
        
        latency_ms = (time.time() - start_time) * 1000
        self.metrics['total_latency_ms'] += latency_ms
        self.metrics['avg_latency_ms'] = self.metrics['total_latency_ms'] / self.metrics['total_queries']
        
        result['from_cache'] = False
        result['latency_ms'] = round(latency_ms, 2)
        
        # Cache the result
        if use_cache and self.enable_cache:
            self.cache.set(query, result)
        
        return result
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        cache_hit_rate = 0
        if self.metrics['total_queries'] > 0:
            cache_hit_rate = (self.metrics['cache_hits'] / self.metrics['total_queries']) * 100
        
        metrics = {
            **self.metrics,
            'cache_hit_rate_pct': round(cache_hit_rate, 2),
            'cache_stats': self.cache.get_stats() if self.cache else None
        }
        
        return metrics
    
    def clear_cache(self):
        """Clear the cache"""
        if self.cache:
            self.cache.clear()
            print("✓ Cache cleared")


if __name__ == "__main__":
    # Test caching
    pipeline = CachedRAGPipeline(enable_cache=True)
    
    test_query = "What's the best laptop for students under $800?"
    
    print("=" * 60)
    print("Testing Cache Performance")
    print("=" * 60)
    
    # First query (cache miss)
    print("\n1. First query (cache miss):")
    result1 = pipeline.query(test_query)
    print(f"   From cache: {result1['from_cache']}")
    print(f"   Latency: {result1['latency_ms']}ms")
    
    # Second query (cache hit)
    print("\n2. Second query (cache hit):")
    result2 = pipeline.query(test_query)
    print(f"   From cache: {result2['from_cache']}")
    print(f"   Latency: {result2['latency_ms']}ms")
    
    # Performance metrics
    print("\n3. Performance Metrics:")
    metrics = pipeline.get_performance_metrics()
    print(f"   Total queries: {metrics['total_queries']}")
    print(f"   Cache hits: {metrics['cache_hits']}")
    print(f"   Cache hit rate: {metrics['cache_hit_rate_pct']}%")
    print(f"   Avg latency: {metrics['avg_latency_ms']:.2f}ms")
    
    if metrics['cache_stats']:
        print(f"\n4. Cache Stats:")
        print(f"   Cached entries: {metrics['cache_stats']['total_entries']}")
        print(f"   Cache size: {metrics['cache_stats']['total_size_mb']} MB")