from app.database.core import Core
from app.database.orm import OrmEngine
from app.books.models import Books


DB_URL = "base.db"
engine = OrmEngine(Core(DB_URL))
engine.CreateTable(Books)
