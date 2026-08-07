from pathlib import Path
import fitz

class PDFParser:

    @staticmethod
    def parse(file_path: Path) -> str:
        document = fitz.open(file_path)

        extracted_text = []

        for page in document:
            extracted_text.append(page.get_text())

        document.close()

        return "\n".join(extracted_text)