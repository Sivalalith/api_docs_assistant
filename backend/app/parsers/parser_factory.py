from pathlib import Path

from app.parsers.pdf_parser import PDFParser
from app.parsers.openapi_parser import OpenAPIParser
from app.parsers.postman_parser import PostmanParser


class ParserFactory:

    @staticmethod
    def parse(file_path: Path) -> str:

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFParser.parse(file_path)

        if extension in [".yaml", ".yml"]:
            return OpenAPIParser.parse(file_path)

        if extension == ".json":

            # Temporary.
            # Later we'll detect whether
            # it's OpenAPI or Postman.

            return OpenAPIParser.parse(file_path)

        return "Unsupported file."