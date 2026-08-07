from fastapi import APIRouter, File, UploadFile
from app.schemas.document import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("", response_model=UploadResponse)
async def upload_documents(
    files: list[UploadFile] = File(...)
):
    return await UploadService.upload_documents(files)