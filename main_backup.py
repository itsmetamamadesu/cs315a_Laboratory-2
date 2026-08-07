student_list = ["Diego", "Paul", "Alexandrik", "Bonaparte", "Kent", "Tollis"]


@app.get("/student/{student_id}")
async def get_student(student_id: int):
  return {"message": student_list[student_id]}

@app.post("/student/{student_name}")
async def add_student(student_name: str):
    student_list.append(student_name)
    return {"message": "Student successfully added"}

@app.put("/student/{student_id}")
async def update_student(student_id: int, student_name: str):
    student_list[student_id] = student_name
    return {"message": "Student successfully updated"}


@app.delete("/student/{student_id}")
async def delete_student(student_id: int):
    del student_list[student_id]
    return {"message": "Student successfully deleted"}