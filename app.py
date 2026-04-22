import os
import json
from aiohttp import web

from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

routes = web.RouteTableDef()

# =========================
# HOME
# =========================
@routes.get('/')
async def index(request):
    return web.FileResponse('./templates/index.html')

# =========================
# GENERATE QR
# =========================
@routes.get('/generate_qr')
async def generate_qr(request):

    data = request.query.get("data")

    if not data:
        return web.json_response({"error": "missing data"})

    token = generate_token(data)
    img_bytes = generate_qr_image(token)

    return web.Response(body=img_bytes, content_type='image/png')

# =========================
# VERIFY QR
# =========================
@routes.post('/verify')
async def verify(request):

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
