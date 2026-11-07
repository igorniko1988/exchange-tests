from decimal import Decimal


def test_create_order_shows_correct_quantity(authorized_api):
    deposit = authorized_api.balances.deposit("BTC", 100)
    assert deposit.status_code == 200
    data = {"symbol": "BTC-USDT", "side": "SELL", "type": "LIMIT", "price": 23, "quantity": 23}

    r = authorized_api.orders.create(**data)
    assert r.status_code == 201
    assert Decimal(r.json()["quantity"]) == Decimal(23)


def test_get_orders(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    data = {"symbol": "ETH-USDT", "side": "BUY", "type": "LIMIT", "price": 23, "quantity": 23}
    r = authorized_api.orders.create(**data)
    assert r.status_code == 201

    list_orders = authorized_api.orders.list(status="NEW")
    assert list_orders.status_code == 200
    assert list_orders.json()[0]["id"] == r.json()["id"]


def test_get_order_by_id(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    data = {"symbol": "BTC-USDT", "side": "BUY", "type": "LIMIT", "price": 23, "quantity": 23}
    r = authorized_api.orders.create(**data)
    assert r.status_code == 201
    order_id = r.json()["id"]

    get_order_by_id = authorized_api.orders.get(order_id=order_id)
    assert get_order_by_id.status_code == 200

    assert order_id == get_order_by_id.json()["id"]


def test_user_can_delete_order(authorized_api):
    deposit = authorized_api.balances.deposit("USDT", 1000)
    assert deposit.status_code == 200
    data = {"symbol": "BTC-USDT", "side": "BUY", "type": "LIMIT", "price": 23, "quantity": 23}
    r = authorized_api.orders.create(**data)
    assert r.status_code == 201
    order_id = r.json()["id"]

    delete_order = authorized_api.orders.cancel(order_id=order_id)
    assert delete_order.status_code == 200

    get_deleted_order = authorized_api.orders.get(order_id)
    assert get_deleted_order.status_code == 200
    assert get_deleted_order.json()["status"] == "CANCELED"
