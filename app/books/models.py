from app.database.orm import Table, Column, SQLTypes


class Books(Table):
    id = Column(SQLTypes.INT, "PRIMARY KEY", "AUTOINCREMENT")
    title = Column(SQLTypes.STR, "NOT NULL")
    author = Column(SQLTypes.STR, "NOT NULL")
    year = Column(SQLTypes.INT, "NOT NULL")
    status = Column(SQLTypes.STR,
                    "NOT NULL",
                    "CHECK(status IN ('в наличии', 'выдана'))",
                    "DEFAULT 'в наличии'")
