import json


class PostmanParser:

    @staticmethod
    def parse(file_path):
        documents = []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        collection_name = data.get("info", {}).get("name", "Unknown")

        PostmanParser.parse_items(
            data.get("item", []),
            documents,
            collection_name
        )

        return documents

    @staticmethod
    def parse_items(
        items,
        documents,
        collection_name,
        folder_path=None
    ):
        folder_path = folder_path or []

        for item in items:

            # Folder
            if "item" in item:
                current_folder = folder_path + [
                    item.get("name", "Unnamed Folder")
                ]

                PostmanParser.parse_items(
                    item["item"],
                    documents,
                    collection_name,
                    current_folder
                )

                continue

            # Request
            if "request" not in item:
                continue

            request = item["request"]

            method = request.get("method", "GET")

            url = request.get("url", "")

            if isinstance(url, dict):
                url = url.get("raw", "")

            name = item.get("name", "Unnamed Request")

            description = request.get(
                "description",
                "No description provided."
            )

            # Searchable text
            text_parts = [
                f"API Endpoint: {method} {url}",
                f"Name: {name}",
                f"Description: {description}",
            ]

            # Headers
            headers = request.get("header", [])

            if headers:
                text_parts.append("Headers:")

                for header in headers:
                    key = header.get("key", "")
                    value = header.get("value", "")

                    text_parts.append(
                        f"{key}: {value}"
                    )

            # Request body
            body = request.get("body", {})

            if body.get("mode") == "raw":
                raw_body = body.get("raw", "")

                if raw_body:
                    text_parts.append("Request Body:")
                    text_parts.append(raw_body)

            # Responses
            responses = item.get("response", [])

            if responses:
                text_parts.append("Responses:")

                for response in responses:

                    response_name = response.get(
                        "name",
                        "Unnamed Response"
                    )

                    response_code = response.get(
                        "code",
                        ""
                    )

                    response_body = response.get(
                        "body",
                        ""
                    )

                    text_parts.append(
                        f"Response: {response_name}"
                    )

                    if response_code:
                        text_parts.append(
                            f"Status Code: {response_code}"
                        )

                    if response_body:
                        text_parts.append("Response Body:")
                        text_parts.append(response_body)

            # Document with searchable text + metadata
            document = {
                "text": "\n".join(text_parts),
                "metadata": {
                    "source_type": "postman_json",
                    "collection": collection_name,
                    "endpoint": url,
                    "method": method,
                    "name": name,
                    "folder": "/".join(folder_path),
                },
            }

            documents.append(document)