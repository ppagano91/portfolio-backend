def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert body["error"] is None


def test_health_check_response_structure(client):
    response = client.get("/api/v1/health")
    body = response.json()
    assert "success" in body
    assert "data" in body
    assert "message" in body
    assert "error" in body
