import os

# import pytest
from starlette.testclient import TestClient
from app import app


client = TestClient(app=app)


def test_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
