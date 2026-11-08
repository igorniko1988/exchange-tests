from decimal import Decimal

import pytest

from framework.models.balance import Balance


def test_get_balances_show_balances_list(authorized_api):
    r = authorized_api.balances.list()
    assert r.status_code == 200
    balances = [Balance.model_validate(b) for b in r.json()]
    assets = {b.asset for b in balances}
    assert assets == {"BTC", "USDT", "ETH"}


@pytest.mark.smoke
def test_balances_show_available_after_deposit(funded_user):
    user = funded_user(asset="USDT", amount=Decimal(10))
    funded_user(user=user, asset="USDT", amount=Decimal(10))
    balances = user.balances.list()
    assert balances.status_code == 200
    balances = [Balance.model_validate(b) for b in balances.json()]
    usdt_balance = [b for b in balances if b.asset == "USDT"]
    assert usdt_balance
    assert usdt_balance[0].available == Decimal(20)
