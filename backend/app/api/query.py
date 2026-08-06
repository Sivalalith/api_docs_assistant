from fastapi import APIRouter

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("")
def query():
    return {
        "endpoint": "POST /login",
        "headers": "Authorization: Bearer <token>",
        "description": "Dummy AI response.",
        "code": """{
  "email": "user@example.com",
  "password": "password123"
}"""
    }