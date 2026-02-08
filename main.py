from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import hmac
import hashlib
import os
from urllib.parse import urlencode

app = FastAPI()

def verify_shopify_proxy(params: dict, secret: str) -> bool:
    params = params.copy()
    signature = params.pop("signature", None)
    if not signature:
        return False

    message = urlencode(sorted(params.items()))
    digest = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(digest, signature)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/proxy/dashboard")
def dashboard(request: Request):
    params = dict(request.query_params)
    secret = os.environ.get("SHOPIFY_API_SECRET")

    if not secret:
        raise HTTPException(status_code=500, detail="Missing Shopify secret")

    if not verify_shopify_proxy(params, secret):
        raise HTTPException(status_code=403, detail="Invalid Shopify signature")

    customer_id = params.get("customer_id")

    if not customer_id:
        return HTMLResponse(
            "<h2>Please log in to view your Earn Per Run dashboard.</h2>",
            status_code=401
        )

    return HTMLResponse(f"""
        <h1>EBC Earn Per Run</h1>
        <p>Customer ID: {customer_id}</p>
        <p>App Proxy verified and locked.</p>
    """)

