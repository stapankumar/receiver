from flask import Flask, request

app = Flask(__name__)

#store latest notification globally
latest_notification = {
    "headers": None,
    "payload": None,
    "path": None,
    "method": None
}

@app.route("/ae", methods=["POST"])
def receive():
    print("\n📬 Notification received!", flush=True)
    print(f"🔗 URL Path: {request.path}", flush=True)
    print(f"📨 Method: {request.method}", flush=True)
    print(f"📥 Headers:\n{request.headers}", flush=True)
    try:
        payload = request.get_data(as_text=True)
        print(f"📦 Raw Payload:\n{payload}", flush=True)
    except Exception as e:
        print(f"⚠️ Failed to decode payload: {e}", flush=True)

    #update latest notification
    latest_notification = {
        "headers": dict(request.headers),
        "payload": payload,
        "path": request.path,
        "method": request.method
    }

    return "", 200  #only status with no body or oneM2M compliant body can be returned

@app.route("/")
def health():
    if latest_notification["payload"] is None:
        return "✅ Receiver up. No notifications received yet.", 200

    #show latest notification in a simple HTML format
    return f"""
    <h2>📬 Latest Notification Received</h2>
    <p><b>Path:</b> {latest_notification['path']}</p>
    <p><b>Method:</b> {latest_notification['method']}</p>
    <p><b>Headers:</b></p>
    <pre>{latest_notification['headers']}</pre>
    <p><b>Payload:</b></p>
    <pre>{latest_notification['payload']}</pre>
    """, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
