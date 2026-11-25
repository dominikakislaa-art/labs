"""Order status state machine for a delivery service."""

from datetime import datetime, timezone

ALLOWED_TRANSITIONS = {
    "created": ("cooking", "cancelled"),
    "cooking": ("delivering", "cancelled"),
    "delivering": ("done",),
    "done": (),
    "cancelled": (),
}


class OrderStatusError(ValueError):
    pass


def _now(now):
    return now or datetime.now(timezone.utc)


def _check(status):
    if status not in ALLOWED_TRANSITIONS:
        raise OrderStatusError("unknown status: %r" % status)


def next_statuses(status):
    _check(status)
    return list(ALLOWED_TRANSITIONS[status])


def is_final(status):
    _check(status)
    return not ALLOWED_TRANSITIONS[status]


class Order:
    def __init__(self, order_id, now=None):
        if not order_id or not order_id.strip():
            raise ValueError("order_id must be non-empty")
        self.id = order_id
        self.status = "created"
        self.history = [{"status": "created", "timestamp": _now(now)}]

    def can_transition(self, new_status):
        _check(new_status)
        return new_status in ALLOWED_TRANSITIONS[self.status]

    def transition(self, new_status, now=None):
        if not self.can_transition(new_status):
            raise OrderStatusError(
                "cannot move %r from %r to %r" % (self.id, self.status, new_status)
            )
        self.status = new_status
        self.history.append({"status": new_status, "timestamp": _now(now)})
        return self.status

    def cancel(self, now=None):
        return self.transition("cancelled", now)
