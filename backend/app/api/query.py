from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("", response_model=QueryResponse)
def query(request: QueryRequest):
    return QueryService.query(request.query)