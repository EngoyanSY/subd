from src.base_table_model import BaseTableModel
from models import Templan


class TemplanTableModel(BaseTableModel):
    table_class = Templan
    _headers_by_ind = [
        "Код ВУЗа",
        "Наименование ВУЗа",
        "Характер НИР",
        "Аббревиатура ВУЗа",
        "Код ГРНТИ НИР",
        "Руководитель НИР",
        "Пл. финансирование",
        "Наименование НИР",
        "Должность",
        "Номер НИР",
    ]
    _index_by_col = {
        "vuz_code": 0,  #
        "vuz_name": 1,  #
        "nir_type": 2,  #
        "vuz_abb": 3,
        "nir_director": 5,  #
        "value_plan": 6,  #
        "nir_name": 7,  #
        "director_position": 8,  #
        "nir_reg_number": 9,  #
        "grnti_code": 4,  #
    }
