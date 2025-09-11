
import sys
import os
import pytest
from httpx import AsyncClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import app
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_get_all_crew(monkeypatch):
    async def mock_get_all_crew(*args, **kwargs):
        return []
    monkeypatch.setattr("infrastructure.api.controllers.crew_controller.get_all_crew", mock_get_all_crew)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/crew/")
        assert response.status_code in (200, 404)

@pytest.mark.asyncio
async def test_get_all_rosters(monkeypatch):
    async def mock_get_all_rosters(*args, **kwargs):
        return []
    monkeypatch.setattr("infrastructure.api.controllers.roster_controller.get_all_rosters", mock_get_all_rosters)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/rosters/")
        assert response.status_code in (200, 404)
