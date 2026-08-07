# TORRE, JIBRIELLE R.
# LAB 2 - PART 2(lab2_part2.py)
# BSCS 3-A/CSIT 315a



from fastapi import FastAPI, Query, Path

app = FastAPI()


tasks_db: list[str] = ["Setup environment", "Write unit tests", "Deploy application",]


inventory_db: dict[int, str] = {
  501: "Mechanical Keyboard",
  502: "Ergonomic Mouse",
  503: "USB-C Hub",
  504: "Monitor",
  505: "Boeing 737-MAX8",
  506: "Airbus A380",
  507: "Boeing 747",
  508: "Boeing 777",
  509: "Boeing 787",
  510: "Boeing 757",

}

#Problem 3

#READ
@app.get("/tasks")
def get_all_tasks():
  return {
    "tasks": tasks_db,
    "count": len(tasks_db)
  }


#CREATE
@app.post("/tasks")
def create_task(
  task_name: str = Query(
    ...,
    min_length=3,
    max_length=50,
    title="Task Name",
    description="Name of new task to be added to queue.")
):

  tasks_db.append(task_name)
  return {
    "tasks": tasks_db,
    "count": len(tasks_db)
  }

#DELETING
@app.delete("/tasks/{task_index}")
def delete_task(
  task_index: int = Path(
    ...,
    ge=0,
    title="Task Index",
    description="Zero-based index of task to remove.")
):
  if 0<= task_index < len(tasks_db):
    deleted_task = tasks_db.pop(task_index)
    return {
      "message": "Task is good-bye!",
      "deleted": deleted_task
    }
  return {"error": "Index out of range!"}

#Problem 4

#Get entire inventory
@app.get("/inventory")
def get_inventory():
  return inventory_db

#Get single item
@app.get("/inventory/{item_id}")
def get_item(
  item_id: int = Path(
    ...,
    gt=0,
    title="Item ID",
    description="Positive integer product ID"
  )
):
   if item_id in inventory_db:
     return {
       "item_id": item_id,
       "name": inventory_db[item_id]
     }
   return {"error": "Item not found!"}

#POST create/insert item
@app.post("/inventory/{item_id}")
def create_item(
    item_id: int = Path(
        ...,
        gt=0,
        title="Item ID",
        description="Positive integer product ID"
    ),
    item_name: str = Query(
        ...,
        min_length=2,
        max_length=30,
        title="Item Name",
        description="Name of the product to store"
    )
):
    inventory_db[item_id] = item_name
    return {
        "message": "Item added",
        "item_id": item_id,
        "name": item_name,
        "inventory": inventory_db
    }


# DELETE
@app.delete("/inventory/{item_id}")
def delete_item(
    item_id: int = Path(
        ...,
        gt=0,
        title="Item ID",
        description="Positive integer product ID"
    )
):
    if item_id in inventory_db:
        deleted_name = inventory_db.pop(item_id)
        return {
            "message": "Item removed",
            "item_id": item_id,
            "deleted": deleted_name
        }
    return {"error": "Item not found"}