import json

def parse_edu(payload):
    try:
        return json.loads(payload) if isinstance(payload, str) else payload
    except Exception:
        return {}
