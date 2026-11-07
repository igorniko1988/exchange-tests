from decimal import Decimal


def test_get_balances_show_balances_list(authorized_api):
    r = authorized_api.balances.list()
    assert r.status_code == 200
    assert len(r.json()) == 3
    assert "asset" in r.json()[0]


def test_balances_show_available_after_deposit(authorized_api):
    data = {"asset": "USDT", "amount": 10}
    deposit = authorized_api.balances.deposit(**data)
    assert deposit.status_code == 200
    balances = authorized_api.balances.list()
    assert balances.status_code == 200
    usdt = [b for b in balances.json() if b["asset"] == data["asset"]]
    assert Decimal(usdt[0]["available"]) == Decimal(data["amount"])
