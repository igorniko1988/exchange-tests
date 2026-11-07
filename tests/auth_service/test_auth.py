import pytest


def test_registration_user_returns_user_email(api, creds):
    r = api.auth.register(**creds)
    assert r.status_code == 201
    assert r.json()["email"] == creds["email"]


def test_user_login_returns_access_and_refresh_tokens(api, creds):
    api.auth.register(**creds)
    login = api.auth.login(**creds)
    assert login.status_code == 200
    assert "access_token" in login.json()
    assert "refresh_token" in login.json()


def test_me_returns_users_details(authorized_api):
    r = authorized_api.auth.me()
    assert r.status_code == 200
    assert r.json()["id"] is not None


def test_user_update_account_details(authorized_api):
    r = authorized_api.auth.update_me(display_name="niko")
    users_info = authorized_api.auth.me()
    assert users_info.json()["display_name"] == "niko"
    assert r.status_code == 200


@pytest.mark.xfail(reason="Bug should be fixed, for now role is possible to change", strict=True)
def test_user_shouldnt_change_its_role(authorized_api):
    role = authorized_api.auth.me()
    assert role.status_code == 200
    updated_role = authorized_api.auth.update_me(display_name="superman", role="admin")
    assert updated_role.status_code == 200
    me = authorized_api.auth.me()
    assert role.json()["role"] == me.json()["role"]


def test_user_update_refresh_token(api, creds):
    api.auth.register(**creds)
    response = api.auth.login(**creds)
    assert response.status_code == 200
    refreshed_token = api.auth.refresh_token(response.json()["refresh_token"])
    assert refreshed_token.status_code == 200
    assert response.json()["refresh_token"] != refreshed_token.json()["refresh_token"]
