from pathlib import Path

from app.ai.vector_store import get_vector_store


FILE_TYPE_LABELS = {
    ".pdf": "PDF",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
}


def _format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


class DocumentService:

    @staticmethod
    async def get_documents():
        vector_store = get_vector_store()
        records = vector_store.list_documents()

        documents = []

        for record in records:
            file_name = record.get("file_name", "Unknown")
            extension = Path(file_name).suffix.lower()

            documents.append(
                {
                    "id": record.get("doc_id"),
                    "name": file_name,
                    "type": FILE_TYPE_LABELS.get(extension, "Unknown"),
                    "size": _format_size(record.get("file_size", 0)),
                    "uploaded_at": record.get("uploaded_at"),
                }
            )

        return documents

    @staticmethod
    async def delete_document(document_id: str):
        vector_store = get_vector_store()

        try:
            vector_store.delete_document(document_id)
        except Exception as error:
            return {"message": f"Failed to delete document: {error}"}

        return {"message": "Document deleted successfully."}