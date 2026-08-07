import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")


class DocumentService:

    @staticmethod
    async def get_documents():
        documents = []

        if not UPLOAD_DIR.exists():
            return documents

        for file_ in UPLOAD_DIR.iterdir():

            if not file_.is_file():
                continue

            extension = file_.suffix.lower()

            file_types = {
                ".pdf": "PDF",
                ".yaml": "YAML",
                ".yml": "YAML",
                ".json": "JSON",
            }

            size = file_.stat().st_size

            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"

            documents.append(
                {
                    "id": str(uuid.uuid5(uuid.NAMESPACE_URL, file_.name)),
                    "name": file_.name,
                    "type": file_types.get(extension, "Unknown"),
                    "size": size_str,
                }
            )

        return documents

    @staticmethod
    async def delete_document(document_id: str):

        if not UPLOAD_DIR.exists():
            return {
                "message": "Uploads folder not found."
            }

        for file_ in UPLOAD_DIR.iterdir():

            if not file_.is_file():
                continue

            file_uuid = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    file_.name,
                )
            )

            if file_uuid == document_id:

                file_.unlink()

                return {
                    "message": f"{file_.name} deleted successfully."
                }

        return {
            "message": "Document not found."
        }