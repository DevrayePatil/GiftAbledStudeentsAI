import csv

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


library_router = APIRouter(prefix="/library", tags=["Library"])


class Book(BaseModel):
    id: int
    title: str
    copies: int


@library_router.get("/books")
def get_books():
    books = []
    try:
        with open("books.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(
                    Book(
                        id=int(row["id"]), title=row["title"], copies=int(row["copies"])
                    )
                )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books data not found")
    return {"books": books}


@library_router.get("/books/{book_id}")
def get_book(book_id: int):

    books = []
    try:
        with open("books.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(
                    Book(
                        id=int(row["id"]), title=row["title"], copies=int(row["copies"])
                    )
                )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books data not found")

    book = next((book for book in books if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}


@library_router.post("/books")
def add_book(book: Book):

    with open("books.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "copies"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"id": book.id, "title": book.title, "copies": book.copies})
    return {"message": "Book added successfully", "book": book}


@library_router.delete("/books/{book_id}")
def delete_book(book_id: int):
    books = []
    try:
        with open("books.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                books.append(
                    Book(
                        id=int(row["id"]), title=row["title"], copies=int(row["copies"])
                    )
                )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Books data not found")
    book = next((book for book in books if book.id == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books.remove(book)

    with open("books.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "title", "copies"])
        writer.writeheader()
        for b in books:
            writer.writerow({"id": b.id, "title": b.title, "copies": b.copies})
    return {"message": "Book deleted successfully", "book": book}
