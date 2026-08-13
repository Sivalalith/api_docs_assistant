from pathlib import Path

import yaml


class OpenAPIParser:

    @staticmethod
    def parse(file_path: Path):
        documents = []

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        api_title = data.get("info", {}).get("title", "Unknown")
        api_version = data.get("info", {}).get("version", "Unknown")

        paths = data.get("paths", {})

        for path, path_item in paths.items():

            if not isinstance(path_item, dict):
                continue

            for method, operation in path_item.items():

                if method.lower() not in {
                    "get",
                    "post",
                    "put",
                    "patch",
                    "delete",
                    "options",
                    "head",
                    "trace",
                }:
                    continue

                if not isinstance(operation, dict):
                    continue

                method = method.upper()

                text_parts = [
                    f"API Endpoint: {method} {path}",
                    f"API: {api_title}",
                    f"Version: {api_version}",
                ]

                # Tags
                tags = operation.get("tags", [])

                if tags:
                    text_parts.append(
                        f"Tags: {', '.join(tags)}"
                    )

                # Summary
                summary = operation.get("summary")

                if summary:
                    text_parts.append(
                        f"Summary: {summary}"
                    )

                # Description
                description = operation.get("description")

                if description:
                    text_parts.append(
                        f"Description: {description}"
                    )

                # Operation ID
                operation_id = operation.get("operationId")

                if operation_id:
                    text_parts.append(
                        f"Operation ID: {operation_id}"
                    )

                # Parameters
                parameters = operation.get("parameters", [])

                if parameters:
                    text_parts.append("Parameters:")

                    for parameter in parameters:

                        if not isinstance(parameter, dict):
                            continue

                        name = parameter.get(
                            "name",
                            "Unnamed parameter"
                        )

                        location = parameter.get(
                            "in",
                            ""
                        )

                        parameter_description = parameter.get(
                            "description",
                            ""
                        )

                        required = parameter.get(
                            "required",
                            False
                        )

                        parameter_text = (
                            f"- {name} "
                            f"({location}, "
                            f"required={required})"
                        )

                        if parameter_description:
                            parameter_text += (
                                f": {parameter_description}"
                            )

                        schema = parameter.get("schema", {})

                        if schema:
                            parameter_text += (
                                f" | Schema: "
                                f"{OpenAPIParser.format_schema(schema)}"
                            )

                        text_parts.append(parameter_text)

                # Request body
                request_body = operation.get("requestBody")

                if request_body:
                    text_parts.append("Request Body:")

                    request_description = request_body.get(
                        "description"
                    )

                    if request_description:
                        text_parts.append(
                            f"Description: {request_description}"
                        )

                    content = request_body.get(
                        "content",
                        {}
                    )

                    for media_type, media_info in content.items():

                        text_parts.append(
                            f"Content-Type: {media_type}"
                        )

                        schema = media_info.get(
                            "schema",
                            {}
                        )

                        if schema:
                            text_parts.append(
                                f"Schema: "
                                f"{OpenAPIParser.format_schema(schema)}"
                            )

                # Responses
                responses = operation.get("responses", {})

                if responses:
                    text_parts.append("Responses:")

                    for status_code, response in responses.items():

                        if not isinstance(response, dict):
                            continue

                        response_description = response.get(
                            "description",
                            ""
                        )

                        response_text = (
                            f"Response {status_code}"
                        )

                        if response_description:
                            response_text += (
                                f": {response_description}"
                            )

                        text_parts.append(response_text)

                        # Response headers
                        response_headers = response.get(
                            "headers",
                            {}
                        )

                        if response_headers:
                            text_parts.append(
                                "Response Headers:"
                            )

                            for header_name, header in response_headers.items():

                                if not isinstance(header, dict):
                                    continue

                                header_description = header.get(
                                    "description",
                                    ""
                                )

                                header_text = (
                                    f"- {header_name}"
                                )

                                if header_description:
                                    header_text += (
                                        f": {header_description}"
                                    )

                                header_schema = header.get(
                                    "schema",
                                    {}
                                )

                                if header_schema:
                                    header_text += (
                                        f" | Schema: "
                                        f"{OpenAPIParser.format_schema(header_schema)}"
                                    )

                                text_parts.append(header_text)

                        # Response content
                        content = response.get(
                            "content",
                            {}
                        )

                        if content:
                            text_parts.append(
                                "Response Content:"
                            )

                            for media_type, media_info in content.items():

                                text_parts.append(
                                    f"Content-Type: {media_type}"
                                )

                                schema = media_info.get(
                                    "schema",
                                    {}
                                )

                                if schema:
                                    text_parts.append(
                                        f"Schema: "
                                        f"{OpenAPIParser.format_schema(schema)}"
                                    )

                # Security
                security = operation.get("security")

                if security:
                    text_parts.append("Security:")

                    for security_requirement in security:

                        for scheme, scopes in security_requirement.items():

                            if scopes:
                                text_parts.append(
                                    f"- {scheme}: "
                                    f"{', '.join(scopes)}"
                                )
                            else:
                                text_parts.append(
                                    f"- {scheme}"
                                )

                # Normalized document
                document = {
                    "text": "\n".join(text_parts),
                    "metadata": {
                        "source_type": "openapi_yaml",
                        "file_name": file_path.name,
                        "api_title": api_title,
                        "api_version": api_version,
                        "path": path,
                        "method": method,
                        "operation_id": operation_id,
                        "tags": tags,
                    },
                }

                documents.append(document)

        return documents

    @staticmethod
    def format_schema(schema):
        if not isinstance(schema, dict):
            return str(schema)

        if "$ref" in schema:
            return schema["$ref"]

        schema_type = schema.get("type")

        if schema_type == "array":
            items = schema.get("items", {})

            return (
                f"array of "
                f"{OpenAPIParser.format_schema(items)}"
            )

        parts = []

        if schema_type:
            parts.append(
                f"type={schema_type}"
            )

        schema_format = schema.get("format")

        if schema_format:
            parts.append(
                f"format={schema_format}"
            )

        enum = schema.get("enum")

        if enum:
            parts.append(
                f"enum={enum}"
            )

        default = schema.get("default")

        if default is not None:
            parts.append(
                f"default={default}"
            )

        return ", ".join(parts) if parts else str(schema)