from typing import Callable, Any
from api_client.plugins import BasePlugin
from api_client.models import Request, Response
from pydantic import BaseModel


class CachePluginSettings(BaseModel):
    get_redis_client: Callable[[], str]
    calc_cache_key: Callable[[Any], str]
    ttl: int


class CachePlugin(BasePlugin):
    async def __call__(self, function, *other_function, request: Request) -> Response:
        redis_client = self.get_redis_client()
        cache_key = self._settings.calc_cache_key(...)

        value = await redis_client.get(cache_key)
        if value is None:
            response = await function(*other_function, request=request)
            redis_client.set(cache_key, response.to_json(), self._settings.ttl)
        else:
            response = Response.from_json(value)

        return response


def cache_key_builder(func):
    pass
    # TODO: check correctness of function
