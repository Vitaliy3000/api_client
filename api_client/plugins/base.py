from api_client.models import SubtypeBaseModel
from typing import Any


class BasePlugin:
    def __init__(self, settings: SubtypeBaseModel, *args: Any, **kwargs: Any) -> None:
        self._settings = settings
