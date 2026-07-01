import argparse
import html
import json
import tempfile
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class EvaluationDocument:
    file_name: str
    text: str


@dataclass
class EvaluationQuery:
    query: str
    expected_file: str


DOCUMENTS = [
    EvaluationDocument(
        "qa-fastapi-openapi.docx",
        "FastAPI Swagger OpenAPI healthcheck endpoint backend validation.",
    ),
    EvaluationDocument(
        "qa-elasticsearch-analyzer.docx",
        "Elasticsearch russian analyzer multi match documents index search ranking.",
    ),
    EvaluationDocument(
        "qa-docker-compose-monitoring.docx",
        "Docker Compose backend frontend postgres redis elasticsearch prometheus grafana.",
    ),
    EvaluationDocument(
        "qa-redis-cache-ttl.docx",
        "Redis cache TTL repeated search query response optimization.",
    ),
    EvaluationDocument(
        "qa-react-vite-frontend.docx",
        "React Vite frontend drag and drop upload search pagination cards.",
    ),
    EvaluationDocument(
        "qa-parser-pdf-docx.docx",
        "PDF DOCX parser text extraction pdfplumber python docx documents.",
    ),
    EvaluationDocument(
        "qa-chunk-overlap-index.docx",
        "Chunk overlap one thousand characters metadata page number indexing.",
    ),
    EvaluationDocument(
        "qa-prometheus-grafana.docx",
        "Prometheus metrics response time Grafana dashboard monitoring.",
    ),
    EvaluationDocument(
        "qa-precision-evaluation.docx",
        "Precision at three evaluation top results reference query relevance.",
    ),
    EvaluationDocument(
        "qa-playwright-e2e.docx",
        "Playwright E2E upload indexing search results user scenario.",
    ),
]

QUERIES = [
    EvaluationQuery("FastAPI Swagger", "qa-fastapi-openapi.docx"),
    EvaluationQuery("Elasticsearch analyzer", "qa-elasticsearch-analyzer.docx"),
    EvaluationQuery("Docker Compose services", "qa-docker-compose-monitoring.docx"),
    EvaluationQuery("Redis TTL cache", "qa-redis-cache-ttl.docx"),
    EvaluationQuery("React Vite frontend", "qa-react-vite-frontend.docx"),
    EvaluationQuery("PDF DOCX parser", "qa-parser-pdf-docx.docx"),
    EvaluationQuery("chunk overlap metadata", "qa-chunk-overlap-index.docx"),
    EvaluationQuery("Prometheus Grafana metrics", "qa-prometheus-grafana.docx"),
    EvaluationQuery("Precision top results", "qa-precision-evaluation.docx"),
    EvaluationQuery("Playwright E2E scenario", "qa-playwright-e2e.docx"),
]


def create_docx(path: Path, text: str) -> None:
    escaped_text = html.escape(text)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "word/document.xml",
            f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body><w:p><w:r><w:t>{escaped_text}</w:t></w:r></w:p></w:body>
</w:document>""",
        )


def upload_document(base_url: str, path: Path) -> None:
    boundary = f"----eprac-{uuid.uuid4().hex}"
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    file_bytes = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + file_bytes + f"\r\n--{boundary}--\r\n".encode()

    request = Request(
        f"{base_url.rstrip('/')}/api/v1/documents/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        response.read()


def search(base_url: str, query: str) -> list[str]:
    params = urlencode({"q": query, "page": 1, "page_size": 3})
    url = f"{base_url.rstrip('/')}/api/v1/search?{params}"
    with urlopen(url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return [item["file_name"] for item in payload["results"][:3]]


def render_report(rows: list[dict], score: float) -> str:
    lines = [
        "# Отчёт Precision@3",
        "",
        "## Цель",
        "",
        "Проверить качество поисковой выдачи на 10 эталонных запросах.",
        "Запрос считается успешным, если ожидаемый документ попал в топ-3 результатов.",
        "",
        "## Результаты",
        "",
        "| Запрос | Ожидаемый документ | Топ-3 | Попал в топ-3 |",
        "| --- | --- | --- | --- |",
    ]

    for row in rows:
        top = ", ".join(row["top3"]) if row["top3"] else "нет результатов"
        hit = "да" if row["hit"] else "нет"
        lines.append(f"| {row['query']} | `{row['expected']}` | {top} | {hit} |")

    lines.extend(
        [
            "",
            "## Итог",
            "",
            f"Precision@3: {score:.2f}",
            "",
            f"Успешных запросов: {sum(row['hit'] for row in rows)} из {len(rows)}.",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Precision@3 evaluation for search")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--output", default="docs/precision-at-3-report.md")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for document in DOCUMENTS:
            path = temp_path / document.file_name
            create_docx(path, document.text)
            upload_document(args.base_url, path)

    rows = []
    for item in QUERIES:
        top3 = search(args.base_url, item.query)
        rows.append(
            {
                "query": item.query,
                "expected": item.expected_file,
                "top3": top3,
                "hit": item.expected_file in top3,
            }
        )

    score = sum(row["hit"] for row in rows) / len(rows)
    report = render_report(rows, score)
    Path(args.output).write_text(report, encoding="utf-8")
    print(report)

    return 0 if score >= 0.8 else 1


if __name__ == "__main__":
    raise SystemExit(main())
