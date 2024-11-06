from src.base_table_model import BaseTableModel
from models import Grant


class GrantTableModel(BaseTableModel):
    table_class = Grant
    _headers_by_ind = [
        "Код конкурса",
        "Код НИР",
        "Код ВУЗа",
        "Наименование ВУЗа",
        "Код по ГРНТИ",
        "Пл. объём гранта",
        "Наименование НИР",
        "Руководитель НИР",
        "Должность",
        "Ученое звание",
        "Ученая степень",
    ]
    _index_by_col = {
        "kon_code": 0,
        "nir_code": 1,
        "vuz_code": 2,
        "vuz_name": 3,
        "grnti_code": 4,
        "grant_value": 5,
        "nir_name": 7,
        "nir_director": 6,
        "director_position": 8,
        "director_academic_title": 9,
        "director_academic_degree": 10,
    }
