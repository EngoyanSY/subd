from typing import Optional, ClassVar

from pydantic import BaseModel, Field, validator


class Nir_Grant(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    kon_code: int = Field()
    nir_code: int = Field()
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    grnti_code: Optional[str] = Field(default=None)
    grant_value: int = Field()
    nir_director: str = Field()
    nir_name: str = Field()
    director_position: Optional[str] = Field(default=None)
    director_academic_title: Optional[str] = Field(default=None)
    director_academic_degree: Optional[str] = Field(default=None)
    table_name: ClassVar[str] = "Gr_pr.xlsx"

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_NTP(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    ntp_code: int = Field()
    nir_number: int = Field()
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    grnti_code: Optional[str] = Field(default=None)
    year_value_plan: int = Field()
    nir_director: str = Field()
    nir_type: str = Field()
    nir_name: str = Field()
    director_meta: str = Field()
    table_name: ClassVar[str] = "Ntp_pr.xlsx"

    @validator("grnti_code", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, str):
            return value
        return None


class Nir_Templan(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    vuz_code: int = Field()
    vuz_name: Optional[str] = Field(default=None)
    grnti_code: Optional[str] = Field(default=None)
    value_plan: int = Field()
    nir_director: str = Field()
    nir_type: str = Field()
    nir_reg_number: str = Field()
    nir_name: str = Field()
    director_position: str = Field()
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


class Nir_GRNTI(BaseModel):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    codrub: str = Field()
    rubrika: str = Field()
    table_name: ClassVar[str] = "grntirub.xlsx"

    @validator("codrub", pre=True)
    def validate_grnti_code(cls, value):
        if isinstance(value, int):
            return f"{value:02}"
