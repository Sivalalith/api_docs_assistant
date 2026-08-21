from fastapi import APIRouter, File, UploadFile, Request
from app.schemas.document import UploadResponse
from app.services.upload_service import UploadService
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("", response_model=UploadResponse)
@limiter.limit("5/minute")
async def upload_documents(
    request: Request,
    files: list[UploadFile] = File(...)
):
    return await UploadService.upload_documents(files)