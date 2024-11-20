from src.base_table_model import BaseTableModel
from models import Templan


class TemplanTableModel(BaseTableModel):
    table_class = Templan
    # Column("UniqueID", Integer, primary_key=True),
    #     Column("vuz_code", Integer),
    #     Column("vuz_name", String),
    #     Column("grnti_code", String),
    #     Column("value_plan", Integer),
    #     Column("nir_director", String),
    #     Column("nir_type", String),
    #     Column("nir_reg_number", String),
    #     Column("nir_name", String),
    #     Column("director_position", String),
    _headers_by_ind = [
        "",
        "Код ВУЗа",
        "Наименование ВУЗа",
        "Код ГРНТИ НИР",
        "Пл. финансирование",
        "Руководитель НИР",
        "Характер НИР",
        "Номер НИР",
        "Наименование НИР",
        "Должность",
    ]
    _index_by_col = {
        "vuz_code": 0,  #
        "vuz_name": 1,  #
        "nir_type": 5,  #
        "nir_director": 4,  #
        "value_plan": 3,  #
        "nir_name": 7,  #
        "director_position": 8,  #
        "nir_reg_number": 6,  #
        "grnti_code": 2,  #
    }
