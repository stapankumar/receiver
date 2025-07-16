from flask import Flask, request

app = Flask(__name__)

@app.route("/ae", methods=["POST"])
def receive():
    print("\n📬 Notification received!")
    print(f"🔗 URL Path: {request.path}")
    print(f"📨 Method: {request.method}")
    print(f"📥 Headers:\n{request.headers}")
    try:
        payload = request.get_data(as_text=True)
        print(f"📦 Raw Payload:\n{payload}")
    except Exception as e:
        print(f"⚠️ Failed to decode payload: {e}")

    return "", 200  #only status with no body or oneM2M compliant body can be returned

@app.route("/")
def health():
    return "Receiver up", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
