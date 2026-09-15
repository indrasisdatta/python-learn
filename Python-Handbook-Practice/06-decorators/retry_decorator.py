"""
Implement @retry(attempts=3) that catches only a supplied exception type.
"""

from functools import wraps

def retry(attempts, exception_type):
    
    def retry_api(func):  

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(1, attempts+1):
                try:
                    print(f"Attempt: {attempt}")
                    return func(*args, **kwargs)
                except exception_type as e: 
                    print(f"Retry exception: {e}")    
                    if attempt == attempts:
                        raise

        return wrapper

    return retry_api 

@retry(attempts=3, exception_type=ConnectionError)
def fetch_users():
    print("Fetch users...")
    raise ConnectionError("API timed out")

#retry(3)(retry_api)(fetch_users)

print(fetch_users())