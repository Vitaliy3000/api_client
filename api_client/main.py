import httpx
import itertools
from typing import TypeVar, Any
import logging
from api_client.settings import ClientSettings
from pydantic import BaseModel
from api_client.plugins import BasePlugin, SettingsPluginMapper, NotFoundPluginForSettings
from api_client.models import SubtypeBaseModel, Response, AnyPluginSettings, HttpMethod, Request, Headers
from api_client.plugins import AnyPluginSettings


class ApiMethod:
    def __init__(self,
        client: httpx.AsyncClient,
        endpoint: str,
        headers: Headers,
        method: HttpMethod,
        path_params: list[str],
        plugins: list[AnyPluginSettings]
    ) -> None:
        self._client = client
        self._endpoint = endpoint
        self._headers = headers
        self._method = method
        self._path_params = path_params
        self._plugins = plugins

    async def _call(self, *, request: Request) -> Response:
        raw_response = await self._client.request(
            url=request.endpoint,
            method=request.method,
            headers=request.headers,
            json=request.body
        )
        return Response(raw_response)

    @staticmethod
    async def _plugin_initiator(function, *other_function, request):
        return await function(*other_function, request=request)

    async def __call__(
        self,
        headers: Headers | None = None,
        path_params: dict[str, Any] | None = None,
        body: SubtypeBaseModel | str | None = None,
    ) -> Response:
        request = Request(
            endpoint=self._endpoint,
            path_params=path_params,
            headers=headers,
            body=body,
        )

        return await self._plugin_initiator(
            *self._plugins,
            self._call,
            request=request,
        )


class Client:
    def __init__(
        self,
        settings: ClientSettings,
        plugins_settings: list[AnyPluginSettings],
    ) -> None:
        self._plugins_settings = plugins_settings
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

        for settings in itertools.chain(self._plugins_settings, plugins_settings):
            try:
                plugin_cls = SettingsPluginMapper[settings]
            except KeyError:
                raise NotFoundPluginForSettings(settings)

            plugins.append(plugin_cls(settings))

        return plugins
