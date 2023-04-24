import httpx
from typing import TypeVar, Any
import logging
from api_client.settings import ClientSettings
from pydantic import BaseModel
from api_client.plugins import BasePlugin, SettingsPluginMapper, NotFoundPluginForSettings
from api_client.models import SubtypeBaseModel, Response, AnyPluginSettings, HttpMethod


Headers = dict[str, str]
SubtypeBasePlugin = TypeVar("SubtypeBasePlugin", bound=BasePlugin)


class ApiMethod:
    def __init__(self,
        client: httpx.AsyncClient,
        endpoint: str,
        headers: Headers,
        method: HttpMethod,
        path_params: list[str],
        plugins: list[SubtypeBasePlugin]
    ) -> None:
        self._client = client
        self._endpoint = endpoint
        self._headers = headers
        self._method = method
        self._path_params = path_params
        self._plugins = plugins

    async def _call(
        self,
        headers: Headers | None = None,
        path_params: dict[str, Any] | None = None,
        body: SubtypeBaseModel | str | None = None,
    ) -> Response:
        if isinstance(body, BaseModel):
            body = body.json()

        raw_response = await self._client.request(
            url=self._endpoint.format(**path_params),
            method=self._method.value,
            headers=self._merge_headers(self._headers, headers),
            json=body
        )
        return Response(raw_response)
    
    @staticmethod
    async def plugin_initiator(fn, *args, **kwargs):
        return await fn(*args, **kwargs)

    async def __call__(
        self,
        headers: Headers | None = None,
        path_params: dict[str, Any] | None = None,
        body: SubtypeBaseModel | str | None = None,
    ) -> Response:
        return await self.plugin_initiator(
            *self._plugins,
            self._call,
            body=body,
            path_params=path_params,
            headers=headers
        )


class Client:
    def __init__(self, settings: ClientSettings) -> None:
        self._client = httpx.AsyncClient(base_url=settings.base_url)

    def build_api_method(
        self,
        endpoint: str,
        method: HttpMethod,
        headers: Headers,
        data: SubtypeBaseModel,
        path_params: list[str],
        plugins_settings: list[AnyPluginSettings],
    ):
        logging.info("It's logs")
    
        self._check_path_params(endpoint, path_params)
    
        plugins = self._build_plugins(plugins_settings)

        return ApiMethod(
            endpoint=endpoint,
            headers=headers,
            method=method,
            data=data,
            path_params=path_params,
            plugins=plugins,
        )

    def _build_plugins(self, plugins_settings: list[AnyPluginSettings]):
        plugins = []

        for settings in plugins_settings:
            try:
                plugin_cls = SettingsPluginMapper[settings]
            except KeyError:
                raise NotFoundPluginForSettings(settings)

            plugins.append(plugin_cls(settings))

        return plugins
