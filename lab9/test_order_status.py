from datetime import datetime, timezone

import pytest

from order_status import ALLOWED_TRANSITIONS, Order, OrderStatusError, is_final, next_statuses


def make(*statuses):
    order = Order("A-1")
    for status in statuses:
        order.transition(status)
    return order


def test_full_path():
    order = Order("A-1")
    for status in ("cooking", "delivering", "done"):
        assert order.transition(status) == status
    assert [e["status"] for e in order.history] == [
        "created",
        "cooking",
        "delivering",
        "done",
    ]


@pytest.mark.parametrize("path", [(), ("cooking",)])
def test_cancel_before_courier(path):
    order = make(*path)
    assert order.cancel() == "cancelled"
    assert order.status == "cancelled"


def test_cancel_after_courier_forbidden():
    order = make("cooking", "delivering")
    with pytest.raises(OrderStatusError):
        order.cancel()
    assert order.status == "delivering"


@pytest.mark.parametrize(
    "path,new",
    [((), "done"), (("cooking",), "done"), (("cooking", "delivering"), "cooking"), ((), "created")],
)
def test_invalid_transitions(path, new):
    order = make(*path)
    with pytest.raises(OrderStatusError):
        order.transition(new)
    assert order.status == (path[-1] if path else "created")


@pytest.mark.parametrize("path", [(), ("cooking", "delivering", "done")])
def test_terminal_status_forbids_transitions(path):
    order = make(*path)
    if not path:
        order.cancel()
    assert is_final(order.status) is True
    for status in ALLOWED_TRANSITIONS:
        with pytest.raises(OrderStatusError):
            order.transition(status)


def test_can_transition_does_not_mutate():
    order = Order("A-1")
    assert order.can_transition("cooking") is True
    assert order.can_transition("done") is False
    assert order.status == "created"
    assert len(order.history) == 1


def test_next_statuses():
    assert next_statuses("created") == ["cooking", "cancelled"]
    assert next_statuses("cooking") == ["delivering", "cancelled"]
    assert next_statuses("delivering") == ["done"]
    assert next_statuses("done") == []
    assert next_statuses("cancelled") == []


def test_is_final():
    assert is_final("done") is True
    assert is_final("cancelled") is True
    for status in ("created", "cooking", "delivering"):
        assert is_final(status) is False


def test_history_timestamps():
    t0 = datetime(2026, 11, 25, 10, 0, tzinfo=timezone.utc)
    t1 = datetime(2026, 11, 25, 10, 5, tzinfo=timezone.utc)
    order = Order("A-1", now=t0)
    order.transition("cooking", now=t1)
    assert order.history == [
        {"status": "created", "timestamp": t0},
        {"status": "cooking", "timestamp": t1},
    ]


def test_unknown_status():
    order = Order("A-1")
    with pytest.raises(OrderStatusError):
        order.transition("flying")
    with pytest.raises(OrderStatusError):
        next_statuses("flying")
    with pytest.raises(OrderStatusError):
        is_final("flying")
    assert order.status == "created"


def test_empty_id():
    with pytest.raises(ValueError):
        Order("")


def test_orders_are_isolated():
    first, second = Order("A-1"), Order("A-2")
    first.transition("cooking")
    assert second.status == "created"
    assert len(second.history) == 1


def test_table_is_complete():
    assert set(ALLOWED_TRANSITIONS) == {"created", "cooking", "delivering", "done", "cancelled"}
