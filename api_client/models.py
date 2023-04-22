from typing import TypeVar
from pydantic import BaseModel
import httpx

SubtypeBaseModel = TypeVar("SubtypeBaseModel", bound=BaseModel)

class Response:
    def __init__(self, response: httpx.Response) -> None:
        self.raw_response = response
        self.status_code = response.status_code