import sqlite3
import typing
from app.database.utils import add_kv


class QueryBuilder:
    @staticmethod
    def GetCreateQuery(tablename: str, columns: dict[str, list[str]]) -> str:
        columns_pattern = ", ".join(
            [
                str(key) + " " + " ".join(values)
                for key, values in columns.items()
            ]
        )
        return f"CREATE TABLE IF NOT EXISTS {tablename} ({columns_pattern})"

    @staticmethod
    def GetInsertQuery(tablename: str,
                       columns: list[str],
                       values: list[tuple]) -> tuple[str, list[typing.Any]]:
        values_pattern = ", ".join(
            [
                "(" + ", ".join(["?" for i in range(len(columns))]) + ")"
                for i in range(len(values))
            ]
        )
        query = f"""INSERT INTO {tablename} ({', '.join(columns)})
                VALUES {values_pattern}"""
        args: list[typing.Any] = []
        for val in values:
            args.extend(val)
        return (query, args)

    @staticmethod
    def GetSelectQuery(tablename: str,
                       **filter) -> tuple[str, list[typing.Any]]:
        if not filter:
            return (f"SELECT * FROM {tablename}", [])
        query = f"SELECT * FROM {tablename} WHERE " + " AND ".join(
                [i+"=?" for i in filter.keys()])
        return (query, list(filter.values()))

    @staticmethod
    def GetUpdateQuery(tablename: str,
                       update_fields: dict[str, typing.Any],
                       **filter) -> tuple[str, list[typing.Any]]:
        args: list[typing.Any] = []
        query = f"UPDATE {tablename} SET "
        query = add_kv(query, ", ", **update_fields)
        args.extend(update_fields.values())
        if filter:
            query += " WHERE "
            query = add_kv(query, " AND ", **filter)
            args.extend(filter.values())
        return (query, args)

    @staticmethod
    def GetDeleteQuery(tablename: str,
                       **filter) -> tuple[str, list[typing.Any]]:
        args = list(filter.values())
        query = f"DELETE FROM {tablename} WHERE "
        query = add_kv(query, " AND ", **filter)
        return (query, args)


class Core:
    def __init__(self, url: str):
        self._url = url

    def Create(self, tablename: str, columns: dict[str, list[str]]):
        query = QueryBuilder.GetCreateQuery(tablename, columns)
        with sqlite3.connect(self._url) as conn:
            conn.execute(query)

    def Insert(self, tablename: str, columns: list[str], values: list[tuple]):
        query, args = QueryBuilder.GetInsertQuery(tablename, columns, values)
        with sqlite3.connect(self._url) as conn:
            conn.execute(query, args)

    def Select(self, tablename: str, **filter) -> list[typing.Any]:
        query, args = QueryBuilder.GetSelectQuery(tablename, **filter)
        with sqlite3.connect(self._url) as conn:
            return conn.execute(query, args).fetchall()

    def Update(self,
               tablename: str,
               update_fields: dict[str, typing.Any],
               **filter):
        query, args = QueryBuilder.GetUpdateQuery(
            tablename,
            update_fields,
            **filter
        )
        with sqlite3.connect(self._url) as conn:
            conn.execute(query, args)

    def Delete(self, tablename: str, **filter):
        query, args = QueryBuilder.GetDeleteQuery(tablename, **filter)
        with sqlite3.connect(self._url) as conn:
            conn.execute(query, args)
