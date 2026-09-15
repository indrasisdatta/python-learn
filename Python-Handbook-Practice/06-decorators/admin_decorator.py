"""
Write @require_role("admin") for a function receiving a user object.
"""

def require_role(role):
    def authorize(func):
        def wrapper(*args, **kwargs):   
            if (args[0]['role'] != role): 
                raise Exception("Unauthorized")
            return func(*args, **kwargs)

        return wrapper
    return authorize

@require_role("admin")
def approve_request(user):
    return f"User is authorized"


user = { "id": 1, "name": "User A", "role": "admin" }
print(approve_request(user))