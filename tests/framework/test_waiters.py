import pytest

from framework.waiters import wait_until


def test_wait_until_returns_value_when_condition_is_true_immediately():
    calls = []

    def condition():
        calls.append(1)
        return "ready"

    assert wait_until(condition, timeout=1, interval=0.01) == "ready"
    assert len(calls) == 1


def test_wait_until_returns_value_when_condition_becomes_true():
    calls = []

    def condition():
        calls.append(1)
        return "ready" if len(calls) == 3 else None

    assert wait_until(condition, timeout=1, interval=0.01) == "ready"
    assert len(calls) == 3


def test_wait_until_raises_timeout_with_message_and_last_value():
    with pytest.raises(TimeoutError) as exc:
        wait_until(lambda: 0, timeout=0.3, interval=0.1, message="order not filled")

    assert "order not filled" in str(exc.value)
    assert "last value: 0" in str(exc.value)
