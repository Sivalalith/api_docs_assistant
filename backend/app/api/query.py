from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("", response_model=QueryResponse)
def query(request: QueryRequest):
    
    print(request.question)
    
    return QueryResponse(
        endpoint="POST /login",
        headers="Authorization: Bearer <token>",
        description="Dummy AI response.",
        code="""{
  "email":"user@example.com",
  "password":"password123"
}""",
    )