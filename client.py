"""Token Bucket Traffic Shaper.
100% Python Standard Library.
"""
import time
from typing import Dict, Any

class TokenBucketTrafficShaper:
    """Token bucket traffic shaper with smooth replenishment and burst capacity."""
    def __init__(self):
        self.buckets: Dict[str, Dict[str, float]] = {}

    def _refill(self, bucket_id: str, capacity: float, refill_rate: float) -> None:
        now = time.time()
        if bucket_id not in self.buckets:
            self.buckets[bucket_id] = {"tokens": capacity, "last_refill": now}
            return

        b = self.buckets[bucket_id]
        elapsed = now - b["last_refill"]
        tokens_to_add = elapsed * refill_rate
        b["tokens"] = min(capacity, b["tokens"] + tokens_to_add)
        b["last_refill"] = now

    def consume_tokens(
        self,
        bucket_id: str,
        tokens: float = 1.0,
        capacity: float = 100.0,
        refill_rate: float = 10.0
    ) -> Dict[str, Any]:
        self._refill(bucket_id, capacity, refill_rate)
        b = self.buckets[bucket_id]

        if b["tokens"] >= tokens:
            b["tokens"] -= tokens
            allowed = True
        else:
            allowed = False

        time_to_replenish = max(0.0, (tokens - b["tokens"]) / refill_rate) if not allowed and refill_rate > 0 else 0.0
        return {
            "allowed": allowed,
            "bucket_id": bucket_id,
            "consumed": tokens if allowed else 0.0,
            "available_tokens": round(b["tokens"], 2),
            "capacity": capacity,
            "time_to_replenish_seconds": round(time_to_replenish, 2)
        }

    def get_bucket_status(self, bucket_id: str, capacity: float = 100.0, refill_rate: float = 10.0) -> Dict[str, Any]:
        self._refill(bucket_id, capacity, refill_rate)
        b = self.buckets[bucket_id]
        return {
            "bucket_id": bucket_id,
            "available_tokens": round(b["tokens"], 2),
            "capacity": capacity,
            "refill_rate_per_sec": refill_rate
        }

    def replenish_bucket(self, bucket_id: str, tokens: float, capacity: float = 100.0) -> Dict[str, Any]:
        if bucket_id not in self.buckets:
            self.buckets[bucket_id] = {"tokens": min(capacity, tokens), "last_refill": time.time()}
        else:
            self.buckets[bucket_id]["tokens"] = min(capacity, self.buckets[bucket_id]["tokens"] + tokens)
        return {"bucket_id": bucket_id, "tokens": round(self.buckets[bucket_id]["tokens"], 2)}
