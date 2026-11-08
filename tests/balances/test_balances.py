from decimal import Decimal

from framework.models.balance import Balance


def test_get_balances_show_balances_list(authorized_api):
    r = authorized_api.balances.list()
    assert r.status_code == 200
    balances = [Balance.model_validate(b) for b in r.json()]
    assets = {b.asset for b in balances}
    assert assets == {"BTC", "USDT", "ETH"}


def test_balances_show_available_after_deposit(authorized_api):
    data = {"asset": "USDT", "amount": 10}
    deposit = authorized_api.balances.deposit(**data)
    assert deposit.status_code == 200

    balances = authorized_api.balances.list()
    assert balances.status_code == 200
    balances = [Balance.model_validate(b) for b in balances.json()]
    usdt_balance = [b for b in balances if b.asset == "USDT"]
    assert usdt_balance[0].available == Decimal(data["amount"])
