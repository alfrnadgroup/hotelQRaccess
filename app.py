import os
import json
import tempfile
import aiohttp

from aiohttp import web

from utils.token import generate_token, verify_token
from utils.qr import generate_qr_image

routes = web.RouteTableDef()

WHATSAPP_TOKEN = os.getenv("EAATDkqdl5CQBRsBdB7ZC9BMByZCrdg5ZAxhHiJFK67GZCeE7tXjPFu8Jr5K3VMjQBZBfpv3XAMSxl7Cgn1rUUIyZBZAjTwVZA0njmZBHeRZAAu59DpB803QJnZARkJk251XLMsmC4kXtzyw5zZCbdJ1TGHfpAjmnvZAe8YQtCiMgIuAHNgXhswfhDGclEIZBaUGet4ABOCUZCPZAZAwwhuqU8ci3wY6whyrUBpSgi2eAonoObHyONhgtZC1XiKqwZDZD")
PHONE_NUMBER_ID = os.getenv("1159465090580320")


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
        return web.json_response(
            {"error": "missing data"},
            status=400
        )

    token = generate_token(data)

    img_bytes = generate_qr_image(token)

    return web.Response(
        body=img_bytes,
        content_type='image/png'
    )


# =========================
# SEND PDF TO WHATSAPP
# =========================
@routes.post('/send_whatsapp_pdf')
async def send_whatsapp_pdf(request):

    try:

        reader = await request.multipart()

        pdf_part = await reader.next()

        if not pdf_part:
            return web.json_response(
                {
                    "success": False,
                    "error": "PDF missing"
                },
                status=400
            )

        pdf_bytes = await pdf_part.read()

        phone_part = await reader.next()

        if not phone_part:
            return web.json_response(
                {
                    "success": False,
                    "error": "Phone missing"
                },
                status=400
            )

        phone = await phone_part.text()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        temp_file.write(pdf_bytes)
        temp_file.close()

        headers = {
            "Authorization":
                f"Bearer {WHATSAPP_TOKEN}"
        }

        async with aiohttp.ClientSession() as session:

            upload_data = aiohttp.FormData()

            upload_data.add_field(
                "messaging_product",
                "whatsapp"
            )

            upload_data.add_field(
                "file",
                open(temp_file.name, "rb"),
                filename="QRswoopAccess-card.pdf",
                content_type="application/pdf"
            )

            upload_url = (
                f"https://graph.facebook.com/v23.0/"
                f"{PHONE_NUMBER_ID}/media"
            )

            async with session.post(
                upload_url,
                headers=headers,
                data=upload_data
            ) as upload_response:

                upload_result = (
                    await upload_response.json()
                )

            if "id" not in upload_result:

                return web.json_response(
                    {
                        "success": False,
                        "error": upload_result
                    },
                    status=400
                )

            media_id = upload_result["id"]

            message_payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "document",
                "document": {
                    "id": media_id,
                    "filename":
                        "QRswoopAccess-card.pdf"
                }
            }

            send_url = (
                f"https://graph.facebook.com/v23.0/"
                f"{PHONE_NUMBER_ID}/messages"
            )

            async with session.post(
                send_url,
                headers={
                    **headers,
                    "Content-Type":
                        "application/json"
                },
                json=message_payload
            ) as send_response:

                send_result = (
                    await send_response.json()
                )

        try:
            os.remove(temp_file.name)
        except:
            pass

        return web.json_response({
            "success": True,
            "result": send_result
        })

    except Exception as e:

        return web.json_response(
            {
                "success": False,
                "error": str(e)
            },
            status=500
        )


# =========================
# VERIFY QR (ADMIN SCANNER)
# =========================
@routes.post('/verify')
async def verify(request):

    try:

        body = await request.json()

        token = body.get("token")

        if not token:

            return web.json_response({
                "valid": False,
                "error": "missing token"
            })

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
# ADMIN PAGE
# =========================
@routes.get('/admin')
async def admin(request):
    return web.FileResponse(
        './templates/admin.html'
    )


# =========================
# APP SETUP
# =========================
app = web.Application()

app.add_routes(routes)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

app.router.add_static(
    '/static',
    os.path.join(BASE_DIR, 'static'),
    show_index=False
)


# =========================
# RUN
# =========================
if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 8080)
    )

    web.run_app(
        app,
        host="0.0.0.0",
        port=port
    )
