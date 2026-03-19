import httpx
import asyncio

from .functions import extend_url
from ..structs import ServerInfo

async def wait_for_server(server_url: str, interval: float = 5.0, request_timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        timeout=0
        while True:
            try:
                r = await client.get(extend_url(server_url, "/health"))
                if r.status_code < 500:
                    print(f"{server_url} is ready.")
                    return
            except Exception:
                pass

            print(f"{server_url} not ready yet, retrying in {interval}s...")
            timeout += interval
            if timeout > 60:
                raise Exception(f"{server_url} not ready after {timeout} seconds")
            await asyncio.sleep(interval)


async def add_server(server_url: str, info: ServerInfo, request_timeout: float = 10.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        try:
            r = await client.post(
                extend_url(server_url, "/add-server"),
                json=info.model_dump(),
                timeout=request_timeout
            )
            r.raise_for_status()
        except Exception as e:
            print(f"Failed to add Worker {info.model_id} {info.size_id} to {server_url}: {e}")
            raise e

async def remove_server(server_url: str, info: ServerInfo, request_timeout: float = 5.0):
    async with httpx.AsyncClient(timeout=request_timeout) as client:
        try:
            r = await client.post(
                extend_url(server_url, "/remove-server"),
                json=info.model_dump(),
                timeout=request_timeout
            )
            r.raise_for_status()
        except Exception as e:
            print(f"Failed to remove Worker {info.model_id} {info.size_id} from {server_url}: {e}")
            raise e