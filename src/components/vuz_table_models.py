from models import VUZ
from src.base_table_model import BaseTableModel

class VuzTableModel(BaseTableModel):
    # TODO поправить по порядку
    _headers_by_ind = [
        "Код",
        "ГР ВЭД",
        "Аббревиатура",
        "Статус",
        "Код фед. субъекта",
        "Фед. субъект",
        "Регион",
        "Город",
        "Наименование",
        "Полное наименование",
        "Профиль",
    ]
    _index_by_col = {
        "vuz_code": 0,
        "name": 7,
        "full_name": 8,
        "vuz_name": 1,
        "region": 5,
        "city": 6,
        "status": 2,
        "fed_sub_code": 3,
        "federation_subject": 4,
        "gr_ved": 9,
        "profile": 10,
    }
    table_class = VUZ