import os
import asyncio
from aiohttp import web

from utils.token import generate_token, verify_token

routes = web.RouteTableDef()

# =========================
# MEMORY DB
# =========================
BOOKINGS = {}

# =========================
# HOME
# =========================
@routes.get('/')
async def home(request):
    return web.json_response({"status": "REALACCESS RUNNING"})

# =========================
# CHECKIN
# =========================
@routes.post('/api/checkin')
async def checkin(request):
    data = await request.json()

    room = data["room"]

    BOOKINGS[room] = data

    token = generate_token({
        "room": room,
        "guest_id": data["guest_id"]
    })

    return web.json_response({"qr_token": token})

# =========================
# VERIFY
# =========================
@routes.post('/verify')
async def verify(request):
    body = await request.json()
    token = body.get("token")

    valid, decoded = verify_token(token)

    if not valid:
        return web.json_response({"valid": False})

    room = decoded.get("room")

    return web.json_response({
        "valid": True,
        "room": room,
        "guest": BOOKINGS.get(room, {}).get("name")
    })

# =========================
# APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=False
)

# =========================
# RENDER SAFE START (IMPORTANT FIX)
# =========================
async def init_app():
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    web.run_app(
        init_app(),
        host="0.0.0.0",
        port=port
    )
    body = await request.json()
    token = body.get("token")

    valid, decoded = verify_token(token)

    return web.json_response({
        "valid": valid,
        "data": decoded
    })

# =========================
# APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)

# =========================
# STATIC FILES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=True
)

# =========================
# RUN (RENDER SAFE)
# =========================
PORT = int(os.environ.get("PORT", 8080))

print("Starting on port:", PORT)

web.run_app(app, host="0.0.0.0", port=PORT)async def verify(request):

    body = await request.json()
    token = body.get("token")

    valid, decoded = verify_token(token)

    return web.json_response({
        "valid": valid,
        "data": decoded
    })

# =========================
# APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)

# =========================
# STATIC FILES (FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=True
)

# =========================
# RUN
# =========================
PORT = int(os.environ.get("PORT", 8080))

web.run_app(app, host="0.0.0.0", port=PORT)    return web.json_response({
        "valid": valid,
        "data": decoded
    })


app = web.Application()
app.add_routes(routes)

PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)
