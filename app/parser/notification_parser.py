import json

def parse_generic(payload):
    try:
        return json.loads(payload)
    except Exception:
        return {"raw_payload": payload}
