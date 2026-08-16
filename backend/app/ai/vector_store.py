import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

from qdrant_client.models import (Distance, PointStruct, VectorParams, Filter, FieldCondition, MatchValue)
import uuid
from datetime import datetime, timezone

load_dotenv()

class VectorStore:

    CHUNKS_COLLECTION_NAME = "api_docs"
    DOCUMENTS_COLLECTION_NAME = "api_docs_metadata"

    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        
        self._ensure_chunks_collection()
        self._ensure_documents_collection()
        
    def _collection_exists(self, collection_name: str) -> bool:
        collections = self.client.get_collections().collections

        return any(
            collection.name == collection_name
            for collection in collections
        )
    
    def _ensure_chunks_collection(self):
        if self._collection_exists(self.CHUNKS_COLLECTION_NAME):
            return

        self.client.create_collection(
            collection_name=self.CHUNKS_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )
        
        self.client.create_payload_index(
                    collection_name=self.CHUNKS_COLLECTION_NAME,
                    field_name="doc_id",
                    field_schema="keyword",
                )

    def _ensure_documents_collection(self):
        if self._collection_exists(self.DOCUMENTS_COLLECTION_NAME):
            return

        self.client.create_collection(
            collection_name=self.DOCUMENTS_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1,
                distance=Distance.COSINE,
            ),
        )

        self.client.create_payload_index(
            collection_name=self.DOCUMENTS_COLLECTION_NAME,
            field_name="doc_id",
            field_schema="keyword",
        )
        
    def add_documents(
    self,
    texts: list[str],
    embeddings: list[list[float]],
    metadata: list[dict],
):
        points = []

        for text, embedding, meta in zip(texts, embeddings, metadata):
            payload = {
            "text": text,
            **meta,
            }

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )   

        self.client.upsert(
            collection_name=self.CHUNKS_COLLECTION_NAME,
            points=points,
            )
    
    def add_document_metadata(
    self,
    doc_id: str,
    file_name: str,
    file_size: int,
):
        self.client.upsert(
        collection_name=self.DOCUMENTS_COLLECTION_NAME,
        points=[
            PointStruct(
                id=doc_id, # used 'doc_id' as id for O(1) retrieval
                vector=[0.0],
                payload={
                    "doc_id": doc_id,
                    "file_name": file_name,
                    "file_size": file_size,
                    "uploaded_at": datetime.now(timezone.utc).isoformat(),
                },
            )
        ],
    )
        
    def list_documents(self):
        records, _ = self.client.scroll(
            collection_name=self.DOCUMENTS_COLLECTION_NAME,
            limit=1000,
            with_payload=True,
        )

        return [record.payload for record in records]
    
    # TODO: delete_document()
    
# Singleton accessor — VectorStore's __init__ does network calls (Qdrant
# client setup + collection-existence checks), so it should only run once
# per process, not once per request/upload.
_vector_store_instance: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance