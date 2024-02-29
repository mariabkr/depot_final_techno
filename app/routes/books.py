from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas import Book
import app.services.books as service
from app.database import database

router = APIRouter(prefix="/books", tags=["Books"])


@router.get('/display')
def display_list_of_book_and_number():
    books = service.display_list_of_book_and_number()
    total_books = len(database)  
    return JSONResponse(
        content={"books": books, "total_books": total_books},
        status_code=status.HTTP_200_OK,
    )

@router.post("/update/{id}")
def update_book(id: str, auteur: str, titre: str, editeur: str):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not found",
        )
    # Mettre à jour les détails du livre
    database[id] = {"titre": titre, "auteur": auteur, "editeur": editeur}
    return {"message": "Book updated successfully"}

@router.post("/delete/{id}")
def delete_book(id: str):
    if id not in database:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book not found",
        )
    # Supprimer le livre
    del database[id]
    return {"message": "The book was deleted successfully"}

@router.post('/add_book')
def add_new_book(name: str, auteur: str, editeur: str):
    new_book_data = {
        "id": str(uuid4()),
        "name": name,
        "auteur": auteur,
        "editeur": editeur,
    }
    try:
        new_book = Book.model_validate(new_book_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book name, author, or editor."
        )
    service.save_book(new_book)
    return new_book.model_dump()
