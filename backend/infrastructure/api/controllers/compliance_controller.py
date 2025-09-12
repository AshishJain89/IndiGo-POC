from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List, Literal, Optional
import os
import asyncio

from backend.infrastructure.ai.rag_service import get_chroma_client
from backend.applications.use_cases.update_compliance_rules import update_compliance_rules_from_sources
from backend.applications.use_cases.get_compliance_rules import get_compliance_rules_from_vector_store

class ComplianceRule(BaseModel):
    id: str
    name: str
    type: Literal["hard", "soft"]
    description: str
    status: Literal["active", "inactive"]
    violations: int

router = APIRouter(prefix="/api/compliance", tags=["compliance"])

@router.get("/rules", response_model=List[ComplianceRule])
async def get_compliance_rules():
    data = get_compliance_rules_from_vector_store()
    return [ComplianceRule(**item) for item in data]

class UpdateRulesRequest(BaseModel):
    urls: Optional[List[str]] = None


@router.post("/rules/update", status_code=status.HTTP_200_OK)
async def update_compliance_rules(payload: UpdateRulesRequest | None = None):
    # Accept user-provided URLs or fallback to defaults
    urls = (
        payload.urls
        if payload and payload.urls
        else [
            "https://www.dgca.gov.in/digigov-portal/",
            "https://www.dgca.gov.in/digigov-portal/?page=2067/4310/list-of-advisories-circulars",
            "https://www.icao.int/safety/fatiguemanagement/FRMS/Pages/Regulators.aspx",
        ]
    )
    result = await update_compliance_rules_from_sources(urls)
    return {"status": "ok", **result}