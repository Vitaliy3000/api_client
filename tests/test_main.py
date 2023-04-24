from pydantic import BaseModel

from api_client import (
    Client,
    ClientSettings,
    HttpMethod,
    ValidatorPluginSettings,
    RetryPluginSettings,
    CachePlugin,
    cache_key_builder,
)


class UserModel(BaseModel):
    id: str


class ExampleSDK:
    def __init__(self, base_url: str, redis_client):        
        self._client = Client(ClientSettings(base_url=base_url))
        self._redis_client = redis_client

        self.get_user = self._client.build_api_method(
            endpoint="/user/{id}",
            method=HttpMethod.GET,
            path_params=["id"],
            plugins_settings=[
                ValidatorPluginSettings(
                    on_200=UserModel,
                ),
                RetryPluginSettings(
                    count_attempt=3,
                ),
                CachePlugin(
                    get_redis_client=lambda: self._redis_client,
                    calc_cache_key=self._build_cache_key_func,
                )
            ]
        )

    @cache_key_builder
    @staticmethod
    def _build_cache_key_func(path_params, *args, **kwargs):
        return path_params["id"]





class TestApiClient:
    pass
