from framework.settings import Settings


def test_default_base_url():
    base_url = Settings(_env_file=None).BASE_URL
    assert base_url == "http://localhost:8080"


def test_base_url_from_env(monkeypatch):
    monkeypatch.setenv("EXCHANGE_TESTS_BASE_URL", "http://example.com")
    assert Settings(_env_file=None).BASE_URL == "http://example.com"


def test_password_is_hidden():
    settings = Settings(_env_file=None)

    assert "admin-password" not in repr(settings)
    assert settings.ADMIN_PASSWORD.get_secret_value() == "admin-password"
