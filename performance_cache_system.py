"""
Advanced Caching System for AgriForecast.ai
React Query-inspired caching for Streamlit with intelligent cache management
"""

import streamlit as st
import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Callable, List
import sqlite3
import threading
import pickle
import os

class CacheManager:
    """Intelligent cache manager with React Query-like behavior"""
    
    def __init__(self, cache_dir: str = "cache", default_stale_time: int = 300):
        self.cache_dir = cache_dir
        self.default_stale_time = default_stale_time  # 5 minutes default
        self.memory_cache = {}
        self.cache_metadata = {}
        self._ensure_cache_dir()
        
        # Cache statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'expired': 0,
            'background_updates': 0
        }
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _generate_cache_key(self, query_key: str, params: Dict = None) -> str:
        """Generate unique cache key from query and parameters"""
        cache_data = {
            'query': query_key,
            'params': params or {}
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get file path for cache key"""
        return os.path.join(self.cache_dir, f"{cache_key}.cache")
    
    def _is_stale(self, cache_key: str, stale_time: int) -> bool:
        """Check if cached data is stale"""
        if cache_key not in self.cache_metadata:
            return True
        
        cached_time = self.cache_metadata[cache_key]['timestamp']
        return time.time() - cached_time > stale_time
    
    def get(self, query_key: str, params: Dict = None, stale_time: int = None) -> Optional[Any]:
        """Get data from cache"""
        cache_key = self._generate_cache_key(query_key, params)
        stale_time = stale_time or self.default_stale_time
        
        # Check memory cache first
        if cache_key in self.memory_cache:
            if not self._is_stale(cache_key, stale_time):
                self.stats['hits'] += 1
                return self.memory_cache[cache_key]
            else:
                self.stats['expired'] += 1
        
        # Check persistent cache
        cache_path = self._get_cache_path(cache_key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                    metadata = pickle.load(f)
                
                self.cache_metadata[cache_key] = metadata
                
                if not self._is_stale(cache_key, stale_time):
                    self.memory_cache[cache_key] = data
                    self.stats['hits'] += 1
                    return data
                else:
                    self.stats['expired'] += 1
            except Exception as e:
                print(f"Cache read error: {e}")
        
        self.stats['misses'] += 1
        return None
    
    def set(self, query_key: str, data: Any, params: Dict = None, cache_time: int = None) -> None:
        """Set data in cache"""
        cache_key = self._generate_cache_key(query_key, params)
        timestamp = time.time()
        
        metadata = {
            'timestamp': timestamp,
            'cache_time': cache_time or self.default_stale_time,
            'query_key': query_key,
            'params': params
        }
        
        # Store in memory
        self.memory_cache[cache_key] = data
        self.cache_metadata[cache_key] = metadata
        
        # Store persistently
        cache_path = self._get_cache_path(cache_key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
                pickle.dump(metadata, f)
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def invalidate(self, query_key: str, params: Dict = None) -> None:
        """Invalidate specific cache entry"""
        cache_key = self._generate_cache_key(query_key, params)
        
        # Remove from memory
        if cache_key in self.memory_cache:
            del self.memory_cache[cache_key]
        if cache_key in self.cache_metadata:
            del self.cache_metadata[cache_key]
        
        # Remove persistent cache
        cache_path = self._get_cache_path(cache_key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all cache entries matching pattern"""
        keys_to_remove = []
        for cache_key, metadata in self.cache_metadata.items():
            if pattern in metadata['query_key']:
                keys_to_remove.append(cache_key)
        
        for key in keys_to_remove:
            cache_path = self._get_cache_path(key)
            if os.path.exists(cache_path):
                os.remove(cache_path)
            if key in self.memory_cache:
                del self.memory_cache[key]
            if key in self.cache_metadata:
                del self.cache_metadata[key]
    
    def clear_all(self) -> None:
        """Clear all cache"""
        self.memory_cache.clear()
        self.cache_metadata.clear()
        
        # Remove all cache files
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.cache'):
                os.remove(os.path.join(self.cache_dir, filename))
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.stats,
            'hit_rate': f"{hit_rate:.1f}%",
            'total_requests': total_requests,
            'cache_size': len(self.memory_cache)
        }

