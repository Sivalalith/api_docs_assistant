from fastapi import APIRouter, Request
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("", response_model=QueryResponse)
@limiter.limit("6/minute")
async def query(request: Request, body: QueryRequest):
    return await QueryService.query(body.query)