from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from core.security import generate_token, verify_token
from core.database import save_booking, get_booking, get_all
import datetime
import os

app = Flask(__name__)

# ?? BRIDGE: allow ONLY your frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://hotelqraccess.onrender.com"
        ]
    }
})


# -------------------------
# HEALTH CHECK (BRIDGE TEST)
# -------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "REALACCESS BACKEND RUNNING",
        "bridge": "active"
    })


# -------------------------
# CHECK-IN (FRONTEND ? BACKEND BRIDGE)
# -------------------------
@app.route("/api/checkin", methods=["POST"])
def checkin():

    data = request.get_json()

    # ? validation layer (important for real system)
    required = ["room", "name", "guest_id", "checkin", "checkout"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"missing {r}"}), 400

    booking = {
        "room": data["room"],
        "name": data["name"],
        "guest_id": data["guest_id"],
        "checkin": data["checkin"],
        "checkout": data["checkout"],
        "created_at": str(datetime.datetime.utcnow())
    }

    # store booking
    save_booking(data["room"], booking)

    # generate secure token
    token = generate_token({
        "room": data["room"],
        "guest_id": data["guest_id"]
    })

    return jsonify({
        "qr_token": token,
        "status": "stored"
    })


# -------------------------
# VALIDATE QR (ADMIN SCANNER)
# -------------------------
@app.route("/api/validate", methods=["POST"])
def validate():

    token = request.json.get("token")

    if not token:
        return jsonify({"access": "DENIED", "reason": "missing token"}), 400

    decoded = verify_token(token)

    if not decoded:
        return jsonify({"access": "DENIED", "reason": "invalid token"})

    booking = get_booking(decoded["room"])

    if not booking:
        return jsonify({"access": "DENIED", "reason": "no booking"})

    now = datetime.datetime.utcnow()

    try:
        checkout = datetime.datetime.fromisoformat(booking["checkout"])

        if now > checkout:
            return jsonify({
                "access": "DENIED",
                "reason": "expired"
            })

    except:
        return jsonify({
            "access": "DENIED",
            "reason": "date error"
        })

    return jsonify({
        "access": "GRANTED",
        "room": decoded["room"],
        "guest": booking["name"]
    })


# -------------------------
# BOOKINGS (ADMIN PANEL DATA)
# -------------------------
@app.route("/api/bookings")
def bookings():
    return jsonify(get_all())


# -------------------------
# ADMIN UI (QR SCANNER PAGE)
# -------------------------
@app.route("/admin")
def admin():
    return render_template("admin.html")


# -------------------------
# RUN SERVER (RENDER SAFE)
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)