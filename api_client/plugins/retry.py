from typing import TypeVar, Type
from api_client.plugins import BasePlugin
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt
from exceptions import ApiError
from api_client.models import Request, Response


ApiErrorSubtype = TypeVar("ApiErrorSubtype", bound=ApiError)


class RetryPluginSettings:
    exceptions: tuple[Type[ApiErrorSubtype], ...] = [ApiError]
    count_attempt: int


class RetryPlugin(BasePlugin):
    async def __call__(self, function, *other_function, request: Request) -> Response:
        retrying_policy = AsyncRetrying(
            retry=retry_if_exception_type(self._settings.exceptions),
            stop=stop_after_attempt(self._count_attempt),
        )

        async for attempt in retrying_policy:
           with attempt:
               response = await function(*other_function, request=request)

        return response
