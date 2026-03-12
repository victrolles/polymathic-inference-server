from .structs import ServerInfo

def extend_url(url: str, path: str) -> str:
    return url.rstrip("/") + path

def prints(info):
    print(f"[GATEWAY]:    {info}")

def add_server(servers: list[ServerInfo], new_server: ServerInfo):
    for server in servers:
        if (server.model_name == new_server.model_name) and (server.model_size == new_server.model_size):
            prints(f"Old server {server.model_name} : {server.model_size} has been replaced : {server.url} -> {new_server.url}")
            servers.remove(server)
            break
    servers.append(new_server)
    prints(f"New server registered: {new_server.url}")
    prints(f"Available servers: {servers}")
