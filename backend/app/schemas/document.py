from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    name: str
    type: str
    size: str


class UploadResponse(BaseModel):
    message: str