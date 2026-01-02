import json

def parse_water(payload):
    try:
        return json.loads(payload) if isinstance(payload, str) else payload
    except Exception:
        return {}
