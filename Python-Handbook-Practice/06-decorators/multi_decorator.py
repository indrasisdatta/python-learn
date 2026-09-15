"""
Stack two decorators and write down the decoration order and 
call order before running it.

Decorators are applied bottom to top:
    view_profile = logger(is_admin(view_profile))

Call order is top to bottom:
    logger -> is_admin -> original function 
"""

from functools import wraps

def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling logger function {func}")
        value = func(*args, **kwargs)
        print(f"Logging done...")
        return value
    
    return wrapper


def is_admin(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if (args[0]['role'] != 'admin'):
            raise Exception("Unauthorized access")

        print("Access granted")
        
        return func(*args, **kwargs)
    
    return wrapper

@logger 
@is_admin 
def view_profile(user):
    return f"{user['name']} profile"


print(view_profile({ "name": "John", "role": "admin" }))