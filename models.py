from typing import Optional, ClassVar
import os

from pydantic import BaseModel, Field, validator
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
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np


def create_table(model: BaseModel, table: Table):
    # Считывает xlsx файл
    # Переименовывает столбцы и заменяет отсуттвующие данные на None
    # Построчно валидирует данные через Pydantic и вносит их в таблицу
    data = pd.read_excel(os.path.join("DB", model.table_name))
    data = data.rename(columns=dict(zip(data.columns, list(model.model_fields))))
    data.replace({np.nan: None}, inplace=True)
    engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
    with Session(engine) as session:
        for r in range(data.shape[0]):
            table_model = model.model_validate(data.iloc[r].to_dict())
            stmt = insert(table).values(table_model.dict())
            session.execute(stmt)
        session.commit()
        session.close()


def create_pivot(Grant: Table, Ntp: Table, Templan: Table, Pivot: Table):
    engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
    with Session(engine) as session:
        # Первый запрос
        query1 = select(
            Grant.c.vuz_code,
            Grant.c.vuz_name,
            func.count(Grant.c.nir_code).label("nir_grant_count"),
            func.sum(Grant.c.grant_value).label("total_grant_value"),
            literal_column("0").label("nir_ntp_count"),
            literal_column("0").label("total_year_value_plan"),
            literal_column("0").label("nir_templan_count"),
            literal_column("0").label("total_value_plan"),
        ).group_by(Grant.c.vuz_code, Grant.c.vuz_name)

        # Второй запрос
        query2 = select(
            Ntp.c.vuz_code,
            Ntp.c.vuz_name,
            literal_column("0").label("nir_grant_count"),
            literal_column("0").label("total_grant_value"),
            func.count(Ntp.c.nir_number).label("nir_ntp_count"),
            func.sum(Ntp.c.year_value_plan).label("total_year_value_plan"),
            literal_column("0").label("nir_templan_count"),
            literal_column("0").label("total_value_plan"),
        ).group_by(Ntp.c.vuz_code, Ntp.c.vuz_name)

        # Третий запрос
        query3 = select(
            Templan.c.vuz_code,
            Templan.c.vuz_name,
            literal_column("0").label("nir_grant_count"),
            literal_column("0").label("total_grant_value"),
            literal_column("0").label("nir_ntp_count"),
            literal_column("0").label("total_year_value_plan"),
            func.count(Templan.c.nir_reg_number).label("nir_templan_count"),
            func.sum(Templan.c.value_plan).label("total_value_plan"),
        ).group_by(Templan.c.vuz_code, Templan.c.vuz_name)

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
        insert_stmt = Pivot.insert().values(
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


class Nir_Grant(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    nir_code: int = Field()
    kon_code: int = Field()
    grnti_code: Optional[str] = Field(default=None)
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    grant_value: int = Field()
    nir_director: str = Field()
    director_position: Optional[str] = Field(default=None)
    director_academic_title: Optional[str] = Field(default=None)
    director_academic_degree: Optional[str] = Field(default=None)
    nir_name: str = Field()
    table_name: ClassVar[str] = "Gr_pr.xlsx"

    # Имена столобцов на русском

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_NTP(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    ntp_code: int = Field()
    nir_number: int = Field()
    grnti_code: Optional[str] = Field(default=None)
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    year_value_plan: int = Field()
    nir_director: str = Field()
    director_meta: str = Field()
    nir_type: str = Field()
    nir_name: str = Field()
    table_name: ClassVar[str] = "Ntp_pr.xlsx"

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_Templan(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    grnti_code: Optional[str] = Field(default=None)
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    value_plan: int = Field()
    nir_director: str = Field()
    director_position: str = Field()
    nir_type: str = Field()
    nir_reg_number: str = Field()
    nir_name: str = Field()
    table_name: ClassVar[str] = "Tp_pr.xlsx"

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None

    @validator("nir_reg_number", pre=True)
    def validate_nir_reg_number(cls, value):
        if isinstance(value, str):
            return value
        return str(value)


class Nir_VUZ(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    status: str = Field()
    fed_sub_code: int = Field()
    federation_subject: str = Field()
    region: str = Field()
    city: str = Field()
    name: str = Field()
    full_name: str = Field()
    gr_ved: Optional[str] = Field(default=None)
    profile: Optional[str] = Field(default=None)
    table_name: ClassVar[str] = "VUZ.xlsx"


metadata_obj = MetaData()

Grant = Table(
    "nir_grant",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("nir_code", Integer),
    Column("kon_code", Integer),
    Column("grnti_code", String),
    Column("vuz_code", Integer),
    Column("vuz_name", String),
    Column("grant_value", Integer),
    Column("nir_director", String),
    Column("director_position", String),
    Column("director_academic_title", String),
    Column("director_academic_degree", String),
    Column("nir_name", String),
)

NTP = Table(
    "nir_ntp",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("ntp_code", Integer),
    Column("nir_number", Integer),
    Column("grnti_code", String),
    Column("vuz_code", Integer),
    Column("vuz_name", String),
    Column("year_value_plan", Integer),
    Column("nir_director", String),
    Column("director_meta", String),
    Column("nir_type", String),
    Column("nir_name", String),
)

Templan = Table(
    "nir_templan",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("grnti_code", String),
    Column("vuz_code", Integer),
    Column("vuz_name", String),
    Column("value_plan", Integer),
    Column("nir_director", String),
    Column("director_position", String),
    Column("nir_type", String),
    Column("nir_reg_number", String),
    Column("nir_name", String),
)

VUZ = Table(
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

Pivot = Table(
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
