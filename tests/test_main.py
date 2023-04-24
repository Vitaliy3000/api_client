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




class ExampleCRUDItemSDK:
    def __init__(self, base_url: str, redis_client):        
        self._client = Client(
            ClientSettings(base_url=base_url),
            plugins_settings=[
                RetryPluginSettings(
                    count_attempt=3,
                ),
            ]
        )
        self._redis_client = redis_client

        self.get_item = self._client.build_api_method(
            endpoint="/items/{id}",
            method=HttpMethod.GET,
            plugins_settings=[
                ValidatorPluginSettings(
                    on_200=ItemModel,
                ),
                CachePlugin(
                    get_redis_client=lambda: self._redis_client,
                    calc_cache_key=self._build_cache_key_func_for_get_item,
                    ttl=60,
                )
            ]
        )

        self.get_items = self._client.build_api_method(
            endpoint="/items",
            method=HttpMethod.GET,
            plugins_settings=[
                ValidatorPluginSettings(
                    on_request=GetItemsModel,
                    on_200=ItemsModel,
                ),
                CachePlugin(
                    get_redis_client=lambda: self._redis_client,
                    calc_cache_key=self._build_cache_key_func_for_get_items,
                    ttl=60,
                )
            ]
        )

        self.create_item = self._client.build_api_method(
            endpoint="/items",
            method=HttpMethod.POST,
            plugins_settings=[
                ValidatorPluginSettings(
                    request_model=CreateItemModel,
                    on_200=ItemModel,
                ),
            ]
        )

        self.update_item = self._client.build_api_method(
            endpoint="/items/{id}",
            method=HttpMethod.PATCH,
            plugins_settings=[
                ValidatorPluginSettings(
                    request_model=UpdateItemModel,
                    on_200=ItemModel,
                ),
            ]
        )

        self.delete_item = self._client.build_api_method(
            endpoint="/items/{id}",
            method=HttpMethod.DELETE,
            plugins_settings=[
                ValidatorPluginSettings(
                    on_200=ItemModel,
                ),
            ]
        )

    @cache_key_builder
    @staticmethod
    def _build_cache_key_func_for_get_item(path_params, *args, **kwargs):
        return path_params["id"]


    @cache_key_builder
    @staticmethod
    def _build_cache_key_func_for_get_items(query_params, *args, **kwargs):
        return query_params



class TestApiClient:
    pass
