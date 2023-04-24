from pydantic import BaseModel


class Color:
    WHITE = "white"
    BLACK = "black"


class ItemModel(BaseModel):
    id: int
    name: str
    color: Color | None


class GetItemsModel(BaseModel):
    ids: list[int] | None
    names: list[str] | None
    color: list[Color | None] | None


class ItemsModel(BaseModel):
    __root__: list[ItemModel]


class CreateItemModel(BaseModel):
    name: str
    color: Color | None


class UpdateItemModel(BaseModel):
    name: str | None
    color: Color | None
