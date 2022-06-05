import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../app')

from main import app

from fastapi.testclient import TestClient


client = TestClient(app)


def test_providers():
    response = client.get("/api/v1/providers/")
    assert response.status_code == 200
    #assert response.json() == {"msg": "Hello World"}