class SmartQuery:
    """React Query-like data fetching with caching"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.loading_states = {}
        self.error_states = {}
    
    def use_query(
        self,
        query_key: str,
        query_fn: Callable,
        params: Dict = None,
        stale_time: int = 300,
        cache_time: int = 600,
        retry: int = 3,
        enabled: bool = True,
        background_refetch: bool = True
    ) -> Dict:
        """
        React Query-like data fetching hook
        
        Args:
            query_key: Unique key for the query
            query_fn: Function to fetch data
            params: Parameters for the query
            stale_time: Time before data is considered stale (seconds)
            cache_time: Time to keep data in cache (seconds)
            retry: Number of retry attempts
            enabled: Whether query should run
            background_refetch: Whether to refetch in background when stale
        
        Returns:
            Dict with data, loading, error, and helper functions
        """
        if not enabled:
            return {
                'data': None,
                'loading': False,
                'error': None,
                'is_stale': False,
                'refetch': lambda: None,
                'invalidate': lambda: None
            }
        
        cache_key = f"{query_key}_{hash(str(params))}"
        
        # Check if currently loading
        is_loading = self.loading_states.get(cache_key, False)
        
        # Get cached data
        cached_data = self.cache.get(query_key, params, stale_time)
        is_stale = cached_data is not None and self.cache._is_stale(
            self.cache._generate_cache_key(query_key, params), stale_time
        )
        
        # Get error state
        error = self.error_states.get(cache_key)
        
        def fetch_data(background: bool = False):
            """Fetch data with error handling and retries"""
            if not background:
                self.loading_states[cache_key] = True
                if cache_key in self.error_states:
                    del self.error_states[cache_key]
            
            for attempt in range(retry + 1):
                try:
                    # Show progress for main requests
                    if not background and attempt == 0:
                        with st.spinner(f"Loading {query_key}..."):
                            data = query_fn(params) if params else query_fn()
                    else:
                        data = query_fn(params) if params else query_fn()
                    
                    # Cache the data
                    self.cache.set(query_key, data, params, cache_time)
                    
                    # Clear loading state
                    if cache_key in self.loading_states:
                        del self.loading_states[cache_key]
                    if cache_key in self.error_states:
                        del self.error_states[cache_key]
                    
                    if background:
                        self.cache.stats['background_updates'] += 1
                    
                    return data
                    
                except Exception as e:
                    if attempt == retry:
                        # Final attempt failed
                        self.error_states[cache_key] = str(e)
                        if cache_key in self.loading_states:
                            del self.loading_states[cache_key]
                        
                        if not background:
                            st.error(f"Failed to load {query_key}: {str(e)}")
                    else:
                        # Wait before retry
                        time.sleep(0.5 * (attempt + 1))
            
            return None
        
        # Determine what to do
        if cached_data is None:
            # No cached data - fetch immediately
            if not is_loading:
                data = fetch_data()
                return {
                    'data': data,
                    'loading': False,
                    'error': self.error_states.get(cache_key),
                    'is_stale': False,
                    'refetch': lambda: fetch_data(),
                    'invalidate': lambda: self.cache.invalidate(query_key, params)
                }
            else:
                # Currently loading
                return {
                    'data': None,
                    'loading': True,
                    'error': None,
                    'is_stale': False,
                    'refetch': lambda: fetch_data(),
                    'invalidate': lambda: self.cache.invalidate(query_key, params)
                }
        
        else:
            # Have cached data
            if is_stale and background_refetch and not is_loading:
                # Background refresh
                threading.Thread(
                    target=lambda: fetch_data(background=True),
                    daemon=True
                ).start()
            
            return {
                'data': cached_data,
                'loading': is_loading,
                'error': self.error_states.get(cache_key),
                'is_stale': is_stale,
                'refetch': lambda: fetch_data(),
                'invalidate': lambda: self.cache.invalidate(query_key, params)
            }
    
    def use_mutation(self, mutation_fn: Callable, on_success: Callable = None, on_error: Callable = None):
        """
        React Query-like mutation hook
        
        Args:
            mutation_fn: Function to perform mutation
            on_success: Callback on successful mutation
            on_error: Callback on error
        
        Returns:
            Dict with mutate function and states
        """
        mutation_key = f"mutation_{id(mutation_fn)}"
        
        def mutate(variables: Any = None):
            """Perform mutation"""
            self.loading_states[mutation_key] = True
            if mutation_key in self.error_states:
                del self.error_states[mutation_key]
            
            try:
                with st.spinner("Processing..."):
                    result = mutation_fn(variables) if variables is not None else mutation_fn()
                
                if on_success:
                    on_success(result, variables)
                
                if mutation_key in self.loading_states:
                    del self.loading_states[mutation_key]
                
                return result
                
            except Exception as e:
                self.error_states[mutation_key] = str(e)
                if mutation_key in self.loading_states:
                    del self.loading_states[mutation_key]
                
                if on_error:
                    on_error(e, variables)
                else:
                    st.error(f"Operation failed: {str(e)}")
                
                return None
        
        return {
            'mutate': mutate,
            'loading': self.loading_states.get(mutation_key, False),
            'error': self.error_states.get(mutation_key)
        }

# Global cache manager instance
_cache_manager = None
_smart_query = None

def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager

def get_smart_query() -> SmartQuery:
    """Get global smart query instance"""
    global _smart_query
    if _smart_query is None:
        _smart_query = SmartQuery(get_cache_manager())
    return _smart_query

# Convenience functions for Streamlit apps
def use_query(query_key: str, query_fn: Callable, **kwargs):
    """Convenient use_query for Streamlit apps"""
    return get_smart_query().use_query(query_key, query_fn, **kwargs)

def use_mutation(mutation_fn: Callable, **kwargs):
    """Convenient use_mutation for Streamlit apps"""
    return get_smart_query().use_mutation(mutation_fn, **kwargs)

def invalidate_query(query_key: str, params: Dict = None):
    """Invalidate specific query cache"""
    get_cache_manager().invalidate(query_key, params)

def invalidate_queries(pattern: str):
    """Invalidate queries matching pattern"""
    get_cache_manager().invalidate_pattern(pattern)

def clear_cache():
    """Clear all cache"""
    get_cache_manager().clear_all()

def get_cache_stats():
    """Get cache statistics"""
    return get_cache_manager().get_stats()

# Cache decorators for easy use
def cached_query(query_key: str, stale_time: int = 300, cache_time: int = 600):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            params = {'args': args, 'kwargs': kwargs}
            result = use_query(
                query_key,
                lambda p: func(*p['args'], **p['kwargs']),
                params=params,
                stale_time=stale_time,
                cache_time=cache_time
            )
            return result['data']
        return wrapper
    return decorator

# Example usage functions
def example_usage():
    """Example usage of the caching system"""
    st.title("🚀 Performance Caching System")
    
    # Weather data query
    weather_query = use_query(
        "weather_data",
        lambda: fetch_weather_data(),
        stale_time=300,  # 5 minutes
        cache_time=600   # 10 minutes
    )
    
    if weather_query['loading']:
        st.spinner("Loading weather data...")
    elif weather_query['error']:
        st.error(f"Error: {weather_query['error']}")
    elif weather_query['data']:
        st.success("Weather data loaded!")
        if weather_query['is_stale']:
            st.info("Data is updating in background...")
        
        # Display data
        st.json(weather_query['data'])
        
        # Refresh button
        if st.button("Refresh Weather"):
            weather_query['refetch']()
    
    # Field data mutation
    field_mutation = use_mutation(
        lambda field_data: add_field_to_database(field_data),
        on_success=lambda result, variables: invalidate_queries("field"),
        on_error=lambda error, variables: st.error(f"Failed to add field: {error}")
    )
    
    # Add field form
    with st.form("add_field"):
        field_name = st.text_input("Field Name")
        if st.form_submit_button("Add Field"):
            field_mutation['mutate']({'name': field_name})
    
    # Cache statistics
    if st.button("Show Cache Stats"):
        stats = get_cache_stats()
        st.json(stats)

def fetch_weather_data():
    """Mock weather data fetch"""
    time.sleep(1)  # Simulate API call
    return {
        'temperature': 25.5,
        'humidity': 65,
        'condition': 'Sunny',
        'timestamp': datetime.now().isoformat()
    }

def add_field_to_database(field_data):
    """Mock field addition"""
    time.sleep(0.5)  # Simulate database operation
    return {'id': 123, 'name': field_data['name'], 'status': 'added'}

if __name__ == "__main__":
    example_usage()
