from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/proxy/dashboard")
def dashboard():
    return HTMLResponse("""
        <h1>EBC Earn Per Run</h1>
        <p>Dashboard placeholder</p>
    """)
