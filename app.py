import os
import json
from aiohttp import web

from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

routes = web.RouteTableDef()


# =========================
# 🏠 HOME PAGE
# =========================
@routes.get('/')
async def index(request):
    return web.FileResponse('./templates/index.html')


# =========================
# 🧾 GENERATE QR
# =========================
@routes.get('/generate_qr')
async def generate_qr(request):

    data = request.query.get("data")

    if not data:
        return web.json_response({"error": "missing data"}, status=400)

    try:
        payload = json.loads(data)
    except:
        return web.json_response({"error": "invalid JSON"}, status=400)

    room = payload.get("room")

    if not room:
        return web.json_response({"error": "missing room"}, status=400)

    # ✅ ONLY ROOM goes into token
    token = generate_token(room)

    img_bytes = generate_qr_image(token)

    return web.Response(body=img_bytes, content_type='image/png')


# =========================
# 🔐 VERIFY QR
# =========================
@routes.post('/verify')
async def verify(request):

    try:
        body = await request.json()
        token = body.get("token")

        if not token:
            return web.json_response({"error": "missing token"}, status=400)

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
# 🚀 APP SETUP
# =========================
app = web.Application()
app.add_routes(routes)


# =========================
# 📁 STATIC FILES (LOGO FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=True
)


# =========================
# 🌐 RUN SERVER (RENDER SAFE)
# =========================
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    print("Server starting on port:", PORT)
    web.run_app(app, host="0.0.0.0", port=PORT)
