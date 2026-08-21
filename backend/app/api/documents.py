from fastapi import APIRouter, Request
from app.schemas.document import DocumentResponse, DeleteResponse
from app.services.document_service import DocumentService
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentResponse])
@limiter.limit("30/minute")
async def get_documents(request: Request):
    return await DocumentService.get_documents()


@router.delete("/{document_id}", response_model=DeleteResponse)
@limiter.limit("10/minute")
async def delete_document(request: Request, document_id: str):
    return await DocumentService.delete_document(document_id)