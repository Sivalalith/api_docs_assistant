from pathlib import Path
from fastapi import UploadFile

from app.ai.pipeline import Pipeline

import uuid

UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".yaml",
    ".yml",
    ".json",
}

class UploadService:

    @staticmethod
    async def upload_documents(files: list[UploadFile]):

        UPLOAD_DIR.mkdir(exist_ok=True)

        uploaded_files = []
        
        pipeline = Pipeline()

        for file in files:

            extension = Path(file.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                continue

            destination = UPLOAD_DIR / file.filename

            contents = await file.read()

            with open(destination, "wb") as f:
                f.write(contents)
                
            try:
                
                doc_id = str(uuid.uuid4())
                
                pipeline.index_document(
                    destination,
                    doc_id
                )
                
                uploaded_files.append(file.filename)
                
            except ValueError as error:
                print(error)

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files,
        }