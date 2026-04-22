import jwt
import time

SECRET = "CHANGE_THIS_SECRET"

def generate_token(room, duration=86400):
    payload = {
        "room": room,
        "iat": int(time.time()),
        "exp": int(time.time()) + duration
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return True, decoded
    except Exception as e:
        return False, str(e)