def test_contact_validation_error(client):
    response = client.post(
        "/api/v1/contact",
        json={"name": "", "email": "invalid", "subject": "", "message": ""},
    )
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
