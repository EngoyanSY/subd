import json
from typing import List, Dict

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt, QModelIndex

from models import BaseTable, VUZ, GRNTI, Templan, Grant, NTP


class BaseTableModel(QAbstractTableModel):
    _headers_by_ind: List = []
    _index_by_col: Dict = {}
    table_class = BaseTable

    def __init__(self, filters={}):
        super().__init__()
        self._data = []
        vuz = self.table_class.select_all_json()
        for row in vuz:
<<<<<<< HEAD
            self._data.append(list(json.loads(row).values()))
        self.setFilter(filters)
=======
            self._data.append(list(row.values()))
        self._filtered_data = self._data.copy()
>>>>>>> 1299fb8d3dfe197dbd2b0b76fbe123b0867a0133
    

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers_by_ind)
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._filtered_data)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == Qt.Orientation.Horizontal:
            return self._headers_by_ind[section]
        
        return str(section + 1)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._filtered_data[index.row()][index.column()]
        return None

    def setFilter(self, filters={}):
        self._filtered_data = self._data.copy()
        for key, value in filters.items():
            index = self._index_by_col[key]
            if isinstance(value, str):
                print(value)
                self._filtered_data = [
                    row for row in self._filtered_data if str(row[index + 1]).startswith(value)
                ]
            else:
                self._filtered_data = [
                    row for row in self._filtered_data if row[index + 1] in value
                ]
        self.layoutChanged.emit()


class MakeModel(QAbstractTableModel):
    _headers = []
    
    def __init__(self, filter_cond={}, model: str = "pivot"):
        self.vuz = VUZ.select_filter_sort(filter_cond=filter_cond)
        self.grant = Grant.select_filter_sort(filter_cond=filter_cond)
        self.templan = Templan.select_filter_sort(filter_cond=filter_cond)
        self.ntp = NTP.select_filter_sort(filter_cond=filter_cond)
        self.grnti = GRNTI.select_filter_sort(filter_cond=filter_cond)

        self._data = []
        
        if model == "pivot":
            vuz_names = list(map(lambda x: json.loads(x)["vuz_name"], self.vuz))
            for vuz in self.vuz:
                vuz = list(json.loads(vuz))
                grants = filter(lambda x: x["vuz_name"] in vuz_names, json.loads(self.grant))
                ntp = filter(lambda x: x["vuz_name"] in vuz_names, json.loads(self.ntp))
                templan = filter(lambda x: x["vuz_name"] in vuz_names, json.loads(self.templan))
                value_grant = sum(map(lambda x: x["grant_value"], grants))
                value_ntp = sum(map(lambda x: x["year_value_plan"], ntp))
                value_templan = sum(map(lambda x: x["value_plan"], templan))
                row = [
                    vuz.vuz_code,
                    vuz.vuz_name,
                    len(grants),
                    value_grant,
                    len(ntp),
                    value_ntp,
                    len(templan),
                    value_templan,
                    len(grants) + len(ntp) + len(templan),
                    value_ntp + value_grant + value_templan
                ]
                
                self._data.append(row)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        
        return str(section + 1)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None