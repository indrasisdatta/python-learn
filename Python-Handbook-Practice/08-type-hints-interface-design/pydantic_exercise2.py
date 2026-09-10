# ============================================================
# Exercise — RAG Response Model using Pydantic
# ============================================================
# Create a RAGResponse model with:
# - question: required str, minimum 3 chars
# - answer: required str, minimum 1 char
# - sources: required list of objects containing document_id (str) and score (float 0–1)
# - tokens_used: required int >= 0
#
# 1. @model_validator:
#    If sources=[] then answer must indicate that information could not be found.
#    Example valid: "I could not find relevant information."
#    Example invalid: "Customers can request a refund within 30 days."
#
# 2. @computed_field:
#    Add source_count that returns len(sources). Do not store it as an input field.
#
# 3. Serialization:
#    Create a valid RAGResponse and use model_dump() and model_dump_json().
#    Check whether source_count is included in the serialized output.
#
# Test:
# - Valid response with 2 sources
# - Invalid response with sources=[] and a normal answer
# - Valid response with sources=[] and "not found" answer
# - Invalid source score (e.g. 1.5)
#
# Concepts: nested models, @model_validator, @computed_field, model_dump(),
# model_dump_json(), serialization, validation errors.

from pydantic import BaseModel, Field, ValidationError, computed_field, model_validator
from typing import Annotated

class Source(BaseModel):
    document_id: Annotated[str, Field(description="Document ID")]
    score: Annotated[float, Field(ge=0, le=1)]

class RAGResponse(BaseModel):
    question: Annotated[str, Field(min_length=3)]
    answer: Annotated[str, Field(min_length=1)]
    sources: Annotated[list[Source], Field(description="Sources")]
    tokens_used: Annotated[int, Field(ge=0, description="Tokens used")]

    @computed_field
    @property
    def source_count(self) -> int:
        return len(self.sources)

    @model_validator(mode="after")
    def validate_source_answer(self):
        if not self.sources and "could not find" not in self.answer.lower():
            raise ValueError("Answer must indicate that no relevant answer was found")
        return self


# Test 1 — Valid response with 2 sources
response = RAGResponse(
    question="What is the refund policy?",
    answer="Customers can request a refund within 30 days.",
    sources=[
        {"document_id": "policy_001", "score": 0.92},
        {"document_id": "terms_003", "score": 0.81}
    ],
    tokens_used=450
)
print("Test 1:", response)
print("Source count:", response.source_count)


# Test 2 — Invalid: no sources but normal answer
try:
    response = RAGResponse(
        question="What is the refund policy?",
        answer="Customers can request a refund within 30 days.",
        sources=[],
        tokens_used=450
    )
except ValidationError as e:
    print("Test 2:", e.errors())


# Test 3 — Valid: no sources + not-found answer
response = RAGResponse(
    question="What is the refund policy?",
    answer="I could not find relevant information.",
    sources=[],
    tokens_used=100
)
print("Test 3:", response)
print("Source count:", response.source_count)


# Test 4 — Invalid source score
try:
    response = RAGResponse(
        question="What is the refund policy?",
        answer="Customers can request a refund within 30 days.",
        sources=[
            {"document_id": "policy_001", "score": 1.5}
        ],
        tokens_used=450
    )
except ValidationError as e:
    print("Test 4:", e.errors())