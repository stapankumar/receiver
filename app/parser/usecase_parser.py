import app.parser.parser_registry as parser_registry

PARSER_REGISTRY = parser_registry.PARSER_REGISTRY

def parse_usecase_notification(parser_type, payload):
    """
    Parses usecase oneM2M notification payload.

    Assumptions:
    - payload is already a Python dict (Postgres jsonb)
    - payload structure is fixed for usecase notifications
    - 'con' is always a dict with sensor values
    """

    parser = PARSER_REGISTRY.get(parser_type).get("parser")
    if not parser:
        print(f"[WARN] No parser registered for type: {parser_type}", flush=True)
        return {}

    try:
        return parser(payload)
    except Exception as e:
        print(f"[ERROR] Parser failed [{parser_type}]: {e}", flush=True)
        return {}
    
def parse_usecase_summary(parser_type, rows):
    """
    Dispatch summary parsing for a usecase.
    rows: [(id, payload, received_at), ...]
    """

    entry = PARSER_REGISTRY.get(parser_type)
    if not entry:
        print(f"[WARN] No parser registry for type: {parser_type}", flush=True)
        return {}

    summary_parser = entry.get("summary")
    if not summary_parser:
        print(f"[WARN] No summary parser for type: {parser_type}", flush=True)
        return {}

    try:
        return summary_parser(rows)
    except Exception as e:
        print(f"[ERROR] Summary parser failed [{parser_type}]: {e}", flush=True)
        return {}
    
