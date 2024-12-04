import re

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
