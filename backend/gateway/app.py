import os

from fastapi import FastAPI

from .structs import ServerInfo
from .utils import prints, add_server

GATEWAY_HOST = os.getenv("GATEWAY_HOST", "localhost")
GATEWAY_PORT = os.getenv("GATEWAY_PORT", "8000")

servers: list[ServerInfo] = []

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/add-server-info")
async def receive_server_info(server: ServerInfo):
    add_server(servers, server)
    prints(f"Registered server: {server}")
    return {"registered": True}