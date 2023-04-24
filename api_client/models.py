from typing import TypeVar
from pydantic import BaseModel
import httpx
import enum
from api_client.plugins import (
    ValidatorPluginSettings,
    RetryPluginSettings,
    CachePluginSettings
)


SubtypeBaseModel = TypeVar("SubtypeBaseModel", bound=BaseModel)
AnyPluginSettings = (
    ValidatorPluginSettings
    | RetryPluginSettings
    | CachePluginSettings
)

class Response:
    def __init__(self, response: httpx.Response) -> None:
        self.raw_response = response
        self.status_code = response.status_code

    def from_json():
        pass

    def to_json():
        pass


class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
