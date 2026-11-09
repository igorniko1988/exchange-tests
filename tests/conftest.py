from decimal import Decimal

import pytest

from framework.api import Api
from framework.data.generators import credentials, make_order
from framework.http_client import HttpClient
from framework.models.orders import Order
from framework.settings import Settings


@pytest.fixture(scope="session")
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


@pytest.fixture()
def make_user(settings):

    users: list[Api] = []

    def _make():
        user_creds = credentials()
        http_client = HttpClient(settings.BASE_URL, settings.REQUEST_TIMEOUT)
        app = Api(http_client)
        register = app.auth.register(**user_creds)
        assert register.status_code == 201, register.text
        token = app.auth.login(**user_creds).json()["access_token"]
        app.client.set_token(token)
        users.append(app)
        return app

    yield _make

    for u in users:
        orders = u.orders.list(status="NEW")
        assert orders.status_code == 200
        for order in orders.json():
            cancel = u.orders.cancel(order["id"])
            if cancel.status_code != 200:
                print(f"Order {order['id']}doesnt cancel due to {cancel.text}")


@pytest.fixture()
def funded_user(make_user):
    def _fund(asset: str, amount: Decimal, user: Api | None = None):
        if user is None:
            user = make_user()
        deposit = user.balances.deposit(asset=asset, amount=amount)
        assert deposit.status_code == 200, deposit.text
        return user

    return _fund


@pytest.fixture()
def create_order(funded_user):
    order = make_order(quantity=23)
    user = funded_user(asset="BTC", amount=Decimal(1000))
    r = user.orders.create(order)
    assert r.status_code == 201, r.text
    return user, Order.model_validate(r.json())
