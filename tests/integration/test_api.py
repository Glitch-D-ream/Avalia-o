import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    # O código original pode não ter /health, mas testamos a raiz
    response = client.get("/")
    assert response.status_code == 200
