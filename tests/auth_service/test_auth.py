import pytest

from framework.models.token import Token
from framework.models.user import User, UserMe


def test_registration_user_returns_user_email(api, creds):
    r = api.auth.register(**creds)
    assert r.status_code == 201
    user = User.model_validate(r.json())
    assert user.email == creds["email"]


def test_user_login_returns_access_and_refresh_tokens(api, creds):
    r = api.auth.register(**creds)
    assert r.status_code == 201

    login = api.auth.login(**creds)
    assert login.status_code == 200
    token = Token.model_validate(login.json())
    assert token.token_type == "Bearer"
    assert token.access_token


def test_me_returns_users_details(authorized_api, creds):
    r = authorized_api.auth.me()
    assert r.status_code == 200
    user = UserMe.model_validate(r.json())
    assert user.email == creds["email"]


def test_user_update_account_details(authorized_api):
    r = authorized_api.auth.update_me(display_name="niko")
    assert r.status_code == 200

    users_info = authorized_api.auth.me()
    assert users_info.status_code == 200

    user = UserMe.model_validate(users_info.json())
    assert user.display_name == "niko"


@pytest.mark.xfail(reason="patch/me accepts mass assignment", strict=True)
def test_user_should_not_change_its_role(authorized_api):
    role = authorized_api.auth.me()
    assert role.status_code == 200
    before_me = UserMe.model_validate(role.json())

    update_me = authorized_api.auth.update_me(display_name="superman", role="admin")
    assert update_me.status_code == 200

    me = authorized_api.auth.me()
    assert me.status_code == 200
    after_me = UserMe.model_validate(me.json())
    assert before_me.role == after_me.role


def test_user_update_refresh_token(api, creds):
    register = api.auth.register(**creds)
    assert register.status_code == 201
    response = api.auth.login(**creds)
    assert response.status_code == 200
    before = Token.model_validate(response.json())

    refreshed_token = api.auth.refresh_token(response.json()["refresh_token"])
    assert refreshed_token.status_code == 200
    after = Token.model_validate(refreshed_token.json())
    assert before.refresh_token != after.refresh_token
