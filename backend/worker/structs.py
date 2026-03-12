from pydantic import BaseModel

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: str