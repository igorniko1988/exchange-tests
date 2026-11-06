import pytest

from framework.http_client import HttpClient
from framework.settings import Settings


@pytest.fixture()
def settings():
    return Settings()


@pytest.fixture()
def api_client(settings):
    return HttpClient(settings.BASE_URL, settings.REQUEST_TIMEOUT)


def test_health(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
