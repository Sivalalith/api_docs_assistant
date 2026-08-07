from pathlib import Path
from fastapi import UploadFile

from app.parsers.parser_factory import ParserFactory

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
                
            raw_text = ParserFactory.parse(destination)

            print("\n========== Extracted Text ==========\n")
            print(raw_text)
            print("\n====================================\n")

            uploaded_files.append(file.filename)

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files,
        }