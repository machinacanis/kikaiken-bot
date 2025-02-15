from pydantic import BaseModel

class Config(BaseModel):
    sqlite_path: str = ""