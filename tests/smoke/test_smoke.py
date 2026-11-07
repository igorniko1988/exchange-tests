def test_health(api):
    r = api.client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
