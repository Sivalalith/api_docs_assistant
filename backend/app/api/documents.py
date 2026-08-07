from fastapi import APIRouter
from app.schemas.document import DocumentResponse, DeleteResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentResponse])
async def get_documents():
    return await DocumentService.get_documents()


@router.delete("/{document_id}", response_model=DeleteResponse)
async def delete_document(document_id: str):
    return await DocumentService.delete_document(document_id)