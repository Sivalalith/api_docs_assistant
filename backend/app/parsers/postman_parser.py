from pathlib import Path
import json


class PostmanParser:

    @staticmethod
    def parse(file_path: Path) -> str:

        with open(file_path, "r", encoding="utf-8") as file:
            collection = json.load(file)

        output = []

        info = collection.get("info", {})
        output.append(f"Collection: {info.get('name', 'N/A')}")
        output.append("")

        PostmanParser.parse_items(collection.get("item", []), output)

        return "\n".join(output)

    @staticmethod
    def parse_items(items, output):

        for item in items:

            # Folder
            if "item" in item:

                output.append(f"Folder: {item.get('name', 'Unnamed Folder')}")
                output.append("")

                PostmanParser.parse_items(item["item"], output)

                continue

            request = item.get("request", {})

            output.append(f"Request: {item.get('name', 'Unnamed Request')}")
            output.append(f"Method: {request.get('method', '')}")

            url = request.get("url", {})

            if isinstance(url, dict):
                output.append(f"URL: {url.get('raw', '')}")
            else:
                output.append(f"URL: {url}")

            headers = request.get("header", [])

            if headers:
                output.append("Headers:")

                for header in headers:
                    output.append(
                        f"{header.get('key', '')}: {header.get('value', '')}"
                    )

            body = request.get("body", {})

            if body.get("mode") == "raw":
                output.append("")
                output.append("Body:")
                output.append(body.get("raw", ""))

            output.append("")
            output.append("-" * 40)
            output.append("")