from .structs import ServerInfo

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(info):
    print(f"[GATEWAY]:    {info}")

def add_server(servers: list[ServerInfo], new_server: ServerInfo):
    for server in servers:
        if (server.model_id == new_server.model_id) and (server.size_id == new_server.size_id):
            prints(f"Old server {server.model_id} : {server.size_id} has been replaced : {server.url} -> {new_server.url}")
            servers.remove(server)
            break
    servers.append(new_server)
    prints(f"New server registered: {new_server.url}")
