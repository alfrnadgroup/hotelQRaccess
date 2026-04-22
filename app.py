from aiohttp import web
from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

routes = web.RouteTableDef()

@routes.get('/')
async def home(request):
    return web.Response(text="Hotel QR Access System Running")

@routes.get('/generate_qr')
async def generate_qr(request):
    room = request.query.get("room", "101")

    token = generate_token(room)
    img_bytes = generate_qr_image(token)

    return web.Response(body=img_bytes, content_type='image/png')

@routes.post('/verify')
async def verify(request):
    data = await request.json()
    token = data.get("token")

    valid, decoded = verify_token(token)

    return web.json_response({
        "valid": valid,
        "data": decoded
    })

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=8080)