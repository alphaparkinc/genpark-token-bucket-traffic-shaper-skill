"""MCP Stdio Server for Token Bucket Traffic Shaper.
100% Python Standard Library.
"""
import sys
import json
from client import TokenBucketTrafficShaper

shaper = TokenBucketTrafficShaper()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-token-bucket-traffic-shaper-skill", "version": "1.0.1"},
            "capabilities": {"tools": {}}
        }
        send_response(req_id, res)
    elif method == "tools/list":
        tools = [
            {
                "name": "consume_tokens",
                "description": "Attempt to consume tokens from bucket for rate shaping",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "bucket_id": {"type": "string"},
                        "tokens": {"type": "number", "default": 1.0},
                        "capacity": {"type": "number", "default": 100.0},
                        "refill_rate": {"type": "number", "default": 10.0}
                    },
                    "required": ["bucket_id"]
                }
            },
            {
                "name": "get_bucket_status",
                "description": "Check current token level and replenishment rate",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "bucket_id": {"type": "string"},
                        "capacity": {"type": "number", "default": 100.0},
                        "refill_rate": {"type": "number", "default": 10.0}
                    },
                    "required": ["bucket_id"]
                }
            },
            {
                "name": "replenish_bucket",
                "description": "Manually inject tokens into a traffic bucket",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "bucket_id": {"type": "string"},
                        "tokens": {"type": "number"},
                        "capacity": {"type": "number", "default": 100.0}
                    },
                    "required": ["bucket_id", "tokens"]
                }
            }
        ]
        send_response(req_id, {"tools": tools})
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "consume_tokens":
            out = shaper.consume_tokens(
                args.get("bucket_id", ""),
                float(args.get("tokens", 1.0)),
                float(args.get("capacity", 100.0)),
                float(args.get("refill_rate", 10.0))
            )
        elif name == "get_bucket_status":
            out = shaper.get_bucket_status(
                args.get("bucket_id", ""),
                float(args.get("capacity", 100.0)),
                float(args.get("refill_rate", 10.0))
            )
        elif name == "replenish_bucket":
            out = shaper.replenish_bucket(
                args.get("bucket_id", ""),
                float(args.get("tokens", 0.0)),
                float(args.get("capacity", 100.0))
            )
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return
        send_response(req_id, {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]})

def send_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
