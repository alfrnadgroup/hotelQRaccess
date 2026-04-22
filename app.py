import os
from aiohttp import web

from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

# =========================
# ROUTES
# =========================
routes = web.RouteTableDef()

# =========================
# HOME
# =========================
@routes.get('/')
async def home(request):
    return web.json_response({
        "status": "HOTEL QR ACCESS RUNNING"
    })

# =========================
# GENERATE QR (FRONTEND CALL)
# =========================
@routes.get('/generate_qr')
async def generate_qr(request):

    data = request.query.get("data")

    if not data:
        return web.json_response({"error": "missing data"}, status=400)

    try:
        token = generate_token(data)
        img_bytes = generate_qr_image(token)

        return web.Response(body=img_bytes, content_type='image/png')

    except Exception as e:
        return web.json_response({
            "error": str(e)
        }, status=500)

# =========================
# VERIFY QR (OPTIONAL DOOR SIDE)
# =========================
@routes.post('/verify')
async def verify(request):

    try:
        body = await request.json()
        token = body.get("token")

        valid, decoded = verify_token(token)

        return web.json_response({
            "valid": valid,
            "data": decoded
        })

    except Exception as e:
        return web.json_response({
            "valid": False,
            "error": str(e)
        })

# =========================
# APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)

# =========================
# STATIC FILES (LOGO FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=False
)

# =========================
# RENDER SAFE START
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    print("HOTEL QR ACCESS STARTING ON PORT:", port)

    web.run_app(
        app,
        host="0.0.0.0",
        port=port
    )
    except Exception as e:
        return web.json_response({
            "error": str(e)
        }, status=500)

# =========================
# VERIFY QR (OPTIONAL DOOR SIDE)
# =========================
@routes.post('/verify')
async def verify(request):

    try:
        body = await request.json()
        token = body.get("token")

        valid, decoded = verify_token(token)

        return web.json_response({
            "valid": valid,
            "data": decoded
        })

    except Exception as e:
        return web.json_response({
            "valid": False,
            "error": str(e)
        })

# =========================
# APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)

# =========================
# STATIC FILES (LOGO FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=False
)

# =========================
# RENDER SAFE START
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    print("HOTEL QR ACCESS STARTING ON PORT:", port)

    web.run_app(
        app,
        host="0.0.0.0",
        port=port
    )    return web.json_response({"qr_token": token})

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
