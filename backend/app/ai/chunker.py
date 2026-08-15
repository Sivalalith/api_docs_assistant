from langchain_text_splitters import RecursiveCharacterTextSplitter


class GenericChunker:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def chunk(self, documents):
        chunks = []

        for document in documents:
            text = document.get("text", "")
            metadata = document.get("metadata", {})

            if not text.strip():
                continue

            split_texts = self.splitter.split_text(text)

            for chunk_text in split_texts:
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": metadata.copy(),
                    }
                )

        return chunks