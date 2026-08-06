class DocumentService:

    @staticmethod
    def get_documents():
        return [
            {
                "id": 1,
                "name": "payment-api.pdf",
                "type": "PDF",
                "size": "2.4 MB",
            },
            {
                "id": 2,
                "name": "openapi.yaml",
                "type": "YAML",
                "size": "68 KB",
            },
        ]

    @staticmethod
    def delete_document(document_id: int):
        return {
            "message": f"Document {document_id} deleted"
        }