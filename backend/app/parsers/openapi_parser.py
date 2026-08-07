from pathlib import Path
import json
import yaml


class OpenAPIParser:

    @staticmethod
    def parse(file_path: Path) -> str:

        extension = file_path.suffix.lower()

        with open(file_path, "r", encoding="utf-8") as file:

            if extension == ".json":
                spec = json.load(file)

            else:
                spec = yaml.safe_load(file)

        output = []

        info = spec.get("info", {})

        output.append(f"API Title: {info.get('title', 'N/A')}")
        output.append(f"Version: {info.get('version', 'N/A')}")

        if info.get("description"):
            output.append(f"Description: {info['description']}")

        output.append("")

        paths = spec.get("paths", {})

        for endpoint, methods in paths.items():

            output.append(f"Endpoint: {endpoint}")

            for method, details in methods.items():

                output.append(f"Method: {method.upper()}")

                if details.get("summary"):
                    output.append(f"Summary: {details['summary']}")

                if details.get("description"):
                    output.append(f"Description: {details['description']}")

                output.append("")

        return "\n".join(output)