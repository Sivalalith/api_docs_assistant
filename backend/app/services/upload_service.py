from pathlib import Path
from fastapi import UploadFile

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

        for file in files:

            extension = Path(file.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                continue

            destination = UPLOAD_DIR / file.filename

            contents = await file.read()

            with open(destination, "wb") as f:
                f.write(contents)

            uploaded_files.append(file.filename)

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files,
        }