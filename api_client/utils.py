from pydantic import BaseModel


class StrictModel(BaseModel, allow_mutation=False):
    pass
