import re
from pathlib import Path

import pymupdf


class PDFParser:

    # repeated print-artifact boilerplate seen on every page of
    # Redoc-style PDF exports (date/time stamp, product name, source URL,
    # "X/26" page counter, and the promo banner). Each is matched as a
    # standalone line and stripped before the page text is stored.
    _BOILERPLATE_PATTERNS = [
        r"^\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}\s*[AP]M$",    # "8/15/26, 12:14 PM"
        r"^Redoc Interactive Demo$",
        r"^https?://\S+$",                                        # source URL footer line
        r"^\d+/\d+$",                                             # "1/26" page counter
        r"^A new home for Redoc is on the way\..*$",              # promo banner
    ]

    # Redoc UI action-label noise — button/toggle text that gets
    # captured as plain text when the page is printed, but carries no
    # documentation content of its own.
    _UI_NOISE_PATTERNS = [
        r"^Copy$",
        r"^Expand all$",
        r"^Collapse all$",
        r"^Content type$",
        # top nav bar chrome (repo/star badge, upload button,
        # CORS toggle, try-it button) — only appears on page 1 in this
        # dataset, but matched generically rather than page-scoped so it
        # also catches it if a future export repeats the nav per page.
        r"^Upload a file$",
        r"^CORS$",
        r"^Star$",
        r"^TRY IT$",
        # Star COUNT is a comma-grouped number (e.g. "25,878") — matched
        # by shape, not hardcoded, since the count drifts over time.
        # Status codes (200, 404, ...) never carry commas, so this can't
        # collide with them.
        r"^\d{1,3}(,\d{3})+$",
    ]

    _NOISE_RE = re.compile(
        "|".join(_BOILERPLATE_PATTERNS + _UI_NOISE_PATTERNS)
    )

    # HTTP method + path, matching Postman/OpenAPI parser's
    # "endpoint"/"method" metadata fields for cross-source consistency.
    # In this PDF format the method and path are typically rendered on two
    # consecutive lines (e.g. "PUT" then "/pet"), so the pattern spans a
    # newline; MULTILINE lets ^/$ anchor per line within the full page text.
    _ENDPOINT_RE = re.compile(
        r"(?m)^(GET|POST|PUT|DELETE|PATCH)\s*\n\s*(/\S+)\s*$"
    )

    @staticmethod
    def _clean_text(text: str) -> str:
        # drop any line that matches a boilerplate/noise
        # pattern, then collapse the resulting run of blank lines so
        # removed lines don't leave gaps of empty whitespace behind.
        lines = text.split("\n")
        kept = [
            line for line in lines
            if not PDFParser._NOISE_RE.match(line.strip())
        ]
        cleaned = "\n".join(kept)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()
        

    @staticmethod
    def _extract_endpoint(text: str):
        # best-effort extraction of method + path from the page
        # text, so PDF chunks can carry the same endpoint/method metadata
        # fields your Postman/OpenAPI parsers already provide. Returns
        # (method, path) or (None, None) if the page has no visible
        # endpoint (e.g. an overview/intro page).
        match = PDFParser._ENDPOINT_RE.search(text)
        if not match:
            return None, None
        return match.group(1), match.group(2)
       

    @staticmethod
    def parse(file_path: Path, doc_id: str):
        try:
            document = pymupdf.open(file_path)
        except Exception as exc:
            raise ValueError(f"Failed to open PDF '{file_path.name}': {exc}") from exc

        documents = []

        for page_number, page in enumerate(document, start=1):
            raw_text = page.get_text()

            if not raw_text.strip():
                continue

            # extract endpoint/method from the raw text before
            # cleaning, since cleaning only removes noise lines and doesn't
            # affect the method/path lines themselves — order doesn't
            # actually matter here, but keeping it explicit for clarity.
            method, endpoint = PDFParser._extract_endpoint(raw_text)

            text = PDFParser._clean_text(raw_text)

            if not text:
                # Page was entirely boilerplate/noise once cleaned (rare,
                # but guards against an empty chunk being created).
                continue

            documents.append(
                {
                    "text": text,
                    "metadata": {
                        "source_type": "pdf",
                        "file_name": file_path.name,
                        "page": page_number,
                        # parity fields with Postman/OpenAPI
                        # parsers — None when a page has no visible
                        # endpoint (e.g. intro/overview pages).
                        "method": method,
                        "endpoint": endpoint,
                        "doc_id":  doc_id
                    },
                }
            )

        document.close()

        return documents