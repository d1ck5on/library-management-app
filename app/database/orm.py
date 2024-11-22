from enum import Enum
import typing
from app.database.core import Core


class SQLTypes(str, Enum):
    INT = "INTEGER"
    STR = "STR"


class Column:
    def __init__(self, sqltype: SQLTypes, *params):
        self.sqltype = sqltype
        self.params = params
        self.name: str | None = None

    def set_name(self, name: str):
        self.name = name


class ProcessorTable(type):
    def __new__(mcs, name, bases, namespace):
        columns = list()
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, Column):
                attr_value.set_name(attr_name)
                columns.append(attr_value)
        return super(ProcessorTable, mcs).__new__(
            mcs, name, bases, namespace |
            {
                "COLUMNS": columns,
                "TABLENAME": name
            }
        )


class Table(metaclass=ProcessorTable):
    COLUMNS: list[Column]
    TABLENAME: str

    def __init__(self, *args):
        for column, arg in zip(self.COLUMNS, args):
            setattr(self, column.name, arg)

    @classmethod
    def ColumnsToDict(cls) -> dict[str, list[str]]:
        res = {}
        for col in cls.COLUMNS:
            attrs = [col.sqltype.value]
            attrs.extend(col.params)
            res[col.name] = attrs
        return res

    def __repr__(self):
        attrs = []
        for col in self.COLUMNS:
            attrs.append(f"{col.name}: {str(getattr(self, col.name))}")
        return f"<{self.TABLENAME}({', '.join(attrs)})>"

    def __str__(self):
        attrs = []
        for col in self.COLUMNS:
            attrs.append(f"{col.name}: {str(getattr(self, col.name))}")
        return f"[{', '.join(attrs)}]"

    def asdict(self):
        res = dict()
        for col in self.COLUMNS:
            res[col.name] = getattr(self, col.name)
        return res


class OrmEngine:
    def __init__(self, core_engine: Core):
        self._engine = core_engine

    def CreateTable(self, table: type[Table]):
        self._engine.Create(table.TABLENAME, table.ColumnsToDict())

    def SelectFromTable(self, table: type[Table], **filter) -> list[Table]:
        return [
            table(*i) for i in self._engine.Select(table.TABLENAME, **filter)
        ]

    def InsertIntoTable(self,
                        table: type[Table],
                        columns: list[str],
                        values: list[tuple]):
        self._engine.Insert(table.TABLENAME, columns, values)

    def UpdateTable(self,
                    table: type[Table],
                    update_fields: dict[str, typing.Any],
                    **filter):
        self._engine.Update(table.TABLENAME, update_fields, **filter)

    def DeleteFromTable(self, table: type[Table], **filter):
        self._engine.Delete(table.TABLENAME, **filter)
