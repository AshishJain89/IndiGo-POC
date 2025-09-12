import os
from typing import List, Dict

import tiktoken  # type: ignore
from openai import OpenAI  # type: ignore
import chromadb  # type: ignore
from chromadb.config import Settings  # type: ignore
from typing import Optional
from backend.infrastructure.settings import settings
import hashlib

_st_model = None



def _get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key)


def get_chroma_client(persist_directory: str | None = None):
    if persist_directory is None:
        persist_directory = settings.chroma_dir
    os.makedirs(persist_directory, exist_ok=True)
    return chromadb.PersistentClient(path=persist_directory, settings=Settings(anonymized_telemetry=False))


def _get_encoding(model: str = "gpt-4o-mini"):
    try:
        return tiktoken.encoding_for_model(model)
    except Exception:
        return tiktoken.get_encoding("cl100k_base")


def tokenize_text(text: str, model: str = "gpt-4o-mini") -> List[int]:
    enc = _get_encoding(model)
    return enc.encode(text)


def chunk_text(text: str, max_tokens: int = 700, overlap_tokens: int = 80, model: str = "gpt-4o-mini") -> List[str]:
    enc = _get_encoding(model)
    tokens = enc.encode(text)
    chunks: List[str] = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))
        if end == len(tokens):
            break
        start = end - overlap_tokens
        if start < 0:
            start = 0
    return chunks


def embed_texts(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    # Try OpenAI first
    try:
        client = _get_openai_client()
        response = client.embeddings.create(model=model, input=texts)
        return [d.embedding for d in response.data]
    except Exception:
        # Fallback to local SentenceTransformer to avoid rate limits/quota issues
        global _st_model
        if _st_model is None:
            from sentence_transformers import SentenceTransformer  # type: ignore
            _st_model = SentenceTransformer(settings.sentence_transformer_model)
        vectors = _st_model.encode(texts, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
        return [v.tolist() for v in vectors]


def upsert_documents(
    collection_name: str,
    documents: List[Dict[str, str]],
    metadata: Dict[str, str] | None = None,
    persist_directory: str | None = None,
    chunk_tokens: int = 700,
    chunk_overlap: int = 80,
):
    client = get_chroma_client(persist_directory)
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    ids: List[str] = []
    texts: List[str] = []
    metadatas: List[Dict[str, str]] = []
    for doc in documents:
        base_meta = metadata.copy() if metadata else {}
        base_meta.update({k: v for k, v in doc.items() if k not in ("id", "text")})
        # Idempotency via content hash; skip chunks we already have
        doc_id = doc.get("id", "doc")
        content_hash = hashlib.sha256(doc["text"].encode("utf-8")).hexdigest()[:12]
        base_meta["content_hash"] = content_hash
        max_tokens = chunk_tokens or settings.chunk_tokens
        overlap = chunk_overlap or settings.chunk_overlap
        chunks = chunk_text(doc["text"], max_tokens=max_tokens, overlap_tokens=overlap)
        for idx, chunk in enumerate(chunks):
            chunk_hash = hashlib.sha256(chunk.encode("utf-8")).hexdigest()[:12]
            chunk_id = f"{doc_id}-{content_hash}-{idx}-{chunk_hash}"
            ids.append(chunk_id)
            texts.append(chunk)
            meta = base_meta.copy()
            meta.update({"chunk_index": str(idx), "chunk_hash": chunk_hash})
            metadatas.append(meta)
    if texts:
        embeddings = embed_texts(texts)
        collection.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)


def query_similar(
    collection_name: str,
    query: str,
    n_results: int = 5,
    persist_directory: str = ".chroma",
):
    client = get_chroma_client(persist_directory)
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    query_embedding = embed_texts([query])[0]
    return collection.query(query_embeddings=[query_embedding], n_results=n_results)


