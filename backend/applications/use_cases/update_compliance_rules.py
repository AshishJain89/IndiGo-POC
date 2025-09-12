import os
from typing import List, Dict

from backend.infrastructure.ai.scraper import scrape_pages
from backend.infrastructure.ai.rag_service import upsert_documents


async def update_compliance_rules_from_sources(urls: List[str]) -> Dict[str, int]:
    docs = await scrape_pages(urls)
    upsert_documents(
        collection_name="compliance_rules",
        documents=docs,
        metadata={"category": "compliance", "source_type": "web"},
        persist_directory=os.getenv("CHROMA_DIR", "./data/chroma"),
    )
    return {"documents_indexed": len(docs)}


