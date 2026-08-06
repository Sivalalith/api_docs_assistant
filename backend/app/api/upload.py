from fastapi import APIRouter

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
def upload_documents():
    return {
        "message": "Upload endpoint working"
    }