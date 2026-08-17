from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    endpoint: str
    headers: str
    description: str
    code: str