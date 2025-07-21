"""
Retry logic and rate limiting utilities for translation services.

This module provides robust retry mechanisms with exponential backoff
to handle rate limits from Google Translate and OpenAI APIs.
"""

import time
import random
import logging
from typing import Callable, Any, Type, Union, List
from functools import wraps

# Standard error types that indicate rate limiting
RATE_LIMIT_ERRORS = [
    "rate limit",
    "too many requests", 
    "quota exceeded",
    "429",
    "rate_limit_exceeded",
    "requests per minute",
    "requests per day",
    "insufficient_quota"
]

# OpenAI specific error handling
try:
    from openai import OpenAI, RateLimitError, APIError
    OPENAI_RATE_LIMIT_EXCEPTIONS = (RateLimitError,)
    OPENAI_RETRY_EXCEPTIONS = (RateLimitError, APIError)
except ImportError:
    OPENAI_RATE_LIMIT_EXCEPTIONS = ()
    OPENAI_RETRY_EXCEPTIONS = ()

# Google Translate error handling - deep_translator may raise various exceptions
GOOGLE_RATE_LIMIT_EXCEPTIONS = (Exception,)  # Will be filtered by error message content


class RateLimitTracker:
    """
    Tracks rate limit violations and applies exponential delays.
    """
    
    def __init__(self):
        self.consecutive_rate_limits = 0
        self.last_rate_limit_time = 0
        self.base_delay = 1.0  # Base delay in seconds
        self.max_delay = 300.0  # Maximum delay of 5 minutes
        
    def is_rate_limit_error(self, error: Exception) -> bool:
        """
        Determine if an error is related to rate limiting.
        """
        error_str = str(error).lower()
        
        # Check for OpenAI specific rate limit errors
        if OPENAI_RATE_LIMIT_EXCEPTIONS and isinstance(error, OPENAI_RATE_LIMIT_EXCEPTIONS):
            return True
            
        # Check for rate limit keywords in error message
        return any(keyword in error_str for keyword in RATE_LIMIT_ERRORS)
    
    def calculate_delay(self) -> float:
        """
        Calculate delay based on consecutive rate limit errors.
        Uses exponential backoff with jitter.
        """
        if self.consecutive_rate_limits == 0:
            return 0
            
        # Exponential backoff: base_delay * 2^(consecutive_rate_limits - 1)
        delay = self.base_delay * (2 ** (self.consecutive_rate_limits - 1))
        
        # Cap at maximum delay
        delay = min(delay, self.max_delay)
        
        # Add jitter (±25% randomness) to avoid thundering herd
        jitter = delay * 0.25 * (2 * random.random() - 1)
        final_delay = delay + jitter
        
        return max(0, final_delay)
    
    def record_rate_limit(self):
        """Record a rate limit error occurrence."""
        self.consecutive_rate_limits += 1
        self.last_rate_limit_time = time.time()
        
    def record_success(self):
        """Record a successful operation (resets consecutive count)."""
        self.consecutive_rate_limits = 0
        
    def should_apply_preventive_delay(self) -> bool:
        """
        Check if we should apply a preventive delay based on recent rate limits.
        """
        if self.consecutive_rate_limits == 0:
            return False
            
        # Apply preventive delay if we had rate limits in the last 5 minutes
        time_since_last_rate_limit = time.time() - self.last_rate_limit_time
        return time_since_last_rate_limit < 300  # 5 minutes
        
    def get_preventive_delay(self) -> float:
        """
        Get a smaller preventive delay to avoid triggering rate limits.
        """
        if not self.should_apply_preventive_delay():
            return 0
            
        # Use a smaller delay for prevention (1/4 of the retry delay)
        base_preventive_delay = self.calculate_delay() / 4
        return min(base_preventive_delay, 10.0)  # Cap at 10 seconds for prevention


def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
    rate_limit_tracker: RateLimitTracker = None
):
    """
    Decorator that implements retry logic with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exceptions: Exception types to catch and retry on
        rate_limit_tracker: Optional rate limit tracker instance
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            tracker = rate_limit_tracker or RateLimitTracker()
            
            for attempt in range(max_retries + 1):
                try:
                    # Apply preventive delay if we've had recent rate limits
                    if attempt == 0 and tracker.should_apply_preventive_delay():
                        preventive_delay = tracker.get_preventive_delay()
                        if preventive_delay > 0:
                            print(f"⏳ Applying preventive delay: {preventive_delay:.1f}s to avoid rate limits")
                            time.sleep(preventive_delay)
                    
                    result = func(*args, **kwargs)
                    
                    # Record success to reset rate limit tracking
                    tracker.record_success()
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    
                    # Check if this is a rate limit error
                    is_rate_limit = tracker.is_rate_limit_error(e)
                    
                    if is_rate_limit:
                        tracker.record_rate_limit()
                        
                    if attempt >= max_retries:
                        break
                        
                    # Calculate delay for this attempt
                    if is_rate_limit:
                        # Use tracker's exponential backoff for rate limits
                        delay = tracker.calculate_delay()
                    else:
                        # Standard exponential backoff for other errors
                        delay = base_delay * (2 ** attempt)
                        delay = min(delay, max_delay)
                        # Add small jitter
                        jitter = delay * 0.1 * (2 * random.random() - 1)
                        delay = max(0, delay + jitter)
                    
                    error_type = "rate limit" if is_rate_limit else "error"
                    print(f"🔄 {error_type.capitalize()} detected (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
                    
                    if delay > 0:
                        print(f"⏳ Waiting {delay:.1f}s before retry...")
                        time.sleep(delay)
            
            # All retries exhausted
            raise last_exception
            
        return wrapper
    return decorator


class TranslationRateLimiter:
    """
    Global rate limiter for translation services to coordinate delays.
    """
    
    def __init__(self):
        self.google_tracker = RateLimitTracker()
        self.openai_tracker = RateLimitTracker()
        
    def get_tracker(self, service: str) -> RateLimitTracker:
        """Get the appropriate rate limit tracker for a service."""
        if service.lower() == 'openai':
            return self.openai_tracker
        elif service.lower() == 'google':
            return self.google_tracker
        else:
            # Default tracker for unknown services
            return RateLimitTracker()
    
    def apply_service_delay(self, service: str):
        """Apply any necessary preventive delays for a service."""
        tracker = self.get_tracker(service)
        if tracker.should_apply_preventive_delay():
            delay = tracker.get_preventive_delay()
            if delay > 0:
                print(f"⏳ Applying {service} preventive delay: {delay:.1f}s")
                time.sleep(delay)


# Global rate limiter instance
global_rate_limiter = TranslationRateLimiter()


def create_retry_decorator(service: str, max_retries: int = 3):
    """
    Create a retry decorator configured for a specific translation service.
    
    Args:
        service: Service name ('google' or 'openai')
        max_retries: Maximum number of retry attempts
    """
    tracker = global_rate_limiter.get_tracker(service)
    
    if service.lower() == 'openai' and OPENAI_RETRY_EXCEPTIONS:
        exceptions = OPENAI_RETRY_EXCEPTIONS
    else:
        exceptions = Exception
        
    return retry_with_exponential_backoff(
        max_retries=max_retries,
        base_delay=1.0,
        max_delay=300.0,  # 5 minutes max
        exceptions=exceptions,
        rate_limit_tracker=tracker
    )
