from fastembed import TextEmbedding


class Embedder:

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self):
        self.model = TextEmbedding(model_name=self.MODEL_NAME)

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.embed(texts)

        return [embedding.tolist() for embedding in embeddings]