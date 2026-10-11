
import csv
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Student Data API")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

# Read the CSV while preserving row order
CSV_FILE = Path(__file__).parent / "students.csv"

students = []

with open(CSV_FILE, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })


@app.get("/api")
def get_students(
    classes: Optional[List[str]] = Query(
        default=None,
        alias="class"
    )
):
    # No class filter: return all students
    if classes is None:
        return {"students": students}

    # Filter by one or multiple classes
    allowed_classes = set(classes)

    filtered_students = [
        student
        for student in students
        if student["class"] in allowed_classes
    ]

    return {"students": filtered_students}


@app.get("/")
def home():
    return {
        "message": "Student API is running",
        "endpoint": "/api"
    }
