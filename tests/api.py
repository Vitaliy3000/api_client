from fastapi import FastAPI, HTTPException
from tests.models import CreateItemModel, ItemModel

_ITEMS = {}
MAX_ID = 0
app = FastAPI()


def _get_next_id():
    global MAX_ID
    MAX_ID += 1
    return MAX_ID


def _get_item(id: int) -> ItemModel:
    item = _ITEMS.get(id)

    if item is None:
        raise HTTPException(404, detail="Item not found")


@app.get("/items")
def get_items():
    # return _ITEMS
    pass


@app.get("/items/{id}")
def get_item(id: int):
    return _get_item(id)


@app.post("/items")
def create_item(data: CreateItemModel):
    item = ItemModel(
        id=_get_next_id(),
        name=data.name,
        color=data.color,
    )
    _ITEMS[item.id] = item


@app.patch("/items/{id}")
def update_item(id: int):
    item = _get_item(id)


@app.delete("/items/{id}")
def delete_item(id: int):
    item = _get_item(id)
    del _ITEMS[id]
    return item