from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    endpoint: str
    headers: str
    description: str
    code: str