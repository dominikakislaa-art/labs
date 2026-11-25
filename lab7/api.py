import json
import os
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import redis

ALLOWED = {
    "created": ("cooking", "cancelled"),
    "cooking": ("delivering", "cancelled"),
    "delivering": ("done",),
    "done": (),
    "cancelled": (),
}
PORT = int(os.environ.get("PORT", "8000"))
STORE = "orders"
db = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True
)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load(order_id):
    raw = db.hget(STORE, order_id)
    return json.loads(raw) if raw else None


def save(order):
    db.hset(STORE, order["id"], json.dumps(order, ensure_ascii=False))


def set_status(order, status, by):
    order["status"] = status
    order["updatedAt"] = now()
    order["history"].append({"status": status, "at": now(), "by": by})
    save(order)


class Handler(BaseHTTPRequestHandler):
    server_version = "DeliveryAPI/1.0"

    def reply(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body(self):
        size = int(self.headers.get("Content-Length") or 0)
        if not size:
            return {}
        try:
            return json.loads(self.rfile.read(size))
        except json.JSONDecodeError:
            return None

    def route(self):
        return [part for part in urlparse(self.path).path.split("/") if part]

    def log_message(self, fmt, *args):
        print(self.address_string(), fmt % args, flush=True)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":
            try:
                db.ping()
            except redis.RedisError:
                return self.reply(503, {"status": "unavailable"})
            return self.reply(200, {"status": "ok", "redis": "ok"})

        parts = self.route()
        if parts == ["orders"]:
            status = parse_qs(url.query).get("status", [None])[0]
            orders = [order for order in map(load, db.hkeys(STORE)) if order]
            if status:
                orders = [order for order in orders if order["status"] == status]
            orders.sort(key=lambda order: order["id"])
            return self.reply(200, {"count": len(orders), "orders": orders})
        if len(parts) == 2 and parts[0] == "orders":
            order = load(parts[1])
            if order is None:
                return self.reply(404, {"error": "order not found"})
            return self.reply(200, order)
        self.reply(404, {"error": "not found"})

    def do_POST(self):
        parts = self.route()
        if parts == ["orders"]:
            data = self.body()
            if data is None:
                return self.reply(400, {"error": "invalid json"})
            items = data.get("items")
            if not isinstance(items, list) or not items:
                return self.reply(422, {"error": "items must be a non-empty list"})
            order = {
                "id": uuid.uuid4().hex[:8],
                "items": items,
                "status": "created",
                "createdAt": now(),
                "updatedAt": now(),
                "history": [{"status": "created", "at": now(), "by": "customer"}],
            }
            save(order)
            return self.reply(201, order)
        if len(parts) == 3 and parts[0] == "orders" and parts[2] == "cancel":
            order = load(parts[1])
            if order is None:
                return self.reply(404, {"error": "order not found"})
            if "cancelled" not in ALLOWED[order["status"]]:
                return self.reply(409, {"error": "cannot cancel in status " + order["status"]})
            set_status(order, "cancelled", "customer")
            return self.reply(200, order)
        self.reply(404, {"error": "not found"})

    def do_PATCH(self):
        parts = self.route()
        if not (len(parts) == 3 and parts[0] == "orders" and parts[2] == "status"):
            return self.reply(404, {"error": "not found"})
        order = load(parts[1])
        if order is None:
            return self.reply(404, {"error": "order not found"})
        data = self.body()
        if data is None:
            return self.reply(400, {"error": "invalid json"})
        new = data.get("status")
        if new not in ALLOWED:
            return self.reply(422, {"error": "unknown status"})
        if new == order["status"]:
            return self.reply(200, order)
        if new not in ALLOWED[order["status"]]:
            return self.reply(
                409, {"error": "transition %s -> %s is not allowed" % (order["status"], new)}
            )
        set_status(order, new, data.get("by", "restaurant"))
        self.reply(200, order)


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("delivery api on :%d" % PORT, flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
