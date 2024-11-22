from app.service.base import BaseService
from app.books.models import Books
from app.database.orm import OrmEngine


class BookService(BaseService):
    model = Books

    @classmethod
    def AddBook(cls, eng: OrmEngine, title: str, author: str, year: int):
        eng.InsertIntoTable(
            cls.model,
            ["title", "author", "year"],
            [(title, author, year)]
        )

    @classmethod
    def UpdateStatus(cls, eng: OrmEngine, id: int, new_status: str):
        eng.UpdateTable(cls.model, {"status": new_status}, id=id)
