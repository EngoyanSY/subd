from typing import Optional, ClassVar, List

from pydantic import BaseModel, Field, field_validator
from core import Session

class BaseSchema(BaseModel):

    @field_validator("grnti_code", mode='before', check_fields=False)
    def validate_grnti_code(cls, value):
        if isinstance(value, int):
            return str(value)
        return value


class Nir_Grant(BaseSchema):
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

    
class Nir_NTP(BaseSchema):
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


class Nir_Templan(BaseSchema):
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

    @field_validator("nir_reg_number", mode='before')
    def validate_nir_reg_number(cls, value):
        if isinstance(value, int):
            return str(value)
        return value


class Nir_VUZ(BaseSchema):
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


class Nir_GRNTI(BaseSchema):
    UniqueID: Optional[int] = Field(default=None, primary_key=True, nullable=None)
    codrub: str = Field()
    rubrika: str = Field()
    table_name: ClassVar[str] = "grntirub.xlsx"

    @field_validator("codrub", mode='before')
    def validate_grnti_code(cls, value):
        if isinstance(value, int):
            return f"{value:02}"
        return value


