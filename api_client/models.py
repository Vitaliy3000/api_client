from typing import TypeVar, Any
from pydantic import BaseModel
import httpx
import enum


SubtypeBaseModel = TypeVar("SubtypeBaseModel", bound=BaseModel)
Headers = dict[str, str]

class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"



class Request:
    def __init__(
        self,
        endpoint: str,
        method: HttpMethod,
        headers: Headers | None = None,
        path_params: dict[str, Any] | None = None,
        body: SubtypeBaseModel | str | None = None,
    ) -> None:
        self._endpoint = endpoint
        self._headers = headers
        self._method = method
        self._path_params = path_params

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def endpoint(self) -> str:
        return self._endpoint.format(**self._path_params)

    @property
    def method(self) -> str:
        self._method.value

    @property
    def headers(self) -> Headers:
        self._merge_headers(self._headers, headers)



class Response:
    def __init__(self, response: httpx.Response) -> None:
        self.raw_response = response
        self.status_code = response.status_code

    def from_json():
        pass

    def to_json():
        pass


