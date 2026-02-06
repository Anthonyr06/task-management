import time
import random
import json, hmac, hashlib
import httpx
from datetime import datetime, timezone

def _sign(secret: str, body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

def build_event(event_type: str, data: dict) -> dict:
    return {
        "event": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }

def backoff_delays(max_retries: int, base: float = 0.5, cap: float = 10.0):
    for attempt in range(max_retries):
        delay = min(cap, base * (2 ** attempt))
        jitter = random.uniform(0, delay * 0.25)
        yield delay + jitter

def send_webhook(url: str, secret: str, payload: dict, max_retries: int = 5):
    body = json.dumps(payload).encode("utf-8")
    sig = _sign(secret, body)

    headers = {"Content-Type": "application/json", "X-Signature": sig}

    with httpx.Client(timeout=5.0) as client:
        for delay in backoff_delays(max_retries):
            try:
                r = client.post(url, content=body, headers=headers)
                if 200 <= r.status_code < 300:
                    return True
            except Exception:
                pass
            time.sleep(delay)

    return False
