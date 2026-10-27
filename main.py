from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from library import library_router

app = FastAPI()
app.include_router(library_router)

class Student(BaseModel):
    id: int
    name: str
    course: str

students = {
    1: {"name": "Anu", "course": "Python"},
    2: {"name": "Rahul", "course": "Java"}
}

@app.get("/")
def home():
    return {"message": "Student API is running"}


@app.get("/students")
def get_students():
    return {"students": students}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": student}


@app.post("/students")
def add_student(student: Student):
    students[student.id] = {"name": student.name, "course": student.course}
    return {"message": "Student added successfully", "student": students[student.id]}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    removed = students.pop(student_id)
    return {"deleted": removed}