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
    return web.json_response({"status": "HOTEL QR SYSTEM RUNNING"})

# =========================
# GENERATE QR
# =========================
@routes.get('/generate_qr')
async def generate_qr(request):

    data = request.query.get("data")

    if not data:
        return web.json_response({"error": "missing data"}, status=400)

    token = generate_token(data)
    img_bytes = generate_qr_image(token)

    return web.Response(body=img_bytes, content_type='image/png')

# =========================
# VERIFY QR
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=False
)

# =========================
# RUN SERVER (RENDER SAFE)
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    print("HOTEL QR STARTING ON PORT:", port)

    web.run_app(
        app,
        host="0.0.0.0",
        port=port
)
