from flask import Flask, request

app = Flask(__name__)

@app.route("/ae", methods=["POST"])
def receive():
    print("Notification received:", request.data.decode())
    return "ACK", 200

@app.route("/")
def health():
    return "Receiver up", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
