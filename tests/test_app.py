import os

import pytest
from starlette.testclient import TestClient
from app import app


client = TestClient(app=app)
prefix = "/api/v1/pdf-qa"


def test_endpoint():
    response = client.get(f"{prefix}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
