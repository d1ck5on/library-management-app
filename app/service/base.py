from app.database.orm import OrmEngine, Table
import json


class BaseService:
    model: type[Table] | None = None

    @classmethod
    def FindAll(cls, eng: OrmEngine, **filters) -> list[Table]:
        return eng.SelectFromTable(cls.model, **filters)

    @classmethod
    def DeleteById(cls, eng: OrmEngine, id: int):
        eng.DeleteFromTable(cls.model, id=id)

    @classmethod
    def ExportToJson(cls, eng: OrmEngine, filename: str):
        to_json = [row.asdict() for row in cls.FindAll(eng)]
        with open(filename, "w") as file:
            json.dump(to_json, file)
