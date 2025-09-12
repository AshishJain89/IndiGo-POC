from __future__ import annotations

import json
from typing import List, Dict, Literal
from openai import OpenAI  # type: ignore
from backend.infrastructure.ai.perplexity_client import chat_perplexity

from backend.infrastructure.ai.rag_service import get_chroma_client, embed_texts


def _get_openai_client() -> OpenAI:
    return OpenAI()


def _build_extraction_prompt(context: str) -> str:
    return (
        "You are a compliance analyst. From the provided regulations context, extract a concise list of actionable crew rostering rules.\n"
        "Return STRICT JSON array with items having fields: id (string), name (string), type ('hard'|'soft'), description (string), status ('active'|'inactive'), violations (number set to 0).\n"
        "Do not add commentary. JSON only.\n\n"
        f"CONTEXT:\n{context}"
    )


def get_compliance_rules_from_vector_store(top_k: int = 8) -> List[Dict[str, object]]:
    client = get_chroma_client()
    collection = client.get_or_create_collection(name="compliance_rules")
    if collection.count() == 0:
        return []
    # Use a general query
    query_text = "crew rostering regulations and compliance requirements"
    results = collection.query(query_texts=[query_text], n_results=top_k)
    docs = results.get("documents", [[]])[0]
    context = "\n\n".join(docs)

    prompt = _build_extraction_prompt(context)
    # Try OpenAI first
    try:
        oai = _get_openai_client()
        chat = oai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You output JSON only."}, {"role": "user", "content": prompt}],
            temperature=0.1,
        )
        content = chat.choices[0].message.content or "[]"
        data = json.loads(content)
        if isinstance(data, list):
            return data
    except Exception:
        # Fallback to Perplexity chat if available
        try:
            content = asyncio.run(chat_perplexity(prompt, model="pplx-7b-online"))  # type: ignore
            data = json.loads(content)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return []


