def parse_notification_payload(payload):
    """
    Parses agri oneM2M notification payload.

    Assumptions:
    - payload is already a Python dict (Postgres jsonb)
    - payload structure is fixed for agri notifications
    - 'con' is always a dict with sensor values
    """

    if not payload or not isinstance(payload, dict):
        return {}

    try:
        con = (
            payload["m2m:sgn"]
                   ["nev"]
                   ["rep"]
                   ["any"]
                   ["con"]
        )
    except (KeyError, TypeError):
        return {}

    if isinstance(con, dict):
        return con

    return {}
