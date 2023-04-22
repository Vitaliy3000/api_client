from typing import TypeVar, Type
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt
from exceptions import ApiError
from api_client.models import Response


ApiErrorSubtype = TypeVar("ApiErrorSubtype", bound=ApiError)


class RetrySettings:
    exceptions: tuple[Type[ApiErrorSubtype], ...] = [ApiError]
    count_attempt = 3


class Retry:
    def __init__(self, settings) -> None:
        self._settings = settings

    async def __call__(self, fn, *args, **kwargs) -> Response:
        retrying_policy = AsyncRetrying(
            retry=retry_if_exception_type(self._settings.exceptions),
            stop=stop_after_attempt(self._count_attempt),
        )

        async for attempt in retrying_policy:
           with attempt:
               response = await fn(*args, **kwargs)

        return response
