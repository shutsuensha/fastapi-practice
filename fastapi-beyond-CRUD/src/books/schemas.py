from pydantic import BaseModel
import uuid

from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookDetailModel(Book):
    reviews: list[ReviewModel]
    tags: list[TagModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str



class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str