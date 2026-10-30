from __future__ import annotations

import os
from pathlib import Path

import httpx
from pypdf import PdfReader
from pypdf.errors import PdfReadError


class SummarizationError(RuntimeError):
    """Raised when a document cannot be summarized."""


class OllamaSummarizer:
    """Summarize text through Ollama's OpenAI-compatible chat API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        endpoint: str | None = None,
        timeout: float = 120.0,
        max_input_characters: int = 120_000,
    ) -> None:
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        self.model = model or os.getenv("OLLAMA_MODEL", "gpt-oss:20b-cloud")
        self.endpoint = endpoint or os.getenv(
            "OLLAMA_ENDPOINT", "https://ollama.com/api/chat"
        )
        self.timeout = timeout
        self.max_input_characters = max_input_characters

    async def summarize_text(self, text: str) -> str:
        """Return a concise summary for arbitrary text."""
        normalized_text = " ".join(text.split())
        if not normalized_text:
            raise SummarizationError("The document does not contain extractable text")
        if not self.api_key:
            raise SummarizationError("OLLAMA_API_KEY is not configured")

        prompt = (
            "Summarize the following research paper for a searchable paper library. "
            "Write 1-3 concise paragraphs covering the research question, approach, "
            "main findings, and limitations. Do not invent details.\n\n"
            f"Paper text:\n{normalized_text[:self.max_input_characters]}"
        )
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a precise research-paper summarizer.",
                },
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SummarizationError("Ollama could not summarize the document") from exc

        try:
            summary = data["message"]["content"].strip()
        except (KeyError, TypeError, AttributeError) as exc:
            raise SummarizationError("Ollama returned an invalid summary response") from exc
        if not summary:
            raise SummarizationError("Ollama returned an empty summary")
        return summary

    async def summarize_pdf(self, file_path: str | Path) -> str:
        """Extract text from a PDF and summarize it."""
        try:
            reader = PdfReader(str(file_path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except (OSError, PdfReadError, ValueError) as exc:
            raise SummarizationError("The PDF text could not be extracted") from exc
        return await self.summarize_text(text)


summarizer = OllamaSummarizer()


async def summarize_text(text: str) -> str:
    """Summarize text using the configured Ollama model."""
    return await summarizer.summarize_text(text)


async def summarize_pdf(file_path: str | Path) -> str:
    """Summarize a PDF using the configured Ollama model."""
    return await summarizer.summarize_pdf(file_path)


__all__ = [
    "OllamaSummarizer",
    "SummarizationError",
    "summarize_pdf",
    "summarize_text",
]
