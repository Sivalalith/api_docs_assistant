from pathlib import Path

import pymupdf


class PDFParser:

    @staticmethod
    def parse(file_path: Path):
        document = pymupdf.open(file_path)

        documents = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            if not text.strip():
                continue

            documents.append(
                {
                    "text": text,
                    "metadata": {
                        "source_type": "pdf",
                        "file_name": file_path.name,
                        "page": page_number,
                    },
                }
            )

        document.close()

        return documents