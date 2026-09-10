"""
Define a TypedDict for an API response with one optional field.
"""

from typing import TypedDict, NotRequired, Literal

class LoginAPIRequest(TypedDict):
    username: str 
    password: str 
    rememberMe: NotRequired[bool]

class UserType(TypedDict):
    accessToken: str 
    refreshToken: str 
    username: str 
    email: str 
    expiresAt: str

class APIResponse(TypedDict):
    status: Literal[200, 201, 301, 400, 404, 500] 
    error: str | None 
    data: UserType | None

def userLogin(request: LoginAPIRequest) -> APIResponse:
    if (request['username'] == 'admin' and request['password'] == 'admin'):
        return {
            'status': 200,
            'error': None,
            'data': {
                'accessToken': 'accessTokentest', 
                'refreshToken': 'refreshtokentest', 
                'username': 'user1', 
                'email': 'user1@example.com', 
                'expiresAt': '2026-09-20T00:00:00'
            }
        }
    
    return {
        'status': 400,
        'error': 'Invalid credentials',
        'data': None
    }

print(
    userLogin({ 'username': "admin", 'password': "admin" })
)