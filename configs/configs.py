from pydantic import BaseModel, HttpUrl


class InputConfig(BaseModel):
    path: HttpUrl
    extension: str
