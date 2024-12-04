import re

from src.base_table_model import BaseTableModel
from models import NTP


class NTPTableModel(BaseTableModel):
    table_class = NTP
    _headers_by_ind = [
        "",
        "Код НТП",
        "Номер НИР",
        "Код ВУЗа",
        "Наименование ВУЗа",
        "Код ГРНТИ НИР",
        "Пл. фин-е текущего года",
        "Руководитель НИР",
        "Характер НИР",
        "Наименование НИР",
        "Должность, Уч. звание, Уч. степень",
        # "Организация-исполнитель НИР",
        # "Код организации-исполнителя НИР",
    ]
    _index_by_col = {
        "ntp_code": 0,
        "nir_number": 1,
        "vuz_code": 2,
        "vuz_name": 3,
        "grnti_code": 4,
        "year_value_plan": 5,
        "nir_director": 6,
        "nir_type": 7,
        "nir_name": 8,
        "director_meta": 9,
        # "nir_organization": 10,
        # "nir_org_code": 11,
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
