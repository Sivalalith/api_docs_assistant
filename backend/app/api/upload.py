from fastapi import APIRouter
from app.schemas.document import UploadResponse

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("", response_model=UploadResponse)
def upload_documents():
    return UploadResponse(
        message="Upload endpoint working"
    )