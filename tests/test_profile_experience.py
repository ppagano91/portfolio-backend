def test_get_public_profile(client):
    response = client.get("/api/v1/profile")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"] is not None
    assert body["error"] is None
    assert "name" in body["data"]
    assert "experiences" in body["data"]


def test_list_experiences(client):
    response = client.get("/api/v1/experiences")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_list_experiences_ordered(client):
    response = client.get("/api/v1/experiences")
    body = response.json()
    experiences = body["data"]
    if len(experiences) < 2:
        return
    sort_orders = [item["sort_order"] for item in experiences]
    assert sort_orders == sorted(sort_orders)


def test_get_profile_by_slug(client):
    profile_response = client.get("/api/v1/profile")
    if profile_response.status_code != 200:
        return
    slug = profile_response.json()["data"]["slug"]
    response = client.get(f"/api/v1/profiles/{slug}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["slug"] == slug


def test_get_experience_not_found(client):
    response = client.get("/api/v1/experiences/999999")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "NOT_FOUND"
