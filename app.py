from flask import Flask, request, jsonify, render_template
from core.security import generate_token, verify_token
from core.database import save_booking, get_booking, get_all
import datetime
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "QR System Running"})


# -------------------------
# CHECK-IN
# -------------------------
@app.route("/api/checkin", methods=["POST"])
def checkin():

    data = request.get_json()

    booking = {
        "room": data["room"],
        "name": data["name"],
        "guest_id": data["guest_id"],
        "checkin": data["checkin"],
        "checkout": data["checkout"],
        "created_at": str(datetime.datetime.utcnow())
    }

    save_booking(data["room"], booking)

    token = generate_token({
        "room": data["room"],
        "guest_id": data["guest_id"]
    })

    return jsonify({"qr_token": token})


# -------------------------
# VALIDATE QR
# -------------------------
@app.route("/api/validate", methods=["POST"])
def validate():

    token = request.json.get("token")

    decoded = verify_token(token)

    if not decoded:
        return jsonify({"access": "DENIED"})

    booking = get_booking(decoded["room"])

    if not booking:
        return jsonify({"access": "DENIED"})

    now = datetime.datetime.utcnow()

    try:
        checkout = datetime.datetime.fromisoformat(booking["checkout"])
        if now > checkout:
            return jsonify({"access": "DENIED", "reason": "expired"})
    except:
        return jsonify({"access": "DENIED", "reason": "date error"})

    return jsonify({
        "access": "GRANTED",
        "room": decoded["room"],
        "guest": booking["name"]
    })


# -------------------------
# BOOKINGS
# -------------------------
@app.route("/api/bookings")
def bookings():
    return jsonify(get_all())


# -------------------------
# ADMIN PAGE (QR SCANNER)
# -------------------------
@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)