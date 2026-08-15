from pathlib import Path
from fastapi import UploadFile

from app.parsers.parser_factory import ParserFactory

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
                raw_text = ParserFactory.parse(destination, doc_id)

                print("\n" + "=" * 80)
                print(f"Parsed File: {file.filename}")
                print("=" * 80)
                print(raw_text)
                print("=" * 80 + "\n")
            except ValueError as error:
                print(error)
                
            uploaded_files.append(file.filename)

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files,
        }