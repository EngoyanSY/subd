from PyQt6.QtWidgets import QDialog

from ui.py.export_window import Ui_Dialog


class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
