from src.base_table_model import BaseTableModel
from models import GRNTI


class GRNTITableModel(BaseTableModel):
    table_class = GRNTI
    _headers_by_ind = [
        "Код рубрики",
        "Наименование рубрики",
    ]
    _index_by_col = {
        "codrub": 0,
        "rubrika": 1,
    }
