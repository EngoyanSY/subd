from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        data = index.data()

        if isinstance(data, (int, float)):
            option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        elif isinstance(data, str) and len(data) <= 30:
            option.displayAlignment = Qt.AlignmentFlag.AlignCenter
        else:
            option.displayAlignment = Qt.AlignmentFlag.AlignLeft
