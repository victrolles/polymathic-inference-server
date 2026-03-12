import os

from fastapi import FastAPI

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Gateway Server!"}