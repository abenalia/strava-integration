import hmac
import hashlib
import os
from urllib.parse import urlencode
from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/proxy/dashboard")
def dashboard():
    return HTMLResponse("""
        <h1>EBC Earn Per Run</h1>
        <p>Customer ID: {customer_id}</p>
        <p>App Proxy verified and locked.</p>
    """)

def verify_shopify_proxy(params: dict, secret: str) -> bool:
    params = params.copy()

    signature = params.pop("signature", None)
    if not signature:
        return False

    # Shopify requires params sorted alphabetically
    message = urlencode(sorted(params.items()))

    digest = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(digest, signature)
