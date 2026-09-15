"""
Decorator: 
function which takes another function, adds some behavior and returns new function 
"""

from functools import wraps

def logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Obtained inputs: {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"Done")
        return result 

    return wrapper

@logger
def add(num1, num2):
    """ Adds two numbers """
    return num1 + num2 

# Without decorator
# add_result = logger(add)
# print(add_result(5, 7))

print(add(5, 7))

# Original add function metadata is not preserved (name, doc) 
# To preserve, use functools.wrap
print(add.__name__)
print(add.__doc__)
