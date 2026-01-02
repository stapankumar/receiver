from flask import Blueprint, request, jsonify
from app.db.notifications_repo import insert_notification, fetch_latest, fetch_recent

core_bp = Blueprint("core", __name__)

@core_bp.route("/notify", methods=["POST"])
def receive():
    print("\nNotification received!", flush=True)
    print(f"URL Path: {request.path}", flush=True)
    print(f"Method: {request.method}", flush=True)
    print(f"Headers:\n{request.headers}", flush=True)
    try:
        payload = request.get_data(as_text=True)
        print(f"Raw Payload:\n{payload}", flush=True)

        insert_notification(
            request.path,
            request.method,
            request.headers,
            payload
        )

        print("Notification stored", flush=True)

    except Exception as e:
        print(f"Failed to decode payload: {e}", flush=True)

    return "", 200  #only status with no body or oneM2M compliant body can be returned

@core_bp.route("/")
def home():
    return "Receiver is up and running.", 200

@core_bp.route("/getLatest")
def latest():
    row = fetch_latest()
    if row is None:
        return "Receiver is up. No notifications received yet.", 200

    #show latest notification in a simple HTML format
    return f"""
    <h2>Latest Notification Received</h2>
    <p><b>Path:</b> {row[0]}</p>
    <p><b>Method:</b> {row[1]}</p>
    <p><b>Headers:</b></p>
    <pre>{row[2]}</pre>
    <p><b>Payload:</b></p>
    <pre>{row[3]}</pre>
    """, 200

@core_bp.route("/notifications", methods=["GET"])
def get_notifications():
    rows = fetch_recent(50)

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "payload": r[1],
            "received_at": r[2].isoformat()
        })

    return jsonify(result)