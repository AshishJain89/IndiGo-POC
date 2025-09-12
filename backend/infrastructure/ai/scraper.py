from __future__ import annotations

import asyncio
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup  # type: ignore


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def fetch_html(url: str, timeout: float = 30.0) -> str:
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text


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
    html_list = await asyncio.gather(*[fetch_html(u) for u in urls], return_exceptions=False)
    docs: List[Dict[str, str]] = []
    for idx, (url, html) in enumerate(zip(urls, html_list)):
        text = extract_text_from_html(html)
        docs.append({
            "id": f"doc-{idx}",
            "source": url,
            "text": text,
        })
    return docs


