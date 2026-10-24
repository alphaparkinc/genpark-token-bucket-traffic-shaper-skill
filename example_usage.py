"""Example usage for GenPark Token Bucket Traffic Shaper."""
from client import TokenBucketTrafficShaper

def main():
    shaper = TokenBucketTrafficShaper()
    bucket = "claude_stream_token_bucket"

    print("Consuming tokens (burst capacity: 50, refill: 10/s)...")
    res1 = shaper.consume_tokens(bucket, tokens=30.0, capacity=50.0, refill_rate=10.0)
    print(f"Consumed 30: Allowed={res1['allowed']}, Remaining={res1['available_tokens']}")

    res2 = shaper.consume_tokens(bucket, tokens=30.0, capacity=50.0, refill_rate=10.0)
    print(f"Consumed 30 again: Allowed={res2['allowed']}, Time to replenish={res2['time_to_replenish_seconds']}s")

    print("
Bucket Status:", shaper.get_bucket_status(bucket, capacity=50.0, refill_rate=10.0))

if __name__ == "__main__":
    main()
