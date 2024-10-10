import os
import numpy as np

from pydantic import BaseModel
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    create_engine,
    insert,
    select,
    func,
    union_all,
    literal_column,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
import pandas as pd

from schema import (
    Nir_Grant,
    Nir_NTP,
    Nir_Templan,
    Nir_VUZ,
)


def create_pivot(Grant, Ntp, Templan, Pivot):
    engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
    with Session(engine) as session:
        # Первый запрос
        query1 = Grant.grant_summary()

        # Второй запрос
        query2 = Ntp.ntp_summary()

        # Третий запрос
        query3 = Templan.tp_summary()

        # Объединение запросов
        combined_query = union_all(query1, query2, query3)

        # Сводный запрос
        final_query = select(
            combined_query.c.vuz_code,
            combined_query.c.vuz_name,
            func.sum(combined_query.c.nir_grant_count).label("total_nir_grant_count"),
            func.sum(combined_query.c.total_grant_value).label("total_grant_value"),
            func.sum(combined_query.c.nir_ntp_count).label("total_nir_ntp_count"),
            func.sum(combined_query.c.total_year_value_plan).label(
                "total_year_value_plan"
            ),
            func.sum(combined_query.c.nir_templan_count).label(
                "total_nir_templan_count"
            ),
            func.sum(combined_query.c.total_value_plan).label("total_value_plan"),
            func.sum(combined_query.c.nir_grant_count)
            + func.sum(combined_query.c.nir_ntp_count)
            + func.sum(combined_query.c.nir_templan_count).label("total_count"),
            func.sum(combined_query.c.total_grant_value)
            + func.sum(combined_query.c.total_year_value_plan)
            + func.sum(combined_query.c.total_value_plan).label("total_sum"),
        ).group_by(combined_query.c.vuz_code, combined_query.c.vuz_name)

        # Выполнение запроса
        results = session.execute(final_query).fetchall()
        insert_stmt = Pivot.__table__.insert().values(
            [
                {
                    "vuz_code": row[0],
                    "vuz_name": row[1],
                    "total_nir_grant_count": row[2],
                    "total_grant_value": row[3],
                    "total_nir_ntp_count": row[4],
                    "total_year_value_plan": row[5],
                    "total_nir_templan_count": row[6],
                    "total_value_plan": row[7],
                    "total_count": row[8],
                    "total_sum": row[9],
                }
                for row in results
            ]
        )

        session.execute(insert_stmt)
        session.commit()


metadata_obj = MetaData()


class BaseTabel(DeclarativeBase):
    _schema = BaseModel

    def create_table(self):
        # Считывает xlsx файл
        # Переименовывает столбцы и заменяет отсуттвующие данные на None
        # Построчно валидирует данные через Pydantic и вносит их в таблицу
        data = pd.read_excel(os.path.join("DB", self._schema.table_name))
        data = data.rename(
            columns=dict(zip(data.columns, list(self._schema.model_fields)))
        )
        data.replace({np.nan: None}, inplace=True)
        engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
        with Session(engine) as session:
            for r in range(data.shape[0]):
                table_model = self._schema.model_validate(data.iloc[r].to_dict())
                stmt = insert(self.__table__).values(table_model.dict())
                session.execute(stmt)
            session.commit()
            session.close()


class Grant(BaseTabel):
    _schema = Nir_Grant
    __table__ = Table(
        "nir_grant",
        metadata_obj,
        Column("UniqueID", Integer, primary_key=True),
        Column("nir_code", Integer),
        Column("kon_code", Integer),
        Column("vuz_code", Integer),
        Column("vuz_name", String),
        Column("grnti_code", String),
        Column("grant_value", Integer),
        Column("nir_director", String),
        Column("director_position", String),
        Column("director_academic_title", String),
        Column("director_academic_degree", String),
        Column("nir_name", String),
    )

    def grant_summary(self):
        return select(
            self.__table__.c.vuz_code,
            self.__table__.c.vuz_name,
            func.count(self.__table__.c.nir_code).label("nir_grant_count"),
            func.sum(self.__table__.c.grant_value).label("total_grant_value"),
            literal_column("0").label("nir_ntp_count"),
            literal_column("0").label("total_year_value_plan"),
            literal_column("0").label("nir_templan_count"),
            literal_column("0").label("total_value_plan"),
        ).group_by(self.__table__.c.vuz_code, self.__table__.c.vuz_name)


class NTP(BaseTabel):
    _schema = Nir_NTP
    __table__ = Table(
        "nir_ntp",
        metadata_obj,
        Column("UniqueID", Integer, primary_key=True),
        Column("ntp_code", Integer),
        Column("nir_number", Integer),
        Column("vuz_code", Integer),
        Column("vuz_name", String),
        Column("grnti_code", String),
        Column("year_value_plan", Integer),
        Column("nir_director", String),
        Column("director_meta", String),
        Column("nir_type", String),
        Column("nir_name", String),
    )

    def ntp_summary(self):
        return select(
            self.__table__.c.vuz_code,
            self.__table__.c.vuz_name,
            literal_column("0").label("nir_grant_count"),
            literal_column("0").label("total_grant_value"),
            func.count(self.__table__.c.nir_number).label("nir_ntp_count"),
            func.sum(self.__table__.c.year_value_plan).label("total_year_value_plan"),
            literal_column("0").label("nir_templan_count"),
            literal_column("0").label("total_value_plan"),
        ).group_by(self.__table__.c.vuz_code, self.__table__.c.vuz_name)


class Templan(BaseTabel):
    _schema = Nir_Templan
    __table__ = Table(
        "nir_templan",
        metadata_obj,
        Column("UniqueID", Integer, primary_key=True),
        Column("vuz_code", Integer),
        Column("vuz_name", String),
        Column("grnti_code", String),
        Column("value_plan", Integer),
        Column("nir_director", String),
        Column("director_position", String),
        Column("nir_type", String),
        Column("nir_reg_number", String),
        Column("nir_name", String),
    )

    def tp_summary(self):
        return select(
            self.__table__.c.vuz_code,
            self.__table__.c.vuz_name,
            literal_column("0").label("nir_grant_count"),
            literal_column("0").label("total_grant_value"),
            literal_column("0").label("nir_ntp_count"),
            literal_column("0").label("total_year_value_plan"),
            func.count(self.__table__.c.nir_reg_number).label("nir_templan_count"),
            func.sum(self.__table__.c.value_plan).label("total_value_plan"),
        ).group_by(self.__table__.c.vuz_code, self.__table__.c.vuz_name)


class VUZ(BaseTabel):
    _schema = Nir_VUZ
    __table__ = Table(
        "vuz",
        metadata_obj,
        Column("UniqueID", Integer, primary_key=True),
        Column("vuz_code", Integer),
        Column("vuz_name", String),
        Column("status", String),
        Column("fed_sub_code", Integer),
        Column("federation_subject", String),
        Column("region", String),
        Column("city", String),
        Column("name", String),
        Column("full_name", String),
        Column("gr_ved", String),
        Column("profile", String),
    )


class Pivot(BaseModel):
    __table__ = Table(
        "pivot",
        metadata_obj,
        Column("UniqueID", Integer, primary_key=True),
        Column("vuz_code", Integer),
        Column("vuz_name", String),
        Column("total_nir_grant_count", Integer),
        Column("total_grant_value", Integer),
        Column("total_nir_ntp_count", Integer),
        Column("total_year_value_plan", Integer),
        Column("total_nir_templan_count", Integer),
        Column("total_value_plan", Integer),
        Column("total_count", Integer),
        Column("total_sum", Integer),
    )
