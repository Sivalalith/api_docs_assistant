from pathlib import Path

UPLOAD_DIR = Path("uploads")


class DocumentService:

    @staticmethod
    async def get_documents():
        documents = []

        if not UPLOAD_DIR.exists():
            return documents

        for index, file_ in enumerate(UPLOAD_DIR.iterdir(), start=1):

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
                    "id": index,
                    "name": file_.name,
                    "type": file_types.get(extension, "Unknown"),
                    "size": size_str,
                }
            )

        return documents

    @staticmethod
    def delete_document(document_id: int):
        return {
            "message": f"Document {document_id} deleted"
        }