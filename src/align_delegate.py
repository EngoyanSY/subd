from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt


class AlignDelegate(QStyledItemDelegate):
    def __init__(self, table_name=None, parent=None):
        super().__init__(parent)
        self.table_name = table_name

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        data = index.data()

        if isinstance(data, (int)) or isinstance(data, (float)):
            if self.table_name == "pivot":
                option.displayAlignment = Qt.AlignmentFlag.AlignRight
            else:
                option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        elif isinstance(data, str) and len(data) <= 30:
            if self.table_name == "grnti":
                option.displayAlignment = Qt.AlignmentFlag.AlignLeft
            else:
                option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        else:
            option.displayAlignment = Qt.AlignmentFlag.AlignLeft
