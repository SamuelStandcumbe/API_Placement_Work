from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# demo users
USERS = {"alice": "password123", "bob": "hunter2"}

# in-memory store of issued tokens
ACTIVE_TOKENS = {}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if USERS.get(username) == password:
        token = secrets.token_hex(16)
        ACTIVE_TOKENS[token] = username   # remember whose token it is
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/data", methods=["GET"])
def protected_data():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid token"}), 403

    token = auth_header.split(" ")[1]
    if token not in ACTIVE_TOKENS:
        return jsonify({"error": "Unauthorized"}), 403

    username = ACTIVE_TOKENS[token]
    return jsonify({"message": f"Welcome {username}, here’s your protected data!"}), 200

@app.route("/hello")
def hello():
    return "Hello, Locust!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)