import os
import json
from aiohttp import web
from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

routes = web.RouteTableDef()

# Home page
@routes.get('/')
async def index(request):
    return web.FileResponse('./templates/index.html')


# Generate QR
@routes.get('/generate_qr')
async def generate_qr(request):
    data = request.query.get("data", None)

    if not data:
        return web.json_response({"error": "missing data"})

    token = generate_token(data)
    img_bytes = generate_qr_image(token)

    return web.Response(body=img_bytes, content_type='image/png')


# Verify QR (door side)
@routes.post('/verify')
async def verify(request):
    body = await request.json()
    token = body.get("token")

    valid, decoded = verify_token(token)

    return web.json_response({
        "valid": valid,
        "data": decoded
    })


app = web.Application()
app.add_routes(routes)

PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)