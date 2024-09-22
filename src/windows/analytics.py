from PyQt6.QtWidgets import QDialog

from ui.py.analytics_window import Ui_Dialog


class AnalyticsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
