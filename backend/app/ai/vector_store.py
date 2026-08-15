import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

from qdrant_client.models import PointStruct
import uuid

load_dotenv()

class VectorStore:

    COLLECTION_NAME = "api_docs"

    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
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
            collection_name=self.COLLECTION_NAME,
            points=points,
            )