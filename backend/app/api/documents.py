from fastapi import APIRouter
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentResponse])
async def get_documents():
    return await DocumentService.get_documents()


@router.delete("/{document_id}")
def delete_document(document_id: int):
    return DocumentService.delete_document(document_id)