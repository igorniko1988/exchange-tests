import requests
import responses
import pytest
from framework.http_client import HttpClient


def test_client_returns_503_as_is(mocks_servers):
    r = HttpClient("http://stand", 1).get("/health")
    assert r.status_code == 503


def test_mock_server(mocks_servers):

    r = requests.post('http://stand/health/2')

    print(r.json()['message'])

@pytest.fixture()
def mocks_servers():
    with responses.RequestsMock() as mocks:
        mocks.add(responses.GET, "http://stand/health", status=503, json={"error": "down"})
        mocks.add(responses.POST,'http://stand/health/2', status=200, json={'message':'user ok'})
        yield mocks