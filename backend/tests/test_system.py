from fastapi.testclient import TestClient
from app.main import app


def test_system_stats():
    with TestClient(app) as client:
        r = client.get("/api/system/")
        assert r.status_code == 200
        body = r.json()
        assert "cpu_percent" in body
        assert body["memory"]["total"] > 0
