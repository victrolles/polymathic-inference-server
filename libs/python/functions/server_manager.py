from ..structs.general import ServerInfo

class ServerRegistry:
    def __init__(self, servers: list[ServerInfo]):
        self.servers = servers

        self.server_by_model: dict[str, ServerInfo] = {}
        self.server_by_model_size: dict[tuple[str, str], ServerInfo] = {}

    def add_to_registry(self, server: ServerInfo):
        if server.size_id is None:
            self.server_by_model[server.model_id] = server
        else:
            self.server_by_model_size[(server.model_id, server.size_id)] = server

    def remove_from_registry(self, server: ServerInfo):
        if server.size_id is None:
            self.server_by_model.pop(server.model_id)
        else:
            self.server_by_model_size.pop((server.model_id, server.size_id))

    def is_in_registry(self, server: ServerInfo) -> bool:
        if server.size_id is None:
            return server.model_id in self.server_by_model
        else:
            return (server.model_id, server.size_id) in self.server_by_model_size

    def get(self, server: ServerInfo) -> ServerInfo:
        if server.size_id is None:
            return self.server_by_model[server.model_id]
        else:
            return self.server_by_model_size[(server.model_id, server.size_id)]

    def get_server_by_model(self, model_id: str) -> ServerInfo:
        return self.server_by_model[model_id]

    def get_server_by_model_size(self, model_id: str, size_id: str) -> ServerInfo:
        return self.server_by_model_size[(model_id, size_id)]

class ServerManager:
    def __init__(self):
        self.servers: list[ServerInfo] = []
        self.registry: ServerRegistry = ServerRegistry(self.servers)

    def add_server(self, server: ServerInfo):
        if self.registry.is_in_registry(server):
            self.servers.remove(self.registry.get(server))
        self.servers.append(server)
        self.registry.add_to_registry(server)

    def remove_server(self, server: ServerInfo):
        if self.registry.is_in_registry(server):
            self.servers.remove(self.registry.get(server))
            self.registry.remove_from_registry(server)
