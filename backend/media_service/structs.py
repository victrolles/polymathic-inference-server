from pydantic import BaseModel

class IdName(BaseModel):
    id: str
    name: str

class ServerInfo(BaseModel):
    url: str
    model_name: str
    model_size: str

class Model(BaseModel):
    model: IdName
    sizes: list[IdName]
    tasks: list[IdName]