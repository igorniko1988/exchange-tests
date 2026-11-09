from decimal import Decimal

import allure
import pytest

from framework.data.generators import make_order
from framework.models.orders import Order


@allure.feature("Orders")
@allure.story("Cancel order")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Пользователь отменяет свой ордер")
def test_user_can_delete_order(create_order):
    user, order = create_order
    with allure.step("Отменить ордер"):
        cancel = user.orders.cancel(order_id=order.id)
        assert cancel.status_code == 200, cancel.text

    with allure.step("Проверить статус CANCELED"):
        r = user.orders.get(order.id)
        assert r.status_code == 200, r.text
        assert Order.model_validate(r.json()).status == "CANCELED"


@pytest.mark.critical
def test_create_order_shows_correct_quantity(create_order):
    user, order = create_order
    print(order.quantity)
    assert order.quantity == Decimal(23)


@pytest.mark.critical
def test_get_orders(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    order_data = make_order(symbol="ETH-USDT", side="BUY", type="LIMIT", price=23, quantity=23)
    r = authorized_api.orders.create(order_data)
    assert r.status_code == 201

    list_orders = authorized_api.orders.list(status="NEW")
    assert list_orders.status_code == 200
    orders = [Order.model_validate(o) for o in list_orders.json()]
    ids = {o.id for o in orders}
    assert r.json()["id"] in ids


def test_get_order_by_id(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    order_data = make_order(symbol="BTC-USDT", side="BUY", type="LIMIT", price=23, quantity=23)
    r = authorized_api.orders.create(order_data)
    assert r.status_code == 201
    order_id = r.json()["id"]

    get_order_by_id = authorized_api.orders.get(order_id=order_id)
    assert get_order_by_id.status_code == 200
    order = Order.model_validate(get_order_by_id.json())
    assert order.id == order_id


@pytest.mark.critical
def test_user_can_delete_order(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    order_data = make_order(symbol="BTC-USDT", side="BUY", type="LIMIT", price=23, quantity=23)
    r = authorized_api.orders.create(order_data)
    assert r.status_code == 201
    order_id = r.json()["id"]

    delete_order = authorized_api.orders.cancel(order_id=order_id)
    assert delete_order.status_code == 200

    get_deleted_order = authorized_api.orders.get(order_id)
    assert get_deleted_order.status_code == 200
    order = Order.model_validate(get_deleted_order.json())
    assert order.status == "CANCELED"
