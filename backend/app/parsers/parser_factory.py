from pathlib import Path

from app.parsers.pdf_parser import PDFParser
from app.parsers.openapi_parser import OpenAPIParser
from app.parsers.postman_parser import PostmanParser


class ParserFactory:

    @staticmethod
    def parse(file_path: Path):

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFParser.parse(file_path)

        if extension in [".yaml", ".yml"]:
            return OpenAPIParser.parse(file_path)

        if extension == ".json":

            import json

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if "openapi" in data or "swagger" in data:
                return OpenAPIParser.parse(file_path)

            if "info" in data and "item" in data:
                return PostmanParser.parse(file_path)

            raise ValueError(
    "Unknown JSON format. Expected OpenAPI or Postman Collection."
)

        raise ValueError(f"Unsupported file type: {extension}")