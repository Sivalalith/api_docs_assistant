from app.parsers.parser_factory import ParserFactory
from app.ai.chunker import GenericChunker
from app.ai.embedder import Embedder
from app.ai.vector_store import VectorStore, get_vector_store
from app.ai.prompt_builder import PromptBuilder
from app.ai.llm_client import LLMClient

class Pipeline:

    def __init__(self, vector_store: VectorStore = None):
        self.parser = ParserFactory()
        self.chunker = GenericChunker()
        self.embedder = Embedder()
        self.vector_store = vector_store or get_vector_store()
        self.llm_client = LLMClient()

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
        
        # 6. Store document metadata in Qdrant
        self.vector_store.add_document_metadata(
            doc_id=doc_id,
            file_name=file_path.name,
            file_size=file_path.stat().st_size,
        )

        return {
            "doc_id": doc_id,
            "chunk_count": len(chunks),
        }
    
    def remove_document(self, doc_id: str):
        self.vector_store.delete_document(doc_id)
        
    def answer_query(self, query: str, limit: int = 3):
        # 1. Embed query
        query_vector = self.embedder.embed([query])[0]

        # 2. Retrieve relevant chunks
        results = self.vector_store.search_documents(
            query_vector=query_vector,
            limit=limit,
        )

        # 3. Build prompts
        system_prompt, user_prompt = PromptBuilder.build(
            query=query,
            retrieved_chunks=results,
        )
        
        # 4. Generate answer
        answer = self.llm_client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return answer