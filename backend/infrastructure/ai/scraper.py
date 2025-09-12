from __future__ import annotations

import asyncio
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup  # type: ignore
from pypdf import PdfReader  # type: ignore
from io import BytesIO
from backend.infrastructure.settings import settings


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def fetch_html(url: str, timeout: float = 30.0) -> str:
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout or 30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text
async def fetch_bytes(url: str, timeout: float = 60.0) -> bytes:
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout or 60.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.content


def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    texts: List[str] = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join([t.strip() for t in texts if t and t.strip()])



def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # Remove script and style
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Normalize whitespace
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join([line for line in lines if line])


async def scrape_pages(urls: List[str]) -> List[Dict[str, str]]:
    docs: List[Dict[str, str]] = []
    for idx, url in enumerate(urls):
        lower = url.lower()
        try:
            if lower.endswith(".pdf") or "?" in lower and "pdf" in lower.split("?")[0]:
                data = await fetch_bytes(url)
                text = extract_text_from_pdf(data)
            else:
                html = await fetch_html(url)
                text = extract_text_from_html(html)
        except Exception:
            # Skip problematic sources but continue others
            continue
        if not text:
            continue
        docs.append({
            "id": f"doc-{idx}",
            "source": url,
            "text": text,
        })
    return docs


