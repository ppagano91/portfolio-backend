def test_list_education(client):
    response = client.get("/api/v1/education")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_list_education_ordered(client):
    response = client.get("/api/v1/education")
    body = response.json()
    records = body["data"]
    if len(records) < 2:
        return
    sort_orders = [item["sort_order"] for item in records]
    assert sort_orders == sorted(sort_orders)


def test_get_education_not_found(client):
    response = client.get("/api/v1/education/999999")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "NOT_FOUND"
