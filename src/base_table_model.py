import json
from typing import List, Dict

from PyQt6.QtCore import QAbstractTableModel
from PyQt6.QtCore import Qt, QModelIndex

from models import BaseTable


class BaseTableModel(QAbstractTableModel):
    _headers_by_ind: List = []
    _index_by_col: Dict = {}
    table_class = BaseTable

    def __init__(self):
        super().__init__()
        self._data = []
        vuz = self.table_class.select_all_json()
        for row in vuz:
            self._data.append(list(row.values()))
        self._filtered_data = self._data.copy()
    

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
            print(key, index)
            if isinstance(value, str):
                value = [value]
            self._filtered_data = [
                row for row in self._filtered_data if row[index + 1] in value
            ]
        self.layoutChanged.emit()
