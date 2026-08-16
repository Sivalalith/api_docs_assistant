from app.parsers.parser_factory import ParserFactory
from app.ai.chunker import GenericChunker
from app.ai.embedder import Embedder
from app.ai.vector_store import VectorStore


class Pipeline:

    def __init__(self):
        self.parser = ParserFactory()
        self.chunker = GenericChunker()
        self.embedder = Embedder()
        self.vector_store = VectorStore()

    def index_document(self, file_path, doc_id):
        # 1. Parse
        documents = self.parser.parse(file_path, doc_id)

        # 2. Chunk
        chunks = self.chunker.chunk(documents)

        # 3. Extract text
        texts = [chunk["text"] for chunk in chunks]

        # 4. Embed
        embeddings = self.embedder.embed(texts)

        # 5. Store in Qdrant
        self.vector_store.add_documents(
            texts=texts,
            embeddings=embeddings,
            metadata=[chunk["metadata"] for chunk in chunks],
        )

        return {
            "doc_id": doc_id,
            "chunk_count": len(chunks),
        }