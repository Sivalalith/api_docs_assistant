from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.ai.pipeline import Pipeline

import uuid

UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".yaml",
    ".yml",
    ".json",
}

MAX_FILES = 5
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_TOTAL_SIZE = 25 * 1024 * 1024  # 25 MB

class UploadService:

    @staticmethod
    async def upload_documents(files: list[UploadFile]):
        
        # Validate number of files
        if len(files) > MAX_FILES:
            raise HTTPException(
                status_code=413,
                detail=f"Maximum {MAX_FILES} files can be uploaded at once.",
            )
            
        # Validate file sizes before processing anything
        total_size = 0
            
        for file in files:
            file.file.seek(0, 2)
            file_size = file.file.tell()
            file.file.seek(0)

            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"{file.filename} exceeds the maximum file size of 10 MB.",
                )

            total_size += file_size

        if total_size > MAX_TOTAL_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Total upload size cannot exceed 25 MB.",
            )


        UPLOAD_DIR.mkdir(exist_ok=True)

        uploaded_files = []
        
        pipeline = Pipeline()

        for file in files:

            extension = Path(file.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file.filename}",
                )

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
                
            except Exception as error:
                print(f"Failed to process {file.filename}: {error}")
                
            finally:
                destination.unlink(missing_ok=True)

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files,
        }