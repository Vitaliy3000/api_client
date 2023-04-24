from api_client.plugins import BasePlugin
from api_client.models import Response
import enum
from pydantic import BaseModel
from api_client.models import SubtypeBaseModel, Request, Response
from api_client.exceptions import UnexpectedStatusCode


class ActionOnUnexpectedStatusCode(enum.Enum):
    SKIP = "skip"
    EXCEPTION = "exception"


class ValidatorPluginSettings(BaseModel):
    request_model: SubtypeBaseModel | None
    on_200: SubtypeBaseModel | None
    on_201: SubtypeBaseModel | None
    on_204: SubtypeBaseModel | None
    on_400: SubtypeBaseModel | None
    on_401: SubtypeBaseModel | None
    on_403: SubtypeBaseModel | None
    on_404: SubtypeBaseModel | None
    on_500: SubtypeBaseModel | None
    on_501: SubtypeBaseModel | None
    on_502: SubtypeBaseModel | None
    on_503: SubtypeBaseModel | None
    on_504: SubtypeBaseModel | None
    default: ActionOnUnexpectedStatusCode = ActionOnUnexpectedStatusCode.EXCEPTION


class ValidatorPlugin(BasePlugin):
    def _get_validator_by(self, status_code: int) -> SubtypeBaseModel:
        current_settings = getattr(self._settings, f"on_{status_code}", None)
        if current_settings is None and self._settings.default == ActionOnUnexpectedStatusCode.EXCEPTION:
            raise UnexpectedStatusCode(status_code)

    async def __call__(self, function, *other_function, request: Request) -> Response:
        if self._settings.request_model is not None:
            request.body = self._settings.request_model.parse_obj(request.body)

        response = await function(*other_function, request=request)
        validator = self._get_validator_by(response.status_code)
        if validator is not None:
            response.parsed_response = validator.parse_raw(self.response.raw_response.text)
        return response
