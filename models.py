from typing import Optional, ClassVar
import os

from pydantic import BaseModel, Field, validator
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, insert
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
            ntp = model.model_validate(data.iloc[r].to_dict())
            stmt = insert(table).values(ntp.dict())
            session.execute(stmt)
        session.commit()
        session.close()


class Nir_Grant(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    nir_code: int = Field()
    kon_code: int = Field()
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    grnti_code: Optional[str] = Field(default=None)
    grant_value: int = Field()
    nir_name: str = Field()
    nir_director: str = Field()
    director_position: Optional[str] = Field(default=None)
    director_academic_title: Optional[str] = Field(default=None)
    director_academic_degree: Optional[str] = Field(default=None)
    table_name: ClassVar[str] = "Gr_pr.xlsx"

    #Имена столобцов на русском
    
    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_NTP(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    ntp_code: int = Field()
    nir_number: int = Field()
    nir_name: str = Field()
    vuz_name: Optional[str] = Field(default=None)
    vuz_code: int = Field()
    nir_director: str = Field()
    director_meta: str = Field()
    grnti_code: Optional[str] = Field(default_factory=lambda: None)
    nir_type: str = Field()
    year_value_plan: int = Field()
    table_name: ClassVar[str] = "Ntp_pr.xlsx"

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_Templan(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    vuz_code: int = Field()
    nir_type: str = Field()
    vuz_name: Optional[str] = Field(default=None)
    nir_director: str = Field()
    grnti_code: Optional[str] = Field(default=None)
    value_plan: int = Field()
    nir_name: str = Field()
    director_position: str = Field()
    nir_reg_number: str = Field()
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
    name: str = Field()
    full_name: str = Field()
    vuz_name: Optional[str] = Field(default=None)
    region: str = Field()
    city: str = Field()
    status: str = Field()
    fed_sub_code: int = Field()
    federation_subject: str = Field()
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
    Column("vuz_code", Integer),
    Column("vuz_name", String),
    Column("grnti_code", String),
    Column("grant_value", Integer),
    Column("nir_name", String),
    Column("nir_director", String),
    Column("director_position", String),
    Column("director_academic_title", String),
    Column("director_academic_degree", String),
)

NTP = Table(
    "nir_ntp",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("ntp_code", Integer),
    Column("nir_number", Integer),
    Column("nir_name", String),
    Column("vuz_name", String),
    Column("vuz_code", Integer),
    Column("nir_director", String),
    Column("director_meta", String),
    Column("grnti_code", String),
    Column("nir_type", String),
    Column("year_value_plan", Integer),
)

Templan = Table(
    "nir_templan",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("vuz_code", Integer),
    Column("nir_type", String),
    Column("vuz_name", String),
    Column("nir_director", String),
    Column("grnti_code", String),
    Column("value_plan", Integer),
    Column("nir_name", String),
    Column("director_position", String),
    Column("nir_reg_number", String),
)

VUZ = Table(
    "vuz",
    metadata_obj,
    Column("UniqueID", Integer, primary_key=True),
    Column("vuz_code", Integer),
    Column("name", String),
    Column("full_name", String),
    Column("vuz_name", String),
    Column("region", String),
    Column("city", String),
    Column("status", String),
    Column("fed_sub_code", Integer),
    Column("federation_subject", String),
    Column("gr_ved", String),
    Column("profile", String),
)
