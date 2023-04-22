import httpx
from typing import TypeVar
import logging
from api_client.settings import Settings
from pydantic import BaseModel
from api_client.plugins import retry
from api_client.models import SubtypeBaseModel


Headers = dict[str, str]




class Request:
    def __init__(
        self,
        client: httpx.AsyncClient,
        endpoint: str,
        headers: Headers,
        method: str
    ) -> None:
        self._client = client
        self._endpoint = endpoint
        self._headers = headers
        self._method = method
        
        self._plugins = [
            Validator(
                
            )
            Retry(
                ...,
            )
        ]

    async def _call(
        self,
        headers: Headers,
        data: SubtypeBaseModel,
    ) -> Response:
        raw_response = await self._client.request(
            url=self._endpoint,
            method=self._method,
            headers=self._merge_headers(self._headers, headers),
            json=data.json()
        )
        return Response(raw_response)

    async def __call__(
        self,
        headers: Headers,
        data: SubtypeBaseModel,
    ) -> Response:

    
        self._call(
            headers=headers,
            data=data
        )
    


class Client:
    def __init__(self, settings: Settings) -> None:
        self._client = httpx.AsyncClient(base_url=settings.base_url)

    def build_method(
        self,
        endpoint: str,
        method: str,
        headers: Headers,
        data: SubtypeBaseModel,
    ):
        logging.info("It's logs")

        return Request(
            endpoint=endpoint,
            headers=headers,
            method=method,
            data=data,
        )
