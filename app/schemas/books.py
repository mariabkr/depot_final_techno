
from pydantic import BaseModel, Field
from uuid import uuid4



class Book(BaseModel):
    id: str
    name_book: str = Field(...,min_length=1)
    auteur:str=Field(...,min_length=1)
    editeur:str=Field(...,min_length=1)