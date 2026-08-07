from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str # using uuid()
    name: str
    type: str
    size: str


class UploadResponse(BaseModel):
    message: str
    uploaded_files: list[str]
    
class DeleteResponse(BaseModel):
    message: str