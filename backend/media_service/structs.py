from pydantic import BaseModel

class IdName(BaseModel):
    id: str
    name: str

class ServerInfo(BaseModel):
    url: str
    model_id: str
    size_id: str

class Model(BaseModel):
    model: IdName
    sizes: list[IdName]
    tasks: list[IdName]