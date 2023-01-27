import uuid
from fastapi import FastAPI, status, Body
from fastapi.responses import FileResponse, JSONResponse


class Item:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority
        self.id = str(uuid.uuid4())


items = [
    Item("Do homework", "Tasks: 1 - 3", 1),
    Item("Do practical task", "Subject: Functions", 1),
    Item("Meet with the insurer", "Central Park at 3:00 PM", 2)]


def find_item(id):
    for item in items:
        if item.id == id:
            return item
    return None

def not_found():
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Item not found!"}
    )

app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/items")
def get_items():
    return items


@app.get("/api/items/{id}")
def get_item(id):
    item = find_item(id)
    print(item)
    if item == None:
        not_found()
    return item


@app.post("/api/items")
def create_item(data=Body()):
    item = Item(data["title"], data["description"], data["priority"])
    items.append(item)
    return item


@app.put("/api/items")
def edit_item(data=Body()):
    item = find_item(data["id"])
    if item == None:
        not_found()
    item.title = data["title"]
    item.description = data["description"]
    item.priority = data["priority"]
    return item


@app.delete("/api/items/{id}")
def delete_item(id):
    item = find_item(id)
    if item == None:
        not_found()
    items.remove(item)
    return item
