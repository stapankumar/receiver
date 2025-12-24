from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

from parser.notification_parser import parse_notification_payload
from db.notifications_repo import (
    insert_notification,
    fetch_latest,
    fetch_recent
)

load_dotenv()

app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def receive():
    print("\n📬 Notification received!", flush=True)
    print(f"🔗 URL Path: {request.path}", flush=True)
    print(f"📨 Method: {request.method}", flush=True)
    print(f"📥 Headers:\n{request.headers}", flush=True)
    try:
        payload = request.get_data(as_text=True)
        print(f"📦 Raw Payload:\n{payload}", flush=True)

        insert_notification(
            request.path,
            request.method,
            request.headers,
            payload
        )

        print("📬 Notification stored", flush=True)

    except Exception as e:
        print(f"⚠️ Failed to decode payload: {e}", flush=True)

    return "", 200  #only status with no body or oneM2M compliant body can be returned

@app.route("/")
def home():
    return "✅ Receiver is up and running.", 200
    
@app.route("/getLatest")
def latest():
    row = fetch_latest()
    if row is None:
        return "✅ Receiver is up. No notifications received yet.", 200

    #show latest notification in a simple HTML format
    return f"""
    <h2>📬 Latest Notification Received</h2>
    <p><b>Path:</b> {row[0]}</p>
    <p><b>Method:</b> {row[1]}</p>
    <p><b>Headers:</b></p>
    <pre>{row[2]}</pre>
    <p><b>Payload:</b></p>
    <pre>{row[3]}</pre>
    """, 200

@app.route("/notifications", methods=["GET"])
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

@app.route("/agri", methods=["GET"])
def get_parsed_agri_data():
    rows = fetch_recent(50)
    
    parsed_results = []
    for r in rows:
        parsed_con = parse_notification_payload(r[1])

        response_obj = {}

        #flatten sensor data
        if isinstance(parsed_con, dict):
            response_obj.update(parsed_con)

        #append metadata
        response_obj["notification_id"] = r[0]
        response_obj["received_at"] = r[2].isoformat()

        parsed_results.append(response_obj)

    return jsonify(parsed_results)

@app.route("/notify/agri", methods=["POST"])
def receive_agri():
    print("\n🌱 Agri 📬 Notification received!", flush=True)
    print(f"🔗 URL Path: {request.path}", flush=True)
    print(f"📨 Method: {request.method}", flush=True)
    print(f"📥 Headers:\n{request.headers}", flush=True)
    try:
        payload = request.get_data(as_text=True)
        print(f"📦 Raw Payload:\n{payload}", flush=True)

        insert_notification(
            request.path,
            request.method,
            request.headers,
            payload
        )

        print("🌱 Agri 📬 Notification stored", flush=True)

    except Exception as e:
        print(f"⚠️ Failed to decode payload: {e}", flush=True)

    return "", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
