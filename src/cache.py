"""
Simple caching layer for RAG responses
"""
import json
import hashlib
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class SimpleCache:
    """Simple file-based cache for RAG responses"""
    
    def __init__(self, cache_dir: str = ".cache", ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key from query"""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get full path to cache file"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached response for query"""
        cache_key = self._get_cache_key(query)
        cache_path = self._get_cache_path(cache_key)
        
        # Check if cache file exists
        if not os.path.exists(cache_path):
            return None
        
        # Read cache file
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                # Cache expired, remove file
                os.remove(cache_path)
                return None
            
            return cache_data['response']
        
        except (json.JSONDecodeError, KeyError, ValueError):
            # Invalid cache file, remove it
            os.remove(cache_path)
            return None
    
    def set(self, query: str, response: Dict[str, Any]):
        """Cache response for query"""
        cache_key = self._get_cache_key(query)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            'query': query,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def clear(self):
        """Clear all cache"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, filename))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
        
        total_size = 0
        for filename in cache_files:
            filepath = os.path.join(self.cache_dir, filename)
            total_size += os.path.getsize(filepath)
        
        return {
            'total_entries': len(cache_files),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_directory': self.cache_dir
        }