import pytest





@pytest.mark.smoke
def test_health(api):


    print('adas')
    r = api.client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
