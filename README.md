# Research Paper Library

A FastAPI application for storing research-paper PDFs and searchable paper metadata.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Ollama Cloud

## Setup

Set `DATABASE_URL`, `OLLAMA_API_KEY`, and optionally `OLLAMA_MODEL` in `.env`:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/research_db
OLLAMA_API_KEY=your-ollama-cloud-api-key
OLLAMA_MODEL=gpt-oss:20b-cloud
```

Install dependencies, create the database tables, then start the API:

```powershell
uv sync
uv run python -m src.database.create_tables
uv run fastapi dev main.py
```

PDFs are saved in `research_papers/`. The database stores each relative file path,
paper title, author, and a short summary suitable for later RAG retrieval. If
`summary` is omitted from an upload, the API extracts the PDF text and generates
the summary with the configured Ollama Cloud model. A supplied summary remains
supported as an override.

## API

Open `/docs` for the interactive API. Upload a PDF to `POST /paper` as multipart
form data with `file`, `title`, and `author`; `summary` is optional. The reusable
`summarize_text` and `summarize_pdf` functions are available from
`src.services.summarizer`.
