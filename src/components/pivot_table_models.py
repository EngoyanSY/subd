from src.base_table_model import BaseTableModel
from models import Pivot


class PivotTableModel(BaseTableModel):
    table_class = Pivot
    _headers_by_ind = [
        "Код ВУЗа",
        "Наименование ВУЗа",
        "Кол-во по грантам",
        "Сумма по грантам",
        "Кол-во по НТП",
        "Сумма по НТП",
        "Сумма по тем. планам",
        "Кол-во по тем. планам",
        "Общее кол-во",
        "Общая сумма",
    ]
    _index_by_col = {
        "vuz_code": 0,
        "vuz_name": 1,
        "total_nir_grant_count": 2,
        "total_grant_value": 3,
        "total_nir_ntp_count": 4,
        "total_year_value_plan": 5,
        "total_value_plan": 6,
        "total_nir_templan_count": 7,
        "total_count": 8,
        "total_sum": 9,
    }
