from pydantic import BaseModel

class ServerInfo(BaseModel):
    url: str
    model_name: str
    model_size: str