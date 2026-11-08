import pytest

from framework.api import Api
from framework.data.generators import credentials
from framework.http_client import HttpClient
from framework.settings import Settings


@pytest.fixture()
def settings():
    settings = Settings()
    return settings


@pytest.fixture
def creds():
    return credentials()


@pytest.fixture
def http_client(settings):
    return HttpClient(settings.BASE_URL, settings.REQUEST_TIMEOUT)


@pytest.fixture()
def token(api, creds):
    register = api.auth.register(**creds)
    assert register.status_code == 201
    token = api.auth.login(**creds)
    assert token.status_code == 200
    return token.json()["access_token"]


@pytest.fixture()
def api(http_client):
    return Api(http_client)


@pytest.fixture()
def authorized_api(api, token):
    api.client.set_token(token)
    return api
