import os

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient
from app import app


client = TestClient(app=app)
base_url = "http://localhost:8000/api/v1/pdf-qa"


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url=f"{base_url}") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url=f"{base_url}") as client:
        response = await client.get("/chat")
    assert response.status_code == 200
