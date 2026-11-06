import pytest

from framework.settings import Settings


@pytest.fixture
def base_url():
    settings = Settings(_env_file=None)
    return settings.BASE_URL


def test_base_url(base_url):
    assert base_url == "http://localhost:8080"


def test_timeout_is_read_from_env(monkeypatch):
    monkeypatch.setenv("EXCHANGE_TESTS_REQUEST_TIMEOUT", "30")
    settings = Settings(_env_file=None)
    assert settings.REQUEST_TIMEOUT == 30


def test_password():
    settings = Settings(_env_file=None)
    assert 'admin-password' not in repr(settings.ADMIN_PASSWORD)
    assert settings.ADMIN_PASSWORD.get_secret_value() == 'admin-password'
