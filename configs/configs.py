from typing import Union
from pydantic import BaseModel, HttpUrl, FilePath


class InputConfig(BaseModel):
    path: Union[HttpUrl, FilePath]
    extension: str
