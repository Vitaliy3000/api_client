from pydantic import AnyUrl, validator
from utils import StrictModel
from yarl import URL


class Settings(StrictModel):
    base_url: AnyUrl

    @validator("base_url", pre=True, always=True)
    def cutter_base_url(self, value: str):
        url = URL(value)
        return URL.build(scheme=url.scheme, host=url.host, port=url.port)
