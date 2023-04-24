import abc
from api_client.models import SubtypeBaseModel
from typing import Any
from api_client.models import Request, Response


class BasePlugin(abc.ABC):
    def __init__(self, settings: SubtypeBaseModel, *args: Any, **kwargs: Any) -> None:
        self._settings = settings

    @abc.abstractmethod
    async def __call__(self, function, *other_function, request: Request) -> Response:
        pass
