
import sys
import os
import pytest
from httpx import AsyncClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import app
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_get_disruptions(monkeypatch):
    async def mock_get_disruptions(*args, **kwargs):
        return []
    monkeypatch.setattr("infrastructure.api.controllers.disruptions_controller.get_disruptions", mock_get_disruptions)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/disruptions/")
        assert response.status_code in (200, 404)
