import re

from src.base_table_model import BaseTableModel
from models import Grant


class GrantTableModel(BaseTableModel):
    table_class = Grant
    _headers_by_ind = [
        "",
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

    def setFilter(self, filters={}):
        self._filtered_data = self._data.copy()
        for key, value in filters.items():
            index = self._index_by_col[key]
            if isinstance(value, str):
                if key == "grnti_code":
                    regex = r"(^|;){}[\S]*".format(value)
                    print(regex)
                    self._filtered_data = [
                        row
                        for row in self._filtered_data
                        if len(re.findall(regex, str(row[index + 1]))) > 0
                    ]
                else:
                    self._filtered_data = [
                        row
                        for row in self._filtered_data
                        if str(row[index + 1]).startswith(value)
                    ]
            else:
                self._filtered_data = [
                    row for row in self._filtered_data if row[index + 1] in value
                ]
            self.layoutChanged.emit()
