# ============================================================
# Exercise — RAG Query Request Validation using Pydantic
# ============================================================
#
# Create a Pydantic model called RAGQueryRequest for a RAG API.
#
# The API receives data like:
#
# {
#     "question": "What is the refund policy?",
#     "top_k": 5,
#     "session_id": "abc123",
#     "filters": {
#         "category": "policies",
#         "language": "en"
#     }
# }
#
#
# REQUIREMENTS
# ------------------------------------------------------------
#
# 1. question
#    - Required
#    - Must be a string
#    - Minimum 3 characters
#
# 2. top_k
#    - Optional
#    - Default value = 5
#    - Must be between 1 and 20
#
# 3. session_id
#    - Required
#    - Must be a string
#
# 4. filters
#    - Optional
#    - Should be a dictionary/object
#    - category is optional
#    - language is optional
#
#
# CONCEPTS TO PRACTICE
# ------------------------------------------------------------
#
# - BaseModel
# - Required vs optional fields
# - Default values
# - Nested Pydantic models
# - Field constraints
# - Runtime validation
# - Validation errors
# - Custom validation
#
# Try to solve it without looking at the answer first.
#```

from pydantic import BaseModel, Field, field_validator 
from typing import Annotated
from typing import Optional 

class QueryFilter(BaseModel):
    category: Annotated[str | None, Field(description="Category")] = None 
    language: Annotated[str | None, Field(description="Language")] = None

class RAGQueryRequest(BaseModel):
    question: Annotated[
        str, 
        Field(min_length=3, description="Minimum 3 characters")
    ]
    top_k: Annotated[
        Optional[int], 
        Field(default=5, ge=1, le=20, description="Must be between 1 and 20")
    ]
    session_id: Annotated[
        str, 
        Field(min_length=3, description="Must be a string")
    ]
    filters: Annotated[
        Optional[QueryFilter], 
        Field(description="Filters")
    ] = None

    @field_validator('question', mode='before')
    @classmethod
    def strip_question(cls, value):
        if isinstance(value, str):
            return value.strip()
        return value


# TEST CASE 1 — Valid request
# ------------------------------------------------------------
print("TEST CASE 1 — Valid request")

request = RAGQueryRequest(
    question="What is the refund policy?",
    session_id="abc123"
)
print(request)

# TEST CASE 2 — Invalid: question is too short
# ------------------------------------------------------------
print("\nTEST CASE 2 — Invalid: question is too short")

try:
    request = RAGQueryRequest(
        question="Hi",
        session_id="abc123"
    )
except ValueError as e:
    print(e.errors())
else:
    print(request)

# TEST CASE 3 — Invalid: top_k is too high
# ------------------------------------------------------------
print("\nTEST CASE 3 — Invalid: top_k is too high")

try:
    request = RAGQueryRequest(
        question="What is the refund policy?",
        top_k=50,
        session_id="abc123"
    )
except ValueError as e:
    print(e.errors())
else:
    print(request)

# TEST CASE 4 — Invalid: session_id is missing
# ------------------------------------------------------------
print("\nTEST CASE 4 — Invalid: session_id is missing")

try:
    request = RAGQueryRequest(
        question="What is the refund policy?"
    )
except ValueError as e:
    print(e.errors())
else:
    print(request)

# Add validation so that leading/trailing whitespace is removed
# from question.
#
# Example: "   What is the refund policy?   "
#           should become: "What is the refund policy?"

print("\nAdd validation so that leading/trailing whitespace is removed")

try:
    request = RAGQueryRequest(
        question="   What is the refund policy?   ",
        session_id="sess123"
    )
except ValueError as e:
    print(e.errors())
else:
    print(request)