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
        try:
            collections = self.client.get_collections().collections
        except Exception as error:
            raise RuntimeError(
                f"Failed to reach Qdrant while checking collections: {error}"
            ) from error


        return any(
            collection.name == collection_name
            for collection in collections
        )
    
    def _ensure_chunks_collection(self):
        if self._collection_exists(self.CHUNKS_COLLECTION_NAME):
            return
        try:
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
        except Exception as error:
            raise RuntimeError(
                f"Failed to create/initialize '{self.CHUNKS_COLLECTION_NAME}' "
                f"collection: {error}"
            ) from error    
        

    def _ensure_documents_collection(self):
        if self._collection_exists(self.DOCUMENTS_COLLECTION_NAME):
            return

        try:
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
        except Exception as error:
            raise RuntimeError(
                f"Failed to create/initialize '{self.DOCUMENTS_COLLECTION_NAME}' "
                f"collection: {error}"
            ) from error

        
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

        try:
            self.client.upsert(
                collection_name=self.CHUNKS_COLLECTION_NAME,
                points=points,
            )
        except Exception as error:
            raise RuntimeError(
                f"Failed to upsert {len(points)} chunk(s) into "
                f"'{self.CHUNKS_COLLECTION_NAME}': {error}"
            ) from error
            
    def search_documents(
    self,
    query_vector: list[float],
    limit: int = 3,
):
        results = self.client.query_points(
            collection_name=self.CHUNKS_COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        return results.points
    
    def add_document_metadata(
    self,
    doc_id: str,
    file_name: str,
    file_size: int,
):
        try:
            self.client.upsert(
                collection_name=self.DOCUMENTS_COLLECTION_NAME,
                points=[
                    PointStruct(
                        id=doc_id,
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
        except Exception as error:
            raise RuntimeError(
                f"Failed to store metadata for doc_id={doc_id}: {error}"
            ) from error
        
    def list_documents(self):
        try:
            records, _ = self.client.scroll(
                collection_name=self.DOCUMENTS_COLLECTION_NAME,
                limit=1000,
                with_payload=True,
            )
        except Exception as error:
            raise RuntimeError(
                f"Failed to list documents: {error}"
            ) from error

        return [record.payload for record in records]
    
    def delete_document(self, doc_id: str):
        try:
            self.client.delete(
                collection_name=self.CHUNKS_COLLECTION_NAME,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="doc_id",
                            match=MatchValue(value=doc_id),
                        )
                    ]
                ),
            )
            self.client.delete(
                collection_name=self.DOCUMENTS_COLLECTION_NAME,
                points_selector=[doc_id],
            )
        except Exception as error:
            raise RuntimeError(
                f"Failed to delete document doc_id={doc_id}: {error}"
            ) from error

        self.client.delete(
            collection_name=self.DOCUMENTS_COLLECTION_NAME,
            points_selector=[doc_id],
        )
    
# Singleton accessor — VectorStore's __init__ does network calls (Qdrant
# client setup + collection-existence checks), so it should only run once
# per process, not once per request/upload.
_vector_store_instance: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